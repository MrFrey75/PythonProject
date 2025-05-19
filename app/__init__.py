from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oilprojector.db'
    app.config['SECRET_KEY'] = 'super-secret-key'  # Change this later

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
