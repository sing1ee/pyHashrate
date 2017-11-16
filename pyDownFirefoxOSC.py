# -*- coding: utf-8 -*-

from model import HashrateStat, OSCOTC, save_all
import requests
import json
import time
import traceback

buy_payload = {"crypto_currency": "OSC",
               "trade_currency": "CNY",
               "is_buy": 'true',
               "offset": 0,
               "limit": 8,
               }
sell_payload = {"crypto_currency": "OSC",
               "trade_currency": "CNY",
               "is_buy": 'false',
               "offset": 0,
               "limit": 8,
               }
cnt = 0
with open("firefoxOSC.json", 'a+') as w:
    while True:
        try:
            print cnt
            cnt += 1
            br = requests.post('https://otc.firefoxotc.com/api/market/list', data=buy_payload)
            bdata = br.json()
            print bdata
            sr = requests.post('https://otc.firefoxotc.com/api/market/list', data=sell_payload)
            sdata = sr.json()
            if 'data' not in bdata or 'lists' not in bdata['data']\
                    or 'data' not in sdata or 'lists' not in sdata['data']:
                continue
            rows = bdata['data']['lists']
            rows.extends(sdata['data']['lists'])
            w.write(json.dumps(rows) + "\n")
            now = int(time.time())
            hrs = []
            for row in rows:
                row['created_at'] = now
                row['group_label'] = now
                hr = OSCOTC()
                hr.update(**row)
                hrs.append(hr)
            save_all(hrs)
        except:
            traceback.print_exc()
            pass
        time.sleep(60*10)
