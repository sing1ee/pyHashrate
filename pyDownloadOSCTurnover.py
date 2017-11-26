# -*- coding: utf-8 -*-

from model import OSCTurnover, save_all
import requests
import json
import time
import traceback

cnt = 0
with open("turnover.json", 'a+') as w:
    while True:
        try:
            print cnt
            cnt += 1
            r = requests.get('https://x.miguan.in/otc/monitorRecordList?orderBy=turnover')
            data = r.json()
            if 'result' not in data:
                continue
            rows = data['result']
            w.write(json.dumps(rows) + "\n")
            now = int(time.time())
            hrs = []
            for row in rows:
                for (k, v) in row.items():
                    if not v:
                        del row[k] 
                row['created_at'] = now
                if 'dict' not in row or 'code' not in row['dict']:
                    continue
                row['exchange'] = row['dict']['code']
                row['dict_info'] = row['dict']
                del row['dict']
                hr = OSCTurnover()
                hr.update(**row)
                hrs.append(hr)
            save_all(hrs)
        except:
            traceback.print_exc()
            pass
        time.sleep(60*5)