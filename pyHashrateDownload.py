# -*- coding: utf-8 -*-

import requests
import json
import time

cnt = 0
with open("HashRate.json", 'a+') as w:
    while True:
        print cnt
        cnt += 1
        r = requests.get('https://btc.com/stats/api/realtime/poolHashrate?count=12')
        w.write(json.dumps(r.json()) + "\n")
        time.sleep(60)
