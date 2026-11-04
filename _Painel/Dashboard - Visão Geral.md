# 📊 Painel de Controle - Operação de Briques & Marketplace

Bem-vindo ao seu QG de compra e venda! Este painel centraliza todo o fluxo: da busca de cupons até o dinheiro no bolso.

---

## 🧭 Atalhos das Etapas do Negócio

| Etapa | Pasta / Painel | Objetivo |
| :--- | :--- | :--- |
| **💰 Gestão Financeira** | [[Fluxo_de_Caixa]] | **Livro-caixa, saldo, valor investido e lucro** |
| **1. Radar & Pedidos** | [[00_Radar_Compras/]] | Itens comprados com cupom aguardando entrega |
| **2. Estoque em Mãos** | [[01_Estoque_Pronto/]] | Produtos conferidos, fotos tiradas, prontos para subir |
| **3. No Ar (Marketplace)** | [[02_Briques_Ativos/]] | Anúncios ativos rodando no Facebook |
| **4. Alerta de Repostagem** | [[03_Para_Repostar/]] | Anúncios com mais de 7 dias que perderam alcance |
| **5. Caixa & Lucro** | [[04_Vendidos_Lucro/]] | Vendas concluídas com ROI registrado |
| **6. Carteira de Clientes** | [[05_Clientes_CRM/]] | Contatos quentes para recompra |

---

## 📈 Resumo Rápido da Operação

> [!TIP] **Dica para o Obsidian:**
> Se você instalar o plugin comunitário **Dataview** no Obsidian, as tabelas abaixo atualizarão automaticamente com base nas tags e propriedades das notas!

### ⏳ Briques Ativos no Marketplace
```dataview
TABLE status, categoria, custo_total AS "Custo", preco_anuncio_fb AS "Anunciado", lucro_estimado AS "Lucro Est."
FROM "02_Briques_Ativos"
SORT data_anuncio DESC
```

### 🔁 Briques Precisando de Repostagem (Atenção!)
```dataview
TABLE data_anuncio AS "Data Postado", preco_anuncio_fb AS "Preço Atual", preco_minimo_aceitavel AS "Preço Piso"
FROM "03_Para_Repostar"
SORT data_anuncio ASC
```

### 💰 Últimas Vendas Fechadas (Lucro Realizado)
```dataview
TABLE data_venda AS "Data", preco_venda_final AS "Venda (R$)", lucro_realizado AS "Lucro Líquido (R$)", forma_pagamento AS "Pagamento"
FROM "04_Vendidos_Lucro"
SORT data_venda DESC
```

---

## 🧠 Princípios de Ouro da Arbitragem no Marketplace

1. **O Lucro está na Compra:** Quanto maior o desconto no cupom/promoção, maior a sua margem de manobra para fechar rápido sem risco.
2. **Foto Real Vende 5x Mais:** Nunca use apenas fotos de catálogo da internet. Tire foto da caixa na sua mão ou em cima de uma mesa limpa. Isso prova que você tem o produto físico em mãos.
3. **Não Brigue com o Pechincheiro:** Embuta a margem de choro no preço inicial. O cliente só quer a sensação psicológica de vitória.
4. **Renovação Constante:** O Facebook entrega muito tráfego nos primeiros 3 a 5 dias. Depois disso, o alcance despenca. Quando bater 7 dias sem venda, apague o anúncio e recrie.
5. **Giro é Rei:** Mais vale ganhar R$ 30,00 em 2 dias e girar o dinheiro de novo do que segurar o produto 2 meses tentando ganhar R$ 50,00.

