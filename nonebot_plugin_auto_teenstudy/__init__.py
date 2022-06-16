import json
import os
import random
import string
import asyncio
import nonebot
from nonebot import require
from nonebot.log import logger
from datetime import datetime
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, Event
from .msg_pic import pic
from .dxx_hb import auto_hb
from .dxx_jx import auto_jx
from .dxx_zj import auto_zj
from .getData import get_own, get_end_pic, get_answer, crawl_answer

scheduler = require('nonebot_plugin_apscheduler').scheduler
super_id = nonebot.get_driver().config.superusers  # 超管id
# openid_zj = nonebot.get_driver().config.openid_zj  # 浙江地区openid
path = os.path.dirname(__file__) + '/data'  # 数据存放目录
pic_msg = False  # 初始机器人图片回复状态，默认关闭
# 开启机器人图片回复功能
pic_msg_open = on_command('开启大学习图片回复', aliases={'大学习图片回复开'}, rule=to_me(), permission=SUPERUSER)


@pic_msg_open.handle()
async def pic_msg_open(event: Event):
    send_id = event.get_user_id()
    global pic_msg
    pic_msg = True
    if send_id in super_id:
        message = '机器人开启大学习图片回复成功!'
        pict = await pic(message)
        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event, at_sender=True)


# 关闭机器人图片回复功能
pic_msg_close = on_command('大学习关闭图片回复', aliases={'大学习图片回复关'}, rule=to_me(), permission=SUPERUSER)


@pic_msg_close.handle()
async def pic_msg_close(event: Event):
    send_id = event.get_user_id()
    global pic_msg
    pic_msg = False
    if send_id in super_id:
        message = '机器人关闭大学习图片回复成功!'
        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


# 大学习功能，用于提交大学习，全员可用
dxx = on_command('提交大学习', aliases={'sub_dxx'}, priority=5)


@dxx.handle()
async def dxx(event: Event):
    send_id = event.get_user_id()
    try:
        mark = False
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(send_id) == int(item['qq']):
                if item['area'] == '湖北':
                    content = await auto_hb(send_id)
                    status = content['status']
                elif item['area'] == '江西':
                    content = await auto_jx(send_id)
                    status = content['status']
                # elif item['area'] == '浙江':
                #     content = await auto_zj(send_id)
                #     status = content['status']
                else:
                    status = 404
                mark = True
                if status == 200:
                    end = await get_end_pic()
                    area = item['area']
                    name = item['name']
                    openid = item['openid']
                    danwei1 = item['danwei1']
                    danwei2 = item['danwei2']
                    danwei3 = item['danwei3']
                    title = content['title']
                    message = f'大学习{title}提交成功!\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\n学校：{danwei1}\n学院：{danwei2}\n班级(团支部)：{danwei3}'
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        await asyncio.sleep(1)
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end), event=event, at_sender=True)
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        await asyncio.sleep(1)
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end), event=event, at_sender=True)
                else:
                    message = '提交失败！'
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                break
        if not mark:
            message = '用户数据不存在，请先配置用户文件！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


# 大学习功能，用于设置大学习配置，全员可用
set_dxx = on_command('设置大学习配置', aliases={'set_dxx'}, priority=5)


