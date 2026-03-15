import os
import duckdb
import pandas as pd
import tkinter as tk
from tkinter import ttk

caminho = r'C:\Users\luanc\Documents\Estudos\teste_antgravity\Dados\2_Silver'
silver_renda = os.path.join(caminho, 'fato_renda.parquet')
silver_despesa = os.path.join(caminho, 'fato_despesa.parquet')

df = duckdb.sql(f"""
   SELECT 
        *
    FROM read_parquet('{silver_despesa}')
    LIMIT 100
""").df()

# janela
root = tk.Tk()
root.title("Visualização dos Dados")

frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame)
tree.pack(fill="both", expand=True)

tree["columns"] = list(df.columns)
tree["show"] = "headings"

for col in df.columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

for _, row in df.iterrows():
    tree.insert("", "end", values=list(row))

root.mainloop()