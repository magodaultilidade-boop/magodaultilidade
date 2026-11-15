---
tipo: financeiro
saldo_caixa_atual: 245.10
total_investido_estoque_ativo: 123.35 # (27.49 Ali T9 + 66.89 Chaves + 28.97 1x Fone)
total_faturamento_realizado: 325.00 # (70.00 HD + 60.00 Fone 1 + 60.00 Fone 2 + 135.00 Potes)
lucro_liquido_realizado: 173.23 # (70.00 HD + 31.03 Fone 1 + 31.03 Fone 2 + 41.17 Potes)
lucro_projetado_estoque_ativo: 126.55 # (62.51 T9 + 33.01 Chaves + 31.03 Fone)
faturamento_total_previsto_estoque: 249.90 # (90.00 T9 + 99.90 Chaves + 60.00 Fone)
---

# 💰 Gestão Financeira & Fluxo de Caixa

Este é o livro-caixa do seu negócio. O segredo da arbitragem é **nunca misturar o dinheiro da empresa com o dinheiro pessoal** e reinvestir os lucros para o bolo crescer.

---

## 📌 Termômetro Financeiro Atual (15/11/2026 - Pós Vendas FDS)

| Indicador | Valor Atual | Descrição |
| :--- | :--- | :--- |
| 🏦 **Saldo em Caixa Livre (Dinheiro em Mãos)** | **R$ 245,10** 🟢 | Caixa limpo após recebimento dos Pix do fim de semana! |
| 📦 **Capital Total em Mercadoria Ativa** | **R$ 123,35** | 3x Máquinas Buda + Chaves 12 Pçs + 1x Fone V10 |
| 🎯 **Lucro Projetado no Estoque Restante** | **R$ 126,55** | Lucro a realizar conforme os 3 anúncios ativos girarem! 🚀 |
| 💵 **Faturamento Previsto Estoque Restante** | **R$ 249,90** | Potencial de venda dos 3 produtos no ar |
| 🏆 **Lucro Realizado no Bolso** | **R$ 173,23** 🟢 | Lucro líquido limpo já concretizado em 4 vendas! |
| 🚀 **Meta de Caixa da 1ª Rodada** | **R$ 495,00** | Caixa total acumulado ao zerar os itens restantes |

---

## 📜 Extrato de Movimentações (Livro Caixa)

| Data | Tipo | Descrição | Entrada (R$) | Saída (R$) | Saldo Caixa (R$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `30/10/2026` | **Compra Estoque** | 3x Máquinas T9 Vintage (AliExpress) | - | R$ 27,49 | `- R$ 27,49` |
| `02/11/2026` | **Estoque Existente** | HD Xbox 360 Fat (Acervo pessoal) | - | R$ 0,00 | `- R$ 27,49` |
| `04/11/2026` | **Venda Fechada** | HD Xbox 360 Fat ➔ Adriano (Pix) | **R$ 70,00** | - | `+ R$ 42,51` |
| `04/11/2026` | **Compra Estoque** | Jogo de Chaves Combinadas 12 Pçs (ML Full) | - | **R$ 66,89** | `- R$ 24,38` |
| `06/11/2026` | **Aporte Pessoal** | Aporte para compra do lote de fones | **R$ 60,00** | - | `+ R$ 35,62` |
| `06/11/2026` | **Compra Estoque** | 3x Fone Bluetooth Capacete V10 (ML Full) | - | **R$ 86,92** | `- R$ 51,30` |
| `09/11/2026` | **Venda Fechada** | 1x Fone V10 ➔ Mauricio (Pix via Ailton) | **R$ 60,00** | - | `+ R$ 8,70` |
| `10/11/2026` | **Aporte Pessoal** | Aporte para Kit 10 Potes Vidro (ML Full) | **R$ 93,83** | - | `+ R$ 102,53` |
| `10/11/2026` | **Compra Estoque** | Kit 10 Potes Vidro Hermético 640ml (ML Full) | - | **R$ 93,83** | `+ R$ 60,00` |
| `10/11/2026` | **Ferramenta / Assinatura**| Assinatura Meli+ (Frete Grátis > R$ 29 + Cupons) | - | **R$ 9,90** | `+ R$ 50,10` |
| `15/11/2026` | **Venda Fechada** | 1x Fone V10 (Un 2) ➔ Samuel Jesus (Pix) | **R$ 60,00** | - | `+ R$ 110,10` |
| `15/11/2026` | **Venda Fechada** | Kit 10 Potes Vidro ➔ Tia (Pix) | **R$ 135,00** | - | **`R$ 245,10`** 🟢 |

---

## 🤖 Visão Automática de Briques (Dataview)

```dataview
TABLE 
  custo_total AS "Custo Pago", 
  preco_anuncio_fb AS "Preço Anúncio", 
  lucro_estimado AS "Lucro Previsto",
  status AS "Status"
FROM "00_Radar_Compras" OR "01_Estoque_Pronto" OR "02_Briques_Ativos" OR "04_Vendidos_Lucro"
SORT data_compra DESC
```
