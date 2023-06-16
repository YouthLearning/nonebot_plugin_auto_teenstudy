import asyncio
import datetime
import json
import os
import random
import time
import secrets
import re
from httpx import AsyncClient
from anti_useragent import UserAgent
from bs4 import BeautifulSoup
from nonebot.log import logger

path = os.path.dirname(__file__) + '/data'


class AutoDxx:
    @staticmethod
    async def auto_dxx(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    if item['area'] == '湖北':
                        content = await AutoDxx.auto_hubei(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '江西':
                        content = await AutoDxx.auto_jiangxi(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '浙江':
                        content = await AutoDxx.auto_zhejiang(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '安徽':
                        content = await AutoDxx.auto_anhui(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '四川':
                        content = await AutoDxx.auto_sichuan(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '山东':
                        content = await AutoDxx.auto_shandong(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '上海':
                        content = await AutoDxx.auto_shanghai(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '吉林':
                        content = await AutoDxx.auto_jilin(send_id)
                        status = content['status']
                        return content
                    elif item['area'] == '重庆':
                        content = await AutoDxx.auto_chongqing(send_id)
                        status = content['status']
                        return content
                    else:
                        content = {
                            "msg": '该地区暂未支持！',
                            "status": 404
                        }
                        status = content['status']
                        return content
            if not mark:
                content = {
                    "msg": "用户数据不存在，请先配置用户文件！"
                }
                return content
        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    @staticmethod
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
            'User-Agent': UserAgent(platform="iphone", min_version=1, max_version=5).wechat,
            'X-Requested-With': 'XMLHttpRequest'
        }
        return headers

    # 江西共青团青年大学习提交
    @staticmethod
    async def auto_jiangxi(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    nid = item['nid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    suborg = ''
                    headers=await AutoDxx.makeHeader(openid=openid)
                    url = f"http://www.jxqingtuan.cn/pub/vol/volClass/index?userId={random.randint(4363000, 4364000)}"
                    async with AsyncClient(headers=headers) as client:
                        course = await client.get(url=url)
                    course.encoding = course.charset_encoding
                    if json.loads(course.text).get('code') == 0:
                        title = json.loads(course.text).get("list")[0].get("title")
                        coursejson = json.loads(course.text).get('list')[0].get('id')
                        resp_url = 'http://www.jxqingtuan.cn/pub/vol/volClass/join?accessToken='
                        data = {"course": coursejson, "nid": nid, "cardNo": name, "subOrg": suborg}
                        async with AsyncClient(headers=headers) as client:
                            res = await client.post(url=resp_url, json=data)
                            res.encoding = res.charset_encoding
                        resp = json.loads(res.text)
                        if resp.get("status") == 200:
                            item.update(dxx_name=dxx_name, commit_time=commit_time)
                            msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                            data = {
                                "msg": msg,
                                "status": resp.get("status")
                            }
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            return data
                        else:
                            data = {
                                'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                                'status': 503
                            }
                            return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data
        except Exception as result:
            logger.error(f"{datetime.datetime.now()}: 错误信息：{result}")
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 青春浙江青年大学习提交
    @staticmethod
    async def auto_zhejiang(send_id):
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
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    nid = item['nid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    time_stamp = str(int(time.time()))
                    access_token_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid=" + openid + "&nickname=ZhangSan&headimg=&time=" + time_stamp + "&source=common&sign=&t=" + time_stamp
                    async with AsyncClient(headers=headers) as client:
                        access_token_rsp = await client.get(access_token_url)
                    access_token_rsp.encoding = access_token_rsp.charset_encoding
                    access_token = access_token_rsp.text[45:81]
                    course_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken=" + access_token
                    async with AsyncClient(headers=headers) as client:
                        course_rsp = await client.get(course_url)
                        course_rsp.encoding = course_rsp.charset_encoding
                    res_json = json.loads(course_rsp.text)
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
                        sent_rsp.encoding = sent_rsp.charset_encoding
                    resp = json.loads(sent_rsp.text)
                    if resp.get("status") == 200:
                        item.update(dxx_name=dxx_name, commit_time=commit_time)
                        msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                        data = {
                            "msg": msg,
                            "status": resp.get("status")
                        }
                        with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                            json.dump(obj, w, indent=4, ensure_ascii=False)
                        return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data
        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 青春湖北青年大学习提交
    @staticmethod
    async def auto_hubei(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    openid = item['openid']
                    name = item['name']
                    area = item['area']
                    uid = item['uid']
                    danwei1 = item['university']
                    danwei2 = item['college']
                    danwei3 = item['class_name']
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
                        code_resp.encoding = code_resp.charset_encoding
                    code = list(json.loads(code_resp.text))[-1]
                    course_url = 'https://h5.cyol.com/special/daxuexi/' + code + '/m.html'
                    async with AsyncClient(headers=headers1) as client:
                        course_resp = await client.get(course_url)
                    course_resp.encoding = code_resp.charset_encoding
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
                        item.update(dxx_name=dxx_name, commit_time=commit_time)
                        msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nuid:{uid}\n学校：{danwei1}\n学院：{danwei2}\n班级(团支部)：{danwei3}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                        data = {
                            'msg': msg,
                            "status": 200
                        }
                        with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                            json.dump(obj, w, indent=4, ensure_ascii=False)
                        return data
                    else:
                        msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nuid:{uid}\n学校：{danwei1}\n学院：{danwei2}\n班级(团支部)：{danwei3}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                        data = {
                            'msg': msg,
                            "status": 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 安徽共青团青年大学习提交
    @staticmethod
    async def auto_anhui(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    username = item['name']
                    area = item['area']
                    token = item['token']
                    gender = item['gender']
                    mobile = item['mobile']
                    level1 = item['level1']
                    level2 = item['university']
                    level3 = item['college']
                    level4 = item['class_name']
                    level5 = item['level5']
                    headers = {
                        "Host": "dxx.ahyouth.org.cn",
                        "Accept": "application/json, text/plain, */*",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Referer": "http://dxx.ahyouth.org.cn/",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                        'Content-Type': 'application/x-www-form-urlencoded',
                        "X-Requested-With": 'com.tencent.mm',
                        "Origin": 'http://dxx.ahyouth.org.cn',
                        "token": token
                    }
                    data = {
                        'username': username,
                        'gender': gender,
                        'mobile': mobile,
                        'level1': level1,
                        'level2': level2,
                        'level3': level3,
                        'level4': level4,
                        'level5': level5
                    }
                    get_infor_url = 'http://dxx.ahyouth.org.cn/api/saveUserInfo'
                    async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                        infor_response = await client.post(url=get_infor_url, params=data)
                    infor_response.encoding = infor_response.charset_encoding
                    infor_response_json = infor_response.json()
                    if infor_response_json['code'] == 200:
                        username = infor_response_json['content']['username']
                        token = infor_response_json['content']['token']
                        gender = infor_response_json['content']['gender']
                        mobile = infor_response_json['content']['mobile']
                        level1 = infor_response_json['content']['level1']
                        level2 = infor_response_json['content']['level2']
                        level3 = infor_response_json['content']['level3']
                        level4 = infor_response_json['content']['level4']
                        level5 = infor_response_json['content']['level5']
                        headers = {
                            "Host": "dxx.ahyouth.org.cn",
                            "Accept": "application/json, text/plain, */*",
                            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Referer": "http://dxx.ahyouth.org.cn/",
                            "Accept-Encoding": "gzip, deflate",
                            "Connection": "keep-alive",
                            'Content-Type': 'application/x-www-form-urlencoded',
                            "X-Requested-With": 'com.tencent.mm',
                            "Origin": 'http://dxx.ahyouth.org.cn',
                            "token": token
                        }
                        data = {
                            'username': username,
                            'gender': gender,
                            'mobile': mobile,
                            'level1': level1,
                            'level2': level2,
                            'level3': level3,
                            'level4': level4,
                            'level5': level5
                        }
                        await asyncio.sleep(1)
                        commit_url = 'http://dxx.ahyouth.org.cn/api/newLearn'
                        async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                            commit_response = await client.post(url=commit_url, params=data)
                        commit_response.encoding = commit_response.charset_encoding
                        commit_response_json = commit_response.json()
                        if commit_response_json['code'] == 200:
                            item.update(dxx_name=dxx_name, commit_time=commit_time)
                            msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{username}\nQQ号:{send_id}\n地区：{area}\ntoken:{token}\n学校类型:{level1}\n学校：{level2}\n学院：{level3}\n班级(团支部)：{level4}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                            data = {
                                'msg': msg,
                                "status": 200
                            }
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            return data
                        else:
                            data = {
                                'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{username}\nQQ号:{send_id}\n地区：{area}\ntoken:{token}\n学校：{level2}\n学院：{level3}\n班级(团支部)：{level4}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                                'status': 503
                            }
                            return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{username}\nQQ号:{send_id}\n地区：{area}\ntoken:{token}\n学校：{level2}\n学院：{level3}\n班级(团支部)：{level4}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data

        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 天府新青年青年大学习提交
    @staticmethod
    async def auto_sichuan(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    token = item['token']
                    tel = item['tel']
                    org = item['org']
                    lastOrg = item['lastOrg']
                    orgName = item['orgName']
                    allOrgName = item['allOrgName']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    headers = {
                        "Referer": 'http://scyol.com/v_prod6.02/',
                        "Host": "dxx.scyol.com",
                        "Connection": "keep-alive",
                        "Content_Length": '9',
                        "Content_Type": "application/json",
                        "Accept": "*/*",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3224 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                        "Origin": "http://scyol.com",
                        "X-Requested-With": "com.tencent.mm",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "token": token,  # 此处的token需自己手动抓取
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    }
                    data_json = {
                        "name": name,  # 此处填姓名
                        "tel": tel,  # 此处填手机号
                        "org": org,  # #学校所属上级pid#学校pid#学院pid#班级（团支部）pid#
                        "lastOrg": lastOrg,
                        "orgName": orgName,  # 班级名称
                        "allOrgName": allOrgName  # #学校所属上级名称#学校名称#学院名称+团委#班级（团支部）名称#
                    }
                    commit_url = 'https://dxx.scyol.com/api/student/commit'
                    async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                        response = await client.post(url=commit_url, json=data_json)
                    response.encoding = response.charset_encoding
                    if response.json()['code'] == 0:
                        item.update(dxx_name=dxx_name, commit_time=commit_time)
                        msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\ntoken:{token}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                        data = {
                            'msg': msg,
                            "status": 200
                        }
                        with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                            json.dump(obj, w, indent=4, ensure_ascii=False)
                        return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\ntoken:{token}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data

        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 青春山东青年大学习提交
    @staticmethod
    async def auto_shandong(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    cookie = item['cookie']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    version_url = f'http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getNewestVersionInfo&openid={openid}'
                    headers = {
                        "Host": "qndxx.youth54.cn",
                        "Connection": "keep-alive",
                        "Accept": "*/*",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Origin": "http://qndxx.youth54.cn",
                        "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=pageSdtwdt",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cookie": cookie
                    }
                    async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                        version_response = await client.post(url=version_url)
                    version_response.encoding = version_response.charset_encoding
                    version_response_json = version_response.json()
                    if version_response_json['errcode'] == '0':
                        beforeversion = version_response_json['beforeversion']
                        versionname = version_response_json['versionname']
                        version = version_response_json['version']
                        await asyncio.sleep(random.randint(3, 5))
                        commit_url = 'http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=studyLatest'
                        headers = {
                            "Host": "qndxx.youth54.cn",
                            "Connection": "keep-alive",
                            "Accept": "*/*",
                            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                            "X-Requested-With": "XMLHttpRequest",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "http://qndxx.youth54.cn",
                            "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=pageSdtwdt",
                            "Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Cookie": cookie
                        }
                        data = {
                            'openid': openid,
                            'version': version
                        }
                        async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                            response = await client.post(url=commit_url, params=data)
                        response.encoding = response.charset_encoding
                        if response.json()['errcode'] == '0':
                            item.update(dxx_name=dxx_name, commit_time=commit_time)
                            msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                            data = {
                                'msg': msg,
                                "status": 200
                            }
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            return data
                        else:
                            data = {
                                'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                                'status': 503
                            }
                            return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data

        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 青春上海青年大学习提交
    @staticmethod
    async def auto_shanghai(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    nid = item['nid']
                    accessToken = item['accessToken']
                    area = item['area']
                    cookie = item['cookie']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    headers = {
                        "Host": "qcsh.h5yunban.com",
                        "Connection": "keep-alive",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "X-Requested-With": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                        "Content-Type": "application/json;charset=UTF-8",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Referer": "https://qcsh.h5yunban.com/youth-learning/signUp.php?rv=2020",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cookie": cookie
                    }
                    study_url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/course/current?accessToken={accessToken}"
                    async with AsyncClient(headers=headers, max_redirects=5, timeout=10) as client:
                        response = await client.get(url=study_url)
                    if response.status_code == 200:
                        response.encoding = response.charset_encoding
                        course = response.json()['result']['id']
                        commit_url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join?accessToken={accessToken}"
                        params = {
                            "course": course,
                            "nid": nid,
                            "cardNo": name
                        }
                        async with AsyncClient(headers=headers, timeout=10, max_redirects=5) as client:
                            response = await client.post(url=commit_url, json=params)
                        if response.status_code == 200:
                            response.encoding = response.charset_encoding
                            if response.json()['status'] == 200:
                                item.update(dxx_name=dxx_name, commit_time=commit_time)
                                msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\naccessToken：{accessToken}\ncookie：{cookie}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                                data = {
                                    'msg': msg,
                                    "status": 200
                                }
                                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                    json.dump(obj, w, indent=4, ensure_ascii=False)
                                return data
                            else:
                                data = {
                                    'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\naccessToken：{accessToken}\ncookie：{cookie}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                                    'status': 503
                                }
                                return data
                        else:
                            data = {
                                'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\naccessToken：{accessToken}\ncookie：{cookie}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                                'status': 503
                            }
                            return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data

        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 吉青飞扬青年大学习提交
    @staticmethod
    async def auto_jilin(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    student_id = item['student_id']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    headers = {
                        "Host": "jqfy.jl54.org",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "X-Requested-With": "com.tencent.mm",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
                    }
                    url = f"http://jqfy.jl54.org/jltw/wechat/editStudyRecord/{student_id}"
                    params = {
                        "openid": openid
                    }
                    async with AsyncClient(headers=headers, max_redirects=5, timeout=30) as client:
                        response = await client.post(url=url, data=params)
                    response.encoding = response.charset_encoding
                    if response.json()['code'] == '0001':
                        item.update(dxx_name=dxx_name, commit_time=commit_time)
                        msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\nstudent_id：{student_id}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                        data = {
                            'msg': msg,
                            "status": 200
                        }
                        with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                            json.dump(obj, w, indent=4, ensure_ascii=False)
                        return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\nstudent_id：{student_id}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 503
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data

        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data

    # 重庆共青团青年大学习提交
    @staticmethod
    async def auto_chongqing(send_id):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            mark = False
            with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                answer_obj = json.load(a)
            dxx_name = list(answer_obj)[-1]["catalogue"]
            commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    headers = {
                        "Host": "qndxx.cqyouths.com",
                        "Connection": "keep-alive",
                        "Accept": "application/json, text/plain, */*",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                        "X-Requested-With": "com.tencent.mm",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
                    }
                    new_url = f"http://qndxx.cqyouths.com/new_course.json?time={int(time.time())}"
                    async with AsyncClient(headers=headers, max_redirects=5, timeout=30) as client:
                        response = await client.get(url=new_url)
                    if response.status_code == 200:
                        response.encoding = response.charset_encoding
                        course_id = response.json()['data'][0]['id']
                        commit_url = f"http://qndxx.cqyouths.com/api/course/studyCourse?openid={openid}&id={course_id}"
                        async with AsyncClient(headers=headers, max_redirects=5, timeout=30) as client:
                            response = await client.get(url=commit_url)
                        response.encoding = response.charset_encoding
                        if response.json()['status'] == 200 or response.json()['status'] == 201:
                            item.update(dxx_name=dxx_name, commit_time=commit_time)
                            msg = f'\n青年大学习{dxx_name}提交成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}'
                            data = {
                                'msg': msg,
                                "status": 200
                            }
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            return data
                        else:
                            data = {
                                'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                                'status': 503
                            }
                            return data
                    else:
                        data = {
                            'msg': f'\n青年大学习{dxx_name}提交失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 404
                        }
                        return data
            if not mark:
                data = {
                    'msg': f'\n青年大学习{dxx_name}提交失败！\n用户信息不存在！\n添加用户信息指令：设置大学习配置',
                    'status': 404
                }
                return data

        except Exception as result:
            data = {
                "msg": result,
                "status": 404
            }
            return data


AutoDxx = AutoDxx()
