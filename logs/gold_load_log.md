# Log de Execução — `gold_load.py` (Gold)

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

### 2) Entradas da Silver

| Arquivo de entrada | Encontrado | Registros |
|---|---|---|
| `Dados/2_Silver/fato_renda.parquet` | Sim/Não | `<n>` |
| `Dados/2_Silver/fato_despesa.parquet` | Sim/Não | `<n>` |

### 3) Agregações e Regras de Negócio

| Visão | Regra aplicada | Resultado |
|---|---|---|
| Resumo mensal | `Total_Renda`, `Total_Despesa`, `Saldo` | `<ok/erro>` |
| Detalhado despesa | Exclusão de `Status = Cancelado` | `<ok/erro>` |
| Detalhado renda | Ordenação por `Data_Referencia DESC` | `<ok/erro>` |

### 4) Saídas da Gold

| Arquivo de saída | Gerado | Registros finais |
|---|---|---|
| `Dados/3_Gold/resumo_mensal.json` | Sim/Não | `<n>` |
| `Dados/3_Gold/detalhado_despesa.json` | Sim/Não | `<n>` |
| `Dados/3_Gold/detalhado_renda.json` | Sim/Não | `<n>` |

### 5) Erros e Ações Corretivas

| Tipo | Descrição | Ação tomada | Próximo passo |
|---|---|---|---|
| `<erro/alerta>` | `<detalhe>` | `<ação>` | `<item>` |

---