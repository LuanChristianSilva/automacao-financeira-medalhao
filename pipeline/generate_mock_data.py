import json
import os
from datetime import datetime

PATHS = {
    "GOLD": os.path.join("Dados", "3_Gold"),
}

def generate_mock_data():
    print("Gerando dados simulados completos v2 para demonstracao online...")
    
    if not os.path.exists(PATHS["GOLD"]):
        os.makedirs(PATHS["GOLD"])

    # 1. resumo_mensal.json (Estrutura completa para main.js)
    mock_resumo = []
    meses_siglas = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    
    # Geramos 13 meses para o "rolling 12 months" do main.js funcionar
    for i in range(1, 14):
        ano = "2025" if i <= 10 else "2026"
        mes_val = i if i <= 12 else 1 # Para o 13º mês
        mes_num = f"{mes_val:02d}"
        data_comp = f"{ano}-{mes_num}-01"
        renda = 5500.00 + (i * 20)
        despesa = 3800.00 + (i * 15)
        
        mock_resumo.append({
            "Data_Competencia": data_comp,
            "Mes_Sigla": meses_siglas[mes_val-1],
            "Ano": ano,
            "Total_Renda": renda,
            "Total_Despesa": despesa, # CAMPO CORRIGIDO: Era Total_Valor
            "Saldo": renda - despesa
        })

    # 2. indicadores_acao.json (Indicadores estratégicos)
    mock_indicators = []
    # Criar indicadores para os meses que o filtro pode mostrar
    for item in mock_resumo:
        mock_indicators.append({
            "Mes_Referencia": item["Data_Competencia"],
            "Receita_Disponivel": item["Saldo"],
            "Dias_Restantes": 30,
            "Risco_Saldo_Negativo": "Baixo" if item["Saldo"] > 0 else "Alto",
            "Impacto_Divida_Pct": 25.0,
            "Valor_Comprometido": 920.0,
            "Renda_Base": 3680.0,
            "Global_Min_Divida": 294.0,
            "Global_Max_Divida": 4084.0,
            "Meses_Para_Quitar": 6,
            "Top_Gastos": [
                {"item": "Supermercado Mock", "valor": 900.00},
                {"item": "Aluguel", "valor": 2200.00},
                {"item": "Lazer", "valor": 150.00}
            ],
            "Detalhe_Parcelas": [
                {"item": "Notebook", "valor": 450.00, "pagas": 5, "total": 10, "restantes": 5},
                {"item": "Smartphone", "valor": 300.00, "pagas": 3, "total": 10, "restantes": 7}
            ]
        })

    # 3. detalhado_despesa.json (Lista de gastos)
    mock_despesas = []
    for item in mock_resumo:
        for j in range(1, 6):
            mock_despesas.append({
                "Data_Competencia": item["Data_Competencia"],
                "Data_Referencia": f"{item['Data_Competencia'][:8]}{j:02d}",
                "Item": f"Gasto {meses_siglas[int(item['Data_Competencia'][5:7])-1]} {j}",
                "Valor": 100.0 * j,
                "Status": "Pago" if j % 2 == 0 else "Não Pago", # STATUS CORRIGIDO: Era Aberto
                "Credor": "Loja Exemplo",
                "Tipo_Pagamento": "Cartão" if j % 2 == 0 else "Boleto"
            })

    # 4. detalhado_renda.json
    mock_rendas = []
    for item in mock_resumo:
        mock_rendas.append({"Data_Competencia": item["Data_Competencia"], "Item": "Salário", "Valor": 5000.00})
        mock_rendas.append({"Data_Competencia": item["Data_Competencia"], "Item": "Extra", "Valor": item["Total_Renda"] - 5000.00})

    # 5. metas_poupanca.json
    mock_goals = {
        "Valor_Meta": 50000.00,
        "Valor_Acumulado": 15000.00,
        "Necessidade_Restante": 35000.00,
        "Percentual": 30.0,
        "Data_Alvo": "2026-12-31",
        "Status": "Em Dia"
    }

    # Salvando arquivos
    files = {
        "resumo_mensal.json": mock_resumo,
        "indicadores_acao.json": mock_indicators,
        "detalhado_despesa.json": mock_despesas,
        "detalhado_renda.json": mock_rendas,
        "metas_poupanca.json": [mock_goals]
    }

    for filename, content in files.items():
        with open(os.path.join(PATHS["GOLD"], filename), "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

    print("Dados simulados v2 gerados com sucesso na pasta Dados/3_Gold/")

if __name__ == "__main__":
    generate_mock_data()
