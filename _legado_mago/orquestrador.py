#!/usr/bin/env python3
"""
Orquestrador Multi-Agente — Mago das Utilidades
================================================
Pipeline automatizado de criação de conteúdo de afiliado:

  Agente 1 — Analista    : Analisa o produto e cria um briefing
  Agente 2 — Roteirista  : Gera o roteiro no formato padrão do canal
  Agente 3 — Prompts     : Gera os 6 prompts para o Veo3
  Agente 4 — Áudio       : Extrai as falas e gera MP3s via ElevenLabs
  Agente 5 — Títulos     : Gera 5 opções de título para YouTube Shorts

Instalação (uma vez):
    pip install google-genai requests

Uso:
    set GEMINI_API_KEY=sua_chave_aqui
    python orquestrador.py
"""

import os
import re
import sys
import time
import requests
from pathlib import Path
from datetime import date

# ── Verifica dependência antes de importar ───────────────────────────────────
try:
    from google import genai
    from google.genai import types as genai_types
except ImportError:
    print("\n  ERRO: biblioteca 'google-genai' não instalada.")
    print("  Execute: pip install google-genai\n")
    sys.exit(1)

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═════════════════════════════════════════════════════════════════════════════

BASE_DIR     = Path(__file__).parent
ROTEIROS_DIR = BASE_DIR / "02-Roteiros-Prontos"
PROMPTS_DIR  = BASE_DIR / "03-Prompts-Veo3"
AUDIO_DIR    = BASE_DIR / "04-Videos-Publicados" / "audio"

# Google Gemini — GRATUITO: 1500 req/dia
# Obtenha sua chave grátis em: https://aistudio.google.com/apikey
GEMINI_API_KEY_LOCAL = "AIzaSyDh_PV3JXo6Ms_5alnpA30bxaleq0DjMVs"

# ElevenLabs (mesmo da configuração existente no projeto)
ELEVENLABS_KEY  = "sk_5490df3285a58ffddd03c5195ca64766e1e55141fcf4ebf1"
ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"
VOICE_ID        = "HAvvFKatz0uu0Fv55Riy"  # Matthew Schmitz - Ancient Sage Dragon Wizard

MODELO_GEMINI = "gemini-1.5-flash"  # Rápido, gratuito, clássico
TODAY         = date.today().isoformat()
_gemini_client = None  # Inicializado em verificar_api_key()

# ═════════════════════════════════════════════════════════════════════════════
# DISPLAY — Terminal com estilo
# ═════════════════════════════════════════════════════════════════════════════

LINHA = "─" * 62


def cabecalho():
    print()
    print("╔" + "═" * 60 + "╗")
    print("║   Mago das Utilidades — Orquestrador Multi-Agente         ║")
    print("║   Pipeline: Produto → Roteiro → Prompts → Áudio → Título  ║")
    print("╚" + "═" * 60 + "╝")
    print()


def agente_header(numero: int, nome: str, descricao: str):
    print()
    print()
    print("┌" + "─" * 60 + "┐")
    print(f"│  AGENTE {numero} — {nome:<50}│")
    print(f"│  {descricao:<58}│")
    print("└" + "─" * 60 + "┘")
    print()


def ok(msg: str):
    print(f"\n  ✓ {msg}")


def info(msg: str):
    print(f"  · {msg}")


def erro(msg: str):
    print(f"\n  ✗ ERRO: {msg}")


def secao(titulo: str):
    print()
    print(f"  {LINHA}")
    print(f"  {titulo}")
    print(f"  {LINHA}")


# ═════════════════════════════════════════════════════════════════════════════
# UTILITÁRIOS
# ═════════════════════════════════════════════════════════════════════════════

def slugify(texto: str) -> str:
    """'Foam Roller Odin Fit' → 'foam-roller-odin-fit'"""
    texto = texto.lower()
    substituicoes = {
        "a": "áàãâä", "e": "éèêë", "i": "íìîï",
        "o": "óòõôö", "u": "úùûü", "c": "ç", "n": "ñ",
    }
    for base, variantes in substituicoes.items():
        for v in variantes:
            texto = texto.replace(v, base)
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")


def salvar_arquivo(caminho: Path, conteudo: str):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")
    ok(f"Arquivo salvo → {caminho.relative_to(BASE_DIR)}")


# ═════════════════════════════════════════════════════════════════════════════
# GEMINI API — Base de streaming
# ═════════════════════════════════════════════════════════════════════════════

def chamar_gemini(system: str, usuario: str, max_tokens: int = 4096) -> str:
    """
    Chama o Google Gemini com streaming via novo SDK google-genai.
    Mostra o conteúdo sendo gerado em tempo real no terminal.
    Retorna o texto completo ao final.
    """
    config = genai_types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=max_tokens,
        temperature=0.7,
    )

    assert _gemini_client is not None, "Cliente Gemini não inicializado — chame verificar_api_key() primeiro."

    partes = []
    print()  # linha inicial

    for chunk in _gemini_client.models.generate_content_stream(
        model=MODELO_GEMINI,
        contents=usuario,
        config=config,
    ):
        texto = chunk.text or ''
        if texto:
            print(texto, end='', flush=True)
            partes.append(texto)

    print()  # nova linha após streaming
    return ''.join(partes)


# Alias para compatibilidade com o resto do código
chamar_claude = chamar_gemini


# ═════════════════════════════════════════════════════════════════════════════
# AGENTE 1 — ANALISTA
# Recebe: nome/URL/descrição do produto
# Retorna: briefing estruturado
# ═════════════════════════════════════════════════════════════════════════════

SYSTEM_ANALISTA = """Você é um analista de produtos de afiliados do Mercado Livre.
Analise o produto informado e crie um briefing completo para orientar a criação de vídeos curtos de afiliado.

Estruture o briefing com:

## BRIEFING DO PRODUTO

**Nome completo:** [nome comercial do produto]
**Preço estimado:** [faixa de preço no ML se disponível]
**Público-alvo:** [quem compra, perfil demográfico]
**Categoria:** [fitness / cozinha / casa / eletrônico / etc]

## PONTOS DE VENDA
- [benefício 1 — como o cliente usa e o que resolve]
- [benefício 2]
- [benefício 3]

## TIPO DE ARGUMENTO RECOMENDADO
[Escolha: Preço vs academia / Dor e alívio / Educação / Números concretos / Autoridade + FOMO]
**Por quê:** [justificativa em 1 frase]

## TOM DO VÍDEO
[Energético / Empático / Educativo / Urgente / Inspiracional]

## GANCHOS SUGERIDOS
1. [gancho principal — máximo 12 palavras, impactante, direto ao ponto]
2. [gancho alternativo A]
3. [gancho alternativo B]

## PROVA SOCIAL
[Dado de vendas, avaliação estimada ou argumento de credibilidade]

Seja direto e objetivo. Este briefing guia os próximos 4 agentes do pipeline."""


def agente_analista(produto: str) -> str:
    agente_header(1, "ANALISTA", "Analisando o produto e criando briefing...")

    print("  O Agente Analista vai entender o produto, identificar o")
    print("  público-alvo e sugerir o melhor ângulo para o vídeo.\n")

    resultado = chamar_claude(
        system=SYSTEM_ANALISTA,
        usuario=f"Analise este produto para afiliados do Mercado Livre:\n\n{produto}",
        max_tokens=1500,
    )

    ok("Briefing concluído!")
    return resultado


# ═════════════════════════════════════════════════════════════════════════════
# AGENTE 2 — ROTEIRISTA
# Recebe: briefing do produto
# Retorna: roteiro completo no formato padrão + caminho do arquivo salvo
# ═════════════════════════════════════════════════════════════════════════════

