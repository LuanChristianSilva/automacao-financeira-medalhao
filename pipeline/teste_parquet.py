import duckdb

# Caminho do seu arquivo parquet de RENDA
caminho = r'C:\Users\luanc\Documents\Estudos\teste_antgravity\Dados\2_Silver\fato_despesa.parquet'

# SQL para ver o efeito do REPLACE no Item da RENDA
df = duckdb.sql(f"""
    SELECT 
        Item, 
        Valor, 
        Parcelas_Pagas, 
        Total_Parcelas, 
        Origem_Aba
    FROM '{caminho}'
    WHERE Total_Parcelas > 0
    LIMIT 20
""").df()


# Exibe os resultados
print("--- Verificando Fato Renda (Item columns) ---")
print(df.head(20))