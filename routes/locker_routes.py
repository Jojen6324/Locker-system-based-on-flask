from flask import Blueprint, request, jsonify
from models.user import UserModel
from models.locker import LockerModel
from models.location import LocationModel
from datetime import datetime
from utils.responses import msgErr, msgSuccess

locker_bp = Blueprint('locker', __name__)

@locker_bp.route('/locations/<int:location_id>', methods=['GET'])
def get_lockers_status(location_id):
    token = request.headers.get('token')
    locker_model = LockerModel(locker_bp.config)
    lockers = locker_model.get_lockers_by_location(location_id, token)
    return jsonify(lockers), 200

@locker_bp.route('/locations', methods=['GET'])
def get_locations():
    location_model = LocationModel(locker_bp.config)
    locations = location_model.get_all_locations()
    return jsonify(locations), 200

@locker_bp.route('/applyLocker', methods=['POST'])
def apply_locker():
    try:
        data = request.get_json()
        location_id = data.get('locationId')
        expiry_time_str = data.get('expiryTime')
        token = data.get('token')
        locker_number = data.get('lockerNumber')
        
        if not all([location_id, expiry_time_str, token, locker_number]):
            return jsonify(msgErr('缺少必要参数')), 400
        
        try:
            expiry_time = datetime.fromisoformat(expiry_time_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify(msgErr('日期格式错误')), 400
        
        user_model = UserModel(locker_bp.config)
        user_id = user_model.get_user_id_by_token(token)
        if not user_id:
            return jsonify(msgErr('Invalid token')), 401
        
        locker_model = LockerModel(locker_bp.config)
        result = locker_model.apply_locker(location_id, locker_number, user_id, expiry_time)
        
        if result.get('success'):
            return jsonify({'code': 'success', 'message': '申请成功'}), 200
        else:
            return jsonify(msgErr(result.get('message', '申请失败'))), 400
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify(msgErr('服务器错误')), 500

@locker_bp.route('/cancelLocker', methods=['POST'])
def cancel_locker():
    try:
        data = request.get_json()
        location_id = data.get('locationId')
        locker_number = data.get('lockerNumber')
        token = data.get('token')
        
        if not all([location_id, locker_number, token]):
            return jsonify(msgErr('缺少必要参数')), 400
        
        user_model = UserModel(locker_bp.config)
        user_id = user_model.get_user_id_by_token(token)
        if not user_id:
            return jsonify(msgErr('无效的 token')), 401
        
        locker_model = LockerModel(locker_bp.config)
        result = locker_model.cancel_locker(location_id, locker_number, user_id)
        
        if result.get('success'):
            return jsonify({'code': 'success', 'message': '取消成功'}), 200
        else:
            return jsonify(msgErr(result.get('message', '取消失败'))), 400
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify(msgErr('服务器错误')), 500