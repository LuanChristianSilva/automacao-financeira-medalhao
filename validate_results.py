import pandas as pd
import duckdb
import os

def validate():
    print("="*50)
    print("RESUMO DA VALIDAÇÃO DO PIPELINE (BRONZE -> SILVER)")
    print("="*50)

    silver_path = os.path.join("Dados", "2_Silver")
    bronze_path = os.path.join("Dados", "1_Bronze")

    # 1. Validação Silver Renda
    renda_parquet = os.path.join(silver_path, "fato_renda.parquet")
    if os.path.exists(renda_parquet):
        print("\n[SILVER] Tabela: fato_renda.parquet")
        df_renda = pd.read_parquet(renda_parquet)
        print(f"Total de registros: {len(df_renda)}")
        print(f"Colunas: {list(df_renda.columns)}")
        print("\nPrimeiros 5 registros (Renda):")
        print(df_renda.head())
    else:
        print("\n[ERRO] Arquivo fato_renda.parquet não encontrado.")

    # 2. Validação Silver Despesa
    despesa_parquet = os.path.join(silver_path, "fato_despesa.parquet")
    if os.path.exists(despesa_parquet):
        print("\n" + "="*50)
        print("\n[SILVER] Tabela: fato_despesa.parquet")
        df_despesa = pd.read_parquet(despesa_parquet)
        print(f"Total de registros: {len(df_despesa)}")
        print(f"Colunas: {list(df_despesa.columns)}")
        print("\nPrimeiros 5 registros (Despesa):")
        # Selecionando colunas principais para visualização mais limpa
        display_cols = ['Item', 'Valor', 'Status', 'Credor', 'Data_Competencia']
        print(df_despesa[display_cols].head())
    else:
        print("\n[ERRO] Arquivo fato_despesa.parquet não encontrado.")

    # 3. Validação Bronze (Amostra Bruta)
    print("\n" + "="*50)
    print("\n[BRONZE] Amostra de arquivos CSV Consolidados:")
    for f in os.listdir(bronze_path):
        if f.endswith(".csv"):
            df_tmp = pd.read_csv(os.path.join(bronze_path, f), nrows=5)
            print(f"- {f} ({len(df_tmp)} linhas amostradas)")

if __name__ == "__main__":
    validate()
