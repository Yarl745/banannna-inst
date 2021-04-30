import re
from io import BytesIO

import aiohttp
import pytesseract
from PIL import Image, ImageEnhance
from aiohttp import payload
from asgiref.sync import sync_to_async


async def get_banana_num(stories_url: str) -> int:
    stories_data = await get_stories_data(stories_url)
    banana_num = await find_banana_num(stories_data) if stories_data else None
    return banana_num


async def get_stories_data(stories_url: str) -> payload:
    async with aiohttp.ClientSession() as session:
        async with session.get(stories_url) as response:
            return await response.read()


@sync_to_async
def find_banana_num(stories_data: payload):
    image_data = BytesIO(stories_data)
    img: Image.Image = Image.open(image_data)

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(3)

    img_text = pytesseract.image_to_string(img, lang='eng')
    pattern = re.compile(r"#\d+")
    found_strings = re.findall(pattern=pattern, string=img_text)

    return int(found_strings[-1][1:]) if found_strings else None

