from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Blueprints                                             
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # CLI helpers
    from .cli import register_cli
    register_cli(app)

    return app