@set_dxx.handle()
async def set_dxx(event: Event):
    send_id = event.get_user_id()
    mark = False
    try:
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(send_id) == int(item['qq']):
                message = '用户数据存在'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                mark = True
                break
        if not mark:
            qq = int(send_id)
            area = str(event.get_message()).split('#')[-5]
            name = str(event.get_message()).split('#')[-4]
            openid = ''.join(random.sample(string.ascii_letters + string.digits, 28))
            uid = random.randint(4678688, 5678754)
            danwei1 = str(event.get_message()).split('#')[-3]
            danwei2 = str(event.get_message()).split('#')[-2]
            danwei3 = str(event.get_message()).split('#')[-1]
            title = ''
            if area == '湖北':
                data = {'qq': qq, 'area': area, 'openid': openid, 'uid': uid, 'name': name, 'danwei1': danwei1,
                        'danwei2': danwei2, 'danwei3': danwei3, 'title': title}
                obj.append(data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=4)
                content = await auto_hb(send_id)
                status = content['status']
            elif area == '江西':
                with open(path + '/dxx_jx.json', 'r', encoding='utf-8') as f:
                    n = json.load(f)
                mark1 = False
                for item1 in n:
                    if item1['school'] == danwei1 and item1['college'] == danwei2 and item1['class'] == danwei3:
                        nid = item1['id3']
                        mark1 = True
                        break
                if mark1:
                    data = {'qq': qq, 'area': area, 'openid': openid, 'uid': uid, 'name': name, 'danwei1': danwei1,
                            'danwei2': danwei2, 'danwei3': danwei3, 'nid': nid, 'title': title}
                    obj.append(data)
                    with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                        json.dump(obj, f, ensure_ascii=False, indent=4)
                    content = await auto_jx(send_id)
                    status = content['status']
                else:
                    status = 404
            # elif area == '浙江':
            #     with open(path + '/dxx_zj.json', 'r', encoding='utf-8') as f:
            #         n = json.load(f)
            #     mark1 = False
            #     for item1 in n:
            #         if item1['school'] == danwei1 and item1['college'] == danwei2 and item1['class'] == danwei3:
            #             nid = item1['id3']
            #             mark1 = True
            #             break
            #     if mark1:
            #         for i in openid_zj:
            #             openid = str(i)
            #         data = {'qq': qq, 'area': area, 'openid': openid, 'uid': uid, 'name': name, 'danwei1': danwei1,
            #                 'danwei2': danwei2, 'danwei3': danwei3, 'nid': nid, 'title': title}
            #         obj.append(data)
            #         with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
            #             json.dump(obj, f, ensure_ascii=False, indent=4)
            #         content = await auto_zj(send_id)
            #         status = content['status']
            #     else:
            #         status = 404
            else:
                status = 404
            if status == 200:
                message = f'大学习用户信息设置成功!\n用户信息\n姓名：{name}\nQQ号:{send_id}\n地区：{area}\nopenid:{openid}\n学校：{danwei1}\n学院：{danwei2}\n班级(团支部)：{danwei3}'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                                 event=event)
                else:

                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), at_sender=True,
                                                 event=event)
            else:
                message = '设置失败'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                                 event=event)
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), at_sender=True,
                                                 event=event)
    except Exception as e:
        message = f'设置失败！您指令输入有误！\n正确指令格式：设置大学习配置#地区#姓名#学校名称#团委名称#班级\nps:班级名称一定要输入正确，不清楚请使用指令：查组织'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


delete_dxx = on_command('删除大学习配置', aliases={'删除大学习用户', 'del_dxx'}, permission=SUPERUSER)


@delete_dxx.handle()
async def delete_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        delete_id = int(str(event.get_message()).split('#')[-1])
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        list1 = {}
        for item in obj:
            if delete_id == int(item['qq']):
                name = item['name']
                list1 = item
                message = f'已将用户：{name}信息删除！'
                if pic_msg:
                    pict = await pic(message)
                    if send_id in super_id:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                else:
                    if send_id in super_id:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                mark = True
                break
        if not mark:
            message = f'失败！\n用户QQ:{delete_id}不在大学习信息配置表中。'
            if pic_msg:
                pict = await pic(message)
                if send_id in super_id:
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
            else:
                if send_id in super_id:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
        else:
            obj.remove(list1)
            with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=4)
    except Exception as e:
        message = f'出错了\n错误信息：{e}'
        if pic_msg:
            pict = await pic(message)
            if send_id in super_id:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
        else:
            if send_id in super_id:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


add_dxx = on_command('添加大学习配置', aliases={'添加大学习用户', 'add_dxx'}, permission=SUPERUSER)


