import asyncio
from playwright.async_api import async_playwright

LINKS = [
    ("Foam Roller", "https://meli.la/2zhXMif"),
    ("Tornozeleira", "https://meli.la/2KcdM1E"),
    ("Corda de Pular", "https://meli.la/23Wtqdd"),
    ("Mini Bands", "https://meli.la/2fHSKT9"),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for name, url in LINKS:
            ctx = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                locale="pt-BR",
            )
            page = await ctx.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
            print(f"\n=== {name} ===")
            print("URL:", page.url)
            imgs = await page.eval_on_selector_all(
                "img", "els => els.map(e => e.src).filter(s => s.includes('mlstatic'))"
            )
            for i in imgs[:5]:
                print(" ", i[:120])
            fname = name.replace(" ", "_") + ".png"
            await page.screenshot(path=fname)
            print(f"Screenshot: {fname}")
            await ctx.close()
        await browser.close()

asyncio.run(main())
