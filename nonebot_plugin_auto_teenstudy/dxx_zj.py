import json
import os
import time
from httpx import AsyncClient

path = os.path.dirname(__file__) + '/data'


async def auto_zj(send_id):
    with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
    try:
        headers = {
            "Host": "qczj.h5yunban.com",
            "Connection": "keep-alive",
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        mark = False
        for item in obj:
            if int(send_id) == int(item['qq']):
                openid = item['openid']
                name = item['name']
                nid = item['nid']
                time_stamp = str(int(time.time()))
                access_token_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid=" + openid + "&nickname=ZhangSan&headimg=&time=" + time_stamp + "&source=common&sign=&t=" + time_stamp
                async with AsyncClient(headers=headers) as client:
                    access_token_rsp = await client.get(access_token_url)
                    access_token_rsp.encoding = access_token_rsp.apparent_encoding
                access_token = access_token_rsp.text[45:81]
                course_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken=" + access_token
                async with AsyncClient(headers=headers) as client:
                    course_rsp = await client.get(course_url)
                    course_rsp.encoding = course_rsp.apparent_encoding
                res_json = json.loads(course_rsp.text)
                title = res_json['result']['title']
                course_id = res_json['result']['id']
                data = {
                    "course": course_id,
                    "subOrg": None,
                    "nid": nid,
                    "cardNo": name
                }
                sent_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken=" + access_token
                async with AsyncClient(headers=headers) as client:
                    sent_rsp = await client.post(url=sent_url, data=json.dumps(data))
                    sent_rsp.encoding = sent_rsp.apparent_encoding
                resp = json.loads(sent_rsp.text)
                if resp.get("status") == 200:
                    data = {
                        "title": title,
                        "name": name,
                        "nid": nid,
                        "status": resp.get("status")
                    }
                    mark = True
                    break
                else:
                    data = {
                        "title": title,
                        "name": name,
                        "nid": nid,
                        "status": resp.get("status")
                    }
                    mark = True
                    break
            else:
                data = {
                    "status": 503
                }
                mark = True
                break
        if not mark:
            data = {
                "status": 503
            }
        return data
    except Exception as result:
        data = {
            "error": result,
            "status": 404
        }
        return data
