from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from os.path import dirname

fontPath = dirname(__file__) + '/resource/font/MiSans-Light.ttf'


async def pic(text):
    fontSize = 30  # 字体大小
    lines = text.split('\n')
    # 画布颜色
    img = Image.new('RGB', (1080, len(lines) * (fontSize + 7)), (255, 255, 255))  # (fontSize * (len(lines) + 10)
    dr = ImageDraw.Draw(img)
    # 字体样式
    font = ImageFont.truetype(fontPath, fontSize)
    # 文字颜色
    dr.text((0, 0), text, font=font, fill="#000000")
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str
