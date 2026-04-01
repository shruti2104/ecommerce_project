from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static') #Flask sometimes cannot automatically detect the templates folder unless it is explicitly defined.

    app.secret_key = "fw_py"

    from .routes import main
    app.register_blueprint(main)

    return app