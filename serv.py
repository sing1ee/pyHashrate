# -*- coding: utf-8 -*-

from config import SERVER_HOST, SERVER_PORT, app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
from model import HashrateStat
import sys
import os


reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand)


@app.route('/')
def hello():
    return 'Hello'


@app.route('/<name>')
def hello_user(name):
    return "hello {} !".format(name)

if __name__=='__main__':
    manager.run()