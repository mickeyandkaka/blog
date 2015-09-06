# -*- coding: utf-8 -*-

from flask_security import (Security, SQLAlchemyUserDatastore, \
                            UserMixin, RoleMixin, login_required, current_user)
from config import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id'))
)

class Role(db.Model, RoleMixin):
    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return '<Role role_id:%s, role_name:%s>' % (self.role_id, self.role_name)


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    password = db.Column(db.String(1024))
    active = db.Column(db.Boolean())
    create_time = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return '<User user_id:%s, user_name:%s>' % (self.user_id, self.user_name)
