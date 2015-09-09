# -*- coding: utf-8 -*-


from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

from flask_security.utils import verify_password

from config import db
from models import User


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def validate_login(self):
        user = self.get_user()

        if user is None:
            return False

        if not user.is_authenticated():
            return False

        if not user.is_active():
            return False

        if not verify_password(self.password.data, user.password):
            return False

        return True

    def get_user(self):
        return db.session.query(User).filter(User.username == self.username.data).first()
