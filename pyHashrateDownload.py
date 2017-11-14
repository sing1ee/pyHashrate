# -*- coding: utf-8 -*-

from model import save_all
from collections import namedtuple
import requests
import json
import time
import traceback

cnt = 0
with open("HashRate.json", 'a+') as w:
    while True:
        try:
            print cnt
            cnt += 1
            r = requests.get('https://btc.com/stats/api/realtime/poolHashrate?count=12')
            rows = r.json()
            w.write(json.dumps(rows) + "\n")
            now = int(time.time())
            for row in rows:
                row['created_at'] = now
            save_all(map(lambda x: namedtuple('HashrateStat', x), rows))
        except:
            traceback.print_exc()
            pass
        time.sleep(60)