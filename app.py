# app.py - Main application entry point
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from config import Config
from models.database import init_db
from routes import register_blueprints
from tasks.scheduler_tasks import clear_expired_lockers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=clear_expired_lockers, trigger='cron', minute='0,30')
    scheduler.start()
    
    # Register shutdown
    atexit.register(lambda: scheduler.shutdown())
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5000', debug=True)