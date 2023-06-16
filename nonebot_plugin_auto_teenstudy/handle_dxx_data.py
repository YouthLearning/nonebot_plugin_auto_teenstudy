import json
import os
import random
import string
import datetime
from .dxx import AutoDxx

path = os.path.dirname(__file__) + '/data'  # 数据存放目录


class HandleDxx:

    # 修改个人信息
    @staticmethod
    async def change_own(send_id, event):
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        try:
            option = event.split(' ')[-2]
            info = event.split(' ')[-1]
            mark = False
            for item in obj:
                if item['qq'] == int(send_id):
                    if option == '通知方式' or option == '通知':
                        if info == '群聊' or info == 'group':
                            item['auto_commit']['way'] = 'group'
                            group = item['auto_commit']['send_group']
                            status = item['auto_commit']['status']
                            if status:
                                status = '开启'
                            else:
                                status = '关闭'
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            data = {
                                "msg": f"\n青年大学习自动提交通知方式更改成功！\n青年大学习自动提交信息：\n自动提交状态：{status}\n通知方式：群聊\n通知群聊：{group}\n通知QQ：{send_id}",
                                'status': 200
                            }
                            return data
                        elif info == '私聊' or info == 'private':
                            item['auto_commit']['way'] = 'private'
                            group = item['auto_commit']['send_group']
                            status = item['auto_commit']['status']
                            if status:
                                status = '开启'
                            else:
                                status = '关闭'
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            data = {
                                "msg": f"\n青年大学习自动提交通知方式更改成功！\n青年大学习自动提交信息：\n自动提交状态：{status}\n通知方式：私聊\n通知群聊：{group}\n通知QQ：{send_id}",
                                "status": 200
                            }
                            return data
                        else:
                            data = {
                                "msg": f"修改失败，通知方式可选项：群聊|group|私聊|private\n请使用指令 更改信息 通知方式 选项  进行更改！",
                                "status": 404
                            }
                            return data
                    elif option == '通知群聊':
                        item['auto_commit']['send_group'] = info
                        status = item['auto_commit']['status']
                        if status:
                            status = '开启'
                        else:
                            status = '关闭'
                        with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                            json.dump(obj, w, indent=4, ensure_ascii=False)
                        data = {
                            "msg": f"\n青年大学习自动提交通知群聊更改成功！\n青年大学习自动提交信息：\n自动提交状态：{status}\n通知方式：群聊\n通知群聊：{info}\n通知QQ：{send_id}",
                            'status': 200
                        }
                        return data
                    elif option == 'openid':
                        area_list = ['浙江', '山东', '吉林', '重庆', '贵州', '湖北']
                        if item['area'] in area_list:
                            item['openid'] = info
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            data = {
                                "msg": f"\n青年大学习openid更改成功！\n可发指令 我的大学习 查询个人信息",
                                'status': 200
                            }
                            return data
                        else:
                            data = {
                                "msg": f"\n青年大学习openid更改失败！\n该地区不支持更改！",
                                'status': 404
                            }
                            return data
                    elif option == 'token':
                        area_list = ['安徽', '四川']
                        if item['area'] in area_list:
                            item['token'] = info
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            data = {
                                "msg": f"\n青年大学习token更改成功！\n可发指令 我的大学习 查询个人信息",
                                'status': 200
                            }
                            return data
                        else:
                            data = {
                                "msg": f"\n青年大学习token更改失败！\n该地区不支持更改！",
                                'status': 404
                            }
                            return data
                    elif option == 'cookie':
                        area_list = ['山东', '江苏', '辽宁', '上海']
                        if item['area'] in area_list:
                            item['cookie'] = info
                            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                                json.dump(obj, w, indent=4, ensure_ascii=False)
                            data = {
                                "msg": f"\n青年大学习cookie更改成功！\n可发指令 我的大学习 查询个人信息",
                                'status': 200
                            }
                            return data
                        else:
                            data = {
                                "msg": f"\n青年大学习cookie更改失败！\n该地区不支持更改！",
                                'status': 404
                            }
                            return data
                    elif option == 'leader' or option == '团支书':
                        item['leader'] = int(info)
                        with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                            json.dump(obj, w, indent=4, ensure_ascii=False)
                        data = {
                            "msg": f"\n青年大学习团支书QQ更改成功！\n",
                            'status': 200
                        }
                        return data
                    else:
                        data = {
                            "msg": "指令错误！",
                            'status': 200
                        }
                        return data
            if not mark:
                data = {
                    "msg": "用户信息不存在！请使用指令 添加大学习 进行添加！",
                    "status": 404
                }
                return data
        except:
            data = {
                "msg": "指令错误",
                "status": 404
            }
            return data

    # 处理湖北地区用户数据
    @staticmethod
    async def set_hubei(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                qq = int(send_id)
                group = ''
                leader = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                content_json = json.loads(event.split('#')[-1])
                area = event.split('#')[-2]
                name = content_json['name']
                openid = ''.join(random.sample(string.ascii_letters + string.digits, 28))
                uid = random.randint(4678688, 5678754)
                university = content_json['university']
                college = content_json['college']
                class_name = content_json['class_name']
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': name,
                    'openid': openid,
                    'uid': uid,
                    'university': university,
                    'college': college,
                    'class_name': class_name,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_hubei(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nuid:{uid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nuid:{uid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                        'status': 503
                    }
                    return data
                else:
                    data = {
                        'msg': f"出错了\n错误信息：{content['error']}",
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_hubei(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    uid = item['uid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\nopenid：{openid}\nuid：{uid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理江西地区用户数据
    @staticmethod
    async def set_jiangxi(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                content_json = json.loads(event.split('#')[-1])
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                openid = ''.join(random.sample(string.ascii_letters + string.digits, 28))
                university = content_json['university']
                college = content_json['college']
                class_name = content_json['class_name']
                with open(path + '/dxx_jx.json', 'r', encoding='utf-8') as f:
                    n = json.load(f)
                mark1 = False
                for item1 in n:
                    if item1['school'] == university and item1['college'] == college and item1['class'] == class_name:
                        nid = item1['id3']
                        mark1 = True
                        break
                if mark1:
                    write_data = {
                        'qq': qq,
                        'auto_commit': auto_commit,
                        'area': area,
                        'leader': leader,
                        'name': name,
                        'openid': openid,
                        'nid': nid,
                        'university': university,
                        'college': college,
                        'class_name': class_name,
                        'dxx_name': '',
                        'commit_time': ''
                    }
                    data_json.append(write_data)
                    with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                        json.dump(data_json, f, indent=4, ensure_ascii=False)
                    content = await AutoDxx.auto_jiangxi(send_id)
                    status = content['status']
                    if status == 200:
                        with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                            answer_obj = json.load(a)
                        dxx_name = list(answer_obj)[-1]["catalogue"]
                        commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                        data = {
                            'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 200
                        }
                        return data
                    elif status == 503:
                        data = {
                            'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                            'status': 503
                        }
                        return data
                    else:
                        data = {
                            'msg': f"出错了\n错误信息：{content['error']}",
                            'status': 404
                        }
                        return data
                else:
                    data = {
                        'msg': f'设置失败！未找到nid。\n请确认输入的学校、学院和班级名称正确，\n无法确认请使用：查组织 指令',
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_jiangxi(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    nid = item['nid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ:{leader}\n通知群号：{group}\n地区：{area}\nopenid：{openid}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理浙江地区用户数据
    @staticmethod
    async def set_zhejiang(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                content_json = json.loads(event.split("#")[-1])
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                openid = content_json['openid']
                university = content_json['university']
                college = content_json['college']
                class_name = content_json['class_name']
                with open(path + '/dxx_zj.json', 'r', encoding='utf-8') as f:
                    n = json.load(f)
                mark1 = False
                for item1 in n:
                    if item1['school'] == university and item1['college'] == college and item1['class'] == class_name:
                        nid = item1['id3']
                        mark1 = True
                        break
                if mark1:
                    write_data = {
                        'qq': qq,
                        'auto_commit': auto_commit,
                        'area': area,
                        'leader': leader,
                        'name': name,
                        'openid': openid,
                        'nid': nid,
                        'university': university,
                        'college': college,
                        'class_name': class_name,
                        'dxx_name': '',
                        'commit_time': ''
                    }
                    data_json.append(write_data)
                    with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                        json.dump(data_json, f, indent=4, ensure_ascii=False)
                    content = await AutoDxx.auto_zhejiang(send_id)
                    status = content['status']
                    if status == 200:
                        with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                            answer_obj = json.load(a)
                        dxx_name = list(answer_obj)[-1]["catalogue"]
                        commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                        data = {
                            'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                            'status': 200
                        }
                        return data
                    elif status == 503:
                        data = {
                            'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号：{send_id}\n地区：{area}\nopenid：{openid}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                            'status': 503
                        }
                        return data
                    else:
                        data = {
                            'msg': f"出错了\n错误信息：{content['error']}",
                            'status': 404
                        }
                        return data
                else:
                    data = {
                        'msg': f'设置失败！未找到nid。\n请确认输入的学校、学院和班级名称正确，\n无法确认请使用：查组织 指令',
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_zhejiang(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    nid = item['nid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\nopenid：{openid}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理安徽地区用户数据
    @staticmethod
    async def set_anhui(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                """
                username: 姓名,
                gender: 性别（1为男性，0为女性）,
                mobile: 手机号,
                level1: 学校类型,
                level2: 学校名称,
                level3: 学院名称,
                level4: 班级团支部名称,
                level5: 'null'
                """
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group

                }
                content_json = json.loads(event.split("#")[-1])
                leader = ''
                area = event.split('#')[-2]
                username = content_json['username']
                token = content_json['token']
                gender = content_json['gender']
                mobile = content_json['mobile']
                level1 = content_json['level1']
                level2 = content_json['level2']
                level3 = content_json['level3']
                level4 = content_json['level4']
                level5 = content_json['level5']
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': username,
                    'token': token,
                    'gender': gender,
                    'mobile': mobile,
                    'level1': level1,
                    'university': level2,
                    'college': level3,
                    'class_name': level4,
                    'level5': level5,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_anhui(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{username}\nQQ号：{send_id}\n地区：{area}\ntoken：{token}\n学校：{level2}\n学院：{level3}\n班级(团支部)：{level4}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{username}\nQQ号:{send_id}\n地区：{area}\ntoken:{token}\n学校：{level2}\n学院：{level3}\n班级(团支部)：{level4}',
                        'status': 503
                    }
                    return data
                else:
                    data = {
                        'msg': f"出错了\n错误信息：{content['error']}",
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_anhui(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
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
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{username}\nQQ号:{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\n手机号：{mobile}\ntoken：{token}\n学校类型：{level1}\n学校：{level2}\n学院：{level3}\n班级(团支部)：{level4}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理山东地区用户数据
    @staticmethod
    async def set_shandong(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                content_json = json.loads(event.split('#')[-1])
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                openid = content_json['openid']
                cookie = content_json['cookie']
                class_name = content_json['class_name']
                university = content_json['university']
                college = content_json['college']
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': name,
                    'openid': openid,
                    'cookie': cookie,
                    'university': university,
                    'college': college,
                    'class_name': class_name,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_shandong(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                        'status': 503
                    }
                    return data
                else:
                    data = {
                        'msg': f"出错了\n错误信息：{content['error']}",
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_shandong(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid'],
                    cookie = item['cookie']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\nopenid：{openid}\ncookie：{cookie}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理四川地区用户数据
    @staticmethod
    async def set_sichuan(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                content_json = json.loads(event.split('#')[-1])
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                tel = content_json['tel']
                token = content_json['token']
                level1 = content_json['level1']
                level2 = content_json['level2']
                level3 = content_json['level3']
                level4 = content_json['level4']
                class_name = content_json['class_name']
                level1_name = content_json['level1_name']
                university = content_json['university']
                college = content_json['college']
                org = f"#{level1}#{level2}#{level3}#{level4}#"
                lastOrg = ""
                orgName = class_name
                allOrgName = f"#{level1_name}#{university}#{college}#{class_name}#"
                """data_json = {
                    "name": "",  # 此处填姓名
                    "tel": "",  # 此处填手机号
                    "org": "",  # #学校所属上级pid#学校pid#学院pid#班级（团支部）pid#
                    "lastOrg": "",
                    "orgName": "",  # 班级名称
                    "allOrgName": ""  # #学校所属上级名称#学校名称#学院名称+团委#班级（团支部）名称#
                }"""
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': name,
                    'tel': tel,
                    'token': token,
                    'org': org,
                    "lastOrg": lastOrg,
                    "orgName": orgName,
                    "allOrgName": allOrgName,
                    'university': university,
                    'college': college,
                    'class_name': class_name,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_sichuan(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号：{send_id}\n地区：{area}\ntoken：{token}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号：{send_id}\n地区：{area}\ntoken：{token}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                        'status': 503
                    }
                    return data
                else:
                    data = {
                        'msg': f"出错了\n错误信息：{content['error']}",
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_sichuan(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    token = item['token']
                    tel = item['tel']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\n手机号：{tel}\ntoken：{token}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理上海地区用户数据
    @staticmethod
    async def set_shanghai(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                content_json = json.loads(event.split('#')[-1])
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                university = content_json['university']
                college = content_json['college']
                class_name = content_json['class_name']
                accessToken = content_json['accessToken']
                cookie = content_json['cookie']
                nid = content_json['nid']
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': name,
                    'accessToken': accessToken,
                    'cookie': cookie,
                    'nid': nid,
                    'university': university,
                    'college': college,
                    'class_name': class_name,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_shanghai(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\naccessToken：{accessToken}\ncookie：{cookie}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\naccessToken：{accessToken}\ncookie：{cookie}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                        'status': 503
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_shanghai(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    accessToken = item['accessToken']
                    cookie = item['cookie']
                    nid = item['nid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ:{leader}\n通知群号：{group}\n地区：{area}\naccessToken：{accessToken}\ncookie：{cookie}\nnid：{nid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理吉林地区用户数据
    @staticmethod
    async def set_jilin(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                content_json = json.loads(event.split('#')[-1])
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                openid = content_json['openid']
                student_id = content_json['student_id']
                class_name = content_json['class_name']
                university = content_json['university']
                college = content_json['college']
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': name,
                    'student_id': student_id,
                    'openid': openid,
                    'university': university,
                    'college': college,
                    'class_name': class_name,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_jilin(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\nstudent_id：{student_id}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\nstudent_id：{student_id}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                        'status': 503
                    }
                    return data
                else:
                    data = {
                        'msg': f"出错了\n错误信息：{content['error']}",
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_jilin(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    student_id = item['student_id']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\nopenid：{openid}\nstudent_id：{student_id}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    # 处理重庆地区用户数据
    @staticmethod
    async def set_chongqing(send_id, event):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            id_mark = False
            for item in data_json:
                if int(item['qq']) == int(send_id):
                    name = item['name']
                    qq = item['qq']
                    data = {
                        'msg': f'设置失败！{name}({qq})信息存在！',
                        'status': 404
                    }
                    return data
            if not id_mark:
                content_json = json.loads(event.split('#')[-1])
                qq = int(send_id)
                group = ''
                auto_commit = {
                    "status": False,
                    "way": "private",
                    "send_qq": qq,
                    "send_group": group
                }
                leader = ''
                area = event.split('#')[-2]
                name = content_json['name']
                openid = content_json['openid']
                class_name = content_json['class_name']
                university = content_json['university']
                college = content_json['college']
                write_data = {
                    'qq': qq,
                    'auto_commit': auto_commit,
                    'area': area,
                    'leader': leader,
                    'name': name,
                    'openid': openid,
                    'university': university,
                    'college': college,
                    'class_name': class_name,
                    'dxx_name': '',
                    'commit_time': ''
                }
                data_json.append(write_data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=4, ensure_ascii=False)
                content = await AutoDxx.auto_chongqing(send_id)
                status = content['status']
                if status == 200:
                    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                        answer_obj = json.load(a)
                    dxx_name = list(answer_obj)[-1]["catalogue"]
                    commit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习成功！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
                elif status == 503:
                    data = {
                        'msg': f'大学习用户信息设置成功!\n提交最新一期大学习失败！\n请稍后使用指令：提交大学习 提交大学习！\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid：{openid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}',
                        'status': 503
                    }
                    return data
                else:
                    data = {
                        'msg': f"出错了\n错误信息：{content['error']}",
                        'status': 404
                    }
                    return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data

    @staticmethod
    async def check_chongqing(send_id):
        try:
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                obj = json.load(r)
            mark = False
            for item in obj:
                if int(send_id) == int(item['qq']):
                    qq = int(item['qq'])
                    group = item['auto_commit']['send_group']
                    status = item['auto_commit']['status']
                    way = item['auto_commit']['way']
                    if way == "group":
                        way = "群聊"
                    else:
                        way = "私聊"
                    if status:
                        status = '开启'
                    else:
                        status = '关闭'
                    leader = item['leader']
                    name = item['name']
                    area = item['area']
                    openid = item['openid']
                    university = item['university']
                    college = item['college']
                    class_name = item['class_name']
                    dxx_name = item['dxx_name']
                    commit_time = item['commit_time']
                    data = {
                        'msg': f'大学习用户信息查询成功!\n用户信息\n姓名：{name}\nQQ号：{qq}\n团支书QQ：{leader}\n通知群号：{group}\n地区：{area}\nopenid：{openid}\n学校：{university}\n学院：{college}\n班级(团支部)：{class_name}\n自动提交大学习状态：{status}\n自动提交大学习通知方式：{way}\n最近提交的大学习：\n提交期数：{dxx_name}\n提交时间：{commit_time}',
                        'status': 200
                    }
                    return data
            if not mark:
                data = {
                    'msg': '大学习用户信息查询失败！\n用户信息不存在！\n添加用户信息指令：添加大学习',
                    'status': 503
                }
                return data
        except Exception as result:
            data = {
                'status': 404,
                'msg': f'{result}'
            }
            return data



HandleDxx = HandleDxx()
