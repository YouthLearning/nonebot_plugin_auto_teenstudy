import json
import os
import random
import asyncio
import nonebot
from nonebot import require
from nonebot.log import logger
from datetime import datetime
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command,PluginMetadata
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, Event, PrivateMessageEvent, PRIVATE
from .msg_pic import pic
from .dxx import AutoDxx
from .getData import get_own, get_end_pic, get_answer, crawl_answer
from .handle_dxx_data import HandleDxx



__plugin_meta__ = PluginMetadata(
    name='nonebot_plugin_auto_teenstudy',
    description='一个可以自动提交青年大学习的插件',
    usage='添加大学习',
    homepage="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy",
    type="application",
    supported_adapters={"~onebot.v11"},
    extra={
        'author': 'ZM25XC',
        'version': '0.1.9',
        'priority': 5,
    }

)
scheduler = require('nonebot_plugin_apscheduler').scheduler
super_id = nonebot.get_driver().config.superusers  # 超管id
path = os.path.dirname(__file__) + '/data'  # 数据存放目录
pic_msg = True  # 初始机器人图片回复状态，默认关闭
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
    send_id = int(event.get_user_id())
    try:
        mark = False
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(send_id) == int(item['qq']):
                if item['area'] == '湖北':
                    content = await AutoDxx.auto_hubei(send_id)
                    status = content['status']
                elif item['area'] == '江西':
                    content = await AutoDxx.auto_jiangxi(send_id)
                    status = content['status']
                elif item['area'] == '浙江':
                    content = await AutoDxx.auto_zhejiang(send_id)
                    status = content['status']
                elif item['area'] == '安徽':
                    content = await AutoDxx.auto_anhui(send_id)
                    status = content['status']
                elif item['area'] == '四川':
                    content = await AutoDxx.auto_sichuan(send_id)
                    status = content['status']
                elif item['area'] == '山东':
                    content = await AutoDxx.auto_shandong(send_id)
                    status = content['status']
                elif item['area'] == '上海':
                    content = await AutoDxx.auto_shanghai(send_id)
                    status = content['status']
                elif item['area'] == '吉林':
                    content = await AutoDxx.auto_jilin(send_id)
                    status = content['status']
                elif item['area'] == '重庆':
                    content = await AutoDxx.auto_chongqing(send_id)
                    status = content['status']
                else:
                    content = {
                        "msg": '该地区暂未支持！',
                        "status": 404
                    }
                    status = content['status']
                if status == 200:
                    end = await get_end_pic()
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        await asyncio.sleep(1)
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end), event=event, at_sender=True)
                        if item['area'] == '湖北':
                            content = await get_own(send_id)
                            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(
                                '个人信息截图') + MessageSegment.image(content),
                                                         event=event)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        await asyncio.sleep(1)
                        await nonebot.get_bot().send(user_id=send_id,
                                                     message=MessageSegment.text('完成截图\n') + MessageSegment.image(
                                                         end), event=event, at_sender=True)
                        if item['area'] == '湖北':
                            content = await get_own(send_id)
                            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(
                                '个人信息截图') + MessageSegment.image(content),
                                                         event=event, at_sender=True)
                        return None
                else:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event, at_sender=True)
                        return None

        if not mark:
            message = '用户数据不存在，请先配置用户文件！'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                return None
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
set_dxx = on_command('添加大学习', aliases={'set_dxx'}, priority=5)


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
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                    return None
        if not mark:
            area = str(event.get_message()).split('#')[-2]
            if area == '湖北':
                content = await HandleDxx.set_hubei(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '江西':
                content = await HandleDxx.set_jiangxi(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '浙江':
                content = await HandleDxx.set_zhejiang(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '安徽':
                content = await HandleDxx.set_anhui(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '四川':
                content = await HandleDxx.set_sichuan(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '山东':
                content = await HandleDxx.set_shandong(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '上海':
                content = await HandleDxx.set_shanghai(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '吉林':
                content = await HandleDxx.set_jilin(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            elif area == '重庆':
                content = await HandleDxx.set_chongqing(send_id=send_id, event=str(event.get_message()))
                status = content['status']
            else:
                content = {
                    "msg": '添加失败！该地区暂未支持！',
                    "status": 404
                }
                status = content['status']
            message = content['msg']
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), at_sender=True,
                                             event=event)
    except Exception as e:
        message = f'添加失败！您指令输入有误！\n正确指令格式：添加大学习#地区#姓名#学校名称#团委名称#班级\nps:班级名称一定要输入正确，不清楚请使用指令：查组织'
        logger.error(f"{datetime.now()}: 错误信息：{e}")
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)


delete_dxx = on_command('删除大学习', aliases={'删除大学习', 'del_dxx'}, permission=SUPERUSER)


@delete_dxx.handle()
async def delete_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        delete_id = int(str(event.get_message()).split('#')[-1])
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        for item in obj:
            if delete_id == int(item['qq']):
                name = item['name']
                message = f'已将用户：{name}信息删除！'
                obj.remove(item)
                with open(path + '/dxx_list.json', 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=4)
                if pic_msg:
                    pict = await pic(message)
                    if send_id in super_id:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                        return None
                else:
                    if send_id in super_id:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        return None
        if not mark:
            message = f'失败！\n用户QQ:{delete_id}不在大学习信息配置表中。'
            if pic_msg:
                pict = await pic(message)
                if send_id in super_id:
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                    return None
            else:
                if send_id in super_id:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                    return None

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


add_dxx = on_command('设置大学习配置', aliases={'设置大学习用户', 'add_dxx'}, permission=SUPERUSER)


@add_dxx.handle()
async def add_dxx(event: Event):
    send_id = event.get_user_id()
    qq = str(event.get_message()).split('#')[-3]
    mark = False
    try:
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if int(qq) == int(item['qq']):
                message = '用户数据存在!'
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                    return None
        if not mark:
            area = str(event.get_message()).split('#')[-2]
            if area == '湖北':
                content = await HandleDxx.set_hubei(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '江西':
                content = await HandleDxx.set_jiangxi(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '浙江':
                content = await HandleDxx.set_zhejiang(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '安徽':
                content = await HandleDxx.set_anhui(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '四川':
                content = await HandleDxx.set_sichuan(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '山东':
                content = await HandleDxx.set_shandong(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '上海':
                content = await HandleDxx.set_shanghai(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '吉林':
                content = await HandleDxx.set_jilin(send_id=qq, event=str(event.get_message()))
                status = content['status']
            elif area == '重庆':
                content = await HandleDxx.set_chongqing(send_id=qq, event=str(event.get_message()))
                status = content['status']
            else:
                content = {
                    "msg": '设置失败！该地区暂未支持！',
                    "status": 404
                }
                status = content['status']
            message = content['msg']
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), at_sender=True,
                                             event=event)
                return None
    except Exception as e:
        message = f'设置失败！您指令输入有误！'
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
        message = '序号<-->QQ号<-->地区<-->姓名<-->团支部(班级)<-->最近一次提交时间\n'
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        num = 1
        for item in obj:
            qq = item['qq']
            area = item['area']
            name = item['name']
            class_name = item['class_name']
            dxx_name = item['dxx_name']
            commit_time = item['commit_time']
            message = message + f'{num}<-->{qq}<-->{area}<-->{name}<-->{class_name}<-->{commit_time}\n'
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
                if area == '湖北':
                    content = await HandleDxx.check_hubei(send_id=check_id)
                    status = content['status']
                elif area == '江西':
                    content = await HandleDxx.check_jiangxi(send_id=check_id)
                    status = content['status']
                elif area == '浙江':
                    content = await HandleDxx.check_zhejiang(send_id=check_id)
                    status = content['status']
                elif area == '安徽':
                    content = await HandleDxx.check_anhui(send_id=check_id)
                    status = content['status']
                elif area == '四川':
                    content = await HandleDxx.check_sichuan(send_id=check_id)
                    status = content['status']
                elif area == '山东':
                    content = await HandleDxx.check_shandong(send_id=check_id)
                    status = content['status']
                elif area == '上海':
                    content = await HandleDxx.check_shanghai(send_id=check_id)
                    status = content['status']
                elif area == '吉林':
                    content = await HandleDxx.check_jilin(send_id=check_id)
                    status = content['status']
                elif area == '重庆':
                    content = await HandleDxx.check_chongqing(send_id=check_id)
                    status = content['status']
                else:
                    status = 404
                    content = {
                        "msg": '该地区暂未支持！'
                    }
                if status == 200:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:

                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True,
                                                     event=event)
                        return None
                elif status == 503:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:

                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True,
                                                     event=event)
                        return None
                else:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True,
                                                     event=event)
                        return None
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
                if area == '湖北':
                    content = await HandleDxx.check_hubei(send_id=check_id)
                    status = content['status']
                elif area == '江西':
                    content = await HandleDxx.check_jiangxi(send_id=check_id)
                    status = content['status']
                elif area == '浙江':
                    content = await HandleDxx.check_zhejiang(send_id=check_id)
                    status = content['status']
                elif area == '安徽':
                    content = await HandleDxx.check_anhui(send_id=check_id)
                    status = content['status']
                elif area == '四川':
                    content = await HandleDxx.check_sichuan(send_id=check_id)
                    status = content['status']
                elif area == '山东':
                    content = await HandleDxx.check_shandong(send_id=check_id)
                    status = content['status']
                elif area == '上海':
                    content = await HandleDxx.check_shanghai(send_id=check_id)
                    status = content['status']
                elif area == '吉林':
                    content = await HandleDxx.check_jilin(send_id=check_id)
                    status = content['status']
                elif area == '重庆':
                    content = await HandleDxx.check_chongqing(send_id=check_id)
                    status = content['status']
                else:
                    status = 404
                    content = {
                        'msg': '该地区暂未支持！'
                    }
                if status == 200:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:

                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True,
                                                     event=event)
                        return None
                elif status == 503:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:

                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True,
                                                     event=event)
                        return None
                else:
                    message = content['msg']
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True,
                                                     event=event)
                        return None

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


finish_dxx = on_command('完成大学习', aliases={'finish_dxx'}, priority=5)


@finish_dxx.handle()
async def finish_dxx(event: Event):
    send_id = int(event.get_user_id())
    finish_id = int(str(event.get_message()).split('#')[-1])
    try:
        mark = False
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        for item in obj:
            if send_id in super_id or str(item['leader']) == str(send_id):
                if int(finish_id) == int(item['qq']):
                    if item['area'] == '湖北':
                        content = await AutoDxx.auto_hubei(finish_id)
                        status = content['status']
                    elif item['area'] == '江西':
                        content = await AutoDxx.auto_jiangxi(finish_id)
                        status = content['status']
                    elif item['area'] == '浙江':
                        content = await AutoDxx.auto_zhejiang(finish_id)
                        status = content['status']
                    elif item['area'] == '安徽':
                        content = await AutoDxx.auto_anhui(finish_id)
                        status = content['status']
                    elif item['area'] == '四川':
                        content = await AutoDxx.auto_sichuan(finish_id)
                        status = content['status']
                    elif item['area'] == '山东':
                        content = await AutoDxx.auto_shandong(finish_id)
                        status = content['status']
                    elif item['area'] == '上海':
                        content = await AutoDxx.auto_shanghai(finish_id)
                        status = content['status']
                    elif item['area'] == '吉林':
                        content = await AutoDxx.auto_jilin(finish_id)
                        status = content['status']
                    elif item['area'] == '重庆':
                        content = await AutoDxx.auto_chongqing(finish_id)
                        status = content['status']
                    else:
                        content = {
                            "msg": '该地区暂未支持！'
                        }
                        status = 404
                    if status == 200:
                        end = await get_end_pic()
                        message = content['msg']
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                         at_sender=True,
                                                         event=event)
                            await asyncio.sleep(1)
                            await nonebot.get_bot().send(user_id=send_id,
                                                         message=MessageSegment.text(
                                                             '完成截图\n') + MessageSegment.image(
                                                             end), event=event, at_sender=True)
                            return None
                        else:
                            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                            await asyncio.sleep(1)
                            await nonebot.get_bot().send(user_id=send_id,
                                                         message=MessageSegment.text(
                                                             '完成截图\n') + MessageSegment.image(
                                                             end), event=event, at_sender=True)
                            return None
                    else:
                        message = content['msg']
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                         at_sender=True,
                                                         event=event)
                            return None
                        else:
                            await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                            return None
            else:
                message = "无权限！"
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                 at_sender=True,
                                                 event=event)
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                    return None
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
        mark = False
        for item in obj:
            if int(send_id) == int(item['qq']):
                if item['area'] == '湖北':
                    content = await get_own(send_id)
                    await nonebot.get_bot().send(user_id=send_id,
                                                 message=MessageSegment.text('个人信息截图') + MessageSegment.image(
                                                     content), event=event)
                    return None
                else:
                    message = '你所处地区不支持该功能！'
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        return None
        if not mark:
            message = '\n用户信息不存在！请使用 添加大学习 指令添加'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
                return None
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


# 每周一9:00开始检测是否更新，每1.5分检测一次，觉得检测间隔太久，请手动修改asyncio.sleep()，获取到答案后终止检测。
@scheduler.scheduled_job('cron', day_of_week='0', hour=9, minute=0, id='update_dxx', timezone="Asia/Shanghai")
async def remind():
    try:
        num = 0
        while True:
            content = await crawl_answer()
            if content['status'] == 200:
                answer_img = await get_answer()
                end_img = await get_end_pic()
                title = content['catalogue']
                stat_time = content['time']
                message = f'\n本周的大学习开始喽!\n{title}\n开始时间：{stat_time}\n答案见图一\n完成截图见图二\nPs:当各地区大学习更新以后，可使用 提交大学习 指令完成大学习！'
                with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                for qq in obj['qq_list']:
                    await nonebot.get_bot().send_private_msg(user_id=qq, message=MessageSegment.text(
                        message) + MessageSegment.image(answer_img) + MessageSegment.image(end_img))
                    await asyncio.sleep(random.randint(20, 30))
                for group in obj['group_list']:
                    await nonebot.get_bot().send_group_msg(group_id=group, message=MessageSegment.at("all")+MessageSegment.text(
                        message) + MessageSegment.image(answer_img) + MessageSegment.image(end_img))
                    await asyncio.sleep(random.randint(20, 30))
                return None
            else:
                num += 1
                await asyncio.sleep(90)
            if num >= 140:
                message = '\n本周没有大学习！'
                with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                for qq in obj['qq_list']:
                    await nonebot.get_bot().send_private_msg(user_id=qq, message=MessageSegment.text(message))
                    await asyncio.sleep(random.randint(20, 30))
                for group in obj['group_list']:
                    await nonebot.get_bot().send_group_msg(group_id=group, message=MessageSegment.at("all")+MessageSegment.text(message))
                    await asyncio.sleep(random.randint(20, 30))
                return None
    except Exception as e:
        for su in super_id:
            await nonebot.get_bot().send_private_msg(user_id=int(su), message=f'错误信息{e}',
                                                     at_sender=True)


# 每周一11:30执行自动提交大学功能，每30s~120s提交一个人，觉得提交间隔太久，请手动修改asyncio.sleep()，所有开了大学习自动提交的用户都提交后后终止。
@scheduler.scheduled_job('cron', day_of_week='0', hour=11, minute=30, id='auto_dxx', timezone="Asia/Shanghai")
async def auto_dxx_commit():
    with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
        data_json = json.load(r)
    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as r:
        answer_obj = json.load(r)
    dxx_name = list(answer_obj)[-1]["catalogue"]
    try:
        num = 0
        for item in data_json:
            if item['dxx_name'] != dxx_name:
                if item['auto_commit']['status']:
                    auto_content = await AutoDxx.auto_dxx(int(item['qq']))
                    end_img = await get_end_pic()
                    if item['auto_commit']['way'] == 'private':
                        message = '\n青年大学习自动提交结果\n' + auto_content['msg']
                        num += 1
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.image(
                                                                         pict) + MessageSegment.image(end_img))
                        else:
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.text(
                                                                         message) + MessageSegment.image(
                                                                         end_img))
                        if item['area'] == '湖北':
                            own_pict = await get_own(int(item['qq']))
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.text(
                                                                         '个人信息截图') + MessageSegment.image(
                                                                         own_pict))
                    else:
                        message = '\n青年大学习自动提交结果\n' + auto_content['msg']
                        num += 1
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.image(
                                                                       pict) + MessageSegment.image(
                                                                       end_img))
                        else:
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.text(
                                                                       message) + MessageSegment.image(
                                                                       end_img))
                        if item['area'] == '湖北':
                            own_pict = await get_own(item['qq'])
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.text(
                                                                       '个人信息截图') + MessageSegment.image(
                                                                       own_pict))
                    await asyncio.sleep(random.randint(30, 90))
                else:
                    continue
        message = f'大学习用户列表中有{num}名同学开启了自动提交功能\n当前全部执行完毕！'
        for sq in super_id:
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send_private_msg(user_id=int(sq), message=MessageSegment.image(pict),
                                                         at_sender=True)
                return None
            else:
                await nonebot.get_bot().send_private_msg(user_id=int(sq), message=message, at_sender=True)
                return None
    except Exception as e:
        message = f'自动提交大学习出错了!\n错误日志:{e}'
        for sq in super_id:
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send_private_msg(user_id=int(sq), message=MessageSegment.image(pict),
                                                         at_sender=True)
                return None
            else:
                await nonebot.get_bot().send_private_msg(user_id=int(sq), message=MessageSegment.text(message),
                                                         at_sender=True)
                return None


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
recover_task = on_command('开启大学习推送', permission=PRIVATE, rule=to_me())