SYSTEM_ROTEIRISTA = """Você é o roteirista do canal "Mago das Utilidades" — canal de afiliados do Mercado Livre.
Você cria roteiros para Reels, TikTok e YouTube Shorts de 30–45 segundos.

IMPORTANTE: Siga o formato markdown EXATAMENTE como mostrado abaixo.
As falas precisam estar entre *" "* — o script de geração de áudio depende desse padrão.

FORMATO OBRIGATÓRIO:

# Roteiro — [NOME DO PRODUTO]
**Formato:** Reels / TikTok / Shorts
**Duração:** 30–45 segundos
**Produto:** [NOME COMPLETO DO PRODUTO]
**Plataforma de venda:** Mercado Livre Afiliados

---

## ESTRUTURA DO VÍDEO

### 🎬 [0–3s] GANCHO
> *[Descreva a ação visual: o que aparece na tela]*

**Fala / Legenda:**
> *"[Frase de impacto — máximo 12 palavras]"*

**Visual:** [Descrição do ângulo de câmera e composição]

---

### 📌 [3–8s] PROBLEMA
> *[Descreva a cena visual]*

**Legenda na tela:**
> *"[Descrição da dor do público — máximo 2 linhas]"*

**Visual:** [Descrição]

---

### ✅ [8–20s] SOLUÇÃO — DEMONSTRAÇÃO
> *Mostre 3 usos ou exercícios em sequência rápida*

| Uso / Exercício | Posição / Contexto | Legenda |
|---|---|---|
| [uso 1] | [contexto] | *"[benefício]"* |
| [uso 2] | [contexto] | *"[benefício]"* |
| [uso 3] | [contexto] | *"[benefício]"* |

**Fala / narração:**
> *"[2–3 frases explicando o produto de forma simples e direta]"*

---

### 💥 [20–28s] PROVA SOCIAL / CREDIBILIDADE
> *[Descreva o que aparece: avaliações, dados de vendas]*

**Legenda na tela:**
> *"⭐⭐⭐⭐⭐ '[dado de avaliação ou vendas]'"*

**Fala:**
> *"[Frase de transição para a prova social]"*

---

### 🛒 [28–35s] CTA — CHAMADA PARA AÇÃO
> *[Tom: direto, urgente, empático]*

**Fala:**
> *"Link na bio — [reforce o benefício ou preço]. [Gatilho de urgência leve]."*

**Legenda na tela (grande):**
> *"🔗 LINK NA BIO — [Complemento]"*

**Visual:** [Produto em destaque, seta animada]

---

## ROTEIRO COMPLETO (versão falada)

> *"[Repita a frase do gancho].*
> *[Problema — 1 frase que nomeia a dor].*
> *[Solução — 2 frases explicando o produto e benefícios].*
> *[Prova social — 1 frase citando avaliações ou resultado].*
> *[CTA — 1 frase com link na bio e urgência]."*

---

## DICAS DE PRODUÇÃO

| Item | Recomendação |
|---|---|
| **Música** | [estilo e BPM] |
| **Iluminação** | [natural / ring light] |
| **Roupas** | [descrição conforme contexto] |
| **Cenário** | [local que faz sentido para o produto] |
| **Edição** | [ritmo de corte: rápido 1-2s / médio 2-3s] |
| **Legenda** | Sempre ativa — 85% assiste sem som |

---

## VARIAÇÕES DE GANCHO (teste A/B)

1. *"[variação 1 — foco no preço ou economia]"*
2. *"[variação 2 — foco no resultado ou transformação]"*
3. *"[variação 3 — foco em autoridade ou comparação]"*"""


def agente_roteirista(entrada: str, slug: str) -> tuple[str, Path]:
    agente_header(2, "ROTEIRISTA", "Gerando roteiro completo no formato padrão do canal...")

    print("  O Agente Roteirista usa o briefing para criar o roteiro")
    print("  com todas as 5 cenas: Gancho → Problema → Solução →")
    print("  Prova Social → CTA. Salva em 02-Roteiros-Prontos/\n")

    roteiro = chamar_claude(
        system=SYSTEM_ROTEIRISTA,
        usuario=(
            f"Crie o roteiro completo para este produto.\n\n"
            f"BRIEFING:\n{entrada}\n\n"
            f"Data de criação: {TODAY}"
        ),
        max_tokens=3000,
    )

    # Adiciona rodapé de metadados
    roteiro += f"\n\n---\n\n*Criado em: {TODAY}*\n"

    caminho = ROTEIROS_DIR / f"roteiro-{slug}.md"
    salvar_arquivo(caminho, roteiro)  # já exibe ok() internamente
    return roteiro, caminho


# ═════════════════════════════════════════════════════════════════════════════
# AGENTE 3 — PROMPTS VEO3
# Recebe: roteiro completo
# Retorna: arquivo com 6 prompts em inglês para o Veo3
# ═════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPTS = """Você é especialista em geração de vídeos com IA, especificamente no Veo3 do Google.
Você cria prompts cinematográficos em inglês para vídeos de fitness e produtos de afiliado.

