from flask import Flask
import razorpay

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static') #Flask sometimes cannot automatically detect the templates folder unless it is explicitly defined.

    app.secret_key = "fw_py"

    from .routes import main
    app.register_blueprint(main)

    app.razorpay_client = razorpay.Client(
        auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET'])
    )


    return app