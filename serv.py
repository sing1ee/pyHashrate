# -*- coding: utf-8 -*-

from flask import render_template
from config import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
import sys


reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand)


@app.route('/HashChart')
def hash():
    return render_template('hash.html')


if __name__=='__main__':
    manager.run()