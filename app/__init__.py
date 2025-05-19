from flask import Flask
from .models import db
from .routes import main  # Register your blueprint

def create_app():
    app = Flask(__name__)

    # Load config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'change-this-to-env-value'

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main)

    return app
