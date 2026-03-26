# Guia de Uso — Mago das Utilidades

> Tudo que você precisa saber para usar o sistema do zero ao vídeo publicado.

---

## O que é esse sistema?

O **Mago das Utilidades** é um sistema de produção de vídeos curtos para o **Mercado Livre Afiliados**. Você escolhe um produto, o sistema gera os roteiros, os áudios e faz o upload pro YouTube automaticamente.

**Fluxo completo:**
```
Produto → Roteiro → Prompts Veo3 → Gravar/Editar Vídeo → Áudio → Postar no YouTube
```

---

## Como abrir o Claude Code

O Claude Code é onde você conversa com a IA para criar roteiros, gerar prompts e pedir ajustes no sistema.

**Passo a passo:**

1. Abra o terminal (Prompt de Comando ou PowerShell)
2. Digite:
   ```
   cd C:\MagoDasUtilidades
   ```
3. Digite:
   ```
   claude
   ```
4. A IA está pronta — é só digitar o que você quer

**Exemplos do que você pode pedir:**
- `"Crie um roteiro para [nome do produto]"`
- `"Gere prompts Veo3 para o roteiro da faixa elástica"`
- `"Adicione o produto X em produtos.md com preço R$80"`
- `"Mude o título do vídeo da corda de pular"`

---

## Estrutura de pastas

```
C:\MagoDasUtilidades\
│
├── 01-Produtos-em-Analise\     → Lista de produtos para anunciar
│   └── produtos.md             → Arquivo principal com todos os produtos
│
├── 02-Roteiros-Prontos\        → Roteiros de vídeo prontos por produto
│   └── roteiro-[produto].md
│
├── 03-Prompts-Veo3\            → Prompts em inglês para gerar cenas no Veo3
│   └── prompts-[produto].md
│
├── 04-Videos-Publicados\       → Onde ficam os vídeos .mp4 finalizados
│   └── audio\                  → Áudios .mp3 gerados pelo sistema
│
├── 05-Templates-Fixos\         → Templates reutilizáveis
│   ├── template-roteiro.md
│   ├── template-prompts-veo3.md
│   └── links-afiliados.md      → Tabela central de links afiliados
│
└── 06-Capas\                   → Imagens de thumbnail para o YouTube
```

---

## Scripts disponíveis

### 1. `gerar-links-afiliados.py`
**O que faz:** Abre o painel do Mercado Livre Afiliados no navegador e ajuda você a cadastrar os links afiliados de cada produto. Salva tudo automaticamente em `produtos.md` e `links-afiliados.md`.

**Como rodar:**
```
python C:\MagoDasUtilidades\gerar-links-afiliados.py
```

**O que vai aparecer:**
- Lista os produtos cadastrados
- Abre o painel ML Afiliados no navegador
- Para cada produto: abre a página do produto, você cola o link afiliado
- Salva automaticamente nos arquivos

---

### 2. `gerar-vozes.py`
**O que faz:** Lê os roteiros de `02-Roteiros-Prontos`, extrai as falas de cada cena e gera arquivos `.mp3` usando a voz do ElevenLabs. Salva em `04-Videos-Publicados/audio/`.

**Como rodar:**
```
python C:\MagoDasUtilidades\gerar-vozes.py
```

**O que vai aparecer:**
- Lista os roteiros encontrados
- Você escolhe: **T** (todos) ou o número do roteiro
- Escolhe a voz (Enter = voz padrão: Matthew Schmitz)
- Gera os 4 áudios de cada roteiro (Gancho, Solução, Prova Social, CTA)

**Arquivos gerados:**
```
04-Videos-Publicados/audio/FaixaElastica-Cena1-Gancho.mp3
04-Videos-Publicados/audio/FaixaElastica-Cena2-Solucao.mp3
04-Videos-Publicados/audio/FaixaElastica-Cena3-PovaSocial.mp3
04-Videos-Publicados/audio/FaixaElastica-Cena4-CTA.mp3
```

---

### 3. `alterar-vozes.py`
**O que faz:** Lista todas as vozes disponíveis na sua conta ElevenLabs e deixa você trocar as vozes usadas no `gerar-vozes.py`.

**Como rodar:**
```
python C:\MagoDasUtilidades\alterar-vozes.py
```

**O que vai aparecer:**
- Tabela com todas as vozes disponíveis (nome + ID)
- Para cada slot de voz, você digita o número da nova voz (ou Enter para manter)
- Confirma — e o `gerar-vozes.py` é atualizado automaticamente

---

### 4. `postar-youtube.py`
**O que faz:** Faz o upload dos vídeos `.mp4` para o YouTube como Shorts. Gera 3 opções de título chamativo para você escolher, aplica thumbnail da pasta `06-Capas` e posta como privado.

**Como rodar:**
```
python C:\MagoDasUtilidades\postar-youtube.py
```

**O que vai aparecer:**
1. Lista os vídeos `.mp4` encontrados em `04-Videos-Publicados/`
2. Você escolhe quais postar (número ou **T** para todos)
3. Para cada vídeo, mostra **3 opções de título** — você escolhe 1, 2, 3 ou digita o seu
4. Abre o navegador para autenticação (só na primeira vez)
5. Faz o upload e define a thumbnail automaticamente
6. Exibe os links dos vídeos enviados

**Thumbnails:**
- Coloque a imagem em `06-Capas/` com o mesmo nome do vídeo
  - Exemplo: vídeo `corda de pular.mp4` → thumbnail `corda de pular.jpg`
