import asyncio
import base64
import sys

from fastapi import HTTPException
from playwright.async_api import async_playwright


async def take(url: str, save_to_file: bool = False, file_name: str = "screenshot.png"):
    try:
        async with async_playwright() as p:
            # browser = await p.chromium.launch(headless=True)
            browser = await p.chromium.connect("ws://localhost:3000")
            page = await browser.new_page()
            await page.goto(url, timeout=30000)

            await page.set_viewport_size({"width": 1920, "height": 1080})
            await asyncio.sleep(1.5)

            # Take a screenshot
            screenshot_data = await page.screenshot()
            result = base64.b64encode(screenshot_data).decode()

            # print(result)
            return result

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504, detail=f"Timeout while navigating to {url}."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    if sys.platform == "win32":
        # Set the WindowsProactorEventLoopPolicy for compatibility
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # Run the function and print the result
    url = "https://google.com"
    result = asyncio.run(take(url, save_to_file=True))
    # print(result)
