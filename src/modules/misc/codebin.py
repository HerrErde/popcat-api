from datetime import datetime

import aiohttp
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

from config import config

allowed_languages = {"javascript", "html", "json", "css", "markdown"}


async def create(title, description, code):
    try:
        api_url = f"{config.codebin_url}/api/createpaste"

        try:
            lexer = guess_lexer(code)
            lang = lexer.name.strip().lower()
            if lang not in allowed_languages:
                lang = "plaintext"
        except ClassNotFound:
            lang = "plaintext"

        payload = {
            "title": title,
            "description": description,
            "code": code,
            "language": lang,
            "theme": "vs-dark",
            "time": datetime.now().isoformat(),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return True, data.get("slug")

                return False, None

    except aiohttp.ClientError as e:
        print(f"Error creating short URL: {e}")
        return False, None
