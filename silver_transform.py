import duckdb
import os

# ==========================================
# 1. Camada de Configuração (Silver Layer)
# ==========================================
PATHS = {
    "BRONZE": os.path.join("Dados", "1_Bronze"),
    "SILVER": os.path.join("Dados", "2_Silver"),
}

def transform_silver():
    """
    Executa a transformação dos dados da camada Bronze para a Silver usando DuckDB.
    Aplica limpeza, tipagem e filtragem de ruídos via SQL.
    """
    # Garante que a pasta de destino existe
    if not os.path.exists(PATHS["SILVER"]):
        os.makedirs(PATHS["SILVER"])
    
    # Inicia conexão DuckDB (in-memory para processamento rápido)
    con = duckdb.connect()
    
    # Caminhos dos arquivos de origem
    bronze_renda = os.path.join(PATHS["BRONZE"], "consolidado_renda.csv")
    bronze_despesa = os.path.join(PATHS["BRONZE"], "consolidado_despesa.csv")
    
    print("Iniciando processamento SQL via DuckDB...")

    # Query base para calcular Data_Competencia de abas como 'Mar2026' ou 'Fev2026'
    sql_data_competencia = """
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
    ) AS Data_Competencia
    """

    # ==========================================
    # 2. Processamento de Rendas
    # ==========================================
    query_renda = f"""
    CREATE OR REPLACE TABLE silver_renda AS
    SELECT 
        Origem_Aba,
        TRIM("Renda Mensal") AS Item,
        COALESCE(
            TRY_CAST(REPLACE(CAST(Real AS VARCHAR), ',', '.') AS DECIMAL(18,2)),
            0
        ) AS Valor,
        {sql_data_competencia},
        TRY_CAST("Mes Ano Renda" AS DATE) AS Data_Referencia,
        UPPER(LEFT(TRIM(Origem_Aba), 3)) AS Mes_Sigla,
        RIGHT(TRIM(Origem_Aba), 4) AS Ano
    FROM read_csv_auto('{bronze_renda}')
    WHERE "Renda Mensal" NOT ILIKE '%Total%' 
      AND "Renda Mensal" NOT IN ('Renda Mensal', 'Despesa Mensal', 'Origem')
      AND "Renda Mensal" IS NOT NULL
      AND Real IS NOT NULL
      AND Real <> 0;
    """
    con.execute(query_renda)
    
    # Salva em Parquet
    output_renda = os.path.join(PATHS["SILVER"], "fato_renda.parquet")
    con.execute(f"COPY silver_renda TO '{output_renda}' (FORMAT PARQUET)")
    print(f"Camada Silver: Rendas processadas e salvas em {output_renda}")

    # ==========================================
    # 3. Processamento de Despesas
    # ==========================================
    query_despesa = f"""
    CREATE OR REPLACE TABLE silver_despesa AS
    SELECT 
        Origem_Aba,
        TRIM("Despesa Mensal") AS Item,
        COALESCE(
            TRY_CAST(REPLACE(CAST(Real AS VARCHAR), ',', '.') AS DECIMAL(18,2)),
            TRY_CAST(REPLACE(CAST(Valor AS VARCHAR), ',', '.') AS DECIMAL(18,2)),
            0
        ) AS Valor,
        TRIM(Status) AS Status,
        TRIM(Credor) AS Credor,
        TRIM("Tipo Pagamento") AS Tipo_Pagamento,
        {sql_data_competencia},
        TRY_CAST("Data de pagamento" AS DATE) AS Data_Referencia,
        UPPER(LEFT(TRIM(Origem_Aba), 3)) AS Mes_Sigla,
        RIGHT(TRIM(Origem_Aba), 4) AS Ano
    FROM read_csv_auto('{bronze_despesa}')
    WHERE "Despesa Mensal" NOT ILIKE '%Total%' 
      AND "Despesa Mensal" NOT IN ('Despesa Mensal', 'Renda Mensal', 'Origem', 'Origem,Valor,Status,Data prevista pag.,,,,,Fev2026,,,,,,,,')
      AND "Despesa Mensal" IS NOT NULL
      AND (Real IS NOT NULL OR Valor IS NOT NULL);
    """
    con.execute(query_despesa)
    
    # Salva em Parquet
    output_despesa = os.path.join(PATHS["SILVER"], "fato_despesa.parquet")
    con.execute(f"COPY silver_despesa TO '{output_despesa}' (FORMAT PARQUET)")
    print(f"Camada Silver: Despesas processadas e salvas em {output_despesa}")

    con.close()

if __name__ == "__main__":
    try:
        transform_silver()
        print("\nSucesso: Camada Silver populada com dados refinados!")
    except Exception as e:
        print(f"\nErro na transformação Silver: {e}")

# O script acima utiliza DuckDB para processar dados brutos via SQL, 
# removendo ruídos e padronizando tipos antes de salvar em formato Parquet na Silver.