REGRAS OBRIGATÓRIAS para cada prompt:
- SEMPRE em inglês
- Inclua: ângulo de câmera, sujeito com descrição física, produto em destaque, iluminação, cenário
- SEMPRE inclua ao final: "Vertical video format, 9:16 aspect ratio."
- NUNCA inclua texto, legendas ou palavras na cena — são adicionados em edição
- Use sujeitos como: "A fit Brazilian woman in her late 20s" ou "A fit Brazilian man"
- Termine sempre com: "Cinematic, high quality."

CENAS A GERAR:

## CENA 1 — Gancho (0–3s)
Objetivo: Prender atenção, produto em primeiro plano. Close-up ou low angle.

## CENA 2 — Produto solo (B-roll)
Objetivo: Mostrar produto com clareza. Top-down flat lay ou close no detalhe.

## CENA 3 — Demonstração 1 (8–12s)
Objetivo: Primeiro uso/exercício. Medium shot ou floor level.

## CENA 4 — Demonstração 2 (12–16s)
Objetivo: Segundo uso, mostra versatilidade.

## CENA 5 — Demonstração 3 (16–20s)
Objetivo: Terceiro uso, fecha o arco de demonstração.

## CENA 6 — CTA Final (28–35s)
Objetivo: Pessoa segura o produto, olha para a câmera com confiança. Medium shot, eye level.

FORMATO DO ARQUIVO (siga exatamente):

# Prompts Veo3 — [NOME DO PRODUTO]
**Produto:** [NOME]
**Referência de roteiro:** `02-Roteiros-Prontos/roteiro-[SLUG].md`

---

## CENA 1 — Gancho (0–3s)
> Objetivo: Prender atenção nos primeiros 2 segundos

```
[prompt em inglês]
```

---

## CENA 2 — Produto solo em destaque
> Objetivo: Mostrar produto — cor, forma, detalhes

```
[prompt em inglês]
```

[continue para cenas 3, 4, 5, 6]

---

## Notas de edição

