import duckdb

# Caminho do seu arquivo parquet
caminho = r'C:\Users\luanc\Documents\Estudos\teste_antgravity\Dados\2_Silver\fato_renda.parquet'

# Executa a query e transforma em DataFrame
df = duckdb.sql(f"SELECT * FROM '{caminho}'").df()

# Exibe o resultado
print(df.head())