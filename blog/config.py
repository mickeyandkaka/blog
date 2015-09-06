# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from secure import (DB_USERNAME, DB_USERPASS, DB_HOST,
                    DB_PORT, DB_NAME, SECRET_KEY,
                    HASH_METHOD, SALT)


class ProductionConfig(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' %\
                            (DB_USERNAME, DB_USERPASS, DB_HOST, DB_PORT, DB_NAME)

    SECURITY_PASSWORD_HASH = HASH_METHOD

    SECURITY_PASSWORD_SALT = SALT


app = Flask(__name__)
app.config.from_object(ProductionConfig)
db = SQLAlchemy(app)
