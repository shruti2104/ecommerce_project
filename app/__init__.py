from flask import Flask
from dotenv import load_dotenv

import os

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = os.getenv("SECRET_KEY")

    app.config.from_object('config.Config')

    from .routes import main
    app.register_blueprint(main)

    return app