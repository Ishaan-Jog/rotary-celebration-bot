import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def generate_png(html_file):

    html_path = Path(html_file).resolve()

    async with async_playwright() as p:

        browser = await p.chromium.launch()

        page = await browser.new_page(
            viewport={
                "width":1080,
                "height":1080
            }
        )

        await page.goto(
            f"file://{html_path}"
        )

        await page.screenshot(
            path="generated/poster.png"
        )

        await browser.close()

    return "generated/poster.png"