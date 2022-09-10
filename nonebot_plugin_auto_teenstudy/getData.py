import json
import os
import datetime
from bs4 import BeautifulSoup
from io import BytesIO
import base64
import random
from os.path import dirname
from httpx import AsyncClient
from PIL import Image, ImageDraw, ImageFont

fontPath = dirname(__file__) + '/resource/font/MiSans-Light.ttf'
data_path = os.path.dirname(__file__) + '/data'
bg_hb_path = dirname(__file__) + '/resource/own_bg_hb'
dxx_bg_path = dirname(__file__) + '/resource/dxx_bg'
end_path = dirname(__file__) + '/resource/endpic'
headers = {
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


async def get_own(send_id):
    with open(data_path + '/dxx_list.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
    try:
        mark = False
        for item in obj:
            if int(send_id) == int(item['qq']):
                name = item['name']
                uid = item['uid']
                danwei1 = item['university']
                danwei2 = item['college']
                danwei3 = item['class_name']
                text_all = danwei1 + danwei2 + danwei3
                font = ImageFont.truetype(fontPath, 48)
                path_list = []
                files = os.listdir(os.path.dirname(__file__) + '/resource/own_bg_hb')
                for file in files:
                    if file.endswith('.jpg'):
                        path_list.append(file)
                back = random.choice(path_list)
                img = Image.open(bg_hb_path + f'/{back}')
                draw = ImageDraw.Draw(img)
                time = datetime.datetime.now().strftime('%H:%M')
                draw.text((125, 25), text=time, font=font, fill='black')
                with open(data_path + '/dxx_answer.json', 'r', encoding='utf-8') as a:
                    answer_obj = json.load(a)
                title = list(answer_obj)[-1]["catalogue"]
                text = title
                draw.text((380, 1200), text=text, font=font, fill='black')
                text = name
                draw.text((380, 1290), text=text, font=font, fill='black')
                text = str(uid)
                draw.text((380, 1380), text=text, font=font, fill='black')
                text = text_all[:12]
                draw.text((380, 1470), text=text, font=font, fill='black')
                if len(text_all) >= 28:
                    text = text_all[12:31]
                    draw.text((155, 1540), text=text, font=font, fill='black')
                    text = text_all[31:]
                    draw.text((155, 1600), text=text, font=font, fill='black')
                else:
                    text = text[12:]
                    draw.text((155, 1540), text=text, font=font, fill='black')
                    text = ''
                    draw.text((155, 1600), text=text, font=font, fill='black')
                buf = BytesIO()
                img.save(buf, format="PNG")
                base64_str = base64.b64encode(buf.getbuffer()).decode()
                content = "base64://" + base64_str
                return content
        if not mark:
            content = '用户信息不存在！'
            return content
    except Exception as e:
        content = f'出错了\n错误信息：{e}'
        return content


async def get_end_pic():
    with open(data_path + '/dxx_answer.json', 'r', encoding='utf-8') as f:
        answer_obj = json.load(f)
    title = '"青年大学习“' + list(answer_obj)[-1]["catalogue"]
    path_list = []
    files = os.listdir(os.path.dirname(__file__) + '/resource/dxx_bg')
    for file in files:
        if file.endswith('.jpg'):
            path_list.append(file)
    back = random.choice(path_list)
    bg_img = Image.open(dxx_bg_path + f'/{back}')
    end_img = Image.open(end_path + f'/{list(answer_obj)[-1]["catalogue"]}.jpg')
    end_img = end_img.resize((1080, 2200), Image.BILINEAR)
    font = ImageFont.truetype(fontPath, 45)
    img = Image.new('RGB', (end_img.width, bg_img.height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    img.paste(bg_img)
    time = (datetime.datetime.now() + datetime.timedelta(minutes=random.randint(5, 10))).strftime('%H:%M')
    draw.text((120, 30), text=time, font=font, fill='black')
    draw.text((1080 / 2 - (len(title) / 2) * 30, 130), text=title, font=font, fill='black')
    img.paste(end_img, (0, 200))
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return content


async def get_answer():
    with open(data_path + '/dxx_answer.json', 'r', encoding='utf-8') as f:
        answer_obj = json.load(f)
    title = list(answer_obj)[-1]["catalogue"]
    answer = list(answer_obj)[-1]["answer"]
    start_time = list(answer_obj)[-1]['time']
    end_day = (datetime.datetime.strptime(list(answer_obj)[-1]["time"], "%Y年%m月%d日 %H:%M:%S") + datetime.timedelta(
        days=6)).strftime("%Y年%m月%d日")
    end_time = f'{end_day} 22:00:00'
    answer_bg = Image.open(dxx_bg_path + '/answer_bg.png')
    img = Image.new('RGB', (902, 987), (255, 255, 255))
    img.paste(answer_bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontPath, 55)
    draw.text((20, 20), text='青年大学习主题团课', fill='gold', font=font)
    font = ImageFont.truetype(fontPath, 48)
    draw.text((20, 100), text=title, fill='gold', font=font)
    font = ImageFont.truetype(fontPath, 40)
    draw.text((20, 180), fill='gold', font=font, text=answer)
    font = ImageFont.truetype(fontPath, 40)
    draw.text((420, 550), fill='gold', font=font, text=start_time)
    font = ImageFont.truetype(fontPath, 40)
    draw.text((420, 650), fill='gold', font=font, text=end_time)
    font = ImageFont.truetype(fontPath, 40)
    draw.text((550, 500), text='开始时间', fill='gold', font=font)
    font = ImageFont.truetype(fontPath, 40)
    draw.text((550, 600), text='结束时间', fill='gold', font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return content


async def crawl_answer():
    resp_url = 'https://h5.cyol.com/special/weixin/sign.json'
    async with AsyncClient(headers=headers) as client:
        response = await client.get(url=resp_url, timeout=10)
    response.encoding = response.charset_encoding
    code = json.loads(response.text)
    data_url = code[list(code)[-1]]['url']
    with open(data_path + '/dxx_answer.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
    dxx_url_list = []
    for item in obj:
        url = item['url']
        dxx_url_list.append(url)
    if data_url not in dxx_url_list:
        async with AsyncClient(headers=headers, max_redirects=5) as client:
            resp = await client.get(url=data_url, timeout=10)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        title = soup.find('title').text[7:].strip()
        dxx_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        start_div = resp.text.find('<div class="section0 topindex">')
        end_div = resp.text.find('<script type="text/javascript" src="js/index.js')
        soup = BeautifulSoup(resp.text[start_div:end_div], 'lxml')
        tmp = []
        answer_attrs = {"required": [], "optional": []}
        option = "ABCDEF"
        template = "{num}. {check}"
        for div in soup.find("body"):
            if div == "\n":
                continue
            answer = []
            if div.name == "div":
                for i in div.find_all("div"):
                    check = i.get("data-a")
                    if check is not None:
                        answer.append(check)
                if len(answer) > 4:
                    answer = answer[:int(len(answer) / 2)]
                tmp.append(answer)
        req_end = 0
        flag = {"location": 0, "result": True}
        for i, v in enumerate(tmp):
            if len(v) == 0:
                req_end = i + 1
            elif flag["result"]:
                flag["result"] = False
                flag["location"] = i
        for i, v in enumerate(tmp):
            if flag["location"] < req_end and req_end - 1 > i >= flag["location"]:
                field = "required"
                answer_attrs[field].append(v)
            elif flag["location"] == req_end and i >= req_end:
                field = "optional"
                answer_attrs[field].append(v)
            elif flag["location"] < req_end <= i:
                field = "optional"
                answer_attrs[field].append(v)
        output = []
        if len(answer_attrs["required"]) > 0:
            output.append("本期答案\n")
            for i, v in enumerate(answer_attrs["required"]):
                checks = ""
                for j, v2 in enumerate(v):
                    try:
                        if v2 == "1":
                            checks += option[j]
                    except:
                        pass
                output.append(template.format(num=i + 1, check=checks) + "\n")
        if len(answer_attrs["optional"]) != 0:
            output.append("课外习题\n")
            for i, v in enumerate(answer_attrs["optional"]):
                checks = ""
                for j, v2 in enumerate(v):
                    if v2 == "1":
                        checks += option[j]
                output.append(template.format(num=i + 1, check=checks) + "\n")
        result = [output[0]]
        for i, v in enumerate(output):
            if i % 13 != 0 and i != 0:
                result[int(i / 13)] += v
            elif i % 13 == 0 and i != 0:
                result.append(v)
        try:
            end_url = data_url.replace('m.html', 'images/end.jpg')
        except:
            end_url = data_url[:-6] + 'images/end.jpg'
        async with AsyncClient(headers=headers) as client:
            end_jpg = await client.get(end_url, timeout=10)
        with open(end_path + f'/{title}.jpg', 'wb') as e:
            e.write(end_jpg.content)
        data = {'catalogue': title,
                'time': dxx_time,
                'url': data_url,
                'end_url': end_url,
                'answer': result[0]
                }
        with open(data_path + '/dxx_answer.json', 'r', encoding='utf-8') as r:
            answer_obj = json.load(r)
        answer_obj.append(data)
        with open(data_path + '/dxx_answer.json', 'w', encoding='utf-8') as w:
            json.dump(answer_obj, w, indent=4, ensure_ascii=False)
        content = {'status': 200,
                   'catalogue': title,
                   'time': dxx_time
                   }
    else:
        content = {'status': 404,
                   'catalogue': '',
                   'time': ''
                   }
    return content