@add_dxx.handle()
async def add_dxx(event: Event):
    send_id = event.get_user_id()
    qq = str(event.get_message()).split('#')[-6]
    mark = False
    try:
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(qq) == int(item['qq']):
                message = '用户数据存在'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                mark = True
                break
        if not mark:
            area = str(event.get_message()).split('#')[-5]
            name = str(event.get_message()).split('#')[-4]
            openid = ''.join(random.sample(string.ascii_letters + string.digits, 28))
            uid = random.randint(4678688, 5678754)
            danwei1 = str(event.get_message()).split('#')[-3]
            danwei2 = str(event.get_message()).split('#')[-2]
            danwei3 = str(event.get_message()).split('#')[-1]
            title = ''
            if area == '湖北':
                data = {'qq': qq, 'area': area, 'openid': openid, 'uid': uid, 'name': name, 'danwei1': danwei1,
                        'danwei2': danwei2, 'danwei3': danwei3, 'title': title}
                obj.append(data)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=4)
                content = await auto_hb(send_id)
                status = content['status']
            elif area == '江西':
                with open(path + '/dxx_jx.json', 'r', encoding='utf-8') as f:
                    n = json.load(f)
                mark1 = False
                nid = ''
                for item1 in n:
                    if item1['school'] == danwei1 and item1['college'] == danwei2 and item1['class'] == danwei3:
                        nid = item1['id3']
                        mark1 = True
                        break
                if mark1:
                    data = {'qq': qq, 'area': area, 'openid': openid, 'uid': uid, 'name': name, 'danwei1': danwei1,
                            'danwei2': danwei2, 'danwei3': danwei3, 'nid': nid, 'title': title}
                    obj.append(data)
                    with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                        json.dump(obj, f, ensure_ascii=False, indent=4)
                    content = await auto_jx(send_id)
                    status = content['status']
                else:
                    status = 0
            # elif area == '浙江':
            #     with open(path + '/dxx_zj.json', 'r', encoding='utf-8') as f:
            #         n = json.load(f)
            #     mark1 = False
            #     for item1 in n:
            #         if item1['school'] == danwei1 and item1['college'] == danwei2 and item1['class'] == danwei3:
            #             nid = item1['id3']
            #             mark1 = True
            #             break
            #     if mark1:
            #         for i in openid_zj:
            #             openid = str(i)
            #         data = {'qq': qq, 'area': area, 'openid': openid, 'uid': uid, 'name': name, 'danwei1': danwei1,
            #                 'danwei2': danwei2, 'danwei3': danwei3, 'nid': nid, 'title': title}
            #         obj.append(data)
            #         with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
            #             json.dump(obj, f, ensure_ascii=False, indent=4)
            #         content = await auto_zj(send_id)
            #         status = content['status']
            #     else:
            #         status = 404
            else:
                status = 0
            if status == 200:
                message = f'大学习用户信息设置成功!\n用户信息\n姓名：{name}\nQQ号:{qq}\n地区：{area}\nopenid:{openid}\n学校：{danwei1}\n学院：{danwei2}\n班级(团支部)：{danwei3}'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                                 event=event)
                else:

                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), at_sender=True,
                                                 event=event)
            else:
                message = '设置失败'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                                 event=event)
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), at_sender=True,
                                                 event=event)
    except Exception as e:
        message = f'设置失败！您指令输入有误！\n正确指令格式：添加大学习用户#QQ号#地区#姓名#学校名称#团委名称#班级\nps:班级名称一定要输入正确，不清楚请使用指令：查组织'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


check_dxx_list = on_command('查看大学习用户列表', aliases={'check_dxx_list'}, permission=SUPERUSER)


@check_dxx_list.handle()
async def check_dxx_list(event: Event):
    send_id = event.get_user_id()
    try:
        message = '序号<-->QQ号<-->地区<-->姓名<-->团支部(班级)\n'
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        num = 1
        for item in obj:
            qq = item['qq']
            area = item['area']
            name = item['name']
            danwei3 = item['danwei3']
            message = message + f'{num}<-->{qq}<-->{area}<-->{name}<-->{danwei3}\n'
            num += 1
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


check_dxx_user = on_command('查看大学习用户', aliases={'check_dxx_user', '查看大学习配置'}, permission=SUPERUSER)


@check_dxx_user.handle()
async def check_dxx_user(event: Event):
    send_id = event.get_user_id()
    try:
        check_id = str(event.get_message()).split('#')[-1]
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        for item in obj:
            if int(check_id) == int(item['qq']):
                area = item['area']
                name = item['name']
                openid = item['openid']
                danwei1 = item['danwei1']
                danwei2 = item['danwei2']
                danwei3 = item['danwei3']
                message = f'大学习用户信息查询成功！\n姓名：{name}\nQQ号：{check_id}\n地区：{area}\nopenid:{openid}\n学校：{danwei1}\n学院：{danwei2}\n团支部(班级)：{danwei3}'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                mark = True
                break
        if not mark:
            message = f'大学习用户信息查询失败！\n用户：{check_id}不存在！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
    except Exception as e:
        message = f'大学习用户信息查询失败！\n正确指令格式：查看大学习用户#QQ号'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


