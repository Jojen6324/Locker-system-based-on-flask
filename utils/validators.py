import re
from datetime import datetime

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', username))

def validate_password(password):
    if not password or len(password) < 6 or len(password) > 20:
        return False
    return True

def validate_date(date_str):
    try:
        datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def validate_locker_number(locker_number):
    try:
        num = int(locker_number)
        return 1 <= num <= 100  # Assuming valid locker numbers are 1-100
    except ValueError:
        return False