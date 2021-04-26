import pytest

from main import validate_account, get_account_balance, deposit, withdraw_in_pesos
from main import ActionError


@pytest.mark.parametrize(
    "user_id,pin,expected",
    [
        ("user1", 12345, True),
        ("user1", 12346, False),
    ]
)
def test_validate_account(user_id, pin, expected):
    assert validate_account(user_id, pin) is expected


@pytest.mark.parametrize(
    "user_id,pin",
    [
        (1234, 12345),
        ("user1", "12345"),
        (None, 12345),
        ("user1", None),
    ]
)
def test_validate_account_exceptions(user_id, pin):
    with pytest.raises(ActionError):
        validate_account(user_id, pin)


@pytest.mark.parametrize(
    "user_id,expected",
    [
        ("user1", 1000000),
    ]
)
def test_get_account_balance(user_id, expected):
    assert get_account_balance(user_id) == expected


@pytest.mark.parametrize(
    "user_id",
    [
        (12345),
        ("user2"),
        ("user3"),
    ]
)
def test_get_account_balance_exceptions(user_id):
    with pytest.raises(ActionError):
        get_account_balance(user_id)


@pytest.mark.parametrize(
    "user_id,money,expected",
    [
        ("user1", 200000, 1200000),
    ]
)
def test_deposit(user_id, money, expected):
    assert deposit(user_id, money) == expected


@pytest.mark.parametrize(
    "user_id,money",
    [
        (12345, 100000),
        ("user2", 100000),
        ("user3", 100000),
    ]
)
def test_deposit_exceptions(user_id, money):
    with pytest.raises(ActionError):
        deposit(user_id, money)

@pytest.mark.parametrize(
    "user_id,money,expected",
    [
        ("user1", 200000, 1000000),
        ("user1", 800000, 200000),
    ]
)
def test_withdraw_in_pesos(user_id, money, expected):
    assert withdraw_in_pesos(user_id, money) == expected


@pytest.mark.parametrize(
    "user_id,money",
    [
        (12345, 100000),
        ("user2", 100000),
        ("user3", 100000),
        ("user1", 300000),
    ]
)
def test_withdraw_in_pesos_exceptions(user_id, money):
    with pytest.raises(ActionError):
        withdraw_in_pesos(user_id, money)