| Cena | Texto a adicionar em edição |
|---|---|
| 1 | *"[frase do gancho do roteiro]"* |
| 2 | *(sem texto — produto fala por si)* |
| 3 | *"[uso 1] — [benefício]"* |
| 4 | *"[uso 2] — [benefício]"* |
| 5 | *"[uso 3] — [benefício]"* |
| 6 | *"🔗 LINK NA BIO — [complemento]"* |"""


def agente_prompts(roteiro: str, slug: str) -> Path:
    agente_header(3, "PROMPTS VEO3", "Gerando 6 prompts cinematográficos para o Veo3...")

    print("  O Agente Prompts lê o roteiro e cria um prompt em inglês")
    print("  para cada cena: Gancho, Produto solo, 3 Demos e CTA.")
    print("  Salva em 03-Prompts-Veo3/\n")

    prompts = chamar_claude(
        system=SYSTEM_PROMPTS,
        usuario=(
            f"Crie os 6 prompts Veo3 para este roteiro.\n\n"
            f"ROTEIRO:\n{roteiro}\n\n"
            f"Slug do arquivo: {slug}"
        ),
        max_tokens=3500,
    )

    prompts += f"\n\n---\n\n*Criado em: {TODAY}*\n"

    caminho = PROMPTS_DIR / f"prompts-{slug}.md"
    salvar_arquivo(caminho, prompts)

    # salvar_arquivo já exibe ok() internamente
    return caminho


# ═════════════════════════════════════════════════════════════════════════════
# AGENTE 4 — ÁUDIO (ElevenLabs)
# Recebe: roteiro completo + slug
# Retorna: arquivos MP3 em 04-Videos-Publicados/audio/
# Reutiliza a lógica de extração de gerar-vozes.py
# ═════════════════════════════════════════════════════════════════════════════

# Padrões de extração — mesma lógica do gerar-vozes.py existente
CENAS_AUDIO = [
    {
        "nome":   "Cena1-Gancho",
        "secao":  r"GANCHO",
        "padrao": r'\*\*Fala\s*/\s*Legenda[^:]*:\*\*\s*>\s*\*"([^"]+)"',
    },
    {
        "nome":   "Cena2-Solucao",
        "secao":  r"SOLU[ÇC][ÃA]O",
        "padrao": r'\*\*Fala\s*/\s*narra[çc][ãa]o[^:]*:\*\*\s*>\s*\*"([^"]+)"',
    },
    {
        "nome":   "Cena3-ProvaSocial",
        "secao":  r"PROVA\s+SOCIAL",
        "padrao": r'\*\*Fala[^:]*:\*\*\s*>\s*\*"([^"]+)"',
    },
    {
        "nome":   "Cena4-CTA",
        "secao":  r"CTA",
        "padrao": r'\*\*Fala[^:]*:\*\*\s*>\s*\*"([^"]+)"',
    },
]


def _extrair_bloco(texto: str, titulo_regex: str) -> str:
    # Aceita ## ou ### e qualquer emoji/texto ao redor do título
    padrao = rf"#{2,3}[^\n]*{titulo_regex}[^\n]*\n(.*?)(?=\n---|\Z)"
    m = re.search(padrao, texto, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else ""


def _extrair_fala(bloco: str, padrao: str) -> str:
    m = re.search(padrao, bloco, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fallback mais flexível: qualquer texto entre aspas após '>' opcionalmente com '*'
    m2 = re.search(r'>\s*\*?\s*"([^"]+)"', bloco)
    return m2.group(1).strip() if m2 else ""


def _chamar_elevenlabs(texto: str) -> bytes:
    """Chama a API TTS do ElevenLabs e retorna os bytes do MP3."""
    url     = f"{ELEVENLABS_BASE}/text-to-speech/{VOICE_ID}"
    payload = {
        "text":       texto,
        "model_id":   "eleven_multilingual_v2",
        "voice_settings": {
            "stability":        0.5,
            "similarity_boost": 0.75,
            "style":            0.0,
            "use_speaker_boost": True,
        },
    }
    headers = {
        "xi-api-key":   ELEVENLABS_KEY,
        "Content-Type": "application/json",
        "Accept":       "audio/mpeg",
    }

    r = requests.post(url, json=payload, headers=headers, timeout=60)

    if r.status_code == 429:
        info("Rate limit ElevenLabs — aguardando 10s...")
        time.sleep(10)
        r = requests.post(url, json=payload, headers=headers, timeout=60)

    r.raise_for_status()
    return r.content


def agente_audio(roteiro: str, slug: str):
    agente_header(4, "ÁUDIO", "Extraindo falas do roteiro e gerando MP3s via ElevenLabs...")

    print("  O Agente Áudio usa os mesmos padrões de extração do")
    print("  gerar-vozes.py existente. Ele extrai as 4 falas do")
    print("  roteiro (Gancho, Solução, Prova Social, CTA) e chama")
    print("  o ElevenLabs para cada uma.\n")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # Monta nome do produto a partir do slug: foam-roller → FoamRoller
    nome_produto = "".join(p.capitalize() for p in slug.split("-"))

    ok_count  = 0
    err_count = 0

    for cena in CENAS_AUDIO:
        bloco = _extrair_bloco(roteiro, cena["secao"])
        fala  = _extrair_fala(bloco, cena["padrao"])

        print(f"\n  [{cena['nome']}]")

        if not fala:
            info("Fala não encontrada nessa cena — pulando.")
            err_count += 1
            continue

        # Mostra prévia do texto (máx. 90 chars)
        previa = fala[:90] + ("..." if len(fala) > 90 else "")
        info(f'Texto: "{previa}"')

        destino = AUDIO_DIR / f"{nome_produto}-{cena['nome']}.mp3"

        print(f"  Gerando MP3... ", end="", flush=True)
        try:
            audio = _chamar_elevenlabs(fala)
            destino.write_bytes(audio)
            kb = len(audio) / 1024
            print(f"OK ({kb:.1f} KB) → {destino.name}")
            ok_count += 1
        except requests.HTTPError as e:
            resp = e.response
            if resp is not None:
                print(f"ERRO HTTP {resp.status_code}: {resp.text[:100]}")
            else:
                print(f"ERRO HTTP: {e}")
            err_count += 1
        except Exception as e:
            print(f"ERRO: {e}")
            err_count += 1

    print()
    ok(f"{ok_count} MP3(s) gerados, {err_count} erro(s)/pulado(s).")
    info(f"Arquivos em: 04-Videos-Publicados/audio/")


# ═════════════════════════════════════════════════════════════════════════════
# AGENTE 5 — TÍTULOS YOUTUBE
# Recebe: roteiro completo
# Retorna: lista de 5 títulos prontos para uso
# ═════════════════════════════════════════════════════════════════════════════

SYSTEM_TITULOS = """Você é especialista em YouTube Shorts para canais brasileiros de afiliados.
Crie 5 títulos criativos e chamativos para YouTube Shorts de produtos do Mercado Livre.

