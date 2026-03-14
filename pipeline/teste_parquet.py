import duckdb

# Caminho do seu arquivo parquet de RENDA
caminho = r'C:\Users\luanc\Documents\Estudos\teste_antgravity\Dados\2_Silver\fato_renda.parquet'

# SQL para ver o efeito do REPLACE no Item da RENDA
df = duckdb.sql(f"""
    SELECT
        SUM(Valor) AS Valor,
        item
    FROM '{caminho}'
    GROUP BY item
""").df()


# Exibe os resultados
print("--- Verificando Fato Renda (Item columns) ---")
print(df.head(20))