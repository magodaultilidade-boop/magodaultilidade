"""
Postar no YouTube — Shorts Automatico
========================================
Faz upload de videos de 04-Videos-Publicados como YouTube Shorts,
usando titulo criativo e descricao extraidos dos roteiros em 02-Roteiros-Prontos.
Aplica thumbnail da pasta 06-Capas automaticamente.

Dependencias:
    pip install google-auth-oauthlib google-api-python-client

Fluxo:
    1. Autentica via OAuth2 (abre navegador na 1a vez, salva token)
    2. Busca .mp4 em 04-Videos-Publicados (exceto subpasta audio/)
    3. Para cada video, encontra o roteiro correspondente
    4. Gera titulo criativo baseado no gancho do roteiro
    5. Busca thumbnail em 06-Capas pelo nome do video
    6. Faz upload como Short e define thumbnail
"""

import re
import sys
import pickle
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# -- Configuracao ---------------------------------------------------------------

BASE_DIR      = Path(__file__).parent
ROTEIROS_DIR  = BASE_DIR / "02-Roteiros-Prontos"
VIDEOS_DIR    = BASE_DIR / "04-Videos-Publicados"
CAPAS_DIR     = BASE_DIR / "06-Capas"
TOKEN_FILE    = BASE_DIR / "youtube_token.pickle"

CREDENTIALS_FILE = next(BASE_DIR.glob("client_secret_*.json"), None)

# Escopo completo necessario para upload + thumbnails
SCOPES = ["https://www.googleapis.com/auth/youtube"]

HASHTAGS_FIXAS = "#magodaultilidade #mercadolivre #achadosdoml #Shorts"

LINHA = "-" * 60

EXTENSOES_IMAGEM = [".jpg", ".jpeg", ".png", ".webp"]

# -- Autenticacao ---------------------------------------------------------------

def autenticar():
    if CREDENTIALS_FILE is None:
        print("  ERRO: Arquivo client_secret_*.json nao encontrado em", BASE_DIR)
        sys.exit(1)

    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


# -- Utilitarios ----------------------------------------------------------------

def slug(texto: str) -> str:
    """Normaliza texto para comparacao: sem acentos, sem especiais, lowercase."""
    texto = texto.lower()
    subs = {"a": "aáàãâä", "e": "eéèêë", "i": "iíìîï",
            "o": "oóòõôö", "u": "uúùûü", "c": "cç", "n": "nñ"}
    for base, variantes in subs.items():
        for v in variantes:
            texto = texto.replace(v, base)
    return re.sub(r"[^a-z0-9]", "", texto)


# -- Roteiro --------------------------------------------------------------------

def encontrar_roteiro(video_path: Path) -> Path | None:
    chave_video = slug(video_path.stem)
    for roteiro in ROTEIROS_DIR.glob("*.md"):
        chave_roteiro = slug(roteiro.stem.replace("roteiro-", ""))
        if chave_roteiro in chave_video or chave_video in chave_roteiro:
            return roteiro
    return None


def _truncar(texto: str, limite: int) -> str:
    """Trunca texto no limite de chars, cortando na ultima palavra inteira."""
    if len(texto) <= limite:
        return texto
    return texto[:limite].rsplit(" ", 1)[0].rstrip(".,!?") + "..."


def _extrair_dados_roteiro(texto: str) -> dict:
    """Extrai produto, preco e nome curto do produto a partir do roteiro."""
    # Produto completo
    produto_m = re.search(r"\*\*Produto:\*\*\s*(.+)", texto)
    produto = produto_m.group(1).strip() if produto_m else ""

    # Nome curto: primeiras 2-3 palavras relevantes do produto
    nome_curto = produto
    if produto:
        partes = produto.split()
        # Remove palavras genéricas de quantidade/kit no início
        ignorar = {"kit", "conjunto", "par", "jogo", "pack"}
        inicio = 0
        if partes and partes[0].lower() in ignorar:
            inicio = 1
        nome_curto = " ".join(partes[inicio:inicio + 3])

    # Preco: busca R$XX no texto inteiro
    precos = re.findall(r"R\$\s*(\d+(?:[.,]\d+)?)", texto)
    preco = f"R${precos[0]}" if precos else ""

    # Gancho (fala curta)
    gancho_bloco = re.search(
        r"###[^\n]*GANCHO[^\n]*\n(.*?)(?=\n---|\Z)",
        texto, re.DOTALL | re.IGNORECASE
    )
    gancho = ""
    if gancho_bloco:
        m = re.search(r'["""]([^"""]{10,120})["""]', gancho_bloco.group(1))
        if m:
            gancho = m.group(1).strip()

    return {"produto": produto, "nome_curto": nome_curto, "preco": preco, "gancho": gancho}


def gerar_opcoes_titulo(texto: str) -> list[str]:
    """
    Gera 3 opcoes de titulo chamativo para YouTube Shorts.
    Regras: max 60 chars, emoji inicial, preco, urgencia, termina com #Shorts.
    """
    d = _extrair_dados_roteiro(texto)
    nome   = d["nome_curto"] or "produto incrivel"
    preco  = d["preco"]
    sufixo = " #Shorts"
    limite = 60 - len(sufixo)  # espaco util antes do #Shorts

    # Templates com urgencia variada
    templates = [
        ("ACHEI",    "🔥", f"ACHEI {nome}{' por ' + preco if preco else ''}!"),
        ("OLHA",     "⚡", f"OLHA esse achado{' por ' + preco if preco else ''}!"),
        ("MAGO",     "🧙", f"O MAGO encontrou! {nome}{' por ' + preco if preco else ''}!"),
        ("CORRE",    "💥", f"CORRE! {nome}{' por ' + preco if preco else ''} no ML!"),
        ("INCRIVEL", "🛒", f"INCRIVEL! {nome}{' por ' + preco if preco else ''} no ML!"),
        ("SO HOJE",  "⏰", f"SO HOJE! {nome}{' por ' + preco if preco else ''} no ML!"),
    ]

    opcoes = []
    usados = set()
    for _, emoji, corpo in templates:
        candidato = f"{emoji} {_truncar(corpo, limite - len(emoji) - 1)}{sufixo}"
        if candidato not in usados:
            opcoes.append(candidato)
            usados.add(candidato)
        if len(opcoes) == 3:
            break

    # Fallback: se nao tiver 3, completa com variacao numerada
    while len(opcoes) < 3:
        opcoes.append(f"🔥 ACHEI! {_truncar(nome, limite - 10)}{sufixo}")

    return opcoes


def escolher_titulo(video_nome: str, opcoes: list[str]) -> str:
    """Exibe 3 opcoes de titulo e pede escolha ao usuario."""
    print(f"\n  Titulo para: {video_nome}")
    for i, op in enumerate(opcoes, 1):
        print(f"    {i}. {op}  ({len(op)} chars)")
    print()
    while True:
        resp = input("  Escolha o titulo [1/2/3] ou digite o seu proprio: ").strip()
        if resp in ("1", "2", "3"):
            return opcoes[int(resp) - 1]
        if resp:
            titulo_custom = resp if resp.endswith("#Shorts") else resp + " #Shorts"
            return titulo_custom[:100]
        print("  Digite 1, 2, 3 ou o titulo desejado.")


def extrair_descricao(texto: str) -> str:
    """Monta descricao com roteiro completo + hashtags fixas."""
    m = re.search(
        r"## ROTEIRO COMPLETO.*?\n((?:>.+\n?)+)",
        texto, re.DOTALL,
    )
    if m:
        linhas = re.findall(r">\s*\*?(.+?)\*?\s*$", m.group(1), re.MULTILINE)
        resumo = " ".join(linhas).strip()
    else:
        m2 = re.search(r'["""](.+?)["""]', texto)
        resumo = m2.group(1).strip() if m2 else ""

    produto_m = re.search(r"\*\*Produto:\*\*\s*(.+)", texto)
    produto = produto_m.group(1).strip() if produto_m else ""

    hashtags_produto = ""
    if produto:
        slug_prod = re.sub(r"[^a-zA-Z0-9]", "", produto)
        hashtags_produto = f"#{slug_prod}"

    partes = [p for p in [resumo, produto, hashtags_produto, HASHTAGS_FIXAS] if p]
    return "\n\n".join(partes)


# -- Capas (thumbnails) ---------------------------------------------------------

def encontrar_capa(video_path: Path) -> Path | None:
    """
    Busca imagem em 06-Capas com o mesmo nome do video.
    Se nao encontrar, retorna a primeira imagem disponivel.
    """
    if not CAPAS_DIR.exists():
        return None

    chave_video = slug(video_path.stem)

    # Busca por nome correspondente
    for img in CAPAS_DIR.iterdir():
        if img.suffix.lower() in EXTENSOES_IMAGEM:
            if slug(img.stem) == chave_video or chave_video in slug(img.stem):
                return img

    # Fallback: primeira imagem da pasta
    for img in sorted(CAPAS_DIR.iterdir()):
        if img.suffix.lower() in EXTENSOES_IMAGEM:
            return img

    return None


def definir_thumbnail(youtube, video_id: str, capa_path: Path):
    """Faz upload da thumbnail para o video."""
    mime = "image/jpeg" if capa_path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
    media = MediaFileUpload(str(capa_path), mimetype=mime)
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=media,
    ).execute()
    print(f"    Thumbnail definida: {capa_path.name}")


