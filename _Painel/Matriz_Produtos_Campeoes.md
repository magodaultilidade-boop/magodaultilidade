# 🏆 Matriz de Desempenho: Campeões de Venda & Giro de Briques

> **O Radar da Verdade:** Este painel classifica automaticamente cada categoria e produto que passa pela sua mão, separando o ouro da perda de tempo. Usado nas maiores redes de varejo do mundo (Metodologia da **Matriz BCG de Produtos** adaptada para Brique Físico).

---

## 🎯 1. Classificação Estratégica dos Produtos

```
              ALTA VELOCIDADE DE GIRO (Vende em até 5 dias)
                             ▲
                             │
     ⭐ PRODUTOS ESTRELA     │     🚀 PRODUTOS FOGUETE
   (Alto Lucro + Vende Rápido)│   (Lucro Médio + Vende Que Nem Água)
   - Ex: Fone Moto V10       │   - Ex: Cabos, Pilhas, Adaptadores
   ➔ AÇÃO: COMPRAR DE LOTE!  │   ➔ AÇÃO: MANTENHA SEMPRE EM MÃOS!
                             │
─────────────────────────────┼─────────────────────────────► MARGEM DE LUCRO
                             │                               (Acima de 70%)
     🐢 PRODUTOS TARTARUGA   │     💣 PRODUTOS ÂNCORA
   (Baixo Lucro + Demora)    │   (Alto Lucro, mas Giro Lento)
   - Ex: Tranqueiras velhas  │   - Ex: Jogo de Chaves, Ferramentas
   ➔ AÇÃO: NUNCA MAIS COMPRE!│   ➔ AÇÃO: ANCORAR PREÇO E NÃO REPETIR
                             │
              BAIXA VELOCIDADE DE GIRO (Mais de 10 dias parado)
```

---

## 🏅 2. O Ranking dos Campeões (Atualizado em Tempo Real)

### 🥇 1º Escalão: Os Campeões de Velocidade (Venda em < 72h)
| Produto | Categoria | Dias p/ Vender | Margem Real | Status / Veredito |
| :--- | :--- | :--- | :--- | :--- |
| **HD 60GB Xbox 360 Fat** | Games | **2,0 dias** ⚡ | **100,0%** (R$ 70 Pix) | 🏆 **Estrela:** Nicho com comprador faminto em Itu |
| **Fone Capacete Moto V10** | Acessórios Moto | **3,0 dias** ⚡ | **107,1%** (R$ 31 Pix) | 🏆 **Estrela:** Vende no WhatsApp sem taxa |

---

### ⏳ 2º Escalão: Em Teste de Tração (Aguardando Giro)
| Produto | Categoria | Custo Unitário | Lucro Projetado | Dias Anunciado / Previsão |
| :--- | :--- | :--- | :--- | :--- |
| **Kit 10 Potes de Vidro Herméticos** | Casa / Cozinha | R$ 9,38 (R$ 93,83) | + R$ 56,07 | *Chega amanhã (Forte apelo p/ família)* |
| **3x Máquinas T9 Vintage Buda** | Beleza / Cuidados | R$ 9,16 (R$ 27,49) | + R$ 92,21 (+335%) | *Chegando do Ali (Margem absurda)* |
| **2x Fones Moto V10 (Restantes)** | Acessórios Moto | R$ 28,97 | + R$ 61,86 | *Em estoque / Venda direta* |

---

### 🐢 3º Escalão: Produtos Âncora (Alerta de Giro Lento > 5 dias)
| Produto | Categoria | Custo | Preço Anúncio | Dias Ativo | Estratégia de Desova |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Jogo de Chave 12 Pçs The Black Tools** | Ferramentas | R$ 66,89 | R$ 119,90 | **5 dias** | Se não fechar até sábado, baixar para **R$ 90 no Pix** para resgatar o capital e não travar o caixa! |

---

## 📊 3. Análise por Categoria (Onde o Dinheiro Entra Mais Rápido)

```dataview
TABLE 
  rows.produto AS "Briques",
  length(rows) AS "Qtd Itens",
  sum(rows.lucro_realizado) AS "Lucro Realizado",
  sum(rows.lucro_estimado) AS "Lucro Potencial"
FROM "00_Radar_Compras" OR "01_Estoque_Pronto" OR "02_Briques_Ativos" OR "04_Vendidos_Lucro"
GROUP BY categoria
```

---

## 🧠 As 4 Leis da Matriz de Decisão de Compra:

1. **A Lei da Repetição:** Se um produto vendeu em menos de 5 dias com mais de 70% de margem, **repita a compra imediatamente** com o dobro de unidades.
2. **A Lei da Queima Sem Dó:** Se um produto passar de 14 dias sem vender, queime a preço de custo (ou com lucro de R$ 10). **Dinheiro parado é prejuízo escondido.**
3. **A Regra dos 3 Campeões:** Quando você identificar **3 produtos** que vendem sozinhos no seu WhatsApp (ex: Fone Moto, Teclado Gamer, Potes), 80% do seu caixa deve ir para eles.
4. **O Teste Controlado:** Nunca gaste mais de 30% do seu caixa total em uma categoria que você nunca testou antes.

