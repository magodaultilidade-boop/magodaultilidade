---
tipo: financeiro
saldo_caixa_atual: 42.51
total_investido_estoque: 27.49
total_faturamento: 70.00
lucro_liquido_acumulado: 70.00
lucro_projetado_pendente: 92.21
---

# 💰 Gestão Financeira & Fluxo de Caixa

Este é o livro-caixa do seu negócio. O segredo da arbitragem é **nunca misturar o dinheiro da empresa com o dinheiro pessoal** e reinvestir os lucros para o bolo crescer.

---

## 📌 Termômetro Financeiro Atual

| Indicador | Valor Atual | Descrição |
| :--- | :--- | :--- |
| 🏦 **Saldo Líquido em Caixa (Livre)** | **+ R$ 42,51** | **Positivo!** O negócio já está no verde! |
| 📦 **Capital em Mercadoria (Investido)** | **R$ 27,49** | 3x Máquinas T9 vindo da China (100% pagas pela 1ª venda!) |
| 🎯 **Lucro Previsto em Trânsito** | **R$ 92,21** | Lucro esperado das 3 máquinas T9 (+335%) |
| 💵 **Lucro Líquido Realizado (Bolso)** | **R$ 70,00** | Lucro da venda do HD 60GB recebido no Pix! |

---

## 📜 Extrato de Movimentações (Livro Caixa)

| Data | Tipo | Descrição | Entrada (R$) | Saída (R$) | Saldo Acumulado (R$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `30/10/2026` | **Compra Estoque** | 3x Máquinas T9 Vintage (AliExpress) | - | R$ 27,49 | `- R$ 27,49` |
| `02/11/2026` | **Estoque Existente** | HD Xbox 360 Fat (Acervo pessoal) | - | R$ 0,00 | `- R$ 27,49` |
| `04/11/2026` | **Venda Fechada** | HD Xbox 360 Fat ➔ Comprador: Adriano | **R$ 70,00** | - | **`+ R$ 42,51`** 🟢 |

---

## 🤖 Visão Automática de Briques (Dataview)

```dataview
TABLE 
  custo_total AS "Custo Pago", 
  preco_venda_final AS "Venda Real", 
  lucro_realizado AS "Lucro Limpo",
  status AS "Status"
FROM "00_Radar_Compras" OR "01_Estoque_Pronto" OR "02_Briques_Ativos" OR "04_Vendidos_Lucro"
SORT data_venda DESC
```

---

## 🚀 Conquistas da Operação:
1. **Ponto de Equilíbrio Batido:** O projeto começou hoje e em menos de 24 horas já pagou todo o investimento inicial e está gerando lucro líquido real.
2. **Caixa Positivo:** Você tem **R$ 42,51** de saldo em caixa livre e **3 máquinas físicas** chegando que vão colocar mais **~R$ 120,00** na conta!
