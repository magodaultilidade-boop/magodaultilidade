#!/usr/bin/env python3
"""
Publicador de Produtos WooCommerce - Mago da Utilidade
Publica produtos externos/afiliados via WooCommerce REST API.

Autenticação suportada:
  - Application Password (recomendado, nativo no WP 5.6+)
  - Basic Auth com plugin "JSON Basic Authentication" instalado

Uso:
  python publicar-produtos-wordpress.py
  python publicar-produtos-wordpress.py --senha "xxxx xxxx xxxx xxxx xxxx xxxx"
"""

import argparse
import base64
import json
import sys
from getpass import getpass

try:
    import requests
except ImportError:
    print("Erro: biblioteca 'requests' não encontrada.")
    print("Instale com: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configurações do site
# ---------------------------------------------------------------------------
SITE_URL     = "https://magodaultilidade.com.br"
USUARIO      = "magodaultilidade"
WC_API       = f"{SITE_URL}/wp-json/wc/v3"
WP_API       = f"{SITE_URL}/wp-json/wp/v2"
JSON_PADRAO  = "produtos.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def carregar_produtos(caminho: str) -> list:
    """Carrega a lista de produtos de um arquivo JSON."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: arquivo '{caminho}' contém um JSON inválido.")
        return []


def build_headers(senha: str) -> dict:
    """Monta o header de autenticação Basic (funciona para Application
    Passwords e para o plugin JSON Basic Authentication)."""
    credencial = f"{USUARIO}:{senha}"
    token = base64.b64encode(credencial.encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }


def testar_autenticacao(headers: dict) -> bool:
    """Verifica se as credenciais são válidas consultando o perfil do usuário."""
    print("Verificando autenticação...", end=" ")
    try:
        resp = requests.get(f"{WP_API}/users/me", headers=headers, timeout=15)
        if resp.status_code == 200:
            nome = resp.json().get("name", USUARIO)
            print(f"OK (logado como: {nome})")
            return True
        print(f"FALHOU (HTTP {resp.status_code})")
        try:
            print("  Detalhe:", resp.json().get("message", resp.text[:200]))
        except Exception:
            pass
        return False
    except requests.exceptions.SSLError:
        print("ERRO SSL — verifique o certificado do site.")
        return False
    except requests.exceptions.ConnectionError:
        print("ERRO de conexão — verifique se o site está acessível.")
        return False


def obter_ou_criar_categoria(nome: str, headers: dict) -> int | None:
    """Busca categoria WooCommerce pelo nome; cria se não existir."""
    url = f"{WC_API}/products/categories"

    # Busca existente
    resp = requests.get(url, headers=headers, params={"search": nome, "per_page": 10}, timeout=15)
    if resp.status_code == 200:
        for cat in resp.json():
            if cat["name"].strip().lower() == nome.strip().lower():
                return cat["id"]

    # Cria nova categoria
    resp = requests.post(url, headers=headers, json={"name": nome}, timeout=15)
    if resp.status_code in (200, 201):
        cat_id = resp.json()["id"]
        print(f"    Categoria criada: '{nome}' (id={cat_id})")
        return cat_id

    print(f"    Aviso: não foi possível criar categoria '{nome}' — produto será publicado sem ela.")
    return None


def publicar_produto(produto: dict, headers: dict) -> bool:
    """Publica um produto externo/afiliado no WooCommerce."""
    print(f"\n  Publicando: {produto['name']}")

    # Resolve categorias
    cat_ids = []
    for nome_cat in produto.get("categories_names", []):
        cat_id = obter_ou_criar_categoria(nome_cat, headers)
        if cat_id:
            cat_ids.append({"id": cat_id})

    payload = {
        "name":          produto["name"],
        "type":          "external",          # produto externo/afiliado
        "status":        "publish",
        "regular_price": produto["regular_price"],
        "external_url":  produto["external_url"],
        "button_text":   produto["button_text"],
        "description":   produto["description"],
        "categories":    cat_ids,
    }

    resp = requests.post(
        f"{WC_API}/products",
        headers=headers,
        json=payload,
        timeout=20,
    )

    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"    Publicado com sucesso! ID={data['id']} | URL: {data.get('permalink', '-')}")
        return True

    print(f"    ERRO ao publicar (HTTP {resp.status_code})")
    try:
        print("    Detalhe:", resp.json().get("message", resp.text[:300]))
    except Exception:
        print("    Resposta:", resp.text[:300])
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Publica produtos afiliados no WooCommerce.")
    parser.add_argument(
        "--arquivo", "-a",
        default=JSON_PADRAO,
        help=f"Caminho para o arquivo JSON de produtos (padrão: {JSON_PADRAO})",
    )
    parser.add_argument(
        "--senha", "-s",
        help="Application Password ou senha do WordPress "
             "(formato Application Password: 'xxxx xxxx xxxx xxxx xxxx xxxx')",
    )
    args = parser.parse_args()

    produtos = carregar_produtos(args.arquivo)
    if not produtos:
        print(f"Nenhum produto encontrado em '{args.arquivo}'.")
        sys.exit(1)

    print("=" * 60)
    print("  Publicador de Produtos — Mago da Utilidade")
    print("=" * 60)
    print(f"  Site   : {SITE_URL}")
    print(f"  Usuário: {USUARIO}")
    print(f"  Arquivo: {args.arquivo}")
    print()

    senha = args.senha or getpass("  Senha / Application Password: ")
    if not senha.strip():
        print("Erro: senha não informada.")
        sys.exit(1)

    headers = build_headers(senha.strip())

    if not testar_autenticacao(headers):
        print("\nDica: se estiver usando Application Password, copie exatamente")
        print("como gerado no WordPress (com ou sem espaços).")
        sys.exit(1)

    print(f"\nPublicando {len(produtos)} produto(s)...\n" + "-" * 60)

    sucessos = 0
    for produto in produtos:
        if publicar_produto(produto, headers):
            sucessos += 1

    print("\n" + "=" * 60)
    print(f"  Concluído: {sucessos}/{len(produtos)} produto(s) publicado(s).")
    print("=" * 60)

    if sucessos < len(produtos):
        sys.exit(1)


if __name__ == "__main__":
    main()
