# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from config import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
from model import query_last_n_days
from itertools import groupby
import simplejson as json
import collections
import time
import sys


reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand)


@app.route('/HashChart')
def hash():
    ret = query_last_n_days(3)
    group_all = collections.defaultdict(list)
    for hr in ret:
        group_all[hr.relayed_by].append(hr)
    legends = group_all.keys()
    series = []

    x_axis = []
    for key in legends:
        group = group_all[key]
        sorted(group, key = lambda x: x.created_at)
        x_axis = map(lambda x: x.created_at, group)
        series.append({'name': key, 'type': 'line', 'stack': '算力', 'data': map(lambda x: x.hashrate, group)})

    return render_template('hash.html', legends=json.dumps(legends, ensure_ascii=True).replace('"', '\''), series=series, x_axis=x_axis)


@app.route('/data.json')
def data_json():
    ret = query_last_n_days(3)
    group_all = collections.defaultdict(list)
    for hr in ret:
        group_all[hr.relayed_by].append(hr)
    legends = group_all.keys()
    series = []

    x_axis = []
    for key in legends:
        group = group_all[key]
        sorted(group, key = lambda x: x.created_at)
        x_axis = map(lambda x: time.strftime("%d日%H时", time.localtime(x.created_at)), group)
        series.append({'name': key, 'type': 'line', 'stack': '算力', 'data': map(lambda x: x.hashrate, group)})

    return jsonify({"legends": legends, "series": series, "x_axis": x_axis})

if __name__=='__main__':
    manager.run()
