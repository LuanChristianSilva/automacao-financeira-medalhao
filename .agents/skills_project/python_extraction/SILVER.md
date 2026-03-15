# Estrutura da Automação: Camada Silver (Refinamento via SQL)

Este documento detalha a lógica de transformação dos dados da **Bronze** para a **Silver** utilizando **Python + DuckDB** para manipulação via SQL.

## 1. Objetivo
Refinar os dados brutos, aplicando regras de negócio, tipagem estrita e limpeza de ruídos (linhas de totalizadores e nulos), entregando tabelas prontas para consumo analítico.

## 2. Tecnologias e Caminhos
- **Engine:** `duckdb` (SQL Engine in-process)
- **Origem (Bronze):** `.../1_Bronze/consolidado_{tabela}.csv`
- **Destino (Silver):** `.../2_Silver/fato_{tabela}.parquet` (ou .csv)

## 3. Variáveis de Manutenção (Config)
Para manter o código limpo, os nomes das tabelas e termos de exclusão ficam em variáveis:
- `TERMO_EXCLUSAO`: '%Total%'
- `COLUNAS_DESPESA_FINAL`: Nome, Valor, Status, Credor, Tipo_Pagamento, Data_Referencia, Origem_Aba

## 4. Lógica de Transformação SQL

### A. Tabela de Rendas (Silver)
A transformação deve unificar os nomes das colunas e garantir que o valor seja numérico.

```sql
SELECT 
    Origem_Aba,
    TRIM("Renda Mensal") AS Item,
    -- Otimização: Coalesce para tratar nulos
    COALESCE(
        TRY_CAST(REPLACE(CAST(Real AS VARCHAR), ',', '.') AS DECIMAL(18,2)),
        0
    ) AS Valor,
    -- Data de Competência: Criada para cálculos de BI (Ex: 'Mar2026' -> '2026-03-01')
    CAST(
        RIGHT(TRIM(Origem_Aba), 4) || '-' || 
        CASE 
            WHEN TRIM(Origem_Aba) LIKE 'Jan%' THEN '01'
            WHEN TRIM(Origem_Aba) LIKE 'Fev%' THEN '02'
            -- ... (mapeamento de todos os meses PT-BR)
            ELSE '01' 
        END || '-01' AS DATE
    ) AS Data_Competencia,
    TRY_CAST("Mes Ano Renda" AS DATE) AS Data_Referencia,
    UPPER(LEFT(TRIM(Origem_Aba), 3)) AS Mes_Sigla,
    RIGHT(TRIM(Origem_Aba), 4) AS Ano
FROM bronze_renda
WHERE "Renda Mensal" NOT ILIKE '%Total%' 
  AND "Renda Mensal" NOT IN ('Renda Mensal', 'Despesa Mensal', 'Origem')
  AND Real IS NOT NULL

  ----

  ### B. Tabela de Despesas (Silver)

```sql
SELECT 
    Origem_Aba,
    TRIM("Despesa Mensal") AS Item,
    -- Otimização: Coalesce para priorizar Real sobre Valor
    COALESCE(
        TRY_CAST(REPLACE(CAST(Real AS VARCHAR), ',', '.') AS DECIMAL(18,2)),
        TRY_CAST(REPLACE(CAST(Valor AS VARCHAR), ',', '.') AS DECIMAL(18,2)),
        0
    ) AS Valor,
    TRIM(Status) AS Status,
    TRIM(Credor) AS Credor,
    TRIM("Tipo Pagamento") AS Tipo_Pagamento,
    -- Data de Competência: Criada para cálculos de BI
    CAST(
        RIGHT(TRIM(Origem_Aba), 4) || '-' || 
        CASE 
            WHEN TRIM(Origem_Aba) LIKE 'Jan%' THEN '01'
            WHEN TRIM(Origem_Aba) LIKE 'Fev%' THEN '02'
            WHEN TRIM(Origem_Aba) LIKE 'Mar%' THEN '03'
            WHEN TRIM(Origem_Aba) LIKE 'Abr%' THEN '04'
            WHEN TRIM(Origem_Aba) LIKE 'Mai%' THEN '05'
            WHEN TRIM(Origem_Aba) LIKE 'Jun%' THEN '06'
            WHEN TRIM(Origem_Aba) LIKE 'Jul%' THEN '07'
            WHEN TRIM(Origem_Aba) LIKE 'Ago%' THEN '08'
            WHEN TRIM(Origem_Aba) LIKE 'Set%' THEN '09'
            WHEN TRIM(Origem_Aba) LIKE 'Out%' THEN '10'
            WHEN TRIM(Origem_Aba) LIKE 'Nov%' THEN '11'
            WHEN TRIM(Origem_Aba) LIKE 'Dez%' THEN '12'
            ELSE '01' 
        END || '-01' AS DATE
    ) AS Data_Competencia,
    TRY_CAST("Data de pagamento" AS DATE) AS Data_Referencia,
    -- Suporte a Parcelamentos (v6.0)
    COALESCE(TRY_CAST("Parcelas Pagas" AS INTEGER), 0) AS Parcelas_Pagas,
    COALESCE(TRY_CAST("Num. de Parcelas" AS INTEGER), 0) AS Total_Parcelas,
    UPPER(LEFT(TRIM(Origem_Aba), 3)) AS Mes_Sigla,
    RIGHT(TRIM(Origem_Aba), 4) AS Ano
FROM bronze_despesa
WHERE "Despesa Mensal" NOT ILIKE '%Total%' 
  AND "Despesa Mensal" NOT IN ('Despesa Mensal', 'Renda Mensal', 'Origem', 'Origem,Valor,Status,Data prevista pag.,,,,,Fev2026,,,,,,,,')
  AND "Despesa Mensal" IS NOT NULL
  AND (Real IS NOT NULL OR Valor IS NOT NULL)
```

--- 

## 5. Execução e Salvamento
O script deve:
1. Conectar ao DuckDB.
2. Carregar os CSVs da Bronze.
3. Executar as queries SQL acima.
4. Salvar o resultado em `fato_renda.parquet` e `fato_despesa.parquet`.