import datetime
import json

import requests
import time
import pymongo
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import asyncio

base_url = 'http://www.jxqingtuan.cn/pub/vol/config/organization?pid='
# 模拟用户访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3224 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64'}
# 创建数据库
client = pymongo.MongoClient('localhost', 27017)
mydb = client.dxx
dxx_jx = mydb.dxx_jx
sleeptime = random.randint(2, 8)
t = ['N0013', 'N0014', 'N0015']
try:
    for u in t:
        url = base_url + u
        response = requests.get(url, headers)
        response.encoding = response.apparent_encoding
        obj = response.json()
        response.close()
        for item in obj['result']:
            danwei1 = item['title'][:-2]
            id1 = item['id']
            url1 = base_url + id1
            response1 = requests.get(url1, headers)
            response1.encoding = response1.apparent_encoding
            response1.close()
            obj1 = response1.json()
            for item1 in obj1['result']:
                danwei2 = item1['title']
                id2 = item1['id']
                url2 = base_url + id2
                response2 = requests.get(url2, headers)
                response2.encoding = response2.apparent_encoding
                response2.close()
                obj2 = response2.json()
                for item2 in obj2['result']:
                    danwei3 = item2['title']
                    id3 = item2['id']
                    dxx_jx.insert_one({
                        "id1": id1,
                        "school": danwei1,
                        "id2": id2,
                        "college": danwei2,
                        "id3": id3,
                        "class": danwei3
                    })
                    print(f'{danwei1}-{danwei2}-{danwei3}-已写入数据库！')
                print(f'{danwei1}-{danwei2}-已全部写入数据库！')
                time.sleep(sleeptime)
            print(f'{danwei1}-已全部写入数据库！')
            time.sleep(sleeptime)
except Exception as result:
    print(result)
    dxx_jx.insert_one({
        "id1": 'empty',
        "school": 'empty',
        "id2": 'empty',
        "college": 'empty',
        "id3": 'empty',
        "class": 'empty'
    })


