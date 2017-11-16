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
            sr = requests.post('https://otc.firefoxotc.com/api/market/list', data=sell_payload)
            print sr
            sdata = sr.json()
            print bdata
            print sdata
            if 'data' not in bdata or 'lists' not in bdata['data']\
                    or 'data' not in sdata or 'lists' not in sdata['data']:
                continue
            rows = bdata['data']['lists']
            rows.append(sdata['data']['lists'])
            w.write(json.dumps(rows) + "\n")
        except:
            traceback.print_exc()
            pass
        time.sleep(10)