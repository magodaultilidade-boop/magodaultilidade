# 📊 Dashboard Brique — Vendas, Estoque e Giro

> Painel executivo consolidado da sua operação de compra, venda e arbitragem física.

---

## 📈 1. Cockpit de Indicadores (Visão Geral & Mês Atual)

| 🏷️ Métricas Gerais de Estoque e Vendas | Valor Real | 📅 Resumo do Mês Atual (Novembro/2026) | Valor do Mês |
| :--- | :--- | :--- | :--- |
| **Produtos em estoque / trânsito** | `4 unidades` | **Vendidos no mês** | `1 brique` |
| **Total investido no estoque ativo** | `R$ 94,38` | **Faturamento do mês** | `R$ 70,00` |
| **Produtos vendidos (acumulado)** | `1 unidade` | **Lucro líquido do mês** | `R$ 70,00` |
| **Faturamento total realizado** | `R$ 70,00` | **Ticket médio no mês** | `R$ 70,00` |
| **Lucro líquido realizado (Pix)** | `R$ 70,00` | **Produtos parados (+7 ou +30 dias)**| `0 unidades (R$ 0,00)` |
| **Margem líquida média** | `100,0%` | **Faturamento potencial do estoque** | `R$ 239,60` |
| **ROI médio realizado** | `100,0%` | **Lucro potencial em trânsito** | `R$ 145,22` 🚀 |
| **Ticket médio geral** | `R$ 70,00` | **Canal com melhor margem** | `AliExpress (+335%)` |
| **Dias médios para venda (Giro)** | `2,0 dias` 🔥 | **Categoria com maior giro** | `Games (Vendido em 48h)` |

---

## 🚨 2. Alertas Automáticos de Brique

> [!WARNING] **Produto Parado há mais de 7 dias (Marketplace) ou 30 dias (Estoque)**
> O algoritmo do Facebook mata o alcance após 7 dias.
> * **Status Atual:** 🟢 Nenhum produto parado! Seu giro atual é de **2,0 dias**.
> * **Ação se alertar:** Apagar anúncio, trocar a foto de capa e repostar com leve ajuste de preço.

> [!CAUTION] **Alerta de Margem Baixa ou Lucro Negativo**
> * **Status Atual:** 🟢 Saudável! Nenhuma venda abaixo do preço piso.
> * **Regra:** Nunca vender abaixo do **Preço Piso** estipulado na ficha do produto.

> [!TIP] **Origem que mais Vende & Onde Priorizar Compras**
> * **AliExpress (Choice):** Campeão disparado em **ROI e Margem Bruta** (+335% de lucro nas máquinas T9). Ideal para compras com prazo de 10 a 15 dias.
> * **Mercado Livre (FULL):** Campeão absoluto em **Velocidade de Giro** (chega amanhã). Ideal para abastecer o caixa para o fim de semana.

> [!NOTE] **Categoria que mais Gira**
> * **Games & Videogames:** Giro recorde de **48 horas** em Itu (cliente Adriano já cadastrado no CRM para próximas novidades).
> * **Ferramentas:** Alta liquidez com público trabalhador local (Jogo de Chaves chegando amanhã).

---

## 🧭 3. Atalhos das Etapas do Negócio

| Etapa | Pasta / Painel | O que você encontra |
| :--- | :--- | :--- |
| **💰 Gestão Financeira** | [[Fluxo_de_Caixa]] | Livro-caixa, saldo em conta, compras e lucros realizados |
| **📦 1. Radar & Pedidos** | [[00_Radar_Compras/]] | 3x Máquinas T9 (Ali) + 1x Jogo de Chaves 12 Pçs (ML Full) |
| **🛠️ 2. Estoque em Mãos** | [[01_Estoque_Pronto/]] | Produtos conferidos, fotos reais tiradas, prontos para subir |
| **📢 3. No Ar (Marketplace)**| [[02_Briques_Ativos/]] | Anúncios ativos rodando no Facebook e grupos locais |
| **🔁 4. Alerta de Repostagem**| [[03_Para_Repostar/]] | Anúncios que bateram 7 dias e precisam de renovação |
| **🏆 5. Caixa & Lucro** | [[04_Vendidos_Lucro/]] | [[HD 60GB Original Microsoft - Xbox 360 Fat]] (R$ 70,00 Pix) |
| **👥 6. Carteira de Clientes**| [[05_Clientes_CRM/]] | [[Adriano - Xbox 360]] (WhatsApp salvo e conectado) |

---

## 🤖 4. Consultas Dinâmicas Automáticas (Dataview)

### 📦 Mercadorias em Radar / Trânsito
```dataview
TABLE 
  origem_compra AS "Origem", 
  custo_total AS "Custo Pago", 
  preco_anuncio_fb AS "Preço Anúncio", 
  lucro_estimado AS "Lucro Previsto",
  status AS "Status"
FROM "00_Radar_Compras"
SORT data_compra DESC
```

### 📢 Briques Ativos no Marketplace
```dataview
TABLE 
  categoria AS "Categoria", 
  preco_anuncio_fb AS "Preço Anúncio", 
  preco_minimo_aceitavel AS "Piso", 
  data_anuncio AS "Data Postado"
FROM "02_Briques_Ativos"
SORT data_anuncio DESC
```

### 🏆 Vendas Concluídas & Histórico de Giro
```dataview
TABLE 
  data_venda AS "Data Venda", 
  preco_venda_final AS "Venda (R$)", 
  lucro_realizado AS "Lucro Líquido", 
  comprador AS "Cliente",
  forma_pagamento AS "Pagamento"
FROM "04_Vendidos_Lucro"
SORT data_venda DESC
```
