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