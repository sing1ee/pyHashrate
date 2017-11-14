# -*- coding: utf-8 -*-

from flask import render_template
from config import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
from model import query_last_n_days
from itertools import groupby
import sys


reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand)


@app.route('/HashChart')
def hash():
    ret = query_last_n_days(3)
    ret_list = [(name, list(group)) for name, group in groupby(ret, lambda p:p.relayed_by)]
    all_legends = map(lambda x: x[0], ret_list)
    legends = []
    filt = set()
    for l in all_legends:
        if l in filt:
            continue
        legends.append(l)
        filt.add(l)
    series = []

    x_axis = []
    for (key, group) in ret_list:
        sorted(group, lambda x: x.created_at)
        x_axis = map(lambda x: x.created_at, group)
        series.append({'name': key, 'type': 'line', 'stack': '算力', 'data': map(lambda x: x.hashrate, group)})

    return render_template('hash.html', legends=legends, series=series, x_axis=x_axis)


if __name__=='__main__':
    manager.run()