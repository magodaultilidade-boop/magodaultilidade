---
tipo: financeiro
saldo_caixa_atual: 50.10
total_investido_estoque_ativo: 246.21 # (27.49 Ali T9 + 66.89 Chaves + 57.94 2x Fones + 93.83 Potes)
total_faturamento_realizado: 130.00 # (70.00 HD + 60.00 Fone V10)
lucro_liquido_realizado: 101.03 # (70.00 HD + 31.03 Fone V10)
lucro_projetado_estoque_ativo: 263.15 # (92.21 T9 + 53.01 Chaves + 61.86 Fones + 56.07 Potes)
faturamento_total_previsto_estoque: 509.40 # (119.70 T9 + 119.90 Chaves + 119.80 Fones + 149.90 Potes)
---

# 💰 Gestão Financeira & Fluxo de Caixa

Este é o livro-caixa do seu negócio. O segredo da arbitragem é **nunca misturar o dinheiro da empresa com o dinheiro pessoal** e reinvestir os lucros para o bolo crescer.

---

## 📌 Termômetro Financeiro Atual (10/11/2026)

| Indicador | Valor Atual | Descrição |
| :--- | :--- | :--- |
| 🏦 **Saldo em Caixa Livre (Dinheiro em Mãos)** | **R$ 50,10** | Caixa líquido após investimento na assinatura Meli+ |
| 📦 **Capital Total em Mercadoria Ativa** | **R$ 246,21** | 3x Máquinas Ali + Chaves + 2x Fones V10 + Kit 10 Potes |
| 🎯 **Lucro Projetado no Estoque** | **R$ 263,15** | Lucro líquido que vai entrar conforme os briques venderem! 🚀 |
| 💵 **Faturamento Previsto Total do Estoque** | **R$ 509,40** | Meio milhar de reais em vendas contratadas no seu estoque! |
| 🏆 **Lucro Realizado no Bolso** | **R$ 101,03** | Lucro limpo somando o HD (R$ 70) e o 1º Fone V10 (R$ 31,03)! |

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
| `10/11/2026` | **Ferramenta / Assinatura**| Assinatura Meli+ (Frete Grátis > R$ 29 + Cupons) | - | **R$ 9,90** | **`R$ 50,10`** 🟢 |

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

---

## 🧠 Análise Estratégica do Caixa:
* **Assinatura Meli+ Como Custo Operacional:** O próprio caixa do negócio bancou a ferramenta (R$ 9,90), restando **R$ 50,10 livres**.
* **Retorno Imediato:** Agora você tem Frete Grátis a partir de R$ 29 no FULL e cupons exclusivos para as próximas compras de brique.
