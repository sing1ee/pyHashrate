# -*- coding: utf-8 -*-

from config import db
from sqlalchemy import asc
import time


class OSCOTC(db.Model):
    __tablename__ = 'osc_otc'

    id = db.Column(db.Integer, primary_key=True)
    crypto_currency = db.Column(db.String(64))
    oid = db.Column(db.Integer)
    trade_currency = db.Column(db.String(64))
    price = db.Column(db.Numeric(14, 2))
    is_buy = db.Column(db.Boolean)
    max_qty = db.Column(db.Integer)
    min_qty = db.Column(db.Integer)
    max_amount = db.Column(db.Integer)
    min_amount = db.Column(db.Integer)
    name = db.Column(db.String(64))
    group_label = db.Column(db.Integer, index=True)
    created_at = db.Column(db.Integer, index=True)


class HashrateStat(db.Model):
    __tablename__ = 'hashrate_stat'

    id = db.Column(db.Integer, primary_key=True)
    relayed_by = db.Column(db.String(64))
    count = db.Column(db.String(64))
    pool_share = db.Column(db.Numeric(36, 14))
    hash_share = db.Column(db.Numeric(36, 14))
    link = db.Column(db.String(1028))
    pool_id = db.Column(db.String(64))
    real_hashrate = db.Column(db.String(64))
    diff_24h = db.Column(db.Numeric(36, 14))
    pool_icon_class = db.Column(db.String(1028))
    icon_link = db.Column(db.String(1028))
    hashrate = db.Column(db.Numeric(36, 14))
    hashrate_unit = db.Column(db.String(16))
    lucky = db.Column(db.Numeric(36, 14))
    cur2max_percent = db.Column(db.Numeric(36, 14))
    index = db.Column(db.Integer)
    created_at = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<HashrateStat %r>' % self.relayed_by

    def update(self, **entries):
        self.__dict__.update(entries)





def save(hashrate):
    db.session.add(hashrate)
    db.session.commit()


def save_all(hashrates):
    db.session.add_all(hashrates)
    db.session.commit()


def query_last_n_days(days = 1):
    return HashrateStat.query\
        .filter(HashrateStat.created_at > int(time.time()) - 86400 * days)\
        .order_by(asc(HashrateStat.created_at)).all()