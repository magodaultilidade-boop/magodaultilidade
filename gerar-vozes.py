"""
Gerador de Vozes — ElevenLabs
==============================
Lê os roteiros de 02-Roteiros-Prontos, extrai o texto falado de
cada cena e gera arquivos .mp3 via API do ElevenLabs.

Cenas extraídas:
  Cena 1 → GANCHO        (Fala / Legenda)
  Cena 2 → SOLUÇÃO       (Fala / narração)
  Cena 3 → PROVA SOCIAL  (Fala)
  Cena 4 → CTA           (Fala)

Saída: 04-Videos-Publicados/audio/NomeProduto-Cena1.mp3
"""

import re
import sys
import time
import requests
from pathlib import Path

# ── Configuração ───────────────────────────────────────────────────────────────

API_KEY      = "sk_5490df3285a58ffddd03c5195ca64766e1e55141fcf4ebf1"
API_BASE     = "https://api.elevenlabs.io/v1"

# IDs das vozes pré-definidas do ElevenLabs
VOZES = {
    "Matthew Schmitz - Ancient Sage Dragon Wizard": "HAvvFKatz0uu0Fv55Riy",
}
VOZ_PADRAO = "Matthew Schmitz - Ancient Sage Dragon Wizard"

BASE_DIR    = Path(__file__).parent
ROTEIROS    = BASE_DIR / "02-Roteiros-Prontos"
AUDIO_DIR   = BASE_DIR / "04-Videos-Publicados" / "audio"

# ── Extração de texto dos roteiros ────────────────────────────────────────────

# Cada cena é definida por: título da seção no MD e padrão de fala a capturar
CENAS = [
    {
        "nome":    "Cena1-Gancho",
        "secao":   r"GANCHO",
        "padrao":  r"\*\*Fala\s*/\s*Legenda[^:]*:\*\*\s*>\s*\*\"([^\"]+)\"",
    },
    {
        "nome":    "Cena2-Solucao",
        "secao":   r"SOLU[ÇC][ÃA]O",
        "padrao":  r"\*\*Fala\s*/\s*narra[çc][ãa]o[^:]*:\*\*\s*>\s*\*\"([^\"]+)\"",
    },
    {
        "nome":    "Cena3-PovaSocial",
        "secao":   r"PROVA\s+SOCIAL",
        "padrao":  r"\*\*Fala[^:]*:\*\*\s*>\s*\*\"([^\"]+)\"",
    },
    {
        "nome":    "Cena4-CTA",
        "secao":   r"CTA",
        "padrao":  r"\*\*Fala[^:]*:\*\*\s*>\s*\*\"([^\"]+)\"",
    },
]


def extrair_bloco_secao(texto: str, titulo_regex: str) -> str:
    """Retorna o bloco de texto entre o título da seção e o próximo '---'."""
    padrao = rf"###[^\n]*{titulo_regex}[^\n]*\n(.*?)(?=\n---|\Z)"
    m = re.search(padrao, texto, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else ""


def extrair_fala(bloco: str, padrao: str) -> str:
    """Extrai o texto entre aspas de uma linha de fala/legenda."""
    m = re.search(padrao, bloco, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Fallback: qualquer texto entre aspas após '>' dentro do bloco
    m2 = re.search(r'>\s*\*"([^"]+)"', bloco)
    if m2:
        return m2.group(1).strip()

    return ""


def extrair_cenas_roteiro(caminho: Path) -> list[dict]:
    """Retorna lista de {nome, texto} para as 4 cenas de um roteiro."""
    texto = caminho.read_text(encoding="utf-8")
    resultado = []
    for cena in CENAS:
        bloco = extrair_bloco_secao(texto, cena["secao"])
        fala  = extrair_fala(bloco, cena["padrao"])
        resultado.append({"nome": cena["nome"], "texto": fala, "bloco": bloco})
    return resultado


def nome_produto(caminho: Path) -> str:
    """
    roteiro-faixa-elastica.md → FaixaElastica
    roteiro-foam-roller.md    → FoamRoller
    """
    stem = caminho.stem.replace("roteiro-", "")          # faixa-elastica
    partes = stem.split("-")
    return "".join(p.capitalize() for p in partes)        # FaixaElastica


# ── ElevenLabs API ────────────────────────────────────────────────────────────

def listar_vozes() -> dict[str, str]:
    """Retorna {nome: voice_id} de todas as vozes disponíveis na conta."""
    r = requests.get(
        f"{API_BASE}/voices",
        headers={"xi-api-key": API_KEY},
        timeout=15,
    )
    r.raise_for_status()
    return {v["name"]: v["voice_id"] for v in r.json().get("voices", [])}


def resolver_voice_id(nome_voz: str) -> str:
    """
    Tenta usar o ID hardcoded; se falhar, busca dinamicamente na API.
    """
    if nome_voz in VOZES:
        return VOZES[nome_voz]

    print(f"  Voz '{nome_voz}' não encontrada localmente — buscando na API...")
    vozes_api = listar_vozes()
    if nome_voz in vozes_api:
        return vozes_api[nome_voz]

    disponiveis = ", ".join(vozes_api.keys())
    raise ValueError(
        f"Voz '{nome_voz}' não encontrada. Disponíveis: {disponiveis}"
    )


def gerar_audio(texto: str, voice_id: str) -> bytes:
    """Chama a API TTS e retorna os bytes do .mp3."""
    url = f"{API_BASE}/text-to-speech/{voice_id}"
    payload = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability":        0.5,
            "similarity_boost": 0.75,
            "style":            0.0,
            "use_speaker_boost": True,
        },
    }
    headers = {
        "xi-api-key":   API_KEY,
        "Content-Type": "application/json",
        "Accept":       "audio/mpeg",
    }
    r = requests.post(url, json=payload, headers=headers, timeout=60)

    if r.status_code == 429:
        print("  Rate limit atingido — aguardando 10s...")
        time.sleep(10)
        r = requests.post(url, json=payload, headers=headers, timeout=60)

    r.raise_for_status()
    return r.content


