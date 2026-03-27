import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # abre janela visivel
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="pt-BR",
        )
        page = await context.new_page()
        await page.goto("https://meli.la/2zhXMif", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(5000)

        # Pega URL final apos redirecionamentos
        print("URL final:", page.url)

        # Lista todos os imgs da pagina
        imgs = await page.eval_on_selector_all("img", "els => els.map(e => e.src)")
        print("\nImagens encontradas:")
        for src in imgs:
            if src and src.startswith("http"):
                print(" ", src[:120])

        await page.screenshot(path="debug_screenshot.png")
        print("\nScreenshot salvo em debug_screenshot.png")
        await browser.close()

asyncio.run(main())
