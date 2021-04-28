import pytest
import json
from unittest.mock import patch

import requests

from app.workflow.core import WorkFlow, WorkFlowError
from app.models import User

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
            {"from_id": "account_balance", "field_id": "balance", "operator": "gt", "value": 100}
          ],
          "target": "withdraw_30"
        },
        {
          "condition": [
            {"from_id": "account_balance", "field_id": "balance", "operator": "lt", "value": 100}
          ],
          "target": "deposit_20"
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
          "condition": [{"from_id": "withdraw_30", "field_id": "balance", "operator": "lt", "value": 90}],
          "target": "withdraw_30_1"
        },
        {
          "condition": [],
          "target": "account_balance_end_30"
        }
      ]
    },
    {
      "id": "withdraw_30_1",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "money": {"from_id": null, "value": 30}
      },
      "action": "withdraw_in_pesos",
      "transitions": [
        {
          "condition": [],
          "target": "account_balance_end_60"
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
      "id": "account_balance_end_60",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"}
      },
      "action": "get_account_balance",
      "transitions": []
    },
    {
      "id": "deposit_20",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "money": {"from_id": null, "value": 20}
      },
      "action": "deposit",
      "transitions": [
        {
          "condition": [],
          "target": "account_balance_20"
        }
      ]
    },
    {
      "id": "account_balance_20",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"}
      },
      "action": "get_account_balance",
      "transitions": [
        {
          "condition": [
            {"from_id": "account_balance_20", "field_id": "balance", "operator": "gt", "value": 40}
          ],
          "target": "withdraw_50"
        }
      ]
    },
    {
      "id": "withdraw_50",
      "params": {
        "user_id": {"from_id": "start", "param_id": "user_id"},
        "money": {"from_id": null, "value": 50}
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
    WorkFlow(input_json_ok)


def test_bad_json_schema1():
    with pytest.raises(WorkFlowError, match=r".*trigger.*"):
        WorkFlow(input_json_bad1)


def test_bad_json_schema2():
    with pytest.raises(WorkFlowError, match=r".*steps.*"):
        WorkFlow(input_json_bad2)


def test_bad_json():
    with pytest.raises(WorkFlowError, match=r".*well formatted.*"):
        WorkFlow(input_json_bad3)


def test_load_flow():
    j = json.loads(input_json_ok)
    t = j.get("trigger")
    initial_data = {t.get("id"): t.get("params")}

    w = WorkFlow(input_json_ok)
    assert w.data == initial_data

    expected_children_number = len(j.get("steps")) + 1  # trigger

    def count_tree(root):
        total = [1]
        for c in root.get_childrens():
            total.append(count_tree(c))
        return sum(total)

    count = count_tree(w.root_step)

    assert count == expected_children_number


@pytest.mark.parametrize(
    "user_id,pin,expected_balance",
    [
        ("105398891_1", 2090, 100),
        ("105398891_2", 2090, 41),
        ("105398891_3", 2090, 69),
    ]
)
def test_run_flow(user_id, pin, expected_balance):
    j = json.loads(input_json_ok)
    j["trigger"]["params"]["user_id"] = user_id
    j["trigger"]["params"]["pin"] = pin
    w = WorkFlow(json.dumps(j))

    with patch('clients.currconv.requests.get') as mock_get:
        mock_resp = requests.models.Response()
        mock_resp.status_code = 200
        mock_resp._content = json.dumps({"USD_COP": 1}).encode()
        mock_get.return_value = mock_resp
        w.run()

    user = User.objects(user_id=user_id, pin=pin).first()
    assert user.balance == expected_balance


@pytest.mark.parametrize(
    "user_id,pin",
    [
        ("105398891_1", 2091),
    ]
)
def test_run_flow_exceptions(user_id, pin):
    j = json.loads(input_json_ok)
    j["trigger"]["params"]["user_id"] = user_id
    j["trigger"]["params"]["pin"] = pin
    w = WorkFlow(json.dumps(j))
    with patch('clients.currconv.requests.get') as mock_get:
        mock_resp = requests.models.Response()
        mock_resp.status_code = 200
        mock_resp._content = json.dumps({"USD_COP": 1}).encode()
        mock_get.return_value = mock_resp
        history = w.run()
    print(history)
    assert "not found" in history[-1]


@pytest.mark.parametrize(
    "user_id,pin",
    [
        ("105398891_4", 2090),

    ]
)
def test_run_flow_exceptions2(user_id, pin):
    j = json.loads(input_json_ok)
    j["trigger"]["params"]["user_id"] = user_id
    j["trigger"]["params"]["pin"] = pin
    w = WorkFlow(json.dumps(j))
    with patch('clients.currconv.requests.get') as mock_get:
        mock_resp = requests.models.Response()
        mock_resp.status_code = 200
        mock_resp._content = json.dumps({"USD_COP": 1}).encode()
        mock_get.return_value = mock_resp
        history = w.run()
    print(history)
    assert "balance" in history[-1]
