import os
import uuid

class Config:
    SECRET_KEY = str(uuid.uuid4())
    UPLOAD_FOLDER = 'static/uploads'
    FACE_DB_PATH = "static/uploads/face_database"
    FEATURES_PATH = "static/uploads/face_embeddings.pkl"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # MySQL config
    MYSQL_CONFIG = {
        "user": "root",
        "password": "1234",
        "host": "localhost",
        "database": "locker_data",
        "pool_size": 10
    }
    
    # Create necessary directories
    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.FACE_DB_PATH):
            os.makedirs(Config.FACE_DB_PATH)
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        if not os.path.exists("static/uploads/temp"):
            os.makedirs("static/uploads/temp")