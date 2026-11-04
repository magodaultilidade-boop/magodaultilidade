"""
Gerador de Links Afiliados — Mercado Livre
==========================================
Lê os produtos de 01-Produtos-em-Analise/produtos.md,
abre o navegador para cada produto e salva os links gerados
em 05-Templates-Fixos/links-afiliados.md e em produtos.md.
"""

import re
import webbrowser
from datetime import date
from pathlib import Path

# ── Caminhos ──────────────────────────────────────────────────────────────────

BASE_DIR       = Path(__file__).parent
PRODUTOS_MD    = BASE_DIR / "01-Produtos-em-Analise" / "produtos.md"
AFILIADOS_MD   = BASE_DIR / "05-Templates-Fixos" / "links-afiliados.md"
PAINEL_ML      = "https://www.mercadolivre.com.br/afiliados"

# ── Parsing ───────────────────────────────────────────────────────────────────

def extrair_produtos(caminho: Path) -> list[dict]:
    """
    Extrai de produtos.md uma lista de dicts com:
      numero, nome, link_referencia, link_afiliado
    """
    texto = caminho.read_text(encoding="utf-8")

    # Captura cada bloco de produto: ## N. Nome ... até o próximo ## ou fim
    blocos = re.split(r"(?=^## \d+\.)", texto, flags=re.MULTILINE)

    produtos = []
    for bloco in blocos:
        m_num  = re.match(r"^## (\d+)\. (.+)", bloco)
        if not m_num:
            continue

        numero = int(m_num.group(1))
        nome   = m_num.group(2).strip()

        # Link de referência
        m_ref = re.search(
            r"\*\*Link do produto \(referência\)\*\*\s*\|\s*(https?://\S+)",
            bloco
        )
        link_ref = m_ref.group(1).rstrip("|").strip() if m_ref else ""

        # Link afiliado atual (ignora placeholders)
        m_afi = re.search(
            r"\*\*Link Afiliado\*\*\s*\|.*?(https?://\S+)",
            bloco
        )
        link_afi = m_afi.group(1).rstrip("|").strip() if m_afi else ""

        produtos.append({
            "numero":        numero,
            "nome":          nome,
            "link_ref":      link_ref,
            "link_afiliado": link_afi,
        })

    return sorted(produtos, key=lambda p: p["numero"])


# ── Atualização de arquivos ───────────────────────────────────────────────────

def atualizar_produtos_md(caminho: Path, produto: dict, novo_link: str) -> None:
    """Substitui o Link Afiliado do produto em produtos.md."""
    texto = caminho.read_text(encoding="utf-8")

    # Localiza o bloco do produto pelo número e nome
    padrao_bloco = (
        r"(## " + str(produto["numero"]) + r"\. " +
        re.escape(produto["nome"]) +
        r".*?\*\*Link Afiliado\*\*\s*\|)\s*\S+(\s*\|)"
    )
    substituicao = r"\g<1> " + novo_link + r"\g<2>"
    novo_texto = re.sub(padrao_bloco, substituicao, texto, flags=re.DOTALL)

    # Atualiza também a linha do Resumo Comparativo
    padrao_resumo = (
        r"(\|\s*" + str(produto["numero"]) +
        r"\s*\|[^|]+\|[^|]+\|[^|]+\|)\s*[^\|\n]+(\s*\|)"
    )
    novo_texto = re.sub(padrao_resumo, r"\g<1> " + novo_link + r"\g<2>", novo_texto)

    caminho.write_text(novo_texto, encoding="utf-8")


def atualizar_afiliados_md(
    caminho: Path,
    produto: dict,
    novo_link: str,
    data_cadastro: str,
    comissao: str,
) -> None:
    """Substitui a linha do produto em links-afiliados.md."""
    texto = caminho.read_text(encoding="utf-8")

    # Regex para encontrar a linha da tabela pelo número do produto
    padrao = (
        r"(\|\s*" + str(produto["numero"]) +
        r"\s*\|[^|]+\|[^|]+\|)\s*[^\|\n]*(\|)\s*[^\|\n]*(\|)\s*[^\|\n]*(\|)"
    )
    substituicao = (
        r"\g<1> " + novo_link +
        r" \g<2> " + data_cadastro +
        r" \g<3> " + comissao +
        r" \g<4>"
    )
    novo_texto = re.sub(padrao, substituicao, texto)
    caminho.write_text(novo_texto, encoding="utf-8")


# ── Interface de terminal ─────────────────────────────────────────────────────

LINHA = "─" * 60

def cabecalho():
    print()
    print(LINHA)
    print("  Gerador de Links Afiliados — Mercado Livre")
    print(LINHA)

def separador():
    print()
    print(LINHA)

def perguntar_link(produto: dict) -> str | None:
    """Pede o link afiliado ao usuário. Retorna None se quiser pular."""
    while True:
        link = input("  Cole o link afiliado (ou ENTER para pular): ").strip()
        if not link:
            return None
        if link.startswith("http"):
            return link
        print("  Link inválido — deve começar com http. Tente novamente.")

def perguntar_comissao() -> str:
    resp = input("  Comissão % (ENTER para deixar em branco): ").strip()
    return resp if resp else ""


# ── Fluxo principal ───────────────────────────────────────────────────────────

def main():
    cabecalho()

    if not PRODUTOS_MD.exists():
        print(f"\n  ERRO: arquivo não encontrado:\n  {PRODUTOS_MD}")
        return

    produtos = extrair_produtos(PRODUTOS_MD)
    if not produtos:
        print("\n  Nenhum produto encontrado em produtos.md.")
        return

    print(f"\n  {len(produtos)} produto(s) encontrado(s):\n")
    for p in produtos:
        status = p["link_afiliado"] if p["link_afiliado"] else "sem link"
        print(f"  {p['numero']}. {p['nome']}")
        print(f"     Link afiliado atual: {status}")

    print()
    atualizar_todos = input(
        "  Deseja (A) atualizar todos ou (S) selecionar produto específico? [A/S]: "
    ).strip().upper()

    if atualizar_todos == "S":
        try:
            escolha = int(input("  Digite o número do produto: ").strip())
            produtos = [p for p in produtos if p["numero"] == escolha]
            if not produtos:
                print("  Produto não encontrado.")
                return
        except ValueError:
            print("  Entrada inválida.")
            return

    # Abre o painel ML uma única vez
    separador()
    print("\n  Abrindo o Painel ML Afiliados no navegador...")
    webbrowser.open(PAINEL_ML)
    print("  Faça login se necessário e deixe o painel aberto.")
    input("\n  Pressione ENTER quando estiver pronto para começar...")

    hoje = date.today().strftime("%Y-%m-%d")
    atualizados = 0

    for produto in produtos:
        separador()
        print(f"\n  Produto {produto['numero']}/{len(produtos)}: {produto['nome']}")

        if produto["link_afiliado"]:
            print(f"  Link atual: {produto['link_afiliado']}")
            resp = input("  Já tem link. Deseja substituir? [s/N]: ").strip().lower()
            if resp != "s":
                print("  Pulando...")
                continue

        if produto["link_ref"]:
            print(f"\n  Abrindo página do produto no navegador...")
            webbrowser.open(produto["link_ref"])
            print(f"  URL: {produto['link_ref']}")
        else:
            print("  (sem URL de referência — use a busca no painel)")

        print()
        print("  No painel ML Afiliados:")
        print("  1. Cole a URL do produto no campo de busca")
        print("  2. Clique em 'Gerar link'")
        print("  3. Copie o link encurtado (meli.la/...)")

        novo_link = perguntar_link(produto)
        if not novo_link:
            print("  Pulado.")
            continue

        comissao = perguntar_comissao()
        data_cadastro = hoje

        # Salva nos dois arquivos
        atualizar_produtos_md(PRODUTOS_MD, produto, novo_link)
        atualizar_afiliados_md(AFILIADOS_MD, produto, novo_link, data_cadastro, comissao)

        atualizados += 1
        print(f"\n  Salvo: {novo_link}")

    separador()
    print(f"\n  Concluído. {atualizados} link(s) atualizado(s).")
    print(f"  Arquivos atualizados:")
    print(f"    - {PRODUTOS_MD.relative_to(BASE_DIR)}")
    print(f"    - {AFILIADOS_MD.relative_to(BASE_DIR)}")
    print()


if __name__ == "__main__":
    main()
