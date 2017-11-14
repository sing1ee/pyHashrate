# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

SERVER_HOST = "SERVER_HOST"
SERVER_PORT = "SERVER_PORT"
DATABASE_URL = "DATABASE_URL"
CONFIG_PATH = "/Users/zhangcheng/.pyhashrate_env"

app = Flask(__name__)

if os.path.exists(CONFIG_PATH):
    print('Importing environment from %s...' % CONFIG_PATH)
    for line in open(CONFIG_PATH):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

app=Flask(__name__)
app.config.from_object(__name__)
db=SQLAlchemy(app)