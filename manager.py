# -*- coding: utf-8 -*-
from app import  create_app,db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand,upgrade
app = create_app()
manager = Manager(app)
#数据库迁移初始化
migrate= Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.command
def dev():
    from livereload import Server
    live_server=Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)
@manager.command
def test():
    pass

@manager.command
def deploy():
    #数据库迁移
    from app.models import  Role
    upgrade()
    Role.seed()

if __name__ == "__main__":
    manager.run()
    #app.run(debug=True)