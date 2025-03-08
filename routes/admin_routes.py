from flask import Blueprint, request, jsonify
from models.user import UserModel
from models.locker import LockerModel
from utils.responses import msgErr, msgSuccess

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/lockers', methods=['GET'])
def get_all_lockers():
    token = request.headers.get('token')
    user_model = UserModel(admin_bp.config)
    user = user_model.get_user_by_token(token)
    
    if not user or user[0].get('role') != 'admin':
        return jsonify(msgErr('Unauthorized')), 401
    
    locker_model = LockerModel(admin_bp.config)
    lockers = locker_model.get_all_lockers()
    return jsonify(lockers), 200

@admin_bp.route('/admin/force-clear', methods=['POST'])
def force_clear_locker():
    token = request.headers.get('token')
    user_model = UserModel(admin_bp.config)
    user = user_model.get_user_by_token(token)
    
    if not user or user[0].get('role') != 'admin':
        return jsonify(msgErr('Unauthorized')), 401
    
    data = request.get_json()
    location_id = data.get('locationId')
    locker_number = data.get('lockerNumber')
    
    locker_model = LockerModel(admin_bp.config)
    result = locker_model.force_clear_locker(location_id, locker_number)
    
    if result.get('success'):
        return jsonify(msgSuccess('清除成功')), 200
    return jsonify(msgErr(result.get('message', '清除失败'))), 400