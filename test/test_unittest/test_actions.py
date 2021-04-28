import json
from unittest.mock import patch

import pytest
import requests

from app.workflow.core import Action, ActionError


@pytest.mark.parametrize(
    "user_id,pin,expected",
    [
        ("user1", 12345, True)
    ]
)
def test_validate_account(user_id, pin, expected):
    a = Action("validate_account")
    assert a.execute(user_id, pin)["is_valid"] == expected


@pytest.mark.parametrize(
    "user_id,pin",
    [
        (1234, 12345),
        ("user1", "12345"),
        (None, 12345),
        ("user1", None),
        ("user1", 12346),
    ]
)
def test_validate_account_exceptions(user_id, pin):
    a = Action("validate_account")
    with pytest.raises(ActionError):
        a.execute(user_id, pin)


@pytest.mark.parametrize(
    "user_id,expected",
    [
        ("user1", 1000000),
    ]
)
def test_get_account_balance(user_id, expected):
    a = Action("get_account_balance")
    assert a.execute(user_id)["balance"] == expected


@pytest.mark.parametrize(
    "user_id",
    [
        (12345),
        ("user2"),
        ("user3"),
    ]
)
def test_get_account_balance_exceptions(user_id):
    a = Action("get_account_balance")
    with pytest.raises(ActionError):
        a.execute(user_id)


@pytest.mark.parametrize(
    "user_id,money,expected",
    [
        ("user1", 200000, 1200000),
    ]
)
def test_deposit(user_id, money, expected):
    a = Action("deposit")
    assert a.execute(user_id, money)["balance"] == expected


@pytest.mark.parametrize(
    "user_id,money",
    [
        (12345, 100000),
        ("user2", 100000),
        ("user3", 100000),
    ]
)
def test_deposit_exceptions(user_id, money):
    a = Action("deposit")
    with pytest.raises(ActionError):
        a.execute(user_id, money)


@pytest.mark.parametrize(
    "user_id,money,expected",
    [
        ("user1", 200000, 1000000),
        ("user1", 800000, 200000),
    ]
)
def test_withdraw_in_pesos(user_id, money, expected):
    a = Action("withdraw_in_pesos")
    assert a.execute(user_id, money)["balance"] == expected


@pytest.mark.parametrize(
    "user_id,money",
    [
        (12345, 100000),
        ("user2", 100000),
        ("user3", 100000),
        ("user1", 3000000),
    ]
)
def test_withdraw_in_pesos_exceptions(user_id, money):
    a = Action("withdraw_in_pesos")
    with pytest.raises(ActionError):
        a.execute(user_id, money)


@pytest.mark.parametrize(
    "user_id,money,expected",
    [
        ("user1", 50, 100000),
    ]
)
def test_withdraw_in_dollars(user_id, money, expected):
    a = Action("withdraw_in_dollars")
    with patch('clients.currconv.requests.get') as mock_get:
        mock_resp = requests.models.Response()
        mock_resp.status_code = 200
        mock_resp._content = json.dumps({"USD_COP": 2000}).encode()
        mock_get.return_value = mock_resp
        result = a.execute(user_id, money)["balance"]
    assert result == expected


@pytest.mark.parametrize(
    "user_id,money",
    [
        (12345, 50),
        ("user2", 50),
        ("user3", 50),
        ("user1", 600),
    ]
)
def test_withdraw_in_dollars_exceptions(user_id, money):
    a = Action("withdraw_in_dollars")
    with pytest.raises(ActionError):
        with patch('clients.currconv.requests.get') as mock_get:
            mock_resp = requests.models.Response()
            mock_resp.status_code = 200
            mock_resp._content = json.dumps({"USD_COP": 2000}).encode()
            mock_get.return_value = mock_resp
            a.execute(user_id, money)
