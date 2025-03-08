from models.database import execute_query, execute_cud
from datetime import datetime

class LockerModel:
    def __init__(self, config):
        self.config = config
    
    def get_lockers_by_location(self, location_id, token):
        sql = """
        SELECT l.locker_number, l.status, l.user_id, l.expiry_time,
                CASE WHEN l.user_id = (SELECT id FROM users WHERE token = %s) THEN TRUE ELSE FALSE END AS is_owned_by_user
            FROM lockers l
            WHERE l.location_id = %s
            ORDER BY l.locker_number
        """
        val = (token, location_id)
        return execute_query(self.config, sql, val)
    
    def apply_locker(self, location_id, locker_number, user_id, expiry_time):
        # Check if locker is available
        check_sql = """
            SELECT status FROM lockers 
            WHERE location_id = %s AND locker_number = %s
        """
        check_val = (location_id, locker_number)
        result = execute_query(self.config, check_sql, check_val)
        
        if not result or result[0]['status'] != 'unused':
            return {'success': False, 'message': '储物柜已被占用'}
        
        # Apply for locker
        update_sql = """
            UPDATE lockers 
            SET status = 'used', user_id = %s, expiry_time = %s
            WHERE location_id = %s AND locker_number = %s
        """
        update_val = (user_id, expiry_time, location_id, locker_number)
        
        if execute_cud(self.config, update_sql, update_val):
            return {'success': True}
        return {'success': False, 'message': '申请失败'}
    
    def cancel_locker(self, location_id, locker_number, user_id):
        # Verify ownership
        check_sql = """
            SELECT user_id FROM lockers 
            WHERE location_id = %s AND locker_number = %s
        """
        check_val = (location_id, locker_number)
        result = execute_query(self.config, check_sql, check_val)
        
        if not result or result[0]['user_id'] != user_id:
            return {'success': False, 'message': '无权限操作此储物柜'}
        
        # Cancel locker
        update_sql = """
            UPDATE lockers 
            SET status = 'unused', user_id = NULL, expiry_time = NULL
            WHERE location_id = %s AND locker_number = %s
        """
        update_val = (location_id, locker_number)
        
        if execute_cud(self.config, update_sql, update_val):
            return {'success': True}
        return {'success': False, 'message': '取消失败'}