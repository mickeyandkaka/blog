# -*- coding: utf-8 -*-

from flask_security import (Security, SQLAlchemyUserDatastore, \
                            UserMixin, RoleMixin, login_required, current_user)
from config import app, db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(15), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return '<Role role_id:%s, role_name:%s>' % (self.id, self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(63))
    password = db.Column(db.String(1023))
    active = db.Column(db.Boolean())
    create_time = db.Column(db.DateTime())

    roles = db.relationship('Role', backref=db.backref('users'), secondary=roles_users)

    # Flask-Login integration
    def is_authenticated(self):
        return True if self.id == 1 else False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.user_name

    def __str__(self):
        return '<User user_id:%s, user_name:%s>' % (self.id, self.username)
