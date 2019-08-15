import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail


__version__ = '0.1.0'
CONFIRM_SUBSCRIBER_EMAIL = True
CONFIRM_BLOGGER_EMAIL = True


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'kdlsajf;ldksajfd;slkfjadskcmdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # Email configs for reseting things you know.
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from flask_subscription_system.routes import main
    app.register_blueprint(main)

    return app