REGRAS OBRIGATÓRIAS:
- Máximo 60 caracteres no título (sem contar " #Shorts" no final)
- Começa com emoji impactante (🔥⚡💥🛒⏰🧙)
- Inclui o preço se mencionado no roteiro (ex: "por R$60")
- Usa gatilhos de urgência: ACHEI, CORRE, SÓ HOJE, OLHA, INCRÍVEL, MAGO ENCONTROU
- Menciona Mercado Livre ou ML quando couber
- Termina SEMPRE com " #Shorts"
- Varie os gatilhos — não repita o mesmo emoji ou palavra inicial

FORMATO DE RESPOSTA — liste os 5 títulos numerados:
1. [título completo com #Shorts]
2. [título completo com #Shorts]
3. [título completo com #Shorts]
4. [título completo com #Shorts]
5. [título completo com #Shorts]

Nada mais além da lista."""


def agente_titulos(roteiro: str) -> list[str]:
    agente_header(5, "TÍTULOS YOUTUBE", "Gerando 5 opções de título para o Short...")

    print("  O Agente Títulos analisa o produto, preço e gancho do")
    print("  roteiro para criar títulos com máximo impacto e cliques.\n")

    resultado = chamar_claude(
        system=SYSTEM_TITULOS,
        usuario=f"Crie 5 títulos para este roteiro de YouTube Shorts:\n\n{roteiro[:2000]}",
        max_tokens=400,
    )

    # Extrai linhas numeradas do resultado
    titulos = re.findall(r"^\d+\.\s*(.+)", resultado, re.MULTILINE)
    titulos = [t.strip() for t in titulos if len(t.strip()) > 10][:5]

    ok(f"{len(titulos)} títulos gerados!")
    return titulos


# ═════════════════════════════════════════════════════════════════════════════
# ORQUESTRADOR PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

def verificar_api_key():
    global _gemini_client
    # Prioridade: variável de ambiente > chave local no arquivo
    chave = os.environ.get("GEMINI_API_KEY") or GEMINI_API_KEY_LOCAL
    if not chave:
        print()
        print("  ERRO: GEMINI_API_KEY não encontrada!")
        print("  Obtenha sua chave GRÁTIS em: https://aistudio.google.com/apikey")
        print("  Depois cole em GEMINI_API_KEY_LOCAL no topo do arquivo.")
        print()
        sys.exit(1)
    os.environ["GEMINI_API_KEY"] = chave
    _gemini_client = genai.Client(api_key=chave)


def escolher_etapas() -> set[int]:
    print()
    print("  PIPELINE DISPONÍVEL:")
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  1  Analista    Analisa produto → cria briefing      │")
    print("  │  2  Roteirista  Gera roteiro no formato do canal     │")
    print("  │  3  Prompts     Gera 6 prompts para o Veo3           │")
    print("  │  4  Áudio       Gera MP3s via ElevenLabs             │")
    print("  │  5  Títulos     Gera 5 opções de título YouTube      │")
    print("  └─────────────────────────────────────────────────────┘")
    print()
    resp = input("  Quais etapas? [1,2,3,4,5 ou Enter = todas]: ").strip()

    if not resp:
        return {1, 2, 3, 4, 5}

    etapas = set()
    for parte in resp.split(","):
        parte = parte.strip()
        if parte.isdigit() and 1 <= int(parte) <= 5:
            etapas.add(int(parte))

    return etapas if etapas else {1, 2, 3, 4, 5}


def main():
    cabecalho()
    verificar_api_key()

    print("  Bem-vindo! Este orquestrador automatiza a criação de")
    print("  conteúdo de afiliado do início ao fim.")
    print()

    # ── Input do produto ──────────────────────────────────────────────────
    secao("PRODUTO")
    print()
    print("  Informe o produto. Pode ser:")
    print("  · Nome:        'Foam Roller Odin Fit'")
    print("  · URL do ML:   'https://www.mercadolivre.com.br/...'")
    print("  · Descrição:   'Corda de pular digital com contador, R$45'")
    print()

    produto_input = input("  → Produto: ").strip()
    if not produto_input:
        print()
        print("  Nenhum produto informado. Saindo.")
        sys.exit(0)

    # ── Slug para nomes de arquivo ────────────────────────────────────────
    print()
    # Remove URLs e caracteres extras para sugerir um slug (melhorado para PT-BR)
    texto_slug = re.sub(r"https?://\S+", "", produto_input).strip()
    # Mantém letras (incluindo acentos), números e espaços
    texto_slug = re.sub(r"[^a-zA-Z0-9À-ÿ ]", " ", texto_slug).strip()[:50]
    slug_sugerido = slugify(texto_slug) or "produto"

    slug_input = input(f"  → Slug do arquivo [{slug_sugerido}]: ").strip()
    slug = slugify(slug_input) if slug_input else slug_sugerido
    info(f"Arquivos serão nomeados com slug: '{slug}'")

    # ── Seleção de etapas ─────────────────────────────────────────────────
    etapas = escolher_etapas()

    # ═════════════════════════════════════════════════════════════════════
    # EXECUÇÃO DO PIPELINE
    # ═════════════════════════════════════════════════════════════════════

    briefing = ""
    roteiro  = ""
    titulos: list[str] = []

    # Agente 1 — Analista
    if 1 in etapas:
        briefing = agente_analista(produto_input)

    # Agente 2 — Roteirista
    if 2 in etapas:
        entrada = briefing if briefing else produto_input
        roteiro, _ = agente_roteirista(entrada, slug)

    # Se o agente 2 foi pulado, tenta carregar roteiro existente
    if not roteiro:
        caminho_existente = ROTEIROS_DIR / f"roteiro-{slug}.md"
        if caminho_existente.exists():
            roteiro = caminho_existente.read_text(encoding="utf-8")
            info(f"Roteiro existente carregado: roteiro-{slug}.md")

    # Agente 3 — Prompts Veo3
    if 3 in etapas:
        if roteiro:
            agente_prompts(roteiro, slug)
        else:
            info("Agente 3 pulado — roteiro não disponível.")

    # Agente 4 — Áudio
    if 4 in etapas:
        if roteiro:
            agente_audio(roteiro, slug)
        else:
            info("Agente 4 pulado — roteiro não disponível.")

    # Agente 5 — Títulos
    if 5 in etapas:
        if roteiro:
            titulos = agente_titulos(roteiro)
        else:
            info("Agente 5 pulado — roteiro não disponível.")

    # ═════════════════════════════════════════════════════════════════════
    # RESUMO FINAL
    # ═════════════════════════════════════════════════════════════════════

    print()
    print()
    print("╔" + "═" * 60 + "╗")
    print("║   PIPELINE CONCLUÍDO                                       ║")
    print("╚" + "═" * 60 + "╝")
    print()
    print("  ARQUIVOS GERADOS:")

    if 2 in etapas and roteiro:
        print(f"  📄  02-Roteiros-Prontos/roteiro-{slug}.md")
    if 3 in etapas and roteiro:
        print(f"  🎬  03-Prompts-Veo3/prompts-{slug}.md")
    if 4 in etapas and roteiro:
        nome_produto = "".join(p.capitalize() for p in slug.split("-"))
        print(f"  🔊  04-Videos-Publicados/audio/{nome_produto}*.mp3")

    if titulos:
        print()
        print("  TÍTULOS PARA YOUTUBE:")
        for i, t in enumerate(titulos, 1):
            chars = len(t)
            indicador = "✓" if chars <= 68 else "!"
            print(f"  {indicador}  {i}. {t}  ({chars} chars)")

    print()
    print("  PRÓXIMOS PASSOS:")
    print("  1. Revise o roteiro em 02-Roteiros-Prontos/")
    print("  2. Gere os vídeos no Veo3 usando os prompts em 03-Prompts-Veo3/")
    print("  3. Monte o vídeo no editor (adicione áudios + legendas)")
    print("  4. Rode: python postar-youtube.py para publicar no YouTube")
    print()
    print(LINHA)
    print()


if __name__ == "__main__":
    main()