@recover_task.handle()
async def recover_task(event: PrivateMessageEvent):
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
close_task = on_command('关闭大学习推送', permission=PRIVATE, rule=to_me())


@close_task.handle()
async def close_task(event: PrivateMessageEvent):
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


open_auto_dxx = on_command('开启自动提交大学习', aliases={'open_auto_dxx', '大学习自动提交开'}, priority=5)


@open_auto_dxx.handle()
async def open_auto_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        for item in obj:
            if int(item['qq']) == int(send_id):
                if not item['auto_commit']['status']:
                    item['auto_commit']['status'] = True
                    message = f"\n青年大学习自动提交开启成功！"
                    with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                        json.dump(obj, w, indent=4, ensure_ascii=False)
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                                     at_sender=True)
                        return None
                else:
                    message = f"\n当前状态为开启状态，无需更改！"
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                                     at_sender=True)
                        return None
        if not mark:
            message = '\n用户信息不存在！请使用 添加大学习 指令添加'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


close_auto_dxx = on_command('关闭自动提交大学习', aliases={'close_auto_dxx', '大学习自动提交关'}, priority=5)


@close_auto_dxx.handle()
async def close_auto_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        mark = False
        for item in obj:
            if int(item['qq']) == int(send_id):
                if item['auto_commit']['status']:
                    item['auto_commit']['status'] = False
                    message = f"\n青年大学习自动提交关闭成功！"
                    with open(path + '/dxx_list.json', 'w', encoding='utf-8') as w:
                        json.dump(obj, w, indent=4, ensure_ascii=False)
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                                     at_sender=True)
                        return None
                else:
                    message = f"\n当前状态为关闭状态，无需更改！"
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                     at_sender=True)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                                     at_sender=True)
                        return None
        if not mark:
            message = '\n用户信息不存在！请使用 添加大学习 指令添加'
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)


