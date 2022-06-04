import asyncio
import json
import os
import random
import string
import nonebot
from nonebot.log import logger
from datetime import datetime
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, Event
from .msg_pic import pic
from .dxx_hb import auto_hb
from .dxx_jx import auto_jx
from .get_src import get_pic

super_id = nonebot.get_driver().config.superusers  # 超管id
path = os.path.dirname(__file__) + '/data'  # 数据存放目录
pic_msg = False  # 初始机器人图片回复状态，默认关闭
# 开启机器人图片回复功能
pic_msg_open = on_command('开启图片回复', aliases={'图片回复开'}, rule=to_me(), permission=SUPERUSER)


@pic_msg_open.handle()
async def pic_msg_open(event: Event):
    send_id = event.get_user_id()
    global pic_msg
    pic_msg = True
    if send_id in super_id:
        message = '机器人开启图片回复成功!'
        pict = await pic(message)
        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event, at_sender=True)


# 关闭机器人图片回复功能
pic_msg_close = on_command('关闭图片回复', aliases={'图片回复关'}, rule=to_me(), permission=SUPERUSER)


@pic_msg_close.handle()
async def pic_msg_close(event: Event):
    send_id = event.get_user_id()
    global pic_msg
    pic_msg = False
    if send_id in super_id:
        message = '机器人关闭图片回复成功!'
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
                else:
                    status = 404
                mark = True
                if status == 200:
                    img = await get_pic()
                    end = img['end']
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
                        c = "你也可以点击链接进行截图以获取带手机状态栏的完成截图\nhttps://qndxx.scubot.live/\n如果QQ不能直接打开请复制到微信打开！"
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end) + MessageSegment.text(c), event=event, at_sender=True)
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        await asyncio.sleep(1)
                        c = "你也可以点击链接进行截图以获取带手机状态栏的完成截图\nhttps://qndxx.scubot.live/\n如果QQ不能直接打开请复制到微信打开！"
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end) + MessageSegment.text(c), event=event, at_sender=True)
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
            uid = ''
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
            uid = ''
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
        message = '一、主人专用\n1、添加大学习配置|添加大学习用户|add_dxx\n指令格式：添加大学习配置#QQ号#地区#姓名#学校#团委(学院)#团支部(班级)\n2、删除大学习配置|删除大学习用户|del_dxx\n指令格式：删除大学习配置#QQ号\n' \
                  '3、查看大学习用户列表\n4、查看大学习用户|查看大学习配置|check_dxx_user\n指令格式：查看大学习用户#QQ号\n5、完成大学习|finish_dxx\n指令格式：完成大学习#QQ号\n6、开启（关闭）图片回复|图片回复开（关）\n二、全员可用\n1、提交大学习\n2、我的大学习|查看我的大学习|my_dxx\n3、大学习功能|大学习帮助|dxx_help\n' \
                  '4、设置大学习配置|set_dxx\n指令格式：设置大学习配置#地区#姓名#学校#团委(学院)#团支部(班级)\n5、查组织|查班级|check_class\n指令格式：查组织#地区简写(例江西为：jx)#学校名称#团委名称\nPs:查组织功能对湖北用户无效！'
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
                else:
                    status = 404
                mark = True
                if status == 200:
                    img = await get_pic()
                    end = img['end']
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
                        c = "你也可以点击链接进行截图以获取带手机状态栏的完成截图\nhttps://qndxx.scubot.live/\n如果QQ不能直接打开请复制到微信打开！"
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end) + MessageSegment.text(c), event=event, at_sender=True)
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        await asyncio.sleep(1)
                        c = "你也可以点击链接进行截图以获取带手机状态栏的完成截图\nhttps://qndxx.scubot.live/\n如果QQ不能直接打开请复制到微信打开！"
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end) + MessageSegment.text(c), event=event, at_sender=True)
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
