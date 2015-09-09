# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from secure import (DB_USERNAME, DB_USERPASS, DB_HOST,
                    DB_PORT, DB_NAME, SECRET_KEY,
                    HASH_METHOD, SALT)


class ProductionConfig(object):
    WTF_CSRF_ENABLED = True
    # SQLALCHEMY_ECHO = True

    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' %\
                            (DB_USERNAME, DB_USERPASS, DB_HOST, DB_PORT, DB_NAME)

    SECURITY_PASSWORD_HASH = HASH_METHOD
    SECURITY_PASSWORD_SALT = SALT

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    # SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False


app = Flask(__name__)
app.config.from_object(ProductionConfig)
db = SQLAlchemy(app)

# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return db.session.query(User).filter(User.id == user_id).first()

init_login()
