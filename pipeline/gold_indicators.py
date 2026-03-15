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
    logger.start("Iniciando geração de indicadores acionáveis e metas com suporte a filtros.")

    try:
        if not os.path.exists(PATHS["GOLD"]):
            os.makedirs(PATHS["GOLD"])
        
        con = duckdb.connect()
        
        silver_despesa = os.path.join(PATHS["SILVER"], "fato_despesa.parquet")
        silver_renda = os.path.join(PATHS["SILVER"], "fato_renda.parquet")

        if not os.path.exists(silver_despesa) or not os.path.exists(silver_renda):
             logger.log_error("Arquivos Parquet não encontrados na camada Silver.")
             return

        # --- Indicator 1: Actionable Metrics by Month ---
        output_indicators = os.path.join(PATHS["GOLD"], "indicadores_acao.json")
        query_indicators = f"""
        COPY (
            WITH despesas AS (
                SELECT Data_Competencia, SUM(Valor) as Total_Despesa,
                       SUM(CASE WHEN Item LIKE 'Cartão%' THEN Valor ELSE 0 END) as Divida_Cartao
                FROM read_parquet('{silver_despesa}')
                GROUP BY 1
            ),
            rendas AS (
                SELECT Data_Competencia, SUM(COALESCE(Valor, 0)) as Total_Renda
                FROM read_parquet('{silver_renda}')
                GROUP BY 1
            ),
            meses_base AS (
                SELECT r.Data_Competencia, r.Total_Renda, COALESCE(d.Total_Despesa, 0) as Total_Despesa,
                       COALESCE(d.Divida_Cartao, 0) as Divida_Cartao
                FROM rendas r
                LEFT JOIN despesas d ON r.Data_Competencia = d.Data_Competencia
            ),
            installments AS (
                SELECT 
                    Data_Competencia,
                    Item,
                    MAX(Valor) as Valor,
                    MAX(Parcelas_Pagas) as Pagas,
                    MAX(Total_Parcelas) as Total,
                    MAX(Total_Parcelas) - MAX(Parcelas_Pagas) as Restantes
                FROM read_parquet('{silver_despesa}')
                WHERE Total_Parcelas > 0
                GROUP BY 1, 2
            ),
            installments_per_month AS (
                SELECT 
                    Data_Competencia,
                    list(json_object('item', Item, 'valor', Valor, 'pagas', Pagas, 'total', Total, 'restantes', Restantes)) as Parcelas,
                    MAX(Restantes) as Max_Restantes
                FROM installments
                GROUP BY 1
            ),
            top_expenses AS (
                SELECT 
                    Data_Competencia,
                    Item, 
                    SUM(Valor) as Total_Valor
                FROM read_parquet('{silver_despesa}')
                GROUP BY 1, 2
            ),
            top_3_per_month AS (
                SELECT 
                    Data_Competencia,
                    list(json_object('item', Item, 'valor', Total_Valor)) as Gastos
                FROM (
                    SELECT Data_Competencia, Item, Total_Valor,
                           row_number() OVER (PARTITION BY Data_Competencia ORDER BY Total_Valor DESC) as rn
                    FROM top_expenses
                )
                WHERE rn <= 3
                GROUP BY 1
            )
            SELECT 
                m.Data_Competencia as Mes_Referencia,
                m.Total_Renda - m.Total_Despesa AS Receita_Disponivel,
                CASE WHEN m.Total_Despesa > 0 THEN (m.Total_Renda - m.Total_Despesa) / (m.Total_Despesa / 30) ELSE 30 END AS Dias_Restantes,
                CASE WHEN (m.Total_Renda - m.Total_Despesa) < 500 THEN 'Alto' ELSE 'Baixo' END AS Risco_Saldo_Negativo,
                CASE 
                    WHEN (m.Total_Renda - m.Total_Despesa) < 0 THEN 100
                    WHEN m.Total_Renda > 0 THEN (m.Divida_Cartao / m.Total_Renda) * 100 
                    ELSE 0 
                END AS Impacto_Divida_Pct,
                COALESCE(i.Max_Restantes, 0) AS Meses_Para_Quitar,
                COALESCE(t.Gastos, []) AS Top_Gastos,
                COALESCE(i.Parcelas, []) AS Detalhe_Parcelas
            FROM meses_base m
            LEFT JOIN top_3_per_month t ON m.Data_Competencia = t.Data_Competencia
            LEFT JOIN installments_per_month i ON m.Data_Competencia = i.Data_Competencia
            ORDER BY Mes_Referencia DESC
        ) TO '{output_indicators}' (FORMAT JSON, ARRAY TRUE);
        """
        con.execute(query_indicators)

        # --- Indicator 2: Savings Goal ---
        output_goals = os.path.join(PATHS["GOLD"], "metas_poupanca.json")
        query_goals = f"""
        COPY (
            WITH total_savings AS (
                SELECT SUM(Total_Renda - Total_Despesa) as Acumulado
                FROM (
                    SELECT 
                        r.Data_Competencia,
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
