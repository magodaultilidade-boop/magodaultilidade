"""
Alterar Vozes — gerar-vozes.py
================================
Lista as vozes disponíveis na conta ElevenLabs e permite escolher
quais substituir no dicionário VOZES de gerar-vozes.py.
"""

import re
import sys
import requests
from pathlib import Path

API_KEY  = "sk_5490df3285a58ffddd03c5195ca64766e1e55141fcf4ebf1"
API_BASE = "https://api.elevenlabs.io/v1"
SCRIPT   = Path(__file__).parent / "gerar-vozes.py"

LINHA = "─" * 60


def listar_vozes() -> list[dict]:
    r = requests.get(
        f"{API_BASE}/voices",
        headers={"xi-api-key": API_KEY},
        timeout=15,
    )
    r.raise_for_status()
    vozes = r.json().get("voices", [])
    return sorted(vozes, key=lambda v: v["name"])


def exibir_vozes(vozes: list[dict]):
    print()
    print(f"  {'#':<4} {'Nome':<40} {'ID'}")
    print(f"  {'─'*4} {'─'*40} {'─'*22}")
    for i, v in enumerate(vozes, 1):
        categoria = v.get("category", "")
        labels    = v.get("labels", {})
        desc      = labels.get("description", "") or labels.get("use_case", "") or categoria
        print(f"  {i:<4} {v['name']:<40} {v['voice_id']}  {desc}")
    print()


def escolher_voz(vozes: list[dict], slot: str, atual: tuple[str, str]) -> tuple[str, str]:
    print(f"  [{slot}] Atual: {atual[0]} ({atual[1]})")
    resp = input(f"  Número da nova voz (Enter = manter): ").strip()
    if not resp:
        return atual
    if resp.isdigit() and 1 <= int(resp) <= len(vozes):
        v = vozes[int(resp) - 1]
        return v["name"], v["voice_id"]
    print("  Entrada inválida — mantendo voz atual.")
    return atual


def ler_vozes_atuais(texto: str) -> list[tuple[str, str]]:
    """Extrai as vozes atuais do dicionário VOZES no script."""
    padrao = r'"([^"]+)":\s*"([A-Za-z0-9]+)"'
    bloco  = re.search(r"VOZES\s*=\s*\{(.+?)\}", texto, re.DOTALL)
    if not bloco:
        return []
    return re.findall(padrao, bloco.group(1))


def atualizar_vozes(texto: str, novas: list[tuple[str, str]], padrao_voz: str) -> str:
    # Monta novo bloco VOZES
    linhas = ",\n".join(
        f'    "{nome}": "{vid}"'
        for nome, vid in novas
    )
    novo_bloco = f"VOZES = {{\n{linhas},\n}}"
    texto = re.sub(r"VOZES\s*=\s*\{.+?\}", novo_bloco, texto, flags=re.DOTALL)

    # Atualiza VOZ_PADRAO
    texto = re.sub(
        r'VOZ_PADRAO\s*=\s*"[^"]+"',
        f'VOZ_PADRAO = "{padrao_voz}"',
        texto,
    )
    return texto


def main():
    print()
    print(LINHA)
    print("  Alterar Vozes — ElevenLabs")
    print(LINHA)

    print("\n  Buscando vozes disponíveis...")
    try:
        vozes = listar_vozes()
    except requests.HTTPError as e:
        print(f"  Erro ao buscar vozes: {e}")
        sys.exit(1)

    exibir_vozes(vozes)

    # Ler estado atual do script
    texto_original = SCRIPT.read_text(encoding="utf-8")
    atuais = ler_vozes_atuais(texto_original)

    if not atuais:
        print("  Não foi possível ler as vozes atuais de gerar-vozes.py.")
        sys.exit(1)

    print(LINHA)
    print("  Escolha a nova voz para cada slot (ou Enter para manter):")
    print()

    novas = []
    for nome, vid in atuais:
        nova = escolher_voz(vozes, nome, (nome, vid))
        novas.append(nova)

    # Voz padrão
    print()
    print("  Slots configurados:")
    for i, (nome, vid) in enumerate(novas, 1):
        print(f"    {i}. {nome} ({vid})")
    print()
    resp_padrao = input(
        f"  Qual será a voz padrão? (1-{len(novas)}, Enter = manter '{atuais[0][0]}'): "
    ).strip()

    if resp_padrao.isdigit() and 1 <= int(resp_padrao) <= len(novas):
        voz_padrao = novas[int(resp_padrao) - 1][0]
    else:
        voz_padrao = novas[0][0]

    # Confirmar
    print()
    print(LINHA)
    print("  Resumo das alterações:")
    for nome, vid in novas:
        marcador = " ◄ PADRÃO" if nome == voz_padrao else ""
        print(f"    {nome} ({vid}){marcador}")
    print()
    confirmar = input("  Salvar em gerar-vozes.py? [s/N]: ").strip().lower()

    if confirmar != "s":
        print("  Cancelado.")
        return

    novo_texto = atualizar_vozes(texto_original, novas, voz_padrao)
    SCRIPT.write_text(novo_texto, encoding="utf-8")

    print()
    print(LINHA)
    print("  Vozes atualizadas com sucesso em gerar-vozes.py!")
    print(LINHA)
    print()


if __name__ == "__main__":
    main()