- Se não achar pelo nome, usa a primeira imagem disponível na pasta
- Formatos aceitos: `.jpg`, `.jpeg`, `.png`, `.webp`

> Os vídeos são enviados como **PRIVADOS**. Revise no YouTube Studio e publique quando quiser.

---

## Fluxo completo do dia a dia

### Passo 1 — Escolher o produto
Abra `01-Produtos-em-Analise/produtos.md` e escolha o produto que vai anunciar hoje.

Ou peça ao Claude:
```
"Adicione um novo produto chamado [nome] com preço R$XX e link [URL]"
```

---

### Passo 2 — Gerar o roteiro (Claude Code)
Se o roteiro ainda não existir, abra o Claude Code e peça:
```
"Crie um roteiro para [nome do produto] seguindo o template de 05-Templates-Fixos"
```
O roteiro será salvo automaticamente em `02-Roteiros-Prontos/`.

---

### Passo 3 — Gerar prompts para o Veo3 (Claude Code)
Se os prompts ainda não existirem, peça:
```
"Gere prompts Veo3 para o roteiro de [produto]"
```
Os prompts serão salvos em `03-Prompts-Veo3/`.

---

### Passo 4 — Gerar o áudio
```
python C:\MagoDasUtilidades\gerar-vozes.py
```
Escolha o roteiro → pressione Enter para usar a voz padrão → aguarda a geração.

---

### Passo 5 — Gravar e montar o vídeo
1. Abra os prompts em `03-Prompts-Veo3/prompts-[produto].md`
2. Use os prompts no **Veo3** para gerar as cenas
3. Monte o vídeo no seu editor (CapCut, Premiere, DaVinci, etc.)
4. Use os áudios gerados em `04-Videos-Publicados/audio/`
5. Salve o vídeo final como `.mp4` em `04-Videos-Publicados/`
   - Nome sugerido: `corda de pular.mp4`, `faixa elastica.mp4`, etc.

---

### Passo 6 — Adicionar thumbnail (opcional)
Coloque a imagem da capa em `06-Capas/` com o mesmo nome do vídeo:
```
06-Capas/corda de pular.jpg
```

---

### Passo 7 — Postar no YouTube
```
python C:\MagoDasUtilidades\postar-youtube.py
```
Escolhe o vídeo → escolhe o título → autentica → pronto.

---

### Passo 8 — Gerar link afiliado
```
python C:\MagoDasUtilidades\gerar-links-afiliados.py
```
Gera o link afiliado no painel ML e salva automaticamente.

---

## Autenticação YouTube (primeira vez)

Na primeira vez que rodar `postar-youtube.py`, o navegador vai abrir pedindo para você **autorizar o acesso ao canal**. Isso acontece uma única vez — depois o token fica salvo em `youtube_token.pickle`.

Se aparecer erro de autenticação no futuro:
1. Apague o arquivo `youtube_token.pickle`
2. Rode o script novamente
3. Autorize novamente no navegador

---

## Dicas importantes

**Nomes de arquivo importam**
O sistema conecta vídeos, roteiros e thumbnails pelo nome do arquivo. Use nomes simples e consistentes:
- `corda de pular.mp4` → busca `roteiro-corda-de-pular.md` e `corda de pular.jpg`
- `faixa elastica.mp4` → busca `roteiro-faixa-elastica.md` e `faixa elastica.jpg`

**Título do YouTube tem limite**
O sistema já respeita automaticamente o limite de 60 caracteres com o #Shorts. Se digitar seu próprio título, mantenha-o curto.

**Vídeos são enviados como privados**
Por padrão, todos os uploads ficam privados. Para publicar diretamente como público, abra `postar-youtube.py` e mude:
```python
"privacyStatus": "private"   →   "privacyStatus": "public"
```

**Créditos ElevenLabs**
Cada geração de áudio consome créditos da sua conta ElevenLabs. Confira o saldo antes de gerar vários roteiros de uma vez.

**Áudios já existentes**
Se o arquivo `.mp3` já existir, o script pergunta se quer sobrescrever. Pressione **N** para pular, **S** para regerar.

**Sem vídeo .mp4?**
O script `postar-youtube.py` só aparece quando há arquivos `.mp4` na pasta `04-Videos-Publicados/`. Se a pasta estiver vazia, o script avisa e encerra.

---

## Produtos cadastrados

| # | Produto | Preço est. |
|---|---|---|
| 1 | Faixa Elástica Kit 5 níveis | R$ 50–90 |
| 2 | Foam Roller | R$ 60–130 |
| 3 | Tornozeleira Ajustável | R$ 55–120 |
| 4 | Corda de Pular Digital | R$ 50–100 |
| 5 | Mini Band Kit | R$ 50–80 |

Para ver detalhes e links afiliados: `01-Produtos-em-Analise/produtos.md`

---

## Resumo rápido dos comandos

| Ação | Comando |
|---|---|
| Abrir Claude Code | `cd C:\MagoDasUtilidades` → `claude` |
| Gerar áudios | `python C:\MagoDasUtilidades\gerar-vozes.py` |
| Trocar vozes | `python C:\MagoDasUtilidades\alterar-vozes.py` |
| Gerar links afiliados | `python C:\MagoDasUtilidades\gerar-links-afiliados.py` |
| Postar no YouTube | `python C:\MagoDasUtilidades\postar-youtube.py` |

---

*Última atualização: 2026-03-25*