change_info = on_command('更改个人信息', aliases={'更改信息', 'change_info'}, priority=5)


@change_info.handle()
async def change_info(event: Event):
    send_id = int(event.get_user_id())
    try:
        content = await HandleDxx.change_own(send_id=send_id, event=str(event.get_message()))
        message = content['msg']
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None
    except Exception as e:
        message = f"出错了!错误信息：\n{e}"
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


change_user_info = on_command('更改用户信息', aliases={'change_user_info'}, priority=5)


@change_user_info.handle()
async def change_user_info(event: Event):
    send_id = int(event.get_user_id())
    change_id = int(str(event.get_message()).split('#')[-2])
    try:
        content = await HandleDxx.change_own(send_id=change_id, event=str(event.get_message()))
        message = content['msg']
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None
    except Exception as e:
        message = f"出错了!错误信息：\n{e}"
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


update_dxx = on_command('更新大学习', aliases={'update_dxx', '强制更新大学习'}, permission=SUPERUSER)


@update_dxx.handle()
async def update_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        content = await crawl_answer()
        if content['status'] == 200:
            answer_img = await get_answer()
            end_img = await get_end_pic()
            title = content['catalogue']
            stat_time = content['time']
            message = f'青年大学习更新成功!\n{title}\n开始时间：{stat_time}\n答案见图一\n完成截图见图二\nPs:当各地区大学习更新以后，可使用 提交大学习 指令完成大学习！'
            if send_id in super_id:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(
                    message) + MessageSegment.image(answer_img) + MessageSegment.image(end_img), event=event,
                                             at_sender=True)
                return None
            else:
                return None
        else:
            message = f"当前青年大学习已是最新数据！无需更新！"
            if send_id in super_id:
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                                 at_sender=True)
                    return None
            else:
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


