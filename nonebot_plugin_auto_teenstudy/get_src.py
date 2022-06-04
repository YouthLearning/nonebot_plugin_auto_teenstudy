import json
from httpx import AsyncClient
from nonebot.log import logger


async def get_pic():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    try:
        async with AsyncClient(headers=headers) as client:
            response = await client.get(req_url)
            response.encoding = response.apparent_encoding
            json_obj = json.loads(response.text)
            try:
                end = json_obj['result']['uri'].replace('m.html', 'images/end.jpg')
            except Exception as e:
                logger.error(e)
                end = json_obj['result']['uri'][:-6] + 'images/end.jpg'
            data = {
                'end': end
            }
            return data
    except Exception as e:
        logger.error(e)
        raise e
