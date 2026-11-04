---
tipo: financeiro
saldo_caixa_atual: -24.38
total_investido_estoque: 94.38 # (27.49 Ali + 66.89 ML)
total_faturamento_realizado: 70.00
lucro_liquido_realizado: 70.00
lucro_projetado_pendente: 145.22 # (92.21 Maquinas + 53.01 Chaves)
faturamento_total_previsto: 239.60 # (119.70 Maquinas + 119.90 Chaves)
---

# 💰 Gestão Financeira & Fluxo de Caixa

Este é o livro-caixa do seu negócio. O segredo da arbitragem é **nunca misturar o dinheiro da empresa com o dinheiro pessoal** e reinvestir os lucros para o bolo crescer.

---

## 📌 Termômetro Financeiro Atual

| Indicador | Valor Atual | Descrição |
| :--- | :--- | :--- |
| 🏦 **Saldo em Caixa (Líquido)** | **- R$ 24,38** | Pequeno ajuste de giro (100% coberto pelo estoque em trânsito) |
| 📦 **Capital Total em Mercadoria** | **R$ 94,38** | 3x Máquinas T9 (Ali) + 1x Jogo de Chaves 12 Pçs (ML Full) |
| 🎯 **Lucro Previsto em Trânsito** | **R$ 145,22** | Lucro esperado somando os 2 lotes! 🚀 |
| 💵 **Faturamento Previsto Total** | **R$ 239,60** | Dinheiro que vai retornar para o seu caixa nas próximas vendas |
| 🏆 **Lucro Realizado no Bolso** | **R$ 70,00** | Venda do HD 60GB recebida no Pix! |

---

## 📜 Extrato de Movimentações (Livro Caixa)

| Data | Tipo | Descrição | Entrada (R$) | Saída (R$) | Saldo Acumulado (R$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `30/10/2026` | **Compra Estoque** | 3x Máquinas T9 Vintage (AliExpress) | - | R$ 27,49 | `- R$ 27,49` |
| `02/11/2026` | **Estoque Existente** | HD Xbox 360 Fat (Acervo pessoal) | - | R$ 0,00 | `- R$ 27,49` |
| `04/11/2026` | **Venda Fechada** | HD Xbox 360 Fat ➔ Adriano (Pix) | **R$ 70,00** | - | `+ R$ 42,51` |
| `04/11/2026` | **Compra Estoque** | Jogo de Chaves Combinadas 12 Pçs (ML Full) | - | **R$ 66,89** | **`- R$ 24,38`** |

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
* Você reinvestiu praticamente **todo o Pix que acabou de entrar** (R$ 70,00) em uma mercadoria que **chega amanhã**!
* Assim que o jogo de chaves chegar e você vender por **R$ 100 a R$ 120**, seu caixa vai para mais de **R$ 80 a R$ 95 positivos**, e as 3 máquinas do AliExpress ainda estarão a caminho para somar mais **R$ 120**.
* É o ciclo clássico de **giro rápido com alavancagem**: o dinheiro não dorme parado na conta!
