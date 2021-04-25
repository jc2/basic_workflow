import pytest

from .main import ConditionError, execute_conditions

COMMAND_DATA = {
    "test1": {"a": None},
    "test2": {"a": None,  "b": None},
    "test3": {"a": None},
}

ONE_CONDITION = [
    {"from_id": "test2", "field_id": "a", "operator": None, "value": None},
]

MULTIPLE_CONDITION = [
    {"from_id": "test1", "field_id": "a", "operator": None, "value": None},
    {"from_id": "test2", "field_id": "a", "operator": None, "value": None},
]


@pytest.mark.parametrize(
    "operator,left_input,right_input,expected",
    [
        ("gt", 2, 1, True),
        ("gt", 2, 2, False),
        ("gte", 2, 3, False),
        ("gte", 2, 1, True),
        ("gte", 2, 2, True),
        ("lt", 2, 3, True),
        ("lt", 2, 1, False),
        ("lt", 2, 2, False),
        ("lte", 2, 3, True),
        ("lte", 2, 1, False),
        ("lte", 2, 2, True),
        ("eq", 2, 3, False),
        ("eq", 2, 1, False),
        ("eq", 2, 2, True),
    ]
)
def test_one_condition(operator, left_input, right_input, expected):
    COMMAND_DATA["test2"].update({"a": left_input})
    ONE_CONDITION[0].update({"operator": operator, "value": right_input})
    assert execute_conditions(COMMAND_DATA, ONE_CONDITION) is expected


@pytest.mark.parametrize(
    "operator1,left_input1,right_input1,operator2,left_input2,right_input2,expected",
    [
        ("gt", 2, 1, "lt", 2, 3, True),
        ("eq", 2, 1, "lt", 2, 3, False),
        ("eq", 2, 2, "lte", 3, 2, False),
        ("gte", 1, 2, "eq", 3, 2, False),
    ]
)
def test_multiple_condition(operator1, left_input1, right_input1, operator2, left_input2, right_input2, expected):
    COMMAND_DATA["test1"].update({"a": left_input1})
    COMMAND_DATA["test2"].update({"a": left_input2})
    MULTIPLE_CONDITION[0].update({"operator": operator1, "value": right_input1})
    MULTIPLE_CONDITION[1].update({"operator": operator2, "value": right_input2})
    assert execute_conditions(COMMAND_DATA, MULTIPLE_CONDITION) is expected


def test_conditions_keys():
    with pytest.raises(ConditionError, match=r".* attributes"):
        execute_conditions({}, [{}])
