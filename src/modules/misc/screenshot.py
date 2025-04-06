import asyncio
import random
from io import BytesIO
from urllib.parse import urlparse

import aiohttp
from PIL import Image
from playwright.async_api import async_playwright

from config import config
from helper import RedisHandler


async def random_proxy():
    base_url = "https://api.proxyscrape.com/v4/free-proxy-list/get"
    params = {
        "request": "get_proxies",
        "country": "us,gb",
        "skip": 0,
        "proxy_format": "protocolipport",
        "format": "json",
        "limit": 15,
        "anonymity": "Transparent",
        "timeout": 2018,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch proxies: {response.status}")

                data = await response.json()
                proxy_list = data.get("proxies", [])

                if not proxy_list:
                    raise Exception("No proxies found in response.")

                return random.choice(proxy_list)["proxy"]
    except Exception as e:
        print(f"Error fetching proxy: {str(e)}")
        return None


async def take(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower().strip()
    path = parsed_url.path.rstrip("/")
    domainpath = f":{path}" if path else ""
    query = parsed_url.query

    cache_key = (
        f"screenshot:{host}{domainpath}?{query}"
        if query
        else f"screenshot:{host}{domainpath}"
    )

    redis_client = await RedisHandler().get_client()

    if redis_client:
        if await redis_client.exists(cache_key):
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return cached_data

    try:
        async with async_playwright() as p:
            if config.playwright_server:
                if config.debug:
                    print("Connected to Remote Playwright Server")
                browser = await p.chromium.connect(config.playwright_server)
            else:
                browser = await p.chromium.launch(headless=True)

            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            if config.screenshot_proxy:
                proxy = await random_proxy()
                context = await browser.contexts.append(
                    proxy={"server": proxy},
                )

            page = await context.new_page()
            response = await page.goto(url)
            await page.wait_for_load_state("domcontentloaded")

            if not response or response.status >= 400:
                await browser.close()
                return None

            await page.set_viewport_size({"width": 1920, "height": 1080})

            response = await page.goto(url)
            content_type = response.headers.get("content-type", "")

            if "text/html" in content_type:
                await asyncio.sleep(1.5)

                image_bytes = await page.screenshot(timeout=config.screenshot_timeout)

            if config.screenshot_compress:
                with Image.open(BytesIO(image_bytes)) as img:
                    output_bytes = BytesIO()
                    img.convert("RGB").save(output_bytes, format="JPEG", quality=75)
                    output_bytes.seek(0)
                    image_bytes = output_bytes.read()

            if redis_client:
                try:
                    await redis_client.setex(
                        cache_key, config.screenshot_cache_exp, image_bytes
                    )
                except Exception as e:
                    print(f"Redis error: {e}")
                    return None

            await browser.close()
            return image_bytes

    except TimeoutError:
        print(f"Timeout while navigating to {url}.")
    except NotImplementedError as e:
        print(f"System does not support required asyncio subprocess: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

    return None


async def takee(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower().strip()
    path = parsed_url.path.rstrip("/")
    domainpath = f":{path}" if path else ""
    query = parsed_url.query

    cache_key = (
        f"screenshot:{host}{domainpath}?{query}"
        if query
        else f"screenshot:{host}{domainpath}"
    )

    redis_client = await RedisHandler().get_client()

    if redis_client:
        if await redis_client.exists(cache_key):
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return cached_data

    screenshot_api_url = (
        f"https://rapidapi-example-screenshot-app.vercel.app/api/screenshot?url={url}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                screenshot_api_url, timeout=config.screenshot_timeout
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Screenshot API request failed with status {response.status}.",
                    )

                # Assuming the API returns JSON with a `screenshotUrl` key
                response_json = await response.json()
                screenshot_url = response_json.get("screenshotUrl")
                if not screenshot_url:
                    raise HTTPException(
                        status_code=500, detail="No screenshot URL returned from API."
                    )

                # Download the image as bytes
                async with session.get(
                    screenshot_url, timeout=config.screenshot_timeout
                ) as image_response:
                    if image_response.status != 200:
                        raise HTTPException(
                            status_code=image_response.status,
                            detail=f"Failed to download image from {screenshot_url}.",
                        )
                    image_bytes = await image_response.read()

                    if config.screenshot_compress:
                        with Image.open(BytesIO(image_bytes)) as img:
                            output_bytes = BytesIO()
                            img.convert("RGB").save(
                                output_bytes, format="JPEG", quality=75
                            )
                            output_bytes.seek(0)
                            image_bytes = output_bytes.read()

                    if redis_client:
                        try:
                            await redis_client.setex(
                                cache_key, config.screenshot_cache_exp, image_bytes
                            )
                        except Exception as e:
                            print(f"Redis error: {e}")
                            return None

                    return image_bytes

    except aiohttp.ClientError as e:
        print(f"HTTP client error: {str(e)}")
        return None
    except asyncio.TimeoutError:
        print(f"Timeout while navigating to {url}.")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


async def takeee(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower().strip()
    path = parsed_url.path.rstrip("/")
    domainpath = f":{path}" if path else ""
    query = parsed_url.query

    cache_key = (
        f"screenshot:{host}{domainpath}?{query}"
        if query
        else f"screenshot:{host}{domainpath}"
    )

    redis_client = await RedisHandler().get_client()

    if redis_client:
        if await redis_client.exists(cache_key):
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return cached_data

    screenshot_api_url = f"https://api.screenshotrobot.com?url={url}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                screenshot_api_url, timeout=config.screenshot_timeout
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Screenshot API request failed with status {response.status}.",
                    )

                # Assuming the API returns JSON with a `screenshotUrl` key
                response_json = await response.json()
                screenshot_url = response_json.get("screenshot_url")
                if not screenshot_url:
                    raise HTTPException(
                        status_code=500, detail="No screenshot URL returned from API."
                    )

                # Download the actual image as bytes
                async with session.get(
                    screenshot_url, timeout=config.screenshot_timeout
                ) as image_response:
                    if image_response.status != 200:
                        raise HTTPException(
                            status_code=image_response.status,
                            detail=f"Failed to download image from {screenshot_url}.",
                        )
                    image_bytes = await image_response.read()

                    if config.screenshot_compress:
                        with Image.open(BytesIO(image_bytes)) as img:
                            output_bytes = BytesIO()
                            img.convert("RGB").save(
                                output_bytes, format="JPEG", quality=75
                            )
                            output_bytes.seek(0)
                            image_bytes = output_bytes.read()

                    if redis_client:
                        try:
                            await redis_client.setex(
                                cache_key, config.screenshot_cache_exp, image_bytes
                            )
                        except Exception as e:
                            print(f"Redis error: {e}")
                            return None

                    return image_bytes

    except aiohttp.ClientError as e:
        print(f"HTTP client error: {str(e)}")
        return None
    except asyncio.TimeoutError:
        print(f"Timeout while navigating to {url}.")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


"""

https://screenshot.abstractapi.com/v1/?api_key={apikey}&capture_full_page=false&url={url}

https://api.apiflash.com/v1/urltoimage?access_key=009198343974493c93edfad9bcf7bcde&format=png&width=1280&height=720&fresh=true&quality=75&response_type=json&no_cookie_banners=true&no_ads=true&no_tracking=trueurl={url}

https://api.restpack.io/screenshot/preview/capture?json=true&format=png&mode=viewport&url={url}

"""
