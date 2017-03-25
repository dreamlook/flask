# -*- coding: utf-8 -*-
from flask import render_template,request,flash,redirect,url_for
from . import auth
from .forms import LoginForm,RegistrationForm
from ..models import User,Role
from .. import db
from flask_login import login_user, logout_user,current_user

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data,password=form.password.data).first()
        print user.name
        if user is not None:
            #login_user()
            return redirect(url_for('main.index'))
    return render_template('login.html',title=u'登录',form=form)

@auth.route('/index')
def index():
    return redirect(url_for('main.hello'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
#后边加上
@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form .validate_on_submit():
        #user_name=User(name='error')
        # user_email=User(email=form.email.data)
        # user_password=User(password=form.password.data)
        user = User(password=form.password.data,
                    name=form.username.data,
                    email=form.email.data
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html',
                           title=u'注册',
                           form=form)