---
tipo: financeiro
saldo_caixa_atual: 0.00
total_investido_estoque: 27.49
total_faturamento: 0.00
lucro_liquido_acumulado: 0.00
lucro_projetado_pendente: 92.21
---

# 💰 Gestão Financeira & Fluxo de Caixa

Este é o livro-caixa do seu negócio. O segredo da arbitragem é **nunca misturar o dinheiro da empresa com o dinheiro pessoal** e reinvestir os lucros para o bolo crescer.

---

## 📌 Termômetro Financeiro Atual

| Indicador | Valor Atual | Descrição |
| :--- | :--- | :--- |
| 🏦 **Caixa Disponível** | **R$ 0,00** | Dinheiro líquido livre para novas compras |
| 📦 **Capital em Mercadoria (Investido)** | **R$ 27,49** | Valor que está na rua/transporte esperando virar venda |
| 🎯 **Lucro Previsto em Trânsito** | **R$ 92,21** | Lucro esperado das 3 máquinas T9 (+335%) |
| 💵 **Lucro Líquido Realizado no Bolso** | **R$ 0,00** | Lucro real de vendas já concluídas no Pix |

---

## 📜 Extrato de Movimentações (Livro Caixa)

| Data | Tipo | Descrição | Entrada (R$) | Saída (R$) | Saldo Acumulado (R$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `30/10/2026` | **Compra Estoque** | 3x Máquinas T9 Vintage (AliExpress) | - | R$ 27,49 | `- R$ 27,49` |
| `02/11/2026` | **Estoque Existente** | HD Xbox 360 Fat (Custo zero / acervo pessoal) | - | R$ 0,00 | `- R$ 27,49` |

---

## 🤖 Visão Automática de Briques (Dataview)

> [!NOTE]
> Essa tabela puxa automaticamente os custos e lucros de todas as notas que você cadastrar nas pastas.

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

## 📈 Regra do Giro de Capital (Dica do Milhão)

1. **Quando vender a primeira máquina por R$ 39,90:**
   * Você já recupera os **R$ 27,49** investidos no lote todo + **R$ 12,41 de lucro limpo**.
   * O custo do lote estará **100% pago** na primeira venda!
2. **As outras 2 máquinas serão 100% lucro puro:**
   * Vendendo as outras 2 a R$ 39,90 = **R$ 79,80 de dinheiro 100% limpo**.
3. **Reinvestimento:**
   * Pegue os R$ 119,70 faturados e compre novos lotes com cupom no Ali/Shopee. Assim seu caixa salta de R$ 27 para R$ 120, de R$ 120 para R$ 400, e assim por diante.

