import json

from flask import Blueprint, jsonify, request, render_template

from app.models import User
from app.workflow.core import WorkFlow, WorkFlowError

bp = Blueprint('bp', __name__)


@bp.route('/users/', methods=['GET'])
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


@bp.route('/users/', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    user = User(**record)
    user.save()
    return jsonify(user)


@bp.route('/users/', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(user_id=record['user_id']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(**record)
    return jsonify(user)


@bp.route('/users/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(user_id=record['user_id']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        json_ = f.read()
        try:
            workflow = WorkFlow(json_)
        except WorkFlowError as e:
            return jsonify({"Error": str(e)})
        else:
            workflow_history = workflow.run()
    return render_template('history.html', history=workflow_history)