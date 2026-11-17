# 📊 Dashboard Brique — Vendas, Estoque e Giro

> Painel executivo consolidado da sua operação de compra, venda e arbitragem física.

---

## 📈 1. Cockpit de Indicadores (Visão Geral & Mês Atual)

| 🏷️ Métricas Gerais de Estoque e Vendas | Valor Real             | 📅 Resumo do Mês Atual (Novembro/2026)  | Valor do Mês                    |
| :-------------------------------------- | :--------------------- | :-------------------------------------- | :------------------------------ |
| **Produtos em estoque / trânsito**      | `7 unidades (5 lotes)` | **Vendidos no mês**                     | `5 briques` 🎉                  |
| **Total investido no estoque ativo**    | `R$ 244,06`            | **Faturamento do mês**                  | `R$ 445,00`                     |
| **Produtos vendidos (acumulado)**       | `5 unidades`           | **Lucro líquido do mês**                | `R$ 222,92` 🟢                  |
| **Faturamento total realizado**         | `R$ 445,00`            | **Ticket médio no mês**                 | `R$ 89,00`                      |
| **Lucro líquido realizado (Pix)**       | `R$ 222,92`            | **Produtos parados (+7 dias no ar)**    | `1 unidade (Chaves)`            |
| **Margem líquida média das vendas**     | `50,1%`                | **Faturamento potencial do estoque**    | `R$ 464,70` 🚀                  |
| **ROI médio realizado**                 | `100,4%`               | **Lucro potencial em trânsito/estoque** | `R$ 220,64`                     |
| **Ticket médio geral**                  | `R$ 89,00`             | **Canal com maior conversão direta**    | `Marketplace + WhatsApp (+ R$ 315)`|
| **Dias médios para venda (Giro)**       | `3,6 dias` 🔥          | **Categorias campeãs comprovadas**      | `Gamer/Tech, Cozinha e Moto`    |

---

## 🚨 2. Alertas Automáticos de Brique

> [!WARNING] **Produto Parado há mais de 7 dias (Marketplace) ou 30 dias (Estoque)**
> * O algoritmo do Facebook mata o alcance após 7 dias.
> * A tabela dinâmica abaixo calcula **automaticamente os dias que cada anúncio está no ar**. Se bater 7 dias, a etiqueta vira 🔴 **ALERTA REPOSTAR**!

> [!CAUTION] **Alerta de Margem Baixa ou Lucro Negativo**
> * **Status Atual:** 🟢 100% no verde! Ambas as vendas (HD a R$ 70 e Fone V10 a R$ 60) foram fechadas com lucros expressivos acima de 100% de ROI.

> [!TIP] **Origem que mais Vende & Onde Priorizar Compras**
> * **Mercado Livre FULL:** Excelente motor de giro (entrega no dia seguinte permite anunciar imediatamente no fim de semana).
> * **AliExpress Choice:** Aguardando chegada das 3 máquinas T9 (margem de 335%).

---

## 🧭 3. Atalhos das Etapas do Negócio

| Etapa | Pasta / Painel | O que você encontra |
| :--- | :--- | :--- |
| **🛡️ Finanças Pessoais & Saída da Caverna** | [[Financas_Pessoais_Recuperacao]] | **Mapa de dívidas, estancamento de vazamentos e transição do seguro** |
| **⚔️ Rotina Blindada & Hábitos** | [[Rotina_Blindada_Evolucao]] | **Controle diário de cigarros, quebra de vícios e energia vital** |
| **📦 Expansão Mercado Livre** | [[Estrategia_Expansao_MercadoLivre]] | **Plano das 10 primeiras vendas e escala nacional híbrida** |
| **🧪 Laboratório de 5 Categorias** | [[Laboratorio_5_Categorias]] | **Mapeamento sistemático para encontrar os Produtos Pioneiros** |
| **🎯 Metas & Evolução Mensal** | [[Metas_Mensais]] | **Termômetro de metas, progresso percentual e roadmap mensal** |
| **💰 Gestão Financeira** | [[Fluxo_de_Caixa]] | Livro-caixa, saldo em conta (R$ 50,10), compras e lucros realizados |
| **🏆 Matriz de Campeões & Giro** | [[Matriz_Produtos_Campeoes]] | Classificação de produtos estrelas, foguetes e tartarugas |
| **🚀 Estratégia WhatsApp & Afiliados** | [[Estrategia_WhatsApp_Afiliados]] | **Plano do Grupo VIP, mensagens prontas e comissões Indique & Ganhe** |
| **📱 Guia de Celulares & Anti-Golpe** | [[Guia_Garimpo_iPhones_Celulares]] | Tabela de preços de iPhones para revenda e regras de segurança |
| **📦 1. Radar & Pedidos** | [[00_Radar_Compras/]] | 3x Máquinas T9 (Ali) + Kit 10 Potes Herméticos 640ml (ML Full) |
| **🛠️ 2. Estoque em Mãos** | [[01_Estoque_Pronto/]] | Produtos conferidos, fotos reais tiradas, prontos para subir |
| **📢 3. No Ar (Marketplace)**| [[02_Briques_Ativos/]] | Jogo de Chaves 12 Pçs + 2x Fones de Capacete V10 |
| **🔁 4. Alerta de Repostagem**| [[03_Para_Repostar/]] | Anúncios que bateram 7 dias e precisam de renovação |
| **🏆 5. Caixa & Lucro** | [[04_Vendidos_Lucro/]] | HD 60GB Xbox + 1x Fone V10 |
| **👥 6. Carteira de Clientes**| [[05_Clientes_CRM/Painel_Clientes_CRM\|05_Clientes_CRM/]] | Tomas (R$ 120 hoje), Samuel (Parceiro), Tia, Mauricio, Adriano |

---

## 🤖 4. Cronômetro Automático de Dias no Ar & Vendas (Dataview)

### 📢 Briques Ativos: Cronômetro de Dias no Ar (Atualiza Sozinho Todo Dia!)
```dataview
TABLE 
  categoria AS "Categoria", 
  preco_anuncio_fb AS "Preço Anúncio", 
  data_anuncio AS "Data Postado",
  (date(today) - date(data_anuncio)).days + " dias" AS "Tempo no Ar",
  choice((date(today) - date(data_anuncio)).days >= 7, "🔴 REPOSTAR!", choice((date(today) - date(data_anuncio)).days >= 4, "🟡 Atenção", "🟢 Recente")) AS "Termômetro"
FROM "02_Briques_Ativos"
SORT data_anuncio ASC
```

### 🏆 Vendas Concluídas: Cronômetro de Giro (Tempo Congelado na Venda!)
```dataview
TABLE 
  data_venda AS "Data Venda", 
  preco_venda_final AS "Venda (R$)", 
  lucro_realizado AS "Lucro Limpo", 
  (date(data_venda) - date(data_anuncio)).days + " dias" AS "Tempo p/ Vender (Giro)",
  comprador AS "Cliente"
FROM "04_Vendidos_Lucro"
SORT data_venda DESC
```

### 📦 Mercadorias no Radar (Aguardando Entrega)
```dataview
TABLE 
  origem_compra AS "Origem", 
  custo_total AS "Custo Pago", 
  preco_anuncio_fb AS "Preço Previsto", 
  lucro_estimado AS "Lucro Estimado",
  data_compra AS "Data Pedido"
FROM "00_Radar_Compras"
SORT data_compra DESC
```