my_dxx = on_command('我的大学习', aliases={'查看我的大学习', 'my_dxx'}, priority=5)


@my_dxx.handle()
async def my_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        check_id = int(send_id)
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        for item in obj:
            if int(check_id) == int(item['qq']):
                area = item['area']
                name = item['name']
                openid = item['openid']
                danwei1 = item['danwei1']
                danwei2 = item['danwei2']
                danwei3 = item['danwei3']
                if area == '湖北':
                    message = f'大学习用户信息查询成功！\n姓名：{name}\nQQ号：{check_id}\n地区：{area}\nopenid:{openid}\n学校：{danwei1}\n学院：{danwei2}\n团支部(班级)：{danwei3}'
                elif area == '江西':
                    nid = item['nid']
                    message = f'大学习用户信息查询成功！\n姓名：{name}\nQQ号：{check_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{danwei1}\n学院：{danwei2}\n团支部(班级)：{danwei3}'
                # elif area == '浙江':
                #     nid = item['nid']
                #     message = f'大学习用户信息查询成功！\n姓名：{name}\nQQ号：{check_id}\n地区：{area}\nopenid:{openid}\nnid:{nid}\n学校：{danwei1}\n学院：{danwei2}\n团支部(班级)：{danwei3}'
                else:
                    pass
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                mark = True
                break
        if not mark:
            message = f'大学习用户信息查询失败！\n用户：{check_id}不存在！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


check_class = on_command('查组织', aliases={'查班级', 'check_class'}, priority=5)


@check_class.handle()
async def check_class(event: Event):
    send_id = event.get_user_id()
    try:
        area = str(event.get_message()).split("#")[-3]
        school = str(event.get_message()).split("#")[-2]
        college = str(event.get_message()).split("#")[-1]
        with open(path + f'/dxx_{area}.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        class_list = '序号<-->学校<-->班级\n'
        num = 1
        for item in obj:
            if school == item['school'] and college == item['college']:
                title = item['class']
                class_list = class_list + f'{num}<-->{school}<-->{title}\n'
                mark = True
                num += 1
        if mark:
            if pic_msg:
                pict = await pic(class_list)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(class_list), event=event,
                                             at_sender=True)
        else:
            message = f'查询失败！\n请检查学校或团委名称是否输入正确！\n正确指令格式：查组织#地区简写(例江西为：jx)#学校名称#团委名称'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except Exception as e:
        message = f'查询失败！\n正确指令格式：查组织#地区简写(例江西为：jx)#学校名称#团委名称'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


dxx_help = on_command('大学习帮助', aliases={'大学习功能', 'dxx_help'}, priority=5)


@dxx_help.handle()
async def dxx_help(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_help.txt', 'r', encoding='utf-8') as f:
            message = f.read()
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


finish_dxx = on_command('完成大学习', aliases={'finish_dxx'}, permission=SUPERUSER)


@finish_dxx.handle()
async def finish_dxx(event: Event):
    send_id = event.get_user_id()
    finish_id = str(event.get_message()).split('#')[-1]
    try:
        mark = False
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(finish_id) == int(item['qq']):
                if item['area'] == '湖北':
                    content = await auto_hb(finish_id)
                    status = content['status']
                elif item['area'] == '江西':
                    content = await auto_jx(finish_id)
                    status = content['status']
                # elif item['area'] == '浙江':
                #     content = await auto_zj(finish_id)
                #     status = content['status']
                else:
                    status = 404
                mark = True
                if status == 200:
                    end = await get_end_pic()
                    area = item['area']
                    name = item['name']
                    openid = item['openid']
                    danwei1 = item['danwei1']
                    danwei2 = item['danwei2']
                    danwei3 = item['danwei3']
                    title = content['title']
                    message = f'大学习{title}提交成功!\n用户信息\n姓名：{name}\nQQ号:{finish_id}\n地区：{area}\nopenid:{openid}\n学校：{danwei1}\n学院：{danwei2}\n团支部(班级)：{danwei3}'
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        await asyncio.sleep(1)
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end), event=event, at_sender=True)
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        await asyncio.sleep(1)
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end), event=event, at_sender=True)
                else:
                    message = '提交失败！'
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                break
        if not mark:
            message = '用户数据不存在，请先配置用户文件！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


