import os
import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGO_HOST'),
    'port': int(os.getenv('MONGO_PORT')),
    'db': os.getenv('MONGO_DB'),
    'username': os.getenv('MONGO_USER'),
    'password': os.getenv('MONGO_PASSWORD')
}

db = MongoEngine()
db.init_app(app)


class User(db.Document):
    user_id = db.StringField()
    pin = db.IntField()


@app.route('/users/', methods=['GET'])
def query_records():
    user_id = request.args.get('user_id')
    if user_id:
        user = User.objects(user_id=user_id).first()
        if not user:
            return jsonify({'error': 'data not found'})
        else:
            return jsonify(user)
    else:
        return jsonify(User.objects())


@app.route('/users/', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    user = User(user_id=record['user_id'],
                pin=record['pin'])
    user.save()
    return jsonify(user)


@app.route('/users/', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(user_id=record['user_id']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(pin=record['pin'])
    return jsonify(user)


@app.route('/users/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(user_id=record['user_id']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user)


if __name__ == "__main__":
    app.run(debug=True)
