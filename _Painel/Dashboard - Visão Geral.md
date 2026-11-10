# 📊 Dashboard Brique — Vendas, Estoque e Giro

> Painel executivo consolidado da sua operação de compra, venda e arbitragem física.

---

## 📈 1. Cockpit de Indicadores (Visão Geral & Mês Atual)

| 🏷️ Métricas Gerais de Estoque e Vendas | Valor Real | 📅 Resumo do Mês Atual (Novembro/2026) | Valor do Mês |
| :--- | :--- | :--- | :--- |
| **Produtos em estoque / trânsito** | `7 unidades (4 lotes)` | **Vendidos no mês** | `2 briques` 🎉 |
| **Total investido no estoque ativo** | `R$ 246,21` | **Faturamento do mês** | `R$ 130,00` |
| **Produtos vendidos (acumulado)** | `2 unidades` | **Lucro líquido do mês** | `R$ 101,03` 🟢 |
| **Faturamento total realizado** | `R$ 130,00` | **Ticket médio no mês** | `R$ 65,00` |
| **Lucro líquido realizado (Pix)** | `R$ 101,03` | **Produtos parados (+7 ou +30 dias)**| `0 unidades (R$ 0,00)` |
| **Margem líquida média das vendas** | `77,7%` | **Faturamento potencial do estoque** | `R$ 509,40` 🚀 |
| **ROI médio realizado** | `103,5%` | **Lucro potencial em trânsito/estoque**| `R$ 263,15` |
| **Ticket médio geral** | `R$ 65,00` | **Canal com maior conversão direta** | `WhatsApp / Status (+107% ROI)` |
| **Dias médios para venda (Giro)** | `2,5 dias` 🔥 | **Categorias mais rápidas** | `Games e Acessórios Moto` |

---

## 🚨 2. Alertas Automáticos de Brique

> [!WARNING] **Produto Parado há mais de 7 dias (Marketplace) ou 30 dias (Estoque)**
> * **Status Atual:** 🟢 O Jogo de Chaves está anunciado há ~5 dias. Se até 12/11 não fechar, basta apagar o anúncio e repostar com nova foto de capa e título calibrado.
> * **Ação recomendada:** Compartilhar o link do Jogo de Chaves para mais 5 grupos de mecânica, obras e feira do rolo da região.

> [!CAUTION] **Alerta de Margem Baixa ou Lucro Negativo**
> * **Status Atual:** 🟢 100% no verde! Ambas as vendas (HD a R$ 70 e Fone V10 a R$ 60) foram fechadas com lucros expressivos acima de 100% de ROI.

> [!TIP] **Origem que mais Vende & Onde Priorizar Compras**
> * **Mercado Livre FULL:** Excelente motor de giro (entrega no dia seguinte permite anunciar imediatamente no fim de semana).
> * **AliExpress Choice:** Aguardando chegada das 3 máquinas T9 (margem de 335%).

> [!NOTE] **Estratégia dos Status do WhatsApp (Descoberta Valiosa!)**
> * A venda do fone para o **Mauricio** através do status do **Ailton da Master** provou que o WhatsApp local é uma máquina de venda sem algoritmo para atrapalhar.
> * **Ação:** Continue pedindo para colegas do trabalho/amigos compartilharem fotos dos seus produtos nos status!

---

## 🧭 3. Atalhos das Etapas do Negócio

| Etapa | Pasta / Painel | O que você encontra |
| :--- | :--- | :--- |
| **💰 Gestão Financeira** | [[Fluxo_de_Caixa]] | Livro-caixa, saldo em conta (R$ 60), compras e lucros realizados |
| **🏆 Matriz de Campeões & Giro** | [[Matriz_Produtos_Campeoes]] | **Classificação de produtos estrelas, foguetes e tartarugas** |
| **📱 Guia de Celulares & Anti-Golpe** | [[Guia_Garimpo_iPhones_Celulares]] | Tabela de preços de iPhones para revenda e regras de segurança |
| **📦 1. Radar & Pedidos** | [[00_Radar_Compras/]] | 3x Máquinas T9 (Ali) + Kit 10 Potes Herméticos 640ml (ML Full) |
| **🛠️ 2. Estoque em Mãos** | [[01_Estoque_Pronto/]] | Produtos conferidos, fotos reais tiradas, prontos para subir |
| **📢 3. No Ar (Marketplace)**| [[02_Briques_Ativos/]] | Jogo de Chaves 12 Pçs + 2x Fones de Capacete V10 |
| **🔁 4. Alerta de Repostagem**| [[03_Para_Repostar/]] | Anúncios que bateram 7 dias e precisam de renovação |
| **🏆 5. Caixa & Lucro** | [[04_Vendidos_Lucro/]] | [[HD 60GB Original Microsoft - Xbox 360 Fat]] + [[1x Fone Bluetooth Capacete Moto V10 - Mercado Livre]] |
| **👥 6. Carteira de Clientes**| [[05_Clientes_CRM/]] | [[Adriano - Xbox 360]] + [[Mauricio - Fone Moto V10]] |

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

### 📢 Briques Ativos no Marketplace / Estoque
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
