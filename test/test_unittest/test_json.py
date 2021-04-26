import pytest

from main import load_workflow, WorkflowError

input_json_ok = """
{
  "steps": [
    {
      "id": "validate_account",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "pin": {"from_id": "start", "param_id": "pin"}
      },
      "action": "validate_account",
      "transitions": [
        {
          "condition": [
            {"from_id": "validate_account", "field_id": "is_valid", "operator": "eq", "value": true}
          ],
          "target": "account_balance"
        }
      ]
    },
    {
      "id": "account_balance",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"}
      },
      "action": "get_account_balance",
      "transitions": [
        {
          "condition": [
            {"from_id": "account_balance", "field_id": "balance", "operator": "gt", "value": 100000}
          ],
          "target": "withdraw_30"
        },
        {
          "condition": [
            {"from_id": "account_balance", "field_id": "balance", "operator": "lt", "value": 100000}
          ],
          "target": "deposit_200"
        }
      ]
    },
    {
      "id": "withdraw_30",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "money": {"from_id": null, "value": 30}
      },
      "action": "withdraw_in_dollars",
      "transitions": [
        {
          "condition": [],
          "target": "account_balance_end_30"
        }
      ]
    },
    {
      "id": "account_balance_end_30",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"}
      },
      "action": "get_account_balance",
      "transitions": []
    },
    {
      "id": "deposit_200",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "money": {"from_id": null, "value": 200000}
      },
      "action": "deposit",
      "transitions": [
        {
          "condition": [],
          "target": "account_balance_200"
        }
      ]
    },
    {
      "id": "account_balance_200",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"}
      },
      "action": "get_account_balance",
      "transitions": [
        {
          "condition": [
            {"from_id": "account_balance", "field_id": "balance", "operator": "gt", "value": 250000}
          ],
          "target": "withdraw_50"
        }
      ]
    },
    {
      "id": "withdraw_50",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "money": {"from_id": null, "value": 50000}
      },
      "action": "withdraw_in_dollars",
      "transitions": [
        {
          "condition": [],
          "target": "account_balance_end_50"
        }
      ]
    },
    {
      "id": "account_balance_end_50",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"}
      },
      "action": "get_account_balance",
      "transitions": []
    }
  ],
  "trigger": {
    "params": {
        "user_id": "105398891",
        "pin": 2090
    },
    "transitions": [
      {
        "target": "validate_account",
        "condition": []
      }
    ],
    "id": "start"
  }
}
"""

input_json_bad1 = """
{
  "steps": [
    {
      "id": "validate_account",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "pin": {"from_id": "start", "param_id": "pin"}
      },
      "action": "validate_account",
      "transitions": [
        {
          "condition": [
            {"from_id": "validate_account", "field_id": "is_valid", "operator": "eq", "value": true}
          ],
          "target": "account_balance"
        }
      ]
    }
  ]
}
"""

input_json_bad2 = """
{
  "trigger": {
    "params": {
        "user_id": "105398891",
        "pin": 2090
    },
    "transitions": [
      {
        "target": "validate_account",
        "condition": []
      }
    ],
    "id": "start"
  }
}
"""

input_json_bad3 = """
{
  "trigger": {
    "params": {
        "user_id": "105398891",
        "pin": 2090
    },
    "transitions": [
      {
        "target": "validate_account",
        "condition": []
      }
    ],
    "id": "start"
}
"""


def test_json_schema_ok():
    load_workflow(input_json_ok)


def test_bad_json_schema1():
    with pytest.raises(WorkflowError, match=r".*trigger.*"):
        load_workflow(input_json_bad1)


def test_bad_json_schema2():
    with pytest.raises(WorkflowError, match=r".*steps.*"):
        load_workflow(input_json_bad2)


def test_bad_json():
    with pytest.raises(WorkflowError, match=r".*well formatted.*"):
        load_workflow(input_json_bad3)
