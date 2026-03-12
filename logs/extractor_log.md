# Log de Execução — `extractor.py` (Bronze)

## Status de Publicação

- Publicado no repositório: **Sim**
- Formato: **Markdown (template operacional)**
- Integração BI: complementar aos arquivos `.csv` da mesma etapa


## Execução: <YYYY-MM-DD HH:MM:SS>

### 1) Identificação da Execução

| Campo | Valor |
|---|---|
| Status | ✅ SUCESSO / ⚠️ ALERTA / ❌ FALHA |
| Executor | Local / CI |
| Branch | `<branch>` |
| Commit | `<sha>` |
| Duração | `<hh:mm:ss>` |
| Arquivo de entrada | `<path do Excel>` |

### 2) Leitura e Varredura de Abas

| Métrica | Valor |
|---|---|
| Total de abas no Excel | `<n>` |
| Abas elegíveis (Jan-Dez) | `<n>` |
| Abas ignoradas (`Viagem*`) | `<n>` |
| Abas com erro de leitura | `<n>` |

| Aba | Renda encontrada | Despesa encontrada | Observações |
|---|---|---|---|
| `<Jan2026>` | Sim/Não | Sim/Não | `<ex.: stop condition por Total de Renda>` |
| `<Fev2026>` | Sim/Não | Sim/Não | `<...>` |

### 3) Extração e Regras Aplicadas

| Regra | Resultado |
|---|---|
| `START_KEYWORD` renda localizada | Sim/Não |
| `STOP_CONDITION` renda acionada por "Total de Renda" | Sim/Não |
| `STOP_CONDITION` renda por 2 linhas vazias | Sim/Não |
| Stop de despesa por "valor em atraso do mes anterior" | Sim/Não |

### 4) Saídas da Camada Bronze

| Arquivo de saída | Gerado | Registros |
|---|---|---|
| `Dados/1_Bronze/consolidado_renda.csv` | Sim/Não | `<n>` |
| `Dados/1_Bronze/consolidado_despesa.csv` | Sim/Não | `<n>` |

### 5) Erros e Ações Corretivas

| Tipo | Descrição | Ação tomada | Próximo passo |
|---|---|---|---|
| `<erro/alerta>` | `<detalhe>` | `<ação>` | `<item>` |

---

## Dicionário de Dados das Colunas (Exportação para Power BI)

A execução deste script gera (ou incrementa) um arquivo `.csv` correspondente. Abaixo está o detalhamento de cada coluna enviada ao Power BI:

| Coluna | Descrição |
|---|---|
| `log_id` | Identificador único (UUID) específico desta linha de log. |
| `run_id` | Identificador único (UUID) compartilhado por todos os logs de uma mesma execução do script. |
| `event_ts` | Timestamp do momento exato do evento, no formato ISO-8601 UTC. |
| `stage` | Indica a camada atual do pipeline (Bronze, Silver, Gold, Validation). |
| `script_name` | O nome do script Python que gerou o log (ex: `extractor.py`). |
| `status` | Situação do evento gerado (STARTED, SUCCESS, WARNING, ERROR, FINISHED). |
| `severity` | Nível de criticidade da linha de log (INFO, WARN, ERROR). |
| `environment` | Ambiente onde o script foi rodado (`local` ou `ci`). |
| `branch` | Nome da branch atual do Git no momento da execução. |
| `commit_sha` | Hash curto (SHA) do commit do Git ativo na execução. |
| `input_path` | Caminho do diretório/arquivo consumido pela etapa. |
| `output_path` | Caminho do diretório/arquivo gerado pela etapa. |
| `entity_name` | O nome do bloco de dados referenciado pela métrica (ex: "Excel Tabs", "Silver Renda"). |
| `metric_name` | O nome da variável aferida (ex: `total_tabs`, `rows_extracted_renda`, `rows_transformed`). |
| `metric_value` | O valor numérico ou quantitativo aferido para aquela métrica. |
| `metric_unit` | Unidade de contagem (ex: `count`, `rows`, `files`). |
| `row_count` | O número exato de linhas processadas e salvas naquela entidade de dados. |
| `error_code` | Código mapeado de erro do sistema (quando houver falhas). |
| `error_message` | Retorno textual completo da Exception ou do erro (`str(e)`). |
| `action_taken` | Medida de mitigação ou status de ação caso o erro não seja fatal. |
| `duration_ms` | Tempo percorrido desde o STARTED até este passo (em milissegundos). Presente no evento FINISHED. |
| `notes` | Anotações adicionais e descritivos abertos do evento. |
