import json
from json.decoder import JSONDecodeError
from collections import namedtuple
from attr import has

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from validators import WORKFLOW_SCHEMA

operator_functions = {
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "eq": lambda a, b: a == b,
}


class ConditionError(Exception):
    pass


def execute_conditions(data, conditions):
    try:
        return all([operator_functions[c["operator"]](data[c["from_id"]][c["field_id"]], c["value"]) for c in conditions])
    except KeyError:
        raise ConditionError("Conditions does not have proper attributes")


class WorkflowError(Exception):
    pass


def load_workflow(input_json):
    try:
        data = json.loads(input_json)
    except JSONDecodeError as e:
        raise WorkflowError(f"Can not parse to Python Dict, is the json well formatted?: {str(e)}")

    try:
        validate(instance=data, schema=WORKFLOW_SCHEMA)
    except ValidationError as e:
        raise WorkflowError(f"Schema does not match: {str(e)}")

    return data


class ActionError(Exception):
    pass


class User():
    def __init__(self, user_id, pin, balance, has_active_session):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.has_active_session = has_active_session


users = [
    User('user1', 12345, 1000000, True),
    User('user2', 12345, 1000000, False),
]


def validate_account(user_id, pin):
    if type(user_id) != str or type(pin) != int:
        raise ActionError("Validate account error: Inputs do not have proper type")
    for user in users:
        if user.user_id == user_id and user.pin == pin:
            return True
    return False


def get_account_balance(user_id):
    if type(user_id) != str:
        raise ActionError("Get account balance error: Inputs do not have proper type")
    for user in users:
        if user.user_id == user_id:
            if not user.has_active_session:
                raise ActionError("Get account balance error: User needs to be validated first")
            return user.balance
    raise ActionError("Get account balance error: User not found")


def deposit(user_id, money):
    if type(user_id) != str or type(money) != int:
        raise ActionError("Deposit error: Inputs do not have proper type")
    for user in users:
        if user.user_id == user_id:
            if not user.has_active_session:
                raise ActionError("Deposit error: User needs to be validated first")
            user.balance = user.balance + money
            return user.balance
    raise ActionError("Deposit error: User not found")


def withdraw_in_pesos(user_id, money):
    if type(user_id) != str or type(money) != int:
        raise ActionError("Withdraw error: Inputs do not have proper type")
    for user in users:
        if user.user_id == user_id:
            if not user.has_active_session:
                raise ActionError("Withdraw error: User needs to be validated first")
            if user.balance < money:
                raise ActionError("Withdraw error: Insufficient balance")
            user.balance = user.balance - money
            return user.balance
    raise ActionError("Withdraw error: User not found")
