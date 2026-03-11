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