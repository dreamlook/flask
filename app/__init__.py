# -*- coding: utf-8 -*-
from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import  Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import  BaseConverter
from flask_login import LoginManager

class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]

basedir = path.abspath(path.dirname(__file__))#数据库配置

#全局变量 跨文件引用
bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
#manager = Manager(app)

def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_pyfile('config')
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    nav.register_element('top', Navbar(u'flask入门',
                                       View(u'主页', 'index'),
                                       View(u'关于', 'about'),
                                       View(u'服务', 'services'),
                                       View(u'项目', 'projects'), ))
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    nav.init_app(app)
    #init_views(app)
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    app.register_blueprint(main_blueprint, static_folder='static')
    return app

def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x,y:x+y,md_file.readlines())
    return content.decode('utf-8')

