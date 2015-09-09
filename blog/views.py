# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort
from flask.ext.admin.contrib import sqla
from flask.ext.admin import Admin
import flask_login as login
import flask_admin as aadmin
from flask_admin import helpers, expose
from config import app, db
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

from forms import LoginForm

@app.route("/")
# @app.route("/index")
def hello():
    return render_template('index.html')
    user = {'nickname': 'mickey'}
    posts = [  # fake array of posts
            {
                'author': {'nickname': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'nickname': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }
        ]
    return render_template('index.html',
                           title='home',
                           user=user,
                           posts=posts
            )

class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active() or not current_user.is_authenticated():
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))



# Create customized index view class that handles login & registration
class MyAdminIndexView(aadmin.AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))

        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user is None:
                return redirect(url_for('.index'))

            if form.validate_login():
                login.login_user(user)

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    # @expose('/register/', methods=('GET', 'POST'))
    # def register_view(self):
        # form = RegistrationForm(request.form)
        # if helpers.validate_form_on_submit(form):
            # user = User()

            # form.populate_obj(user)
            # # we hash the users password to avoid saving it as plaintext in the db,
            # # remove to use plain text:
            # user.password = generate_password_hash(form.password.data)

            # db.session.add(user)
            # db.session.commit()

            # login.login_user(user)
            # return redirect(url_for('.index'))
        # link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        # self._template_args['form'] = form
        # self._template_args['link'] = link
        # return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

admin = Admin(
    app,
    'mickey-blog',
    index_view=MyAdminIndexView(),
    base_template='my_master.html',
    template_mode='bootstrap3',
)

from models import Role, User
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)

# @security.context_processor
# def security_context_processor():
    # return dict(
        # admin_base_template=admin.base_template,
        # admin_view=admin.index_view,
        # h=helpers,
    # )
