import duckdb
import os
import json
from pipeline.utils.logger import PipelineLogger

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
    logger = PipelineLogger(
        stage="Gold",
        script_name="gold_load.py",
        log_file_path=os.path.join("logs", "gold_load_log.csv")
    )
    logger.start("Iniciando geração de relatórios JSON da Camada Gold.")

    try:
        # Garante que a pasta de destino existe
        if not os.path.exists(PATHS["GOLD"]):
            os.makedirs(PATHS["GOLD"])
        
        # Inicia conexão in-memory com o DuckDB
        con = duckdb.connect()
        
        silver_despesa = os.path.join(PATHS["SILVER"], "fato_despesa.parquet")
        silver_renda = os.path.join(PATHS["SILVER"], "fato_renda.parquet")
        
        if not os.path.exists(silver_despesa) or not os.path.exists(silver_renda):
             logger.log_error("Arquivos Parquet não encontrados na camada Silver.")
             print(f"Erro: Arquivos Parquet não encontrados na camada Silver.")
             logger.finish()
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
                Data_Competencia,
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
                Data_Competencia,
                Item,
                Valor
            FROM read_parquet('{silver_renda}')
            ORDER BY Data_Referencia DESC
        ) TO '{output_detalhado_renda}' (FORMAT JSON, ARRAY TRUE);
        """
        con.execute(query_detalhado_renda)
        print(f"Camada Gold: Detalhes de rendas gerados em {output_detalhado_renda}")

        # Log metrics para os JSONs gerados
        def contar_registros_json(filepath):
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return len(data)
            return 0

        qtde_resumo = contar_registros_json(output_resumo)
        qtde_det_despesa = contar_registros_json(output_detalhado_despesa)
        qtde_det_renda = contar_registros_json(output_detalhado_renda)

        logger.log_metric("Gold Output", "json_resumo_mensal", qtde_resumo, metric_unit="rows", row_count=qtde_resumo)
        logger.log_metric("Gold Output", "json_detalhe_despesa", qtde_det_despesa, metric_unit="rows", row_count=qtde_det_despesa)
        logger.log_metric("Gold Output", "json_detalhe_renda", qtde_det_renda, metric_unit="rows", row_count=qtde_det_renda)

        con.close()
        logger.finish("Camada Gold populada com sucesso.")

    except Exception as e:
        logger.log_error(f"Erro na geração da Camada Gold: {str(e)}")
        raise e

if __name__ == "__main__":
    try:
        load_gold()
        print("\nSucesso: Camada Gold populada com dados JSON prorntos para o Front-end!")
    except Exception as e:
        print(f"\nErro na geração da Camada Gold: {e}")
