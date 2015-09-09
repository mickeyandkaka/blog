#!/usr/bin/env python
# -*- coding: utf-8 -*-


from models import User, Role
from config import app, db
from flask_security.utils import encrypt_password
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user


db.drop_all()
db.create_all()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

with app.app_context():
    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

    test_user = user_datastore.create_user(
        username='admin',
        password=encrypt_password('admin'),
        active=True,
        roles=[user_role, super_user_role],
    )

    db.session.commit()