get_own_xx = on_command('个人信息截图', aliases={'青春湖北截图'}, priority=5)


@get_own_xx.handle()
async def get_own_xx(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(send_id) == int(item['qq']) and item['area'] == '湖北':
                content = await get_own(send_id)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(content), event=event)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


dxx_end_img = on_command('大学习完成截图', aliases={'完成截图', '大学习截图', 'dxx_end'}, priority=5)


@dxx_end_img.handle()
async def dxx_eng_img(event: Event):
    send_id = event.get_user_id()
    try:
        end_img = await get_end_pic()
        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(end_img), event=event)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


dxx_answer = on_command('青年大学习', aliases={'大学习', 'dxx_answer'}, priority=5)


@dxx_answer.handle()
async def dxx_answer(event: Event):
    send_id = event.get_user_id()
    try:
        answer_img = await get_answer()
        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(answer_img), event=event)
    except Exception as e:
        message = f'出错了\n错误信息:{e}'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


# 每周一10:00开始检测是否更新，每3分检测一次，觉得检测间隔太久，请手动修改asyncio.sleep()，获取到答案后终止检测。
@scheduler.scheduled_job('cron', day_of_week='0', hour=10, minute=0, id='a', timezone="Asia/Shanghai")
async def remind():
    try:
        num = 0
        while True:
            content = await crawl_answer()
            if content['status'] == 200:
                num = 0
                answer_img = await get_answer()
                end_img = await get_end_pic()
                title = content['catalogue']
                stat_time = content['time']
                message = f'本周的大学习开始喽!\n{title}\n开始时间：{stat_time}\n答案见图一\n完成截图见图二\nPs:当各地区大学习更新以后，可使用 提交大学习 指令完成大学习！'
                with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                for qq in obj['qq_list']:
                    await nonebot.get_bot().send_private_msg(user_id=qq, message=MessageSegment.text(
                        message) + MessageSegment.image(answer_img) + MessageSegment.image(end_img))
                    await asyncio.sleep(random.randint(2, 5))
                for group in obj['group_list']:
                    await nonebot.get_bot().send_group_msg(group_id=group, message=MessageSegment.text(
                        message) + MessageSegment.image(answer_img) + MessageSegment.image(end_img))
                    await asyncio.sleep(random.randint(2, 5))
                break
            else:
                num += 1
                await asyncio.sleep(180)
            if num >= 70:
                num = 0
                message = '本周没有大学习！'
                with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                for qq in obj['qq_list']:
                    await nonebot.get_bot().send_private_msg(user_id=qq, message=MessageSegment.text(message))
                    await asyncio.sleep(random.randint(2, 5))
                for group in obj['group_list']:
                    await nonebot.get_bot().send_group_msg(group_id=group, message=MessageSegment.text(message))
                    await asyncio.sleep(random.randint(2, 5))
                break
    except Exception as e:
        for su in super_id:
            await nonebot.get_bot().send_private_msg(user_id=int(su), message=f'错误信息{e}',
                                                     at_sender=True)


close_time_task = on_command('全局关闭大学习推送', aliases={'全局关闭推送'}, permission=SUPERUSER)


@close_time_task.handle()
async def close_time_task(event: Event):
    send_id = event.get_user_id()
    try:
        message = "已全局关闭青年大学习自动检查更新推送。"
        scheduler.pause_job(job_id='a')
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                         event=event)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, at_sender=True, event=event)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                         event=event)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, at_sender=True, event=event)


recover_time_task = on_command('全局开启大学习推送', aliases={'全局开启推送'}, permission=SUPERUSER)


@recover_time_task.handle()
async def recover_time_task(event: Event):
    send_id = event.get_user_id()
    try:
        message = "已全局开启青年大学习自动检查更新推送。"
        scheduler.resume_job(job_id='a')
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                         event=event)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, at_sender=True, event=event)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                         event=event)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, at_sender=True, event=event)


# 机器人主人使用，用于添加推送好友
add_friend_list = on_command('添加推送好友', permission=SUPERUSER)


