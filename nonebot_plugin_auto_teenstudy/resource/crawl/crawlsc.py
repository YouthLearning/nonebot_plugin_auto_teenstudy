import pymongo
import random
import time
import requests

client = pymongo.MongoClient('localhost', 27017)
mydb = client.dxx
dxx_sc = mydb.dxx_sc
sleeptime = random.randint(2, 8)
t = [3, 4]
all_list = []
headers = {
    "Referer": 'http://scyol.com/v_prod6.02/',
    "Host": "dxx.scyol.com",
    "Connection": "keep-alive",
    "Content_Length": '9',
    "Content_Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3224 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Origin": "http://scyol.com",
    "X-Requested-With": "com.tencent.mm",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "token": '',  # 此处的token需自己手动抓取
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}
url = 'https://dxx.scyol.com/api/organize/list'
data = {
    "pid": 30447
}
for item in t:
    id1 = item
    if item == 3:
        danwei1 = '市（州）'
        data_one = {
            "pid": item
        }
        try:
            response = requests.post(url=url, headers=headers, json=data_one)
        except:
            time.sleep(10)
            response = requests.post(url=url, headers=headers, json=data_one)
        response.encoding = response.apparent_encoding
        data_one_json = response.json()
        response.close()
        data_one_list = data_one_json['data']
        time.sleep(sleeptime)
        for item2 in data_one_list:
            danwei2 = item2['label']
            id2 = item2['value']
            data_two = {
                "pid": id2
            }
            try:
                response2 = requests.post(url, headers=headers, json=data_two)
            except:
                time.sleep(10)
                response2 = requests.post(url, headers=headers, json=data_two)
            response2.encoding = response2.apparent_encoding
            data_two_json = response2.json()
            response2.close()
            data_two_list = data_two_json['data']
            two_list = []
            for i in data_two_list:
                if "大学" in i['label'] or '学院' in i['label']:
                    two_list.append(i)
                else:
                    continue
            time.sleep(sleeptime)
            for item3 in two_list:
                danwei3 = item3['label']
                id3 = item3['value']
                data_three = {
                    "pid": id3
                }
                try:
                    response3 = requests.post(url, headers=headers, json=data_three, timeout=30)
                except:
                    time.sleep(10)
                    response3 = requests.post(url, headers=headers, json=data_three, timeout=30)
                response3.encoding = response3.apparent_encoding
                data_three_json = response3.json()
                if data_three_json['code'] == 501:
                    time.sleep(sleeptime)
                    continue
                else:
                    response3.close()
                    data_three_list = data_three_json['data']
                    time.sleep(sleeptime)
                    for item4 in data_three_list:
                        id4 = item4['value']
                        danwei4 = item4['label']
                        data_four = {
                            "pid": id4
                        }
                        try:
                            response4 = requests.post(url, headers=headers, json=data_four)
                        except:
                            time.sleep(10)
                            response4 = requests.post(url, headers=headers, json=data_four)
                        response4.encoding = response4.apparent_encoding
                        data_four_json = response4.json()
                        time.sleep(sleeptime)
                        data_four_list = data_four_json['data']
                        for item5 in data_four_list:
                            id5 = item5['value']
                            danwei5 = item5['label']
                            dxx_sc.insert_one({
                                "id1": str(id1),
                                "danwei1": danwei1,
                                "id2": str(id2),
                                "danwei2": danwei2,
                                "id3": str(id3),
                                "danwei3": danwei3,
                                "id4": str(id4),
                                "danwei4": danwei4,
                                "id5": str(id5),
                                "danwei5": danwei5
                            })
                            print(f'{danwei3}-{danwei4}-{danwei5}-已完成！')
                        print(f'{danwei2}-{danwei3}-{danwei4}-已完成！')
                    print(f'{danwei2}-{danwei3}-已完成！')
        print(f'{danwei1}-已完成')
    else:
        danwei1 = '省直属'
        data_one = {
            "pid": item
        }
        try:
            response = requests.post(url=url, headers=headers, json=data_one)
        except:
            time.sleep(10)
            response = requests.post(url=url, headers=headers, json=data_one)
        response.encoding = response.apparent_encoding
        data_one_json = response.json()
        response.close()
        data_one_list = data_one_json['data']
        time.sleep(sleeptime)
        for item2 in data_one_list:
            danwei2 = item2['label']
            id2 = item2['value']
            data_two = {
                "pid": id2
            }
            try:
                response2 = requests.post(url, headers=headers, json=data_two)
            except:
                time.sleep(10)
                response2 = requests.post(url, headers=headers, json=data_two)
            response2.encoding = response2.apparent_encoding
            data_two_json = response2.json()
            response2.close()
            data_two_list = data_two_json['data']
            two_list = []
            for i in data_two_list:
                if "大学" in i['label'] or '学院' in i['label']:
                    two_list.append(i)
                else:
                    continue
            time.sleep(sleeptime)
            for item3 in two_list:
                danwei3 = item3['label']
                id3 = item3['value']
                data_three = {
                    "pid": id3
                }
                try:
                    response3 = requests.post(url, headers=headers, json=data_three, timeout=30)
                except:
                    time.sleep(10)
                    response3 = requests.post(url, headers=headers, json=data_three, timeout=30)
                response3.encoding = response3.apparent_encoding
                data_three_json = response3.json()
                if data_three_json['code'] == 501:
                    time.sleep(sleeptime)
                    continue
                else:
                    response3.close()
                    data_three_list = data_three_json['data']
                    time.sleep(sleeptime)
                    for item4 in data_three_list:
                        id4 = item4['value']
                        danwei4 = item4['label']
                        dxx_sc.insert_one({
                            "id1": str(id1),
                            "danwei1": danwei1,
                            "id2": str(id2),
                            "danwei2": danwei2,
                            "id3": str(id3),
                            "danwei3": danwei3,
                            "id4": str(id4),
                            "danwei4": danwei4
                        })
                        print(f'{danwei2}-{danwei3}-{danwei4}-已完成！')
                    print(f'{danwei2}-{danwei3}-已完成！')
        print(f'{danwei1}-已完成')
print('四川高校团支部数据抓取完成！')
