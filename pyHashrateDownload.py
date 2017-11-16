# -*- coding: utf-8 -*-

from model import HashrateStat, save_all
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
            data = r.json()
            if 'data' not in data:
                continue
            rows = data['data']
            w.write(json.dumps(rows) + "\n")
            now = int(time.time())
            hrs = []
            for row in rows:
                row['created_at'] = now
                hr = HashrateStat()
                hr.update(**row)
                hrs.append(hr)
            save_all(hrs)
        except:
            traceback.print_exc()
            pass
        time.sleep(60*10)