@add_friend_list.handle()
async def add_friend_list(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的好友
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_list = obj['qq_list']
        add_qq = int(str(event.get_message()).split('#')[-1])
        if add_qq not in qq_list:
            qq_list.append(add_qq)
            obj['qq_list'] = qq_list
            with open(path + '/dxx_push_list.json', 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4, ensure_ascii=False)
            message = f'已将好友：{add_qq}加入推送列表'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)

        else:
            message = f'加入失败！\n好友：{add_qq}已经在推送列表中了'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                         event=event)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, at_sender=True, event=event)


# 机器人主人使用，用于删除推送好友
del_friend_list = on_command('删除推送好友', permission=SUPERUSER)


@del_friend_list.handle()
async def del_friend_list(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的好友
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_list = obj['qq_list']
        del_qq = int(str(event.get_message()).split('#')[-1])
        if del_qq not in qq_list:
            message = f'删除失败!\n好友：{del_qq}不在好友推送列表'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            qq_list.remove(del_qq)
            obj['qq_list'] = qq_list
            with open(path + '/dxx_push_list.json', 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4, ensure_ascii=False)
            message = f'已将好友：{del_qq}移出推送列表！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                         event=event)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, at_sender=True, event=event)


add_group_list = on_command('添加推送群聊', permission=SUPERUSER)


@add_group_list.handle()
async def add_group_list(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的群
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        group_list = obj['group_list']
        add_group = int(str(event.get_message()).split('#')[-1])
        if add_group not in group_list:
            group_list.append(add_group)
            obj['group_list'] = group_list
            with open(path + '/dxx_push_list.json', 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
            message = f'已将群：{add_group}加入推送列表'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            message = f'加入失败！\n群：{add_group}已经在推送列表中了'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


# 机器人主人使用，用于删除推送群聊
del_group_list = on_command('删除推送群聊', permission=SUPERUSER)


@del_group_list.handle()
async def del_group_list(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的群
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        group_list = obj['group_list']
        del_group = int(str(event.get_message()).split('#')[-1])
        if del_group not in group_list:
            message = f'删除失败！\n群：{del_group}不在推送列表'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            group_list.remove(del_group)
            obj['group_list'] = group_list
            with open(path + '/dxx_push_list.json', 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4, ensure_ascii=False)
            message = f'已将群：{del_group}移出推送列表！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


# 机器人主人使用，用于查询推送群聊列表
index_group_list = on_command('查询推送群聊列表', permission=SUPERUSER)


@index_group_list.handle()
async def index_group_list(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的群
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        group_list = obj['group_list']
        if group_list:
            message = ''
            for i in group_list:
                message = message + '群：' + str(i) + '\n' + ''
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            message = '暂无推送群聊！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


# 机器人主人使用，用于查询推送好友列表
index_qq_list = on_command('查询推送好友列表', permission=SUPERUSER)


@index_qq_list.handle()
async def index_qq_list(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的好友
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_list = obj['qq_list']
        if qq_list:
            message = ''
            for i in qq_list:
                message = message + '好友：' + str(i) + '\n' + ''
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            message = '暂无推送好友！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)

    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


# 开启大学习定时更新推送
recover_task = on_command('开启大学习推送', priority=5, rule=to_me())


@recover_task.handle()
async def recover_task(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的好友
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_list = obj['qq_list']
        if int(send_id) not in qq_list:
            qq_list.append(int(send_id))
            obj['qq_list'] = qq_list
            with open(path + '/dxx_push_list.json', 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4, ensure_ascii=False)
                message = '青年大学习定时更新推送开启成功!'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            message = '你已经开启了青年大学习定时更新推送了！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except:
        message = '出错了!请询问机器人主人以解决问题！'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


# 关闭大学习定时更新推送
close_task = on_command('关闭大学习推送', priority=5)


@close_task.handle()
async def close_task(event: Event):
    send_id = event.get_user_id()
    try:
        # 读取需要推送的好友
        with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_list = obj['qq_list']
        if int(send_id) not in qq_list:
            message = '你已经关闭青年大学习定时更新推送了！!'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
        else:
            qq_list.remove(int(send_id))
            obj['qq_list'] = qq_list
            with open(path + '/dxx_push_list.json', 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4, ensure_ascii=False)
            message = '青年大学习定时更新推送关闭成功!'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
    except:
        message = '出错了!请询问机器人主人以解决问题！'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
