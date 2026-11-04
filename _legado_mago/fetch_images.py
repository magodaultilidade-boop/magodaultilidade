"""
Busca as imagens dos produtos diretamente nas páginas do Mercado Livre
e atualiza o produtos.json com os campos image_url.
"""

import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

PRODUTOS_JSON = Path(__file__).parent / "produtos.json"


async def fetch_image_url(page, url: str, product_name: str) -> str | None:
    print(f"  Abrindo: {product_name}...")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)

        # Pega todas as imagens do mlstatic
        # As 2 primeiras são banner/header do canal — pula e usa a 3ª (produto destacado)
        imgs = await page.eval_on_selector_all(
            "img",
            "els => els.map(e => e.src).filter(s => s.includes('mlstatic.com') && s.startsWith('http'))"
        )

        ml_imgs = [src for src in imgs if src]
        target = ml_imgs[2] if len(ml_imgs) >= 3 else (ml_imgs[0] if ml_imgs else None)

        if target:
            # Converte para versão maior
            target = (target
                .replace("-V.webp", "-F.webp")
                .replace("-V.jpg", "-F.jpg")
                .replace("-T.webp", "-F.webp")
                .replace("-T.jpg", "-F.jpg")
            )
            print(f"  OK Imagem encontrada: {target[:100]}...")
            return target

        print(f"  FALHA Imagem nao encontrada para: {product_name}")
        return None

    except Exception as e:
        print(f"  ERRO ao abrir {product_name}: {e}")
        return None


async def main():
    produtos = json.loads(PRODUTOS_JSON.read_text(encoding="utf-8"))

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for produto in produtos:
            url = produto.get("external_url", "")
            name = produto.get("name", "")
            if not url:
                continue

            # Novo contexto isolado por produto (sem cache compartilhado)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="pt-BR",
            )
            page = await context.new_page()
            image_url = await fetch_image_url(page, url, name)
            await context.close()

            if image_url:
                produto["image_url"] = image_url

        await browser.close()

    PRODUTOS_JSON.write_text(
        json.dumps(produtos, ensure_ascii=False, indent=4), encoding="utf-8"
    )
    print("\nProdutos.json atualizado com sucesso!")
    for p in produtos:
        print(f"  {p['name']}: {p.get('image_url', 'SEM IMAGEM')}")


if __name__ == "__main__":
    asyncio.run(main())