# ── Interface de terminal ─────────────────────────────────────────────────────

LINHA = "─" * 60


def cabecalho():
    print()
    print(LINHA)
    print("  Gerador de Vozes — ElevenLabs")
    print(LINHA)


def perguntar_voz() -> str:
    nomes = list(VOZES.keys())
    print()
    print("  Vozes disponíveis:")
    for i, n in enumerate(nomes, 1):
        print(f"    {i}. {n}")
    print()
    escolha = input(
        f"  Escolha a voz [{'/'.join(nomes)}] (Enter = {VOZ_PADRAO}): "
    ).strip()

    if not escolha:
        return VOZ_PADRAO
    if escolha in VOZES:
        return escolha
    # Aceita número
    if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
        return nomes[int(escolha) - 1]

    print(f"  Opção inválida — usando {VOZ_PADRAO}.")
    return VOZ_PADRAO


def perguntar_roteiros(roteiros: list[Path]) -> list[Path]:
    print()
    print("  Roteiros encontrados:")
    for i, r in enumerate(roteiros, 1):
        print(f"    {i}. {r.name}")
    print()
    resp = input(
        "  Processar (T)odos ou número(s) separados por vírgula? [T]: "
    ).strip().upper()

    if not resp or resp == "T":
        return roteiros

    selecionados = []
    for parte in resp.split(","):
        parte = parte.strip()
        if parte.isdigit() and 1 <= int(parte) <= len(roteiros):
            selecionados.append(roteiros[int(parte) - 1])
        else:
            print(f"  Ignorando entrada inválida: '{parte}'")
    return selecionados if selecionados else roteiros


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    cabecalho()

    # Listar roteiros
    roteiros = sorted(ROTEIROS.glob("roteiro-*.md"))
    if not roteiros:
        print(f"\n  Nenhum roteiro encontrado em {ROTEIROS}")
        sys.exit(1)

    # Escolher roteiros e voz
    selecionados = perguntar_roteiros(roteiros)
    nome_voz     = perguntar_voz()
    voice_id     = resolver_voice_id(nome_voz)

    # Criar pasta de saída
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print(LINHA)
    total_ok  = 0
    total_err = 0

    for roteiro in selecionados:
        produto = nome_produto(roteiro)
        print(f"\n  Produto: {produto}")

        cenas = extrair_cenas_roteiro(roteiro)

        for cena in cenas:
            destino = AUDIO_DIR / f"{produto}-{cena['nome']}.mp3"

            if not cena["texto"]:
                print(f"    {cena['nome']}: texto não encontrado — pulando.")
                total_err += 1
                continue

            # Pula se já existe
            if destino.exists():
                resp = input(
                    f"    {destino.name} já existe. Sobrescrever? [s/N]: "
                ).strip().lower()
                if resp != "s":
                    print(f"    Pulando {destino.name}.")
                    continue

            print(f"    {cena['nome']}: gerando áudio... ", end="", flush=True)
            try:
                audio = gerar_audio(cena["texto"], voice_id)
                destino.write_bytes(audio)
                kb = len(audio) / 1024
                print(f"OK ({kb:.1f} KB) → {destino.name}")
                total_ok += 1
            except requests.HTTPError as e:
                print(f"ERRO HTTP {e.response.status_code}: {e.response.text[:120]}")
                total_err += 1
            except Exception as e:
                print(f"ERRO: {e}")
                total_err += 1

    print()
    print(LINHA)
    print(f"  Concluído — {total_ok} gerado(s), {total_err} erro(s)/pulado(s).")
    print(f"  Arquivos em: {AUDIO_DIR}")
    print(LINHA)
    print()


if __name__ == "__main__":
    main()
