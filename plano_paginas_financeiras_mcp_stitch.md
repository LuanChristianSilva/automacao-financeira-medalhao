# Plano de implementação — novas páginas de indicadores acionáveis

## Objetivo
Criar novas páginas no dashboard financeiro com foco em indicadores orientados à ação, usando uma sequência controlada de trabalho:

1. Estruturar as páginas via MCP Stitch
2. Definir e refinar as telas
3. Preparar os dados necessários
4. Integrar os dados nas interfaces

**Importante:** este plano não contém código. Ele define a execução, os critérios e as entregas de cada etapa.

---

## Escopo das páginas

### Página 1 — Indicadores de ação financeira
Esta página deve concentrar os indicadores com foco em decisão imediata:

1. **Receita Disponível para Gastar**
2. **Dias que o dinheiro precisa durar**
3. **Alerta de estouro de orçamento**
4. **Despesa que mais cresceu**
5. **Impacto das dívidas**
6. **Tempo para quitar dívida**
7. **Risco de saldo negativo**
8. **Top 3 gastos do mês**

### Página 2 — Meta de poupança
**Status: 🛑 Suspensa Temporariamente (Código Preservado)**
Esta página está estruturada mas desativada via UI (Shield de Bloqueio) para priorizar a correção de lógica da Página 1.

---

## Princípios de construção

- Priorizar indicadores acionáveis, não apenas descritivos.
- Garantir leitura simples e executiva.
- Manter consistência visual com o dashboard atual.
- Trabalhar responsividade desde a definição da tela, não apenas no final.
- Separar claramente regra de negócio, preparação dos dados e camada visual.
- Evitar criar componentes dependentes de dados não definidos.
- Validar cada etapa antes de avançar para a próxima.

---

## Etapa 1 — Criar as páginas via MCP Stitch

### Objetivo da etapa
Criar a estrutura base das novas páginas no fluxo/projeto, definindo navegação, organização e intenção de cada tela.

### O que será feito
- Criar uma página para **Indicadores de ação financeira**.
- Criar uma página separada para **Meta de poupança**.
- Definir nomes, títulos e posicionamento dessas páginas dentro da navegação do produto.
- Garantir que a arquitetura da informação faça sentido com o restante do dashboard.
- Definir se essas páginas entram como item de menu principal, submenu ou agrupamento temático.
- Planejar a navegação entre visão geral financeira e páginas analíticas.

### Entregáveis da etapa
- Estrutura das páginas criada no projeto.
- Navegação prevista e coerente.
- Organização macro aprovada antes do desenho detalhado.

### Boas práticas da etapa
- Usar nomes claros e orientados ao negócio.
- Evitar páginas com títulos genéricos demais.
- Garantir separação lógica entre indicadores operacionais e meta de poupança.
- Pensar desde já na escalabilidade para páginas futuras.

### Critério de conclusão
A etapa termina quando as duas páginas estiverem formalmente definidas no projeto, com navegação e propósito claros.

---

## Etapa 2 — Desenhar a tela de cada página

### Objetivo da etapa
Transformar cada página em uma experiência visual clara, executiva e orientada à ação.

### O que será feito na Página 1 — Indicadores de ação financeira
Definir a melhor organização visual para os seguintes indicadores:

- Receita Disponível para Gastar
- Dias que o dinheiro precisa durar
- Alerta de estouro de orçamento
- Despesa que mais cresceu
- Impacto das dívidas
- Tempo para quitar dívida
- Risco de saldo negativo
- Top 3 gastos do mês

### O que será feito na Página 2 — Meta de poupança
Definir uma página dedicada ao acompanhamento da meta, contendo:

- status da meta atual
- percentual atingido
- valor acumulado
- valor necessário para atingir a meta
- ritmo necessário até o fim do período
- projeção de atingimento
- alertas de atraso ou avanço

### Diretrizes de UX/UI
- Organizar os elementos por prioridade de decisão.
- Colocar os indicadores mais urgentes no topo.
- Dar destaque para alertas e riscos.
- Usar linguagem visual que responda “o que fazer agora”.
- Evitar excesso de gráficos decorativos.
- Priorizar cards, barras comparativas, alertas e ranking quando fizer mais sentido que charts complexos.
- Garantir leitura rápida em desktop e adaptação consistente em telas menores.
- Prever estados de: carregando, sem dados, erro e dados parciais.

### O que precisa ser decidido nessa etapa
- Quais indicadores serão KPI cards.
- Quais terão detalhe expandido ou bloco explicativo.
- Quais precisam de comparação temporal.
- Quais precisam de sinalização semântica de risco, atenção ou saudável.
- Como será a hierarquia entre resumo e detalhe.

### Entregáveis da etapa
- Estrutura visual definida para as duas páginas.
- Hierarquia dos componentes validada.
- Distribuição dos indicadores aprovada.
- Critérios de responsividade previstos.

### Boas práticas da etapa
- Não desenhar componente sem propósito decisório.
- Não misturar visual executivo com excesso de informação operacional.
- Não depender de textos longos para explicar o indicador.
- Garantir consistência com o design system atual.
- Preservar espaçamentos, contraste e legibilidade.

### Critério de conclusão
A etapa termina quando o layout de cada página estiver decidido e pronto para receber dados reais.

---

## Etapa 3 — Preparar os dados

### Objetivo da etapa
Definir, organizar e disponibilizar os dados necessários para alimentar cada indicador com regras consistentes.

### O que será feito
- Mapear a origem dos dados necessários para cada indicador.
- Definir regras de cálculo, filtros e granularidade.
- Identificar dependências entre receitas, despesas, dívidas, orçamento e poupança.
- Criar o dicionário de métricas e validar a lógica com o objetivo de negócio.
- Garantir que os indicadores possam ser reproduzidos de forma confiável.

### Indicadores e o que precisam considerar

#### Receita Disponível para Gastar
- receita do período
- despesas fixas
- compromissos obrigatórios
- dívidas previstas
- eventuais reservas já separadas

#### Dias que o dinheiro precisa durar
- saldo disponível atual
- dias restantes do período
- regra para divisão diária

#### Alerta de estouro de orçamento
- orçamento por categoria
- realizado da categoria
- limite percentual de alerta
- severidade do estouro

#### Despesa que mais cresceu
- comparação com período anterior
- variação absoluta e percentual
- regra para ignorar ruído de categorias irrelevantes

#### Impacto das dívidas
- valor total de dívidas
- peso da dívida sobre a renda
- comprometimento mensal

#### Tempo para quitar dívida
- saldo devedor
- pagamento médio mensal
- simulação simples de quitação
- regra para cenário sem amortização suficiente

#### Risco de saldo negativo
- projeção do fechamento do período
- entradas previstas
- saídas previstas
- saldo projetado final

#### Top 3 gastos do mês
- ranking de despesas do período
- agrupamento por categoria ou natureza
- critério de desempate e ordenação

#### Meta de poupança
- valor alvo
- valor acumulado
- percentual atingido
- necessidade restante
- prazo da meta
- ritmo esperado vs ritmo atual

### Boas práticas da etapa
- Documentar definição de cada métrica.
- Evitar cálculos ambíguos na camada visual.
- Tratar nulos, períodos sem movimentação e categorias inconsistentes.
- Garantir comparabilidade temporal.
- Separar claramente dado bruto, dado tratado e indicador final.
- Validar nomes semânticos e fáceis de manter.

### Entregáveis da etapa
- Lista de fontes e campos necessários.
- Definição de regra de negócio de cada indicador.
- Estrutura de dados pronta para consumo da interface.
- Mapeamento de exceções e estados sem dados.

### Critério de conclusão
A etapa termina quando cada indicador tiver sua regra definida, seus dados preparados e sua saída esperada documentada.

---

## Etapa 4 — Usar os dados na tela

### Objetivo da etapa
Conectar a camada visual aos dados preparados e garantir que cada componente exiba informação confiável, clara e útil.

### O que será feito
- Ligar cada card, ranking, alerta ou bloco analítico ao dado tratado correspondente.
- Garantir que os valores exibidos respeitem o período selecionado.
- Exibir corretamente estados positivos, neutros e negativos.
- Validar formatação monetária, percentual e textual.
- Ajustar textos de apoio para traduzir o dado em ação.
- Garantir consistência entre valor principal, subtítulo e comparação.

### Pontos de validação
- O dado mostrado corresponde à regra definida.
- O período do filtro impacta corretamente a página.
- A responsividade preserva leitura e hierarquia.
- Os alertas aparecem apenas quando fizer sentido.
- Componentes não quebram quando houver ausência parcial de dados.
- O usuário consegue entender rapidamente o que precisa fazer.

### Estados que devem existir
- carregando
- sem dados
- erro
- dado incompleto
- valor zerado
- valor negativo quando aplicável

### Boas práticas da etapa
- Não deixar a interpretação do indicador dependente apenas da cor.
- Não usar visual bonito com regra errada.
- Não misturar dado calculado em tempo real sem controle com dado já tratado.
- Garantir consistência entre todos os componentes da página.

### Entregáveis da etapa
- Páginas alimentadas com dados reais.
- Indicadores funcionando com filtros e regras corretas.
- Interface final pronta para revisão funcional.

### Critério de conclusão
A etapa termina quando a tela estiver usando dados reais de forma consistente, responsiva e validada.
**Status Página 1: ✅ Concluído (Refinado na v7.0 com nova lógica de cartão).**
**Status Página 2: ⏸️ Pausado (Aguardando retomada do roadmap).**

---

## Ordem recomendada de execução

1. Criar páginas no MCP Stitch
2. Definir layout e hierarquia visual
3. Preparar e validar dados
4. Integrar dados na interface
5. Revisar comportamento responsivo
6. Revisar semântica dos textos e sinais de alerta
7. Homologar regras e consistência visual

---

## Checklist de qualidade final

- As páginas estão separadas corretamente.
- Cada indicador responde a uma ação prática.
- A tela está clara sem depender de explicação externa.
- Os dados batem com as regras de negócio.
- O layout continua consistente com o dashboard atual.
- A navegação está coerente.
- A responsividade está resolvida.
- Estados de ausência de dados foram considerados.
- Meta de poupança ficou isolada em página própria.

---

## Resultado esperado
Ao final, o produto deve ter:

- uma página de **indicadores financeiros acionáveis**, voltada para decisão imediata;
- uma página separada de **meta de poupança**, voltada para acompanhamento e projeção;
- fluxo de construção organizado;
- separação limpa entre arquitetura, design, dados e integração;
- base pronta para evoluções futuras com mais métricas e análises.

## 📝 Notas de Versão (v7.0)
- **Refinamento Crítico**: O indicador "Impacto das Dívidas" foi renomeado para "Uso do Cartão de Crédito" e sua fórmula foi corrigida para refletir o comprometimento real da renda.
- **Segurança**: Adicionado shield de redirecionamento na `poupanca.html` para evitar acesso a funcionalidades incompletas na versão online.

