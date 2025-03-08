from datetime import datetime
from models.database import execute_cud
from flask import current_app

def clear_expired_lockers():
    try:
        now = datetime.now()
        sql_clear_expired_lockers = """
            UPDATE lockers
            SET status = 'unused', user_id = NULL, expiry_time = NULL
            WHERE expiry_time < %s AND status = 'used'
        """
        params = (now,)
        config = current_app.config['MYSQL_CONFIG']
        success = execute_cud(config, sql_clear_expired_lockers, params)
        if success:
            print(f"Cleared expired lockers at {now}")
        else:
            print(f"Failed to clear expired lockers at {now}")
    except Exception as e:
        print(f"An unexpected error occurred during locker clearing: {e}")