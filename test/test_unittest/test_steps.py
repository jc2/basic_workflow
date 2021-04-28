import pytest

from app.workflow.core import StepError, Step

WORKFLOW_DATA = {
    "test1": {"a": None},
    "test2": {"a": None,  "b": None},
    "test3": {"a": None},
}

PARAMS = {
    "a": {"from_id": "test1", "param_id": "a"},
    "b": {"from_id": "test2", "param_id": "b"},
    "c": {"from_id": None, "value": 1},
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
        ("eq", True, True, True),
        ("eq", False, True, False),
        ("eq", True, False, False),
        ("gt", True, False, True),
    ]
)
def test_one_condition(operator, left_input, right_input, expected):
    WORKFLOW_DATA["test2"].update({"a": left_input})
    ONE_CONDITION[0].update({"operator": operator, "value": right_input})

    s = Step("", None, None, None, ONE_CONDITION)
    assert s._execute_conditions(WORKFLOW_DATA) is expected


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
    WORKFLOW_DATA["test1"].update({"a": left_input1})
    WORKFLOW_DATA["test2"].update({"a": left_input2})
    MULTIPLE_CONDITION[0].update({"operator": operator1, "value": right_input1})
    MULTIPLE_CONDITION[1].update({"operator": operator2, "value": right_input2})
    s = Step("", None, None, None, MULTIPLE_CONDITION)
    assert s._execute_conditions(WORKFLOW_DATA) is expected


def test_conditions_exceptions():
    s = Step("", None, None, None, [{"test1": ""}])
    with pytest.raises(StepError, match=r"Attributes .*"):
        s._execute_conditions({})


def test_params():
    WORKFLOW_DATA["test1"].update({"a": 10})
    WORKFLOW_DATA["test2"].update({"b": 20})
    s = Step("", None, PARAMS, None, None)
    result = s._get_params(WORKFLOW_DATA)
    assert result == {"a": 10, "b": 20, "c": 1}


def test_params_bad():
    WORKFLOW_DATA.pop("test1")
    s = Step("", None, PARAMS, None, None)
    with pytest.raises(StepError, match=r"Attributes .*"):
        s._get_params(WORKFLOW_DATA)
