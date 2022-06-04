import json
import os
import secrets
from anti_useragent import UserAgent
from httpx import AsyncClient

path = os.path.dirname(__file__) + '/data'  # 数据存放目录


async def makeHeader(openid):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'close',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'JSESSIONID=' + secrets.token_urlsafe(40),
        'Host': 'www.jxqingtuan.cn',
        'Origin': 'http://www.jxqingtuan.cn',
        'Referer': 'http://www.jxqingtuan.cn/html/h5_index.html?&accessToken=' + openid,
        'User-Agent': UserAgent(platform="iphone").wechat,
        'X-Requested-With': 'XMLHttpRequest'
    }
    return headers


async def auto_jx(send_id):
    with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
    try:
        mark = False
        for item in obj:
            if int(send_id) == int(item['qq']):
                openid = item['openid']
                nid = item['nid']
                name = item['name']
                suborg = ''
                url = "http://www.jxqingtuan.cn/pub/vol/volClass/current"
                headers = await makeHeader(openid=openid)
                async with AsyncClient(headers=headers) as client:
                    course = await client.get(url)
                    course.encoding = course.apparent_encoding
                if json.loads(course.text).get('status') == 200:
                    title = json.loads(course.text).get('result').get('title')
                    coursejson = json.loads(course.text).get("result").get('id')
                    resp_url = 'http://www.jxqingtuan.cn/pub/vol/volClass/join?accessToken='
                    data = {"course": coursejson, "nid": nid, "cardNo": name, "subOrg": suborg}
                    async with AsyncClient(headers=headers) as client:
                        res = await client.post(url=resp_url, data=json.dumps(data))
                        res.encoding = res.apparent_encoding
                    resp = json.loads(res.text)
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
