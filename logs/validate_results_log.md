# Log de Execução — `validate_results.py` (Validação)

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

### 2) Checagens de Arquivos

| Checagem | Resultado | Observações |
|---|---|---|
| `Dados/2_Silver/fato_renda.parquet` existe | Sim/Não | `<detalhe>` |
| `Dados/2_Silver/fato_despesa.parquet` existe | Sim/Não | `<detalhe>` |
| Pasta `Dados/1_Bronze` acessível | Sim/Não | `<detalhe>` |

### 3) Métricas de Validação

| Tabela/Arquivo | Total de registros | Colunas esperadas | Status |
|---|---:|---|---|
| `fato_renda.parquet` | `<n>` | `<lista>` | `<ok/erro>` |
| `fato_despesa.parquet` | `<n>` | `<lista>` | `<ok/erro>` |
| `consolidado_renda.csv` (amostra) | `<n>` | `<lista>` | `<ok/erro>` |
| `consolidado_despesa.csv` (amostra) | `<n>` | `<lista>` | `<ok/erro>` |

### 4) Inconsistências Encontradas

| Tipo | Evidência | Impacto | Recomendação |
|---|---|---|---|
| `<inconsistência>` | `<detalhe>` | `<alto/médio/baixo>` | `<ação>` |

### 5) Parecer Final

| Critério | Resultado |
|---|---|
| Pipeline apto para seguir para Gold | Sim/Não |
| Necessita intervenção manual | Sim/Não |
| Prioridade de correção | Alta/Média/Baixa |

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
