# -*- coding: utf-8 -*-

from config import db


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
    created_at = db.Column(db.Integer)

    def __repr__(self):
        return '<HashrateStat %r>' % self.relayed_by
