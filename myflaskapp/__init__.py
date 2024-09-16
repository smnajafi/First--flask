from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    
    # Register Blueprints (e.g., routes)
    from .routes import main
    app.register_blueprint(main)
    
    return app