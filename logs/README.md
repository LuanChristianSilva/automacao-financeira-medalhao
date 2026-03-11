# Logs do Pipeline em Formato Power BI

Para leitura eficiente no Power BI, os logs devem ser gerados em **CSV** (UTF-8), com **schema fixo** e colunas padronizadas entre todos os scripts.

## Estratégia adotada

- **1 arquivo CSV por script** (mantém separação por etapa):
  - `logs/extractor_log.csv`
  - `logs/silver_transform_log.csv`
  - `logs/gold_load_log.csv`
  - `logs/validate_results_log.csv`
- Todos os CSVs usam o **mesmo cabeçalho** para facilitar `Append` no Power BI.
- Cada linha representa um **evento de execução** (início, métrica, saída, erro, fim).

## Schema padrão (colunas)

| Coluna | Tipo sugerido no Power BI | Descrição |
|---|---|---|
| `log_id` | Texto | Identificador único da linha de log. |
| `run_id` | Texto | Identificador da execução completa (correlação). |
| `event_ts` | DateTime | Data/hora do evento (ISO-8601). |
| `stage` | Texto | Bronze / Silver / Gold / Validation. |
| `script_name` | Texto | Nome do script emissor do log. |
| `status` | Texto | STARTED / SUCCESS / WARNING / ERROR / FINISHED. |
| `severity` | Texto | INFO / WARN / ERROR. |
| `environment` | Texto | local / ci. |
| `branch` | Texto | Branch Git da execução. |
| `commit_sha` | Texto | Commit relacionado à execução. |
| `input_path` | Texto | Arquivo de entrada relacionado ao evento. |
| `output_path` | Texto | Arquivo de saída relacionado ao evento. |
| `entity_name` | Texto | Entidade da métrica (aba, tabela, arquivo, regra). |
| `metric_name` | Texto | Nome da métrica (ex.: `rows_extracted`). |
| `metric_value` | Decimal | Valor da métrica. |
| `metric_unit` | Texto | Unidade da métrica (rows, files, ms, etc.). |
| `row_count` | Número inteiro | Quantidade de linhas associada ao evento. |
| `error_code` | Texto | Código de erro (quando aplicável). |
| `error_message` | Texto | Mensagem de erro (quando aplicável). |
| `action_taken` | Texto | Ação corretiva executada (quando aplicável). |
| `duration_ms` | Número inteiro | Duração do passo/evento em milissegundos. |
| `notes` | Texto | Observações adicionais. |

## Regras para garantir compatibilidade com Power BI

1. Salvar em **UTF-8**.
2. Usar **separador vírgula** e manter cabeçalho idêntico em todos os arquivos.
3. Registrar `event_ts` em formato ISO (`YYYY-MM-DDTHH:MM:SS`).
4. Não mudar nomes de colunas sem versionamento do schema.
5. Evitar campos livres com quebra de linha.

## Sugestão de modelagem no Power BI

- Importar os 4 CSVs e aplicar **Append Queries** para tabela única `f_pipeline_logs`.
- Criar dimensões derivadas:
  - `d_stage` (stage)
  - `d_status` (status/severity)
  - `d_script` (script_name)
- Métricas comuns:
  - total de erros por stage
  - duração média por script
  - volume de linhas processadas por execução (`run_id`)


## Publicação dos arquivos Markdown

Os templates em Markdown também estão publicados para uso operacional/manual:

- `logs/extractor_log.md`
- `logs/silver_transform_log.md`
- `logs/gold_load_log.md`
- `logs/validate_results_log.md`

> Esses arquivos `.md` funcionam como runbook e apoio ao preenchimento. Para o Power BI, a fonte recomendada continua sendo os `.csv` com schema fixo.
