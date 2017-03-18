# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for,make_response,abort
from werkzeug.routing import  BaseConverter
from werkzeug.utils import secure_filename
from os import path
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_nav import  Nav
from flask_nav.elements import *

class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]

app = Flask(__name__)
app.url_map.converters['regex']=RegexConverter
Bootstrap(app)
nav = Nav()
manager = Manager(app)

nav.register_element('top',Navbar(u'flask入门',
                                  View(u'主页','index'),
                                  View(u'关于','about'),
                                  View(u'服务','services'),
                                  View(u'项目','projects'),))
nav.init_app(app)

@app.route("/")
def hello():
    response=make_response(render_template('index.html',
                                           title='welcome flask',
                                           body='## hello'))
    response.set_cookie('username','')
    return response

@app.route("/services")
def services():
    return 'service'

@app.route('/about')
def about():
    return 'about'

@app.route('/inde')
def index():
    return 'index'

@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'user %s' % user_id

@app.route('/projects/')
@app.route('/our-works/')
def projects():
    return 'the project page'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
    else:
        username = request.args['username']
    return render_template('login.html',method=request.method)

@app.route('/upload',methods=['GET','POST'])
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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@app.template_test('current_link')
def is_current_link(link):
    return link == request.path

@manager.command
def dev():
    from livereload import Server
    live_server=Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x,y:x+y,md_file.readlines())
    return content.decode('utf-8')

@app.context_processor
def inject_methods():
    return dict(read_md=read_md)

@app.template_filter('md')
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)
if __name__ == "__main__":
    #app.run(debug=True)
    manager.run()