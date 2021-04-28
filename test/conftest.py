from app.models import User
from app import init_app


init_app()

users = [
        {"user_id": 'user1', "pin": 12345, "balance": 1000000, "has_active_session": True},
        {"user_id": 'user2', "pin": 12345, "balance": 1000000},
        {"user_id": '105398891_1', "pin": 2090, "balance": 100},
        {"user_id": '105398891_2', "pin": 2090, "balance": 101},
        {"user_id": '105398891_3', "pin": 2090, "balance": 99},
        {"user_id": '105398891_4', "pin": 2090, "balance": 25}
    ]


def pytest_sessionstart(session):
    for u in users:
        user = User(**u)
        user.save()


def pytest_sessionfinish(session, exitstatus):
    for u in users:
        user = User.objects(user_id=u['user_id']).first()
        user.delete()