send_dxx = on_command('推送大学习', aliases={'send_dxx'}, permission=SUPERUSER)


@send_dxx.handle()
async def send_dxx(event: Event):
    send_id = event.get_user_id()
    try:
        content = await crawl_answer()
        if content['status'] == 200:
            msg = '检测到青年大学习有更新，启动更新推送并执行自动提交大学习功能！'
            if pic_msg:
                pict = await pic(msg)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(msg), event=event,
                                             at_sender=True)
            answer_img = await get_answer()
            end_img = await get_end_pic()
            title = content['catalogue']
            stat_time = content['time']
            message = f'\n本周的大学习开始喽!\n{title}\n开始时间：{stat_time}\n答案见图一\n完成截图见图二\nPs:当各地区大学习更新以后，可使用 提交大学习 指令完成大学习！'
            with open(path + '/dxx_push_list.json', 'r', encoding='utf-8') as f:
                obj = json.load(f)
            for qq in obj['qq_list']:
                await nonebot.get_bot().send_private_msg(user_id=qq, message=MessageSegment.text(
                    message) + MessageSegment.image(answer_img) + MessageSegment.image(end_img))
                await asyncio.sleep(random.randint(2, 5))
            for group in obj['group_list']:
                await nonebot.get_bot().send_group_msg(group_id=group,
                                                       message=MessageSegment.at(user_id="all") + MessageSegment.text(
                                                           message) + MessageSegment.image(
                                                           answer_img) + MessageSegment.image(end_img))
                await asyncio.sleep(random.randint(2, 5))
            with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
                data_json = json.load(r)
            await asyncio.sleep(random.randint(180, 600))
            for item in data_json:
                if item['auto_commit']['status']:
                    auto_content = await AutoDxx.auto_dxx(item['qq'])
                    if item['auto_commit']['way'] == 'private':
                        message = '\n自动提交青年大学习结果\n' + auto_content['msg']
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.image(
                                                                         pict) + MessageSegment.image(end_img))
                        else:
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.text(
                                                                         message) + MessageSegment.image(
                                                                         end_img))
                        if item['area'] == '湖北':
                            own_pict = await get_own(item['qq'])
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.text(
                                                                         '个人信息截图') + MessageSegment.image(
                                                                         own_pict))
                    else:
                        message = '\n自动提交青年大学习结果\n' + auto_content['msg']
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.image(
                                                                       pict) + MessageSegment.image(
                                                                       end_img))
                        else:
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.text(
                                                                       message) + MessageSegment.image(
                                                                       end_img))
                        if item['area'] == '湖北':
                            own_pict = await get_own(item['qq'])
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.text(
                                                                       '个人信息截图') + MessageSegment.image(
                                                                       own_pict))
                    await asyncio.sleep(random.randint(60, 120))
                else:
                    await asyncio.sleep(random.randint(60, 120))
                    continue
            return None
        else:
            message = f"当前青年大学习已是最新数据！无需推送！"
            if send_id in super_id:
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                                 at_sender=True)
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                                 at_sender=True)
                    return None
            else:
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


