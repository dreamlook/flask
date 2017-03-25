# -*- coding: utf-8 -*-
from os import path

from flask import render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename
from . import  main

#def init_views(app):
@main.route("/")
def hello():
    return render_template('index.html', title='welcome flask')

@main.route("/services")
def services():
    return 'service'

@main.route('/about')
def about():
    return redirect(url_for('auth.login'))

@main.route('/register')
def register():
    return redirect(url_for('auth.register'))

@main.route('/index')
def index():
    return 'index'

@main.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'user %s' % user_id

@main.route('/projects/')
@main.route('/our-works/')
def projects():
    return 'the project page'

@main.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        '''
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        filename = secure_filename(f.filename)
        upload_path=path.join(basepath,'static','uploads',filename)
        f.save(upload_path)
        '''
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(path.join('static/uploads',filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

# @main.template_test('current_link')
# def is_current_link(link):
#     return link == request.path

# @main.template_filter('md')
# def markdown_to_html(txt):
#     from markdown import markdown
#     return markdown(txt)
