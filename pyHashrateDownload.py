# -*- coding: utf-8 -*-

from model import save_all, convert
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
            for row in rows:
                row['created_at'] = now
            save_all(map(lambda x: convert(x), rows))
        except:
            traceback.print_exc()
            pass
        time.sleep(60)