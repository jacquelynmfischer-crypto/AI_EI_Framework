import asyncio, glob
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = await b.new_page(viewport={'width':600,'height':720}, device_scale_factor=2)
        for f in sorted(glob.glob('*.svg')):
            await pg.goto('file:///'+__import__('os').path.abspath(f)); await pg.screenshot(path=f.replace('.svg','.png'))
        await b.close()
asyncio.run(main())
