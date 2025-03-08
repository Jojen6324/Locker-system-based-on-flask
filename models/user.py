import uuid
from models.database import execute_query, execute_insert, execute_cud

def generate_uuid_token():
    return str(uuid.uuid4())

class UserModel:
    def __init__(self, config):
        self.config = config
    
    def register(self, username, password):
        # Check if user exists
        sql = "SELECT username FROM users WHERE username = %s"
        val = (username,)
        res = execute_query(self.config, sql, val)
        if res:
            return 0
        
        # Create new user
        sql = "INSERT INTO users (username, password, token) VALUES (%s, %s, %s)"
        val = (username, password, generate_uuid_token())
        execute_insert(self.config, sql, val)
        return 1
    
    def login(self, username, password):
        sql = "SELECT username FROM users WHERE username = %s AND password = %s"
        val = (username, password)
        res = execute_query(self.config, sql, val)
        if res:
            return 1
        return 0
    
    def get_status(self, username):
        sql = "SELECT token FROM users WHERE username = %s"
        val = (username,)
        return execute_query(self.config, sql, val)[0]
    
    def get_user_by_token(self, token):
        sql = "SELECT username FROM users WHERE token = %s"
        val = (token,)
        return execute_query(self.config, sql, val)
    
    def get_user_id_by_token(self, token):
        sql = "SELECT id FROM users WHERE token = %s"
        val = (token,)
        result = execute_query(self.config, sql, val)
        if result:
            return result[0]['id']
        return None