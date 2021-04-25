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