all_submit = on_command("一键提交", aliases={'全员大学习', 'all_submit'}, priority=5)


@all_submit.handle()
async def all_submit(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as r:
            answer_obj = json.load(r)
        dxx_name = list(answer_obj)[-1]["catalogue"]
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        item_list = []
        finish_list = []
        finished_list = []
        unfinished_list = []
        for item in obj:
            if str(send_id) == str(item['leader']):
                if item['dxx_name'] != dxx_name:
                    if item['area'] == '湖北':
                        content = await AutoDxx.auto_hubei(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '江西':
                        content = await AutoDxx.auto_jiangxi(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '浙江':
                        content = await AutoDxx.auto_zhejiang(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '安徽':
                        content = await AutoDxx.auto_anhui(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '四川':
                        content = await AutoDxx.auto_sichuan(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '山东':
                        content = await AutoDxx.auto_shandong(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '上海':
                        content = await AutoDxx.auto_shanghai(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '吉林':
                        content = await AutoDxx.auto_jilin(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '重庆':
                        content = await AutoDxx.auto_chongqing(int(item['qq']))
                        status = content['status']
                    else:
                        content = {
                            "msg": '该地区暂未支持！',
                            "status": 404
                        }
                        status = content['status']
                    if status == 200:
                        finish_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                    else:
                        unfinished_list.append(
                            {"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                else:
                    finished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                item_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
        if len(item_list):
            unfinish_list = finish_list + unfinished_list
            message = f"\n一键提交青年大学习成功！\n团支部一共有{len(item_list)}名同学\n"
            if len(finished_list):
                message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for x, finished in enumerate(finished_list):
                    message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
            if len(unfinish_list):
                message = message + f"执行前未完成大学习的有{len(unfinish_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for y, unfinish in enumerate(unfinish_list):
                    message = message + f"{y + 1}<-->{unfinish['name']}<-->{unfinish['commit_time']}<-->{unfinish['qq']}\n"
            if len(unfinished_list):
                message = message + f"本次提交失败共有{len(unfinished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for z, unfinished in enumerate(unfinished_list):
                    message = message + f"{z + 1}<-->{unfinished['name']}<-->{unfinished['commit_time']}<-->{unfinished['qq']}\n"
            else:
                if len(finish_list):
                    message = message + f"本次提交成功共有{len(finish_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                    for k, finish in enumerate(finish_list):
                        message = message + f"{k + 1}<-->{finish['name']}<-->{finish['commit_time']}<-->{finish['qq']}\n"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                return None
        if send_id in super_id:
            finish_list = []
            finished_list = []
            unfinished_list = []
            for item in obj:
                if item['dxx_name'] != dxx_name:
                    if item['area'] == '湖北':
                        content = await AutoDxx.auto_hubei(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '江西':
                        content = await AutoDxx.auto_jiangxi(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '浙江':
                        content = await AutoDxx.auto_zhejiang(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '安徽':
                        content = await AutoDxx.auto_anhui(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '四川':
                        content = await AutoDxx.auto_sichuan(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '山东':
                        content = await AutoDxx.auto_shandong(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '上海':
                        content = await AutoDxx.auto_shanghai(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '吉林':
                        content = await AutoDxx.auto_jilin(int(item['qq']))
                        status = content['status']
                    elif item['area'] == '重庆':
                        content = await AutoDxx.auto_chongqing(int(item['qq']))
                        status = content['status']
                    else:
                        content = {
                            "msg": '该地区暂未支持！',
                            "status": 404
                        }
                        status = content['status']
                    if status == 200:
                        finish_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                    else:
                        unfinished_list.append(
                            {"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                else:
                    finished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
            item_list = finish_list + finished_list + unfinished_list
            unfinish_list = finish_list + unfinished_list
            message = f"\n一键提交青年大学习成功！\n一共有{len(item_list)}名同学\n"
            if len(finished_list):
                message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for x, finished in enumerate(finished_list):
                    message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
            if len(unfinish_list):
                message = message + f"执行前未完成大学习的有{len(unfinish_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for y, unfinish in enumerate(unfinish_list):
                    message = message + f"{y + 1}<-->{unfinish['name']}<-->{unfinish['commit_time']}<-->{unfinish['qq']}\n"
            if len(unfinished_list):
                message = message + f"本次提交失败共有{len(unfinished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for z, unfinished in enumerate(unfinished_list):
                    message = message + f"{z + 1}<-->{unfinished['name']}<-->{unfinished['commit_time']}<-->{unfinished['qq']}\n"
            else:
                if len(finish_list):
                    message = message + f"本次提交成功共有{len(finish_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                    for k, finish in enumerate(finish_list):
                        message = message + f"{k + 1}<-->{finish['name']}<-->{finish['commit_time']}<-->{finish['qq']}\n"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                return None
        else:
            message = "无权限！"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


dxx_remind = on_command('一键提醒', priority=5)


@dxx_remind.handle()
async def dxx_remind(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as r:
            answer_obj = json.load(r)
        dxx_name = list(answer_obj)[-1]["catalogue"]
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        item_list = []
        finished_list = []
        unfinished_list = []
        for item in obj:
            if str(send_id) == str(item['leader']):
                if item['dxx_name'] != dxx_name:
                    unfinished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                else:
                    finished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                item_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
        if len(item_list):
            if len(unfinished_list):
                for item2 in unfinished_list:
                    message = f"{item2['name']}同学，请及时完成青年大学习{dxx_name}！"
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=item2['qq'], message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                    else:
                        await nonebot.get_bot().send(user_id=item2['qq'], message=message, event=event, at_sender=True)
                    await asyncio.sleep(random.randint(5, 10))
                message = f"\n一键提醒成功！\n团支部一共有{len(item_list)}名同学\n"
                if len(finished_list):
                    message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                    for x, finished in enumerate(finished_list):
                        message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
                if len(unfinished_list):
                    message = message + f"截至本次提醒前未完成青年大学习共有{len(unfinished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                    for z, unfinished in enumerate(unfinished_list):
                        message = message + f"{z + 1}<-->{unfinished['name']}<-->{unfinished['commit_time']}<-->{unfinished['qq']}\n"
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                                 event=event)
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                    return None
            else:
                message = f"\n一键提醒成功！\n团支部一共有{len(item_list)}名同学\n本团支部所有同学都完成了青年大学习{dxx_name}\n"
                if len(finished_list):
                    message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                    for x, finished in enumerate(finished_list):
                        message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
                if pic_msg:
                    pict = await pic(message)
                    await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                                 event=event)
                    return None
                else:
                    await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                    return None
        if send_id in super_id:
            finished_list = []
            unfinished_list = []
            for item in obj:
                if item['dxx_name'] != dxx_name:
                    unfinished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                else:
                    finished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                item_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
            if len(item_list):
                if len(unfinished_list):
                    for item2 in unfinished_list:
                        message = f"{item2['name']}同学，请及时完成青年大学习{dxx_name}！"
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send(user_id=item2['qq'], message=MessageSegment.image(pict),
                                                         at_sender=True,
                                                         event=event)
                        else:
                            await nonebot.get_bot().send(user_id=item2['qq'], message=message, event=event,
                                                         at_sender=True)
                        await asyncio.sleep(random.randint(5, 10))
                    message = f"\n一键提醒成功！\n一共有{len(item_list)}名同学\n"
                    if len(finished_list):
                        message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                        for x, finished in enumerate(finished_list):
                            message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
                    if len(unfinished_list):
                        message = message + f"截至本次提醒前未完成青年大学习共有{len(unfinished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                        for z, unfinished in enumerate(unfinished_list):
                            message = message + f"{z + 1}<-->{unfinished['name']}<-->{unfinished['commit_time']}<-->{unfinished['qq']}\n"
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        return None
                else:
                    message = f"\n一键提醒成功！\n一共有{len(item_list)}名同学\n本团支部所有同学都完成了青年大学习{dxx_name}\n"
                    if len(finished_list):
                        message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                        for x, finished in enumerate(finished_list):
                            message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
                    if pic_msg:
                        pict = await pic(message)
                        await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True,
                                                     event=event)
                        return None
                    else:
                        await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                        return None
        else:
            message = "无权限！"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


dxx_check = on_command('一键查询', priority=5)


@dxx_check.handle()
async def dxx_check(event: Event):
    send_id = event.get_user_id()
    try:
        with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as r:
            answer_obj = json.load(r)
        dxx_name = list(answer_obj)[-1]["catalogue"]
        with open(path + '/dxx_list.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        item_list = []
        finish_list = []
        finished_list = []
        for item in obj:
            if str(send_id) == str(item['leader']):
                if item['dxx_name'] != dxx_name:
                    finish_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                else:
                    finished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                item_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
        if len(item_list):
            unfinish_list = finish_list
            message = f"\n一键查询成功！\n团支部一共有{len(item_list)}名同学\n"
            if len(finished_list):
                message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for x, finished in enumerate(finished_list):
                    message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
            if len(unfinish_list):
                message = message + f"执行前未完成大学习的有{len(unfinish_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for y, unfinish in enumerate(unfinish_list):
                    message = message + f"{y + 1}<-->{unfinish['name']}<-->{unfinish['commit_time']}<-->{unfinish['qq']}\n"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                return None
        if send_id in super_id:
            finish_list = []
            finished_list = []
            for item in obj:
                if item['dxx_name'] != dxx_name:
                    finish_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
                else:
                    finished_list.append({"name": item['name'], "qq": item['qq'], "commit_time": item['commit_time']})
            item_list = finish_list + finished_list
            unfinish_list = finish_list
            message = f"\n一键查询成功！\n一共有{len(item_list)}名同学\n"
            if len(finished_list):
                message = message + f"其中执行前已完成大学习的有{len(finished_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for x, finished in enumerate(finished_list):
                    message = message + f"{x + 1}<-->{finished['name']}<-->{finished['commit_time']}<-->{finished['qq']}\n"
            if len(unfinish_list):
                message = message + f"执行前未完成大学习的有{len(unfinish_list)}名同学\n依次为：\n序号<-->姓名<-->提交时间<-->QQ号\n"
                for y, unfinish in enumerate(unfinish_list):
                    message = message + f"{y + 1}<-->{unfinish['name']}<-->{unfinish['commit_time']}<-->{unfinish['qq']}\n"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), at_sender=True,
                                             event=event)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=message, event=event, at_sender=True)
                return None
        else:
            message = "无权限！"
            if pic_msg:
                pict = await pic(message)
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                             at_sender=True)
                return None
            else:
                await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                             at_sender=True)
                return None
    except Exception as e:
        message = f'出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.image(pict), event=event,
                                         at_sender=True)
            return None
        else:
            await nonebot.get_bot().send(user_id=send_id, message=MessageSegment.text(message), event=event,
                                         at_sender=True)
            return None


start_auto_dxx = on_command("启动自动提交", aliases={'执行自动提交', 'auto_dxx'}, permission=SUPERUSER)


@start_auto_dxx.handle()
async def start_auto_dxx(event: Event):
    send_id = int(event.get_user_id())
    with open(path + '/dxx_list.json', 'r', encoding='utf-8') as r:
        data_json = json.load(r)
    with open(path + '/dxx_answer.json', 'r', encoding='utf-8') as r:
        answer_obj = json.load(r)
    dxx_name = list(answer_obj)[-1]["catalogue"]
    try:
        num = 0
        for item in data_json:
            if item['dxx_name'] != dxx_name:
                if item['auto_commit']['status']:
                    auto_content = await AutoDxx.auto_dxx(int(item['qq']))
                    end_img = await get_end_pic()
                    if item['auto_commit']['way'] == 'private':
                        message = '\n自动提交青年大学习结果\n' + auto_content['msg']
                        num += 1
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.image(
                                                                         pict) + MessageSegment.image(end_img))
                        else:
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.text(
                                                                         message) + MessageSegment.image(
                                                                         end_img))
                        if item['area'] == '湖北':
                            own_pict = await get_own(item['qq'])
                            await nonebot.get_bot().send_private_msg(user_id=int(item['auto_commit']['send_qq']),
                                                                     message=MessageSegment.text(
                                                                         '个人信息截图') + MessageSegment.image(
                                                                         own_pict))
                    else:
                        message = '\n自动提交青年大学习结果\n' + auto_content['msg']
                        num += 1
                        if pic_msg:
                            pict = await pic(message)
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.image(
                                                                       pict) + MessageSegment.image(
                                                                       end_img))
                        else:
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.text(
                                                                       message) + MessageSegment.image(
                                                                       end_img))
                        if item['area'] == '湖北':
                            own_pict = await get_own(item['qq'])
                            await nonebot.get_bot().send_group_msg(group_id=int(item['auto_commit']['send_group']),
                                                                   message=MessageSegment.at(user_id=int(
                                                                       item['auto_commit'][
                                                                           'send_qq'])) + MessageSegment.text(
                                                                       '个人信息截图') + MessageSegment.image(
                                                                       own_pict))
                    await asyncio.sleep(random.randint(30, 120))
                else:
                    continue
        message = f'大学习用户列表中有{num}名同学开启了自动提交功能\n当前全部执行完毕！'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send_private_msg(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True)
            return None
        else:
            await nonebot.get_bot().send_private_msg(user_id=send_id, message=message, at_sender=True)
            return None
    except Exception as e:
        message = f'自动提交大学习出错了!\n错误日志:{e}'
        if pic_msg:
            pict = await pic(message)
            await nonebot.get_bot().send_private_msg(user_id=send_id, message=MessageSegment.image(pict),
                                                     at_sender=True)
            return None
        else:
            await nonebot.get_bot().send_private_msg(user_id=send_id, message=MessageSegment.text(message),
                                                     at_sender=True)
            return None
