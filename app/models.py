from app import db


class User(db.Document):
    user_id = db.StringField()
    pin = db.IntField()
    balance = db.FloatField()
    has_active_session = db.BooleanField(default=False)
