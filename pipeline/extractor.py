import pandas as pd
import openpyxl
import os

from pipeline.utils.logger import PipelineLogger

# ==========================================
# 1. Camada de Configuração (Maintenance Layer)
# ==========================================
# Centraliza todos os parâmetros para facilitar mudanças futuras
CONFIG = {
    "ARQUIVO_PATH": r"C:\Users\luanc\OneDrive\Controles_Luan\Mensal.xlsx",
    "PADRAO_ABAS": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    "CONFIG_RENDA": {
        "START_KEYWORD": "Renda Mensal",
        "STOP_CONDITION": "Total de Renda ou 2 linhas vazias",
        "COL_RANGE": "B:D"
    },
    "CONFIG_DESPESA": {
        "START_KEYWORD": "Despesa Mensal",
        "COL_RANGE": "B:I",
        "USE_AUTOFILTER": True
    }
}

# ==========================================
# 2. Módulo de Extração (Função Genérica)
# ==========================================
def extrair_bloco_dados(sheet_name, excel_file, config_type):
    """
    Localiza e extrai um bloco específico de dados (Renda ou Despesa) dentro de uma aba.
    Aplica lógica de parada dinâmica para a Renda.
    """
    # Carrega a aba inteira para localização inicial
    df_raw = pd.read_excel(excel_file, sheet_name=sheet_name)
    conf = CONFIG[config_type]
    
    # 1. Localização: Busca a linha que contém a START_KEYWORD
    start_row = None
    for idx, row in df_raw.iterrows():
        if row.astype(str).str.contains(conf["START_KEYWORD"]).any():
            start_row = idx + 1 # +1 para começar na linha seguinte ao cabeçalho
            break
            
    if start_row is None:
        return pd.DataFrame()

    # 2. Delimitação e Extração Dinâmica (Stop Condition)
    # Lemos os dados usando a linha de keywords como cabeçalho de colunas (header=0 padrão)
    df_full = pd.read_excel(
        excel_file, 
        sheet_name=sheet_name, 
        skiprows=start_row, 
        usecols=conf["COL_RANGE"]
    )
    
    rows_validas = []
    empty_count = 0
    
    for _, row in df_full.iterrows():
        primeira_coluna = str(row.iloc[0]).strip().lower()
        
        # Condições de parada
        if config_type == "CONFIG_RENDA" and primeira_coluna == "total de renda":
            break
        elif config_type == "CONFIG_DESPESA" and primeira_coluna == "valor em atraso do mes anterior":
            break
            
        # Detectar linhas vazias consecutivas (apenas para Renda)
        if config_type == "CONFIG_RENDA":
            if row.isnull().all() or (row.astype(str).str.strip() == "").all() or primeira_coluna == "nan":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            
        rows_validas.append(row)
        
    df_bloco = pd.DataFrame(rows_validas) if rows_validas else pd.DataFrame()

    if df_bloco.empty:
        return pd.DataFrame()

    # Reaplica nomes padronizados nas Rendas para evitar conflitos na Silver
    if config_type == "CONFIG_RENDA":
        df_bloco.columns = ["Renda Mensal", "Real", "Mes Ano Renda"]

    # Identificação da Origem (Rastreabilidade)
    df_bloco["Origem_Aba"] = sheet_name
    
    # 3. Módulo de Limpeza e Tipagem
    df_bloco = df_bloco.dropna(how='all').reset_index(drop=True)
    df_bloco = df_bloco.apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    return df_bloco

# ==========================================
# 3. Fluxo de Execução Principal
# ==========================================
def main():
    logger = PipelineLogger(
        stage="Bronze",
        script_name="extractor.py",
        log_file_path=os.path.join("logs", "extractor_log.csv")
    )
    logger.start("Iniciando varredura e extração de planilhas locais.")
    path = CONFIG["ARQUIVO_PATH"]
    
    if not os.path.exists(path):
        logger.log_error(f"Arquivo não encontrado em {path}")
        print(f"Erro: Arquivo não encontrado em {path}")
        logger.finish()
        return

    # Módulo de Varredura
    # Filtra apenas as abas que correspondem aos meses/ano definidos
    # ADENDO: Desconsidera abas que iniciam com "Viagem" conforme solicitado
    try:
        with pd.ExcelFile(path) as reader:
            abas_validas = [
                s for s in reader.sheet_names 
                if any(mes in s for mes in CONFIG["PADRAO_ABAS"]) 
                and not s.startswith("Viagem")
            ]
            
            # Log de métrica (quantas abas no total vs válidas)
            logger.log_metric("Excel Tabs", "total_tabs", len(reader.sheet_names), metric_unit="count")
            logger.log_metric("Excel Tabs", "eligible_tabs", len(abas_validas), metric_unit="count")            
            
            lista_rendas = []
            lista_despesas = []

            for aba in abas_validas:
                print(f"Processando aba: {aba}...")
                
                # Extração de Renda
                df_renda = extrair_bloco_dados(aba, reader, "CONFIG_RENDA")
                if not df_renda.empty:
                    lista_rendas.append(df_renda)
                    
                # Extração de Despesa
                df_despesa = extrair_bloco_dados(aba, reader, "CONFIG_DESPESA")
                if not df_despesa.empty:
                    lista_despesas.append(df_despesa)
            
            logger.log_metric("Extraction Data", "processed_tabs", len(abas_validas), metric_unit="count")

            # Módulo de Consolidação (Output)
            # Agrupa tudo em um dataframe final e salva em CSV na camada Bronze
            output_dir = os.path.join("Dados", "1_Bronze")
            os.makedirs(output_dir, exist_ok=True)

            if lista_rendas:
                df_final_renda = pd.concat(lista_rendas, ignore_index=True)
                path_renda = os.path.join(output_dir, "consolidado_renda.csv")
                df_final_renda.to_csv(path_renda, index=False, encoding='utf-8-sig')
                logger.log_metric("Consolidate Output", "rows_extracted_renda", len(df_final_renda), metric_unit="rows", row_count=len(df_final_renda))
                print(f"Total de registros de Renda salvos em Bronze: {len(df_final_renda)}")
                
            if lista_despesas:
                df_final_despesa = pd.concat(lista_despesas, ignore_index=True)
                path_despesa = os.path.join(output_dir, "consolidado_despesa.csv")
                df_final_despesa.to_csv(path_despesa, index=False, encoding='utf-8-sig')
                logger.log_metric("Consolidate Output", "rows_extracted_despesa", len(df_final_despesa), metric_unit="rows", row_count=len(df_final_despesa))
                print(f"Total de registros de Despesa salvos em Bronze: {len(df_final_despesa)}")

    except Exception as e:
        logger.log_error(f"Erro fatal na extração: {str(e)}")
        print(f"Erro fatal: {e}")

    logger.finish()

if __name__ == "__main__":
    main()

# O código acima segue a estrutura modular solicitada na Skill: 
# Manutenção centralizada, varredura inteligente, extração genérica e limpeza de dados.
