import pandas as pd
import openpyxl
import os

# ==========================================
# 1. Camada de Configuração (Maintenance Layer)
# ==========================================
# Centraliza todos os parâmetros para facilitar mudanças futuras
CONFIG = {
    "ARQUIVO_PATH": r"C:\Users\luanc\OneDrive\Controles_Luan\Mensal.xlsx",
    "PADRAO_ABAS": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    "CONFIG_RENDA": {
        "START_KEYWORD": "Renda Mensal",
        "END_KEYWORD": "Total de Renda",
        "END_ROW": 14,  # Limite máximo de linha para a coluna B
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
    """
    # Carrega a aba inteira para localizar as keywords
    df_raw = pd.read_excel(excel_file, sheet_name=sheet_name)
    conf = CONFIG[config_type]
    
    # Localização: Busca a linha que contém a START_KEYWORD
    # O script percorre as células para encontrar o cabeçalho do bloco
    start_row = None
    for idx, row in df_raw.iterrows():
        if row.astype(str).str.contains(conf["START_KEYWORD"]).any():
            start_row = idx + 1 # +1 pois o pandas ignora o header na contagem
            break
            
    if start_row is None:
        return pd.DataFrame()

    # Delimitação e Extração Real
    # Lê apenas o range de colunas definido na configuração
    # Se houver END_ROW (como na Renda), limita o número de linhas lidas
    nrows = None
    if "END_ROW" in conf:
        # Calcula quantas linhas restam até o limite (considerando o skiprows)
        nrows = conf["END_ROW"] - start_row

    df_bloco = pd.read_excel(
        excel_file, 
        sheet_name=sheet_name, 
        skiprows=start_row, 
        usecols=conf["COL_RANGE"],
        nrows=nrows
    )

    # Identificação da Origem (Rastreabilidade)
    df_bloco["Origem_Aba"] = sheet_name
    
    # Módulo de Limpeza e Tipagem
    # Remove linhas vazias e limpa espaços em branco em strings
    df_bloco = df_bloco.dropna(how='all').reset_index(drop=True)
    df_bloco = df_bloco.apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    return df_bloco

# ==========================================
# 3. Fluxo de Execução Principal
# ==========================================
def main():
    path = CONFIG["ARQUIVO_PATH"]
    
    if not os.path.exists(path):
        print(f"Erro: Arquivo não encontrado em {path}")
        return

    # Módulo de Varredura
    # Filtra apenas as abas que correspondem aos meses/ano definidos
    # ADENDO: Desconsidera abas que iniciam com "Viagem" conforme solicitado
    with pd.ExcelFile(path) as reader:
        abas_validas = [
            s for s in reader.sheet_names 
            if any(mes in s for mes in CONFIG["PADRAO_ABAS"]) 
            and not s.startswith("Viagem")
        ]
        
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

        # Módulo de Consolidação (Output)
        # Agrupa tudo em um dataframe final e salva em CSV na camada Bronze
        output_dir = os.path.join("Dados", "1_Bronze")
        os.makedirs(output_dir, exist_ok=True)

        if lista_rendas:
            df_final_renda = pd.concat(lista_rendas, ignore_index=True)
            path_renda = os.path.join(output_dir, "consolidado_renda.csv")
            df_final_renda.to_csv(path_renda, index=False, encoding='utf-8-sig')
            print(f"Total de registros de Renda salvos em Bronze: {len(df_final_renda)}")
            
        if lista_despesas:
            df_final_despesa = pd.concat(lista_despesas, ignore_index=True)
            path_despesa = os.path.join(output_dir, "consolidado_despesa.csv")
            df_final_despesa.to_csv(path_despesa, index=False, encoding='utf-8-sig')
            print(f"Total de registros de Despesa salvos em Bronze: {len(df_final_despesa)}")

if __name__ == "__main__":
    main()

# O código acima segue a estrutura modular solicitada na Skill: 
# Manutenção centralizada, varredura inteligente, extração genérica e limpeza de dados.
