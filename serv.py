# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from config import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
from model import query_last_n_days, query_buy, query_sell
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
    return render_template('hash.html')


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
        x_axis = map(lambda x: time.strftime("%d日%H时%M分", time.localtime(x.created_at)), group)
        series.append({'name': key, 'type': 'line', 'data': map(lambda x: x.hashrate, group)})

    return jsonify({"legends": legends, "series": series, "x_axis": x_axis})


@app.route('/osc.json')
def osc_json():
    legends = ['买', '卖']
    start = int(time.time()) - 5 * 86400  # 5 days

    buy_data = query_buy(start=start)
    sell_data = query_sell(start=start)
    x_axis = map(lambda x: time.strftime("%d日%H时%M分", time.localtime(x[1])), buy_data)
    new_buy_data = []
    for i in range(len(buy_data) - 1, -1, -1):
        if buy_data[i][0] > buy_data[i - 1][0] * 5:
            new_buy_data.append(buy_data[i - 1][0], buy_data[i - 1][1])
        else:
            new_buy_data.append(buy_data[i])
    new_buy_data.reverse()
    series = [{"name": "买", "type": "line", "stack": "价格", "data": map(lambda x: x[0], new_buy_data)},
              {"name": "卖", "type": "line", "stack": "价格", "data": map(lambda x: x[0], sell_data)}]

    return jsonify({"legends": legends, "series": series, "x_axis": x_axis})


@app.route('/wkc_otc')
def osc():
    return render_template('osc.html')

if __name__=='__main__':
    manager.run()
