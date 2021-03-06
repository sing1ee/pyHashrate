# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from config import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
from model import query_last_n_days, query_buy, query_sell, buy_max_price, sell_min_price, query_turnover
from itertools import groupby
import simplejson as json
from decimal import Decimal
from itertools import repeat
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
    x_axis = []
    for hr in ret:
        group_all[hr.relayed_by].append(hr)
        x_axis.append(hr.created_at)
    legends = group_all.keys()
    series = []
    x_axis = sorted(list(set(x_axis)))

    total_hashrate = list(repeat(0, len(x_axis)))
    for key in legends:
        group = {}
        for hr in group_all[key]:
            group[hr.created_at] = hr
        hashrate = []
        for x in x_axis:
            if x in group:
                hashrate.append(group[x].hashrate)
            else:
                hashrate.append(0)
        series.append({'name': key, 'type': 'line', 'data': hashrate})
        for i in range(0, len(x_axis)):
            total_hashrate[i] += hashrate[i]
    
    legends.append('总算力')
    series.append({'name': '总算力', 'type': 'line', 'data': total_hashrate})
    x_axis = map(lambda x: time.strftime("%d日%H时%M分", time.localtime(x)), x_axis)
    return jsonify({"legends": legends, "series": series, "x_axis": x_axis})


@app.route('/turnover.json')
def turnover_json():

    start = int(time.time()) - 5 * 86400  # 5 days
    ret = query_turnover(start)
    group_all = collections.defaultdict(list)
    x_axis = []
    for ot in ret:
        group_all[ot.exchange].append(ot)
        x_axis.append(ot.created_at)
    legends = group_all.keys()
    series, x_axis = [], sorted(list(set(x_axis)))
    total_data = list(repeat(0, len(x_axis)))
    for key in legends:
        group = {}
        for x in group_all[key]:
            group[x.created_at] = x
        turnover = []
        for x in x_axis:
            if x in group:
                turnover.append(group[x].turnover)
            else:
                turnover.append(0)
        series.append({'name': key, 'type': 'line', 'data': turnover})
        for i in range(0, len(x_axis)):
            total_data[i] += turnover[i]

    legends.append('总交易量')
    series.append({'name': '总交易量', 'type': 'line', 'data': total_data})
    x_axis = map(lambda x: time.strftime("%d日%H时%M分", time.localtime(x)), x_axis)
    return jsonify({"legends": legends, "series": series, "x_axis": x_axis})


@app.route('/osc.json')
def osc_json():
    legends = ['买方最高价', '卖方最低价']
    start = int(time.time()) - 3 * 86400  # 5 days

    buy_data = query_buy(start=start)
    sell_data = query_sell(start=start)
    x_axis = map(lambda x: time.strftime("%d日%H时%M分", time.localtime(x[1])), buy_data)
    new_buy_data = []
    for i in range(len(buy_data) - 1, -1, -1):
        if buy_data[i][0] > sell_data[i][0] * Decimal(5):
            new_buy_data.append((sell_data[i][0] * Decimal(1.1), buy_data[i - 1][1]))
        else:
            new_buy_data.append(buy_data[i])
    new_buy_data.reverse()
    series = [{"name": "买方最高价", "type": "line", "data": map(lambda x: x[0], new_buy_data)},
              {"name": "卖方最低价", "type": "line", "data": map(lambda x: x[0], sell_data)}]

    return jsonify({"legends": legends, "series": series, "x_axis": x_axis})


@app.route('/wkc_otc')
def osc():
    return render_template('osc.html', buy_max=buy_max_price()[0], sell_min=sell_min_price()[0])


@app.route('/home')
def home():
    return render_template('menu.html')


if __name__=='__main__':
    manager.run()
