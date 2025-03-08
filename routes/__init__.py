from routes.auth_routes import auth_bp
from routes.locker_routes import locker_bp
from routes.face_routes import face_bp
from routes.admin_routes import admin_bp

def register_blueprints(app):
    # Pass app config to blueprints
    auth_bp.config = app.config['MYSQL_CONFIG']
    locker_bp.config = app.config['MYSQL_CONFIG']
    face_bp.config = app.config
    admin_bp.config = app.config['MYSQL_CONFIG']
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(locker_bp)
    app.register_blueprint(face_bp)
    app.register_blueprint(admin_bp)