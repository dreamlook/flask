# -*- coding: utf-8 -*-
from flask import render_template,request,flash,redirect,url_for
from . import auth
from .forms import LoginForm,RegistrationForm
from ..models import User
from .. import db

@auth.route('/login',methods=['GET','POST'])
def login():
    from app.auth.forms import  LoginForm
    form = LoginForm()
    flash(u'登录成功')
    '''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
    else:
        username = request.args['username']
    '''
    return render_template('login.html',title=u'登录',form=form)

#后边加上
@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form .validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.submit()
        return redirect(url_for('auth.login'))

    return render_template('register.html',title=u'注册')