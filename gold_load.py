import duckdb
import os

# ==========================================
# 1. Configuração de Caminhos
# ==========================================
PATHS = {
    "SILVER": os.path.join("Dados", "2_Silver"),
    "GOLD": os.path.join("Dados", "3_Gold"),
}

def load_gold():
    """
    Gera as visões de consumo (JSON) a partir dos dados da camada Silver (Parquet).
    """
    # Garante que a pasta de destino existe
    if not os.path.exists(PATHS["GOLD"]):
        os.makedirs(PATHS["GOLD"])
    
    # Inicia conexão in-memory com o DuckDB
    con = duckdb.connect()
    
    silver_despesa = os.path.join(PATHS["SILVER"], "fato_despesa.parquet")
    silver_renda = os.path.join(PATHS["SILVER"], "fato_renda.parquet")
    
    if not os.path.exists(silver_despesa) or not os.path.exists(silver_renda):
         print(f"Erro: Arquivos Parquet não encontrados na camada Silver.")
         return

    print("Iniciando geração da Camada Gold (JSON)...")

    # ==========================================
    # 2. Visão 1: Resumo Mensal (Agregado para Gráficos)
    # ==========================================
    # Agrupa despesas e rendas por mês
    
    output_resumo = os.path.join(PATHS["GOLD"], "resumo_mensal.json")
    query_resumo = f"""
    COPY (
        WITH despesas AS (
            SELECT 
                Data_Competencia,
                Mes_Sigla,
                Ano,
                SUM(Valor) AS Total_Despesa
            FROM read_parquet('{silver_despesa}')
            GROUP BY 1, 2, 3
        ),
        rendas AS (
            SELECT 
                Data_Competencia,
                Mes_Sigla,
                Ano,
                SUM(Valor) AS Total_Renda
            FROM read_parquet('{silver_renda}')
            GROUP BY 1, 2, 3
        )
        SELECT 
            COALESCE(d.Data_Competencia, r.Data_Competencia) AS Data_Competencia,
            COALESCE(d.Mes_Sigla, r.Mes_Sigla) AS Mes_Sigla,
            COALESCE(d.Ano, r.Ano) AS Ano,
            COALESCE(Total_Renda, 0) AS Total_Renda,
            COALESCE(Total_Despesa, 0) AS Total_Despesa,
            COALESCE(Total_Renda, 0) - COALESCE(Total_Despesa, 0) AS Saldo
        FROM despesas d
        FULL OUTER JOIN rendas r ON d.Data_Competencia = r.Data_Competencia
        ORDER BY Data_Competencia
    ) TO '{output_resumo}' (FORMAT JSON, ARRAY TRUE);
    """
    con.execute(query_resumo)
    print(f"Camada Gold: Resumo mensal gerado em {output_resumo}")

    # ==========================================
    # 3. Visão 2: Detalhado (Transações para Tabelas)
    # ==========================================
    
    output_detalhado_despesa = os.path.join(PATHS["GOLD"], "detalhado_despesa.json")
    query_detalhado_despesa = f"""
    COPY (
        SELECT 
            Data_Referencia,
            Item,
            Valor,
            Status,
            Credor,
            Tipo_Pagamento
        FROM read_parquet('{silver_despesa}')
        WHERE Status != 'Cancelado'
        ORDER BY Data_Referencia DESC
    ) TO '{output_detalhado_despesa}' (FORMAT JSON, ARRAY TRUE);
    """
    con.execute(query_detalhado_despesa)
    print(f"Camada Gold: Detalhes de despesas gerados em {output_detalhado_despesa}")

    output_detalhado_renda = os.path.join(PATHS["GOLD"], "detalhado_renda.json")
    query_detalhado_renda = f"""
    COPY (
        SELECT 
            Data_Referencia,
            Item,
            Valor
        FROM read_parquet('{silver_renda}')
        ORDER BY Data_Referencia DESC
    ) TO '{output_detalhado_renda}' (FORMAT JSON, ARRAY TRUE);
    """
    con.execute(query_detalhado_renda)
    print(f"Camada Gold: Detalhes de rendas gerados em {output_detalhado_renda}")

    con.close()

if __name__ == "__main__":
    try:
        load_gold()
        print("\nSucesso: Camada Gold populada com dados JSON prorntos para o Front-end!")
    except Exception as e:
        print(f"\nErro na geração da Camada Gold: {e}")
