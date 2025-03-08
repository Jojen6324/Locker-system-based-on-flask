from flask import Blueprint, request, jsonify
from models.user import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    name = request.json.get('username')
    password = request.json.get('password')
    user_model = UserModel(auth_bp.config)
    code = user_model.login(name, password)
    if code:
        status = user_model.get_status(name)
        response = {'msg': 'success', 'code': code, 'token': status["token"]}
    else:
        response = {'msg': 'success', 'code': code, 'token': 'None'}
    return jsonify(response)

@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.json.get('username')
    password = request.json.get('password')
    user_model = UserModel(auth_bp.config)
    code = user_model.register(name, password)
    response = {'msg': 'success', 'code': code}
    return jsonify(response)

@auth_bp.route('/userinfo', methods=['GET'])
def get_user_info():
    token = request.headers.get('token')
    user_model = UserModel(auth_bp.config)
    user_data = user_model.get_user_by_token(token)
    if user_data and len(user_data) > 0:
        user_info = user_data[0]
        user_info["face_thumbnail"] = f'/static/uploads/face_database/{token}.jpeg'
        return jsonify(user_info), 200
    else:
        return jsonify({'error': '用户不存在'}), 404