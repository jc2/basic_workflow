import json
from json.decoder import JSONDecodeError
from collections import defaultdict

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from clients.currconv import CurrConvError, convert
from app.validators import WORKFLOW_SCHEMA
from app.utils import operator_functions
from app.models import User


class ActionError(Exception):
    pass


class Action:
    def __init__(self, name):
        try:
            self.name = name
            self.execute = getattr(self, f"_{name}")
        except AttributeError:
            raise ActionError(f"Action {self.name} not implemented")

    def _validate_account(self, user_id, pin):
        if type(user_id) != str or type(pin) != int:
            raise ActionError("Inputs do not have proper type")
        user = User.objects(user_id=user_id, pin=pin).first()
        if user:
            user.update(**{"has_active_session": True})
            return {"is_valid": True}
        self._not_found()

    def _get_account_balance(self, user_id):
        if type(user_id) != str:
            raise ActionError("Inputs do not have proper type")
        user = User.objects(user_id=user_id).first()
        if user:
            self._check_session(user)
            return {"balance": user.balance}
        self._not_found()

    def _deposit(self, user_id, money):
        if type(user_id) != str or type(money) != int:
            raise ActionError("Inputs do not have proper type")
        user = User.objects(user_id=user_id).first()
        if user:
            self._check_session(user)
            new_balance = user.balance + money
            user.update(**{"balance": new_balance})
            return {"balance": new_balance}
        self._not_found()

    def _withdraw_in_dollars(self, user_id, money):
        return self._withdraw(user_id, money, "dollars")

    def _withdraw_in_pesos(self, user_id, money):
        return self._withdraw(user_id, money, "pesos")

    def _withdraw(self, user_id, money, mode):
        if type(user_id) != str or type(money) != int:
            raise ActionError("Inputs do not have proper type")
        user = User.objects(user_id=user_id).first()
        if user:
            self._check_session(user)
            if mode == "dollars":
                try:
                    money = (money * convert("usd", "cop"))
                except CurrConvError as e:
                    raise ActionError(f"Can not connect to the currency service (aka: el sistema esta caido) {str(e)}")
            if user.balance < money:
                raise ActionError("Insufficient balance")
            new_balance = user.balance - money
            user.update(**{"balance": new_balance})
            return {"balance": new_balance}

        self._not_found()

    def _check_session(self, user):
        if not user.has_active_session:
            raise ActionError("User needs to be validated first")

    def _not_found(self):
        raise ActionError("User not found")


class StepError(Exception):
    pass


class Step:
    def __init__(self, id, action, params, childrens, conditions=None):
        self.id = id
        self._conditions = conditions
        self._childrens = childrens
        self._action = action
        self._params = params

    def set_conditions(self, new_conditions):
        self._conditions = new_conditions

    def set_childrens(self, new_childrens):
        self._childrens = new_childrens

    def get_childrens(self):
        return self._childrens

    def _execute_conditions(self, data):
        try:
            return all([operator_functions[c["operator"]](data[c["from_id"]][c["field_id"]], c["value"]) for c in self._conditions])
        except KeyError as e:
            raise StepError(f"Attributes not found when validating conditions: {str(e)}")

    def _get_params(self, data):
        try:
            params = {}
            for p, v in self._params.items():
                if v["from_id"] is None:
                    params[p] = v["value"]
                else:
                    params[p] = data[v["from_id"]][v["param_id"]]
            return params
        except KeyError as e:
            raise StepError(f"Attributes not found when getting params {str(e)}")

    def run(self, data):
        if self._action:
            if self._execute_conditions(data):
                params = self._get_params(data)
                return self._action.execute(**params)
            else:
                raise StepError("Step was skipped")
        else:
            return {}

    def __str__(self):
        return f"Step: {self.id} -> Action: {self._action.name if self._action else 'No action'}"


class WorkFlowError(Exception):
    pass


class WorkFlow():
    def __init__(self, input_json):
        self.flow = self._parse_json(input_json)
        self.data = defaultdict(dict)
        self.root_step = None

        self._load_flow()

    def _parse_json(self, input_json):
        try:
            data = json.loads(input_json)
        except JSONDecodeError as e:
            raise WorkFlowError(f"Can not parse to Python Dict, is the json well formatted?: {str(e)}")

        try:
            validate(instance=data, schema=WORKFLOW_SCHEMA)
        except ValidationError as e:
            raise WorkFlowError(f"Schema does not match: {str(e)}")

        return data

    def _save_data(self, step_id, key, value):
        self.data[step_id][key] = value

    def _load_flow(self):
        trigger = self.flow.get("trigger")

        for param, value in trigger.get("params").items():
            self._save_data(trigger.get("id"), param, value)

        self.flow.get("steps").append(trigger)

        try:
            self.root_step = self._build_flow(trigger.get("id"), self.flow.get("steps"))
        except RecursionError:
            raise WorkFlowError("Flow steps are not ending. Review the Steps")

    def _build_flow(self, id, steps):
        step_data = list(filter(lambda x: x.get("id") == id, steps))

        if len(step_data) > 1:
            raise WorkFlowError("There are steps with the same ID. ID must be unique")
        if not step_data:
            raise WorkFlowError(f"Step with ID {id} not found")

        step_data = step_data[0]

        childrens = []
        for transition in step_data.get("transitions"):
            step = self._build_flow(transition.get("target"), steps)
            step.set_conditions(transition.get("condition"))
            childrens.append(step)

        action = Action(step_data.get("action")) if step_data.get("action") else None
        step = Step(step_data.get("id"), action, step_data.get("params", {}), childrens)

        return step

    def _flow(self, step, history):
        history.append(str(step))
        try:
            response = step.run(self.data)
        except (StepError, ActionError) as e:
            history.append(str(e))
            return

        if response is not None:
            for k, v in response.items():
                self._save_data(step.id, k, v)

            for child in step.get_childrens():
                self._flow(child, history)

    def run(self):
        history = []
        self._flow(self.root_step, history)
        return history
