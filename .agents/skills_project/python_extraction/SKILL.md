# Estrutura da Automação: Consolidador de Dados Financeiros (v3 - Modular)

## 1. Camada de Configuração (Maintenance Layer)
Para facilitar a manutenção e o uso em novos arquivos, todos os parâmetros serão centralizados em variáveis globais ou um dicionário de configuração:

* **ARQUIVO_PATH**: `C:\Users\luanc\OneDrive\Controles_Luan\Mensal.xlsx`
* **PADRAO_ABAS**: Meses do ano (Jan, Fev, ..., Dez) + Ano.
* **CONFIG_RENDA**:
    * `START_KEYWORD`: "Renda Mensal"
    * `STOP_CONDITION`: "Encontrar 'Total de Renda' OU 2 linhas vazias consecutivas" 
    * `COL_RANGE`: "B:D"
* **CONFIG_DESPESA**:
    * `START_KEYWORD`: "Despesa Mensal"
    * `STOP_CONDITION`: "Encontrar 'Valor em atraso do mes anterior'"
    * `COL_RANGE`: "B:I"

## 2. Fluxo de Execução Modular

### A. Módulo de Varredura
O script inicia listando todas as abas e comparando com o `PADRAO_ABAS`. Abas que não dão "match" são descartadas imediatamente. Também aplica filtros personalizados (ex: ignorar abas que começam com "Viagem").

### B. Módulo de Extração (Função Genérica)
Criaremos uma função que recebe os parâmetros de configuração e a aba atual.
1.  **Localização**: Localiza a célula (linha/coluna) da `START_KEYWORD`.
2.  **Delimitação**: 
    * Para **Renda**: Lê até a `END_KEYWORD`.
    * Para **Despesa**: Consulta o metadado `auto_filter.ref` da aba para definir o corte final exato.
3.  **Identificação**: Adiciona a coluna `Origem_Aba` com o nome da aba processada.

### C. Módulo de Limpeza e Tipagem
* Conversão de valores para tipos numéricos.
* Remoção de linhas completamente em branco.
* Tratamento de strings (`strip`) para evitar erros em filtros futuros.

### D. Módulo de Consolidação (Output)
* Agrupa todos os blocos extraídos em DataFrames únicos.
* **Exportação**: Gera arquivos CSV na camada **Bronze** usando codificação `utf-8-sig`.

## 3. Estrutura Medalhão (Governance Layer)
A organização dos dados segue o padrão medalhão para garantir a qualidade:

### 🥉 [1_Bronze] - Camada Raw (Bruta)
* **O que faz**: Armazena os dados exatamente como foram extraídos da fonte, sem nenhuma alteração no conteúdo.
* **Objetivo**: Funcionar como um backup histórico e permitir o reprocessamento total caso as regras de negócio mudem.
* **Arquivos**: `consolidado_renda.csv` e `consolidado_despesa.csv`.

### 🥈 [2_Silver] - Camada de Limpeza & Padronização
* **O que faz**: Aplica tratativas de deduplicação, normalização de nomes de categorias, correção de datas e padronização de formatos.
* **Objetivo**: Fornecer uma "fonte única da verdade" com dados confiáveis e prontos para análise técnica.

### 🥇 [3_Gold] - Camada de Negócio
* **O que faz**: Contém tabelas agregadas, cálculos de indicadores (KPIs) e visões otimizadas para ferramentas de BI.
* **Novidade (v6.0)**: Implementação de **Consultoria Ativa**, fornecendo alertas de saúde financeira e gestão real de parcelamentos (identificando meses restantes e progresso individual de dívidas).
* **Objetivo**: Facilitar a criação de dashboards dinâmicos e a tomada de decisão rápida baseada em dados reais e não apenas estimativas.

## 4. Benefícios desta Estrutura
- **Escalabilidade**: Fácil adaptação para novos anos ou arquivos.
- **Segurança**: A camada Bronze protege a integridade dos dados originais.
- **Manutenibilidade**: Configuração centralizada permite ajustes rápidos sem alterar a lógica principal.