---
tipo: financeiro
saldo_caixa_atual: 174.08
total_investido_estoque_ativo: 244.06 # (123.35 estoque ativo + 33.72 Power Bank + 86.99 Lavadora)
total_faturamento_realizado: 445.00 # (70.00 HD + 60.00 Fone 1 + 60.00 Fone 2 + 135.00 Potes + 120.00 Mouse)
lucro_liquido_realizado: 222.92 # (70.00 HD + 31.03 Fone 1 + 31.03 Fone 2 + 41.17 Potes + 49.69 Mouse)
lucro_projetado_estoque_ativo: 210.64 # (164.46 ativo em mãos + 46.18 Power Bank)
faturamento_total_previsto_estoque: 454.70 # (374.80 ativo em mãos + 79.90 Power Bank)
---

# 💰 Gestão Financeira & Fluxo de Caixa

Este é o livro-caixa do seu negócio. O segredo da arbitragem é **nunca misturar o dinheiro da empresa com o dinheiro pessoal** e reinvestir os lucros para o bolo crescer.

---

## 📌 Termômetro Financeiro Atual (17/11/2026 - Fase 2 Venda Recorde)

| Indicador | Valor Atual | Descrição |
| :--- | :--- | :--- |
| 🏦 **Saldo em Caixa Livre (Dinheiro em Mãos)** | **R$ 174,08** 🟢 | Caixa livre recuperado e protegido após venda do Mouse! |
| 📦 **Capital Total em Mercadoria (Ativo + Radar)** | **R$ 244,06** | Estoque atual + Power Bank + Lavadora 2 Baterias |
| 🎯 **Lucro Projetado no Estoque Restante** | **R$ 210,64** | Lucro líquido contratado para entrar nas vendas! 🚀 |
| 💵 **Faturamento Previsto Total do Catálogo** | **R$ 454,70** | Potencial de venda do catálogo restante |
| 🏆 **Lucro Realizado no Bolso** | **R$ 222,92** 🟢 | Lucro líquido já realizado em 5 vendas concluídas |
| 🚀 **Meta de Caixa da Rodada** | **`R$ 628,78`** | Caixa acumulado ao liquidar o catálogo completo |

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
| `15/11/2026` | **Venda Fechada** | Kit 10 Potes Vidro ➔ Tia (Pix) | **R$ 135,00** | - | `+ R$ 245,10` |
| `16/11/2026` | **Compra Estoque** | Power Bank 10.000mAh Slim C/ Cabos (Ali Brasil) | - | **R$ 33,72** | `+ R$ 211,38` |
| `16/11/2026` | **Compra Estoque** | Mouse Gamer Redragon Cobra M711 (ML FULL) | - | **R$ 70,31** | `+ R$ 141,07` |
| `17/11/2026` | **Compra Estoque** | Lavadora Lava Jato 2 Baterias + Maleta (ML FULL) | - | **R$ 86,99** | `+ R$ 54,08` 🟡 |
| `17/11/2026` | **Venda Fechada** | Mouse Gamer Redragon Cobra M711 ➔ Tomas (Pix) | **R$ 120,00** | - | **`R$ 174,08`** 🟢 |

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
