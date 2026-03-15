import duckdb
import os
import json
from datetime import datetime
from pipeline.utils.logger import PipelineLogger

PATHS = {
    "SILVER": os.path.join("Dados", "2_Silver"),
    "GOLD": os.path.join("Dados", "3_Gold"),
}

def load_indicators():
    logger = PipelineLogger(
        stage="Gold_Indicators",
        script_name="gold_indicators.py",
        log_file_path=os.path.join("logs", "gold_indicators_log.csv")
    )
    logger.start("Iniciando geração de indicadores acionáveis e metas.")

    try:
        if not os.path.exists(PATHS["GOLD"]):
            os.makedirs(PATHS["GOLD"])
        
        con = duckdb.connect()
        
        silver_despesa = os.path.join(PATHS["SILVER"], "fato_despesa.parquet")
        silver_renda = os.path.join(PATHS["SILVER"], "fato_renda.parquet")

        if not os.path.exists(silver_despesa) or not os.path.exists(silver_renda):
             logger.log_error("Arquivos Parquet não encontrados na camada Silver.")
             return

        # --- Indicator 1: Actionable Metrics ---
        # Calculation: Available Income, Days to Last, Debt Impact
        output_indicators = os.path.join(PATHS["GOLD"], "indicadores_acao.json")
        query_indicators = f"""
        COPY (
            WITH current_month AS (
                SELECT 
                    MAX(Data_Competencia) as latest_month
                FROM read_parquet('{silver_renda}')
            ),
            data_resumo AS (
                SELECT 
                    r.Data_Competencia,
                    SUM(COALESCE(r.Valor, 0)) as Renda,
                    (SELECT SUM(Valor) FROM read_parquet('{silver_despesa}') d WHERE d.Data_Competencia = r.Data_Competencia) as Despesa
                FROM read_parquet('{silver_renda}') r
                WHERE r.Data_Competencia = (SELECT latest_month FROM current_month)
                GROUP BY 1
            ),
            top_expenses AS (
                SELECT 
                    Item, 
                    SUM(Valor) as Valor
                FROM read_parquet('{silver_despesa}')
                WHERE Data_Competencia = (SELECT latest_month FROM current_month)
                GROUP BY 1
                ORDER BY 2 DESC
                LIMIT 3
            )
            SELECT 
                Renda - Despesa AS Receita_Disponivel,
                CASE WHEN Despesa > 0 THEN (Renda - Despesa) / (Despesa / 30) ELSE 30 END AS Dias_Restantes,
                CASE WHEN (Renda - Despesa) < 500 THEN 'Alto' ELSE 'Baixo' END AS Risco_Saldo_Negativo,
                (SELECT list(json_object('item', Item, 'valor', Valor)) FROM top_expenses) AS Top_Gastos
            FROM data_resumo
        ) TO '{output_indicators}' (FORMAT JSON, ARRAY TRUE);
        """
        con.execute(query_indicators)

        # --- Indicator 2: Savings Goal (Hypothetical goal for demonstration) ---
        # Goal: R$ 50.000,00
        output_goals = os.path.join(PATHS["GOLD"], "metas_poupanca.json")
        query_goals = f"""
        COPY (
            WITH total_savings AS (
                SELECT SUM(Total_Renda - Total_Despesa) as Acumulado
                FROM (
                    SELECT 
                        Data_Competencia,
                        SUM(COALESCE(r.Valor, 0)) as Total_Renda,
                        (SELECT SUM(Valor) FROM read_parquet('{silver_despesa}') d WHERE d.Data_Competencia = r.Data_Competencia) as Total_Despesa
                    FROM read_parquet('{silver_renda}') r
                    GROUP BY 1
                )
            )
            SELECT 
                50000.00 AS Valor_Meta,
                COALESCE(Acumulado, 0) AS Valor_Acumulado,
                CASE WHEN 50000.00 > Acumulado THEN 50000.00 - Acumulado ELSE 0 END AS Necessidade_Restante,
                CASE WHEN Acumulado > 0 THEN (Acumulado / 50000.00) * 100 ELSE 0 END AS Percentual,
                '2026-12-31' AS Data_Alvo,
                'On Track' AS Status
            FROM total_savings
        ) TO '{output_goals}' (FORMAT JSON, ARRAY TRUE);
        """
        con.execute(query_goals)

        logger.finish("Indicadores e Metas populados com sucesso.")
        con.close()

    except Exception as e:
        logger.log_error(f"Erro: {str(e)}")
        raise e

if __name__ == "__main__":
    load_indicators()
