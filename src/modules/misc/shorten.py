import aiohttp

from config import config


async def short(url, short):
    try:
        api_url = f"{config.shortener_url}/api/create"
        payload = {"full": url, "short": short}

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return True, data.get("url")

                return False, None

    except aiohttp.ClientError as e:
        print(f"Error creating short URL: {e}")
        return False, None
