import os
import json
from bs4 import BeautifulSoup
from httpx import AsyncClient

path = os.path.dirname(__file__) + '/data'  # 数据存放目录


async def auto_hb(send_id):
    with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
    try:
        mark = False
        for item in obj:
            if int(send_id) == int(item['qq']):
                openid = item['openid']
                name = item['name']
                danwei1 = item['danwei1']
                danwei2 = item['danwei2']
                danwei3 = item['danwei3']
                headers1 = {
                    "Host": "h5.cyol.com",
                    "Connection": "keep-alive",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                    "Origin": "http://h5.cyol.com",
                    "X-Requested-With": "com.tencent.mm",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                }
                code_url = "https://h5.cyol.com/special/weixin/sign.json"
                async with AsyncClient(headers=headers1) as client:
                    code_resp = await client.get(code_url)
                    code_resp.encoding = code_resp.apparent_encoding
                code = list(json.loads(code_resp.text))[-1]
                course_url = 'https://h5.cyol.com/special/daxuexi/' + code + '/m.html'
                async with AsyncClient(headers=headers1) as client:
                    course_resp = await client.get(course_url)
                    course_resp.encoding = 'utf-8'
                soup = BeautifulSoup(course_resp.text, 'lxml')
                course = soup.title.string[7:]
                headers = {
                    "Host": "cp.fjg360.cn",
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
                url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
                url += "&username=" + name
                url += "&phone=" + "未知"
                url += "&city=" + danwei1
                url += "&danwei2=" + danwei3
                url += "&danwei=" + danwei2
                url += "&openid=" + openid
                url += "&num=10"
                url += "&lesson_name=" + course
                async with AsyncClient(headers=headers) as client:
                    response = await client.get(url)
                response_json = json.loads(response.text)
                if response_json.get('code') == 1:
                    data = {
                        "title": course,
                        "name": name,
                        "status": 200
                    }
                    mark = True
                    break
                else:
                    data = {
                        "course": course,
                        "name": name,
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
            'status': 404
        }
        return data