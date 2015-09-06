# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from secure import (DB_USERNAME, DB_USERPASS, DB_HOST,
                    DB_PORT, DB_NAME, SECRET_KEY)


class ProductionConfig(object):
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' %\
                            (DB_USERNAME, DB_USERPASS, DB_HOST, DB_PORT, DB_NAME)


app = Flask(__name__)
app.config.from_object(ProductionConfig)
db = SQLAlchemy(app)