# -- Upload ---------------------------------------------------------------------

def fazer_upload(youtube, video_path: Path, titulo: str, descricao: str) -> str:
    body = {
        "snippet": {
            "title":                titulo,
            "description":          descricao,
            "categoryId":           "22",
            "defaultLanguage":      "pt",
            "defaultAudioLanguage": "pt",
        },
        "status": {
            "privacyStatus":          "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/*",
        resumable=True,
        chunksize=1024 * 1024 * 5,
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    print(f"  Enviando: {video_path.name}")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"    {pct}%", end="\r", flush=True)

    video_id = response["id"]
    print(f"    Concluido: https://youtu.be/{video_id}        ")
    return video_id


# -- Menu principal -------------------------------------------------------------

def listar_videos() -> list[Path]:
    return [
        p for p in VIDEOS_DIR.rglob("*.mp4")
        if "audio" not in p.parts
    ]


def main():
    print()
    print(LINHA)
    print("  Postar no YouTube - Shorts Automatico")
    print(LINHA)

    videos = listar_videos()
    if not videos:
        print()
        print("  Nenhum .mp4 encontrado em:", VIDEOS_DIR)
        print("  Coloque os videos em 04-Videos-Publicados/ e rode novamente.")
        print()
        sys.exit(0)

    print(f"\n  {len(videos)} video(s) encontrado(s):\n")

    roteiros_map: dict[Path, Path | None] = {}
    capas_map:    dict[Path, Path | None] = {}

    for i, v in enumerate(videos, 1):
        roteiro = encontrar_roteiro(v)
        capa    = encontrar_capa(v)
        roteiros_map[v] = roteiro
        capas_map[v]    = capa

        info_roteiro = roteiro.name if roteiro else "NAO ENCONTRADO"
        info_capa    = capa.name    if capa    else "sem capa"
        print(f"  {i}. {v.name}")
        print(f"       roteiro : {info_roteiro}")
        print(f"       thumbnail: {info_capa}")

    print()
    opcao = input("  Quais postar? (numero, virgula para varios, T = todos): ").strip().lower()

    if opcao == "t":
        selecionados = videos
    else:
        indices = [int(x.strip()) - 1 for x in opcao.split(",") if x.strip().isdigit()]
        selecionados = [videos[i] for i in indices if 0 <= i < len(videos)]

    if not selecionados:
        print("  Nenhum selecionado. Saindo.")
        return

    print()
    print(LINHA)
    print("  Autenticando com o YouTube...")
    youtube = autenticar()
    print("  Autenticado!\n")

    # Fase 1: escolha de titulos (antes de autenticar)
    titulos_map: dict[Path, str] = {}
    textos_map:  dict[Path, str] = {}

    print()
    print(LINHA)
    print("  Escolha os titulos antes de postar:")

    for v in selecionados:
        roteiro_path = roteiros_map[v]
        if roteiro_path:
            texto = roteiro_path.read_text(encoding="utf-8")
            textos_map[v] = texto
            opcoes = gerar_opcoes_titulo(texto)
            titulos_map[v] = escolher_titulo(v.name, opcoes)
        else:
            titulos_map[v] = f"{v.stem} #Shorts"
            textos_map[v]  = ""

    print()
    print(LINHA)
    print("  Autenticando com o YouTube...")
    youtube = autenticar()
    print("  Autenticado!\n")

    resultados = []
    for v in selecionados:
        roteiro_path = roteiros_map[v]
        capa_path    = capas_map[v]
        titulo       = titulos_map[v]
        texto        = textos_map[v]

        descricao = extrair_descricao(texto) if texto else HASHTAGS_FIXAS

        print(f"  Titulo: {titulo}")

        try:
            vid_id = fazer_upload(youtube, v, titulo, descricao)

            if capa_path:
                try:
                    definir_thumbnail(youtube, vid_id, capa_path)
                except Exception as e:
                    print(f"    Aviso: nao foi possivel definir thumbnail — {e}")

            resultados.append((v.name, vid_id, True))
        except Exception as e:
            print(f"    ERRO no upload: {e}")
            resultados.append((v.name, None, False))

        print()

    print(LINHA)
    print("  Resumo:")
    for nome, vid_id, ok in resultados:
        if ok:
            print(f"    OK  {nome} -> https://youtu.be/{vid_id}")
        else:
            print(f"    ERR {nome} -> falhou")
    print()
    print("  Videos enviados como PRIVADOS.")
    print("  Revise no YouTube Studio e publique quando quiser.")
    print("  (Para publicar direto, mude privacyStatus para 'public' no script)")
    print(LINHA)
    print()


if __name__ == "__main__":
    main()
