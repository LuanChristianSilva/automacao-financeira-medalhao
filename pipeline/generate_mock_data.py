import json
import os
from datetime import datetime

PATHS = {
    "GOLD": os.path.join("Dados", "3_Gold"),
}

def generate_mock_data():
    print("Gerando dados simulados para demonstração online...")
    
    if not os.path.exists(PATHS["GOLD"]):
        os.makedirs(PATHS["GOLD"])

    # 1. indicadores_acao.json (Simulado)
    mock_indicators = [
        {
            "Mes_Referencia": "2026-03-01",
            "Receita_Disponivel": 1250.75,
            "Dias_Restantes": 45,
            "Risco_Saldo_Negativo": "Baixo",
            "Impacto_Divida_Pct": 22.5,
            "Meses_Para_Quitar": 6,
            "Top_Gastos": [
                {"item": "Supermercado Exemplo", "valor": 850.00},
                {"item": "Restaurantes", "valor": 420.50},
                {"item": "Assinaturas Stream", "valor": 120.90}
            ],
            "Detalhe_Parcelas": [
                {"item": "Notebook Novo", "valor": 450.00, "pagas": 4, "total": 10, "restantes": 6},
                {"item": "Curso Online", "valor": 190.00, "pagas": 8, "total": 12, "restantes": 4},
                {"item": "Smartphone", "valor": 300.00, "pagas": 2, "total": 10, "restantes": 8}
            ]
        },
        {
            "Mes_Referencia": "2026-02-01",
            "Receita_Disponivel": -150.00,
            "Dias_Restantes": 0,
            "Risco_Saldo_Negativo": "Alto",
            "Impacto_Divida_Pct": 45.0,
            "Meses_Para_Quitar": -1,
            "Top_Gastos": [
                {"item": "Manutenção Carro", "valor": 1200.00},
                {"item": "Aluguel", "valor": 2500.00},
                {"item": "Saúde", "valor": 600.00}
            ],
            "Detalhe_Parcelas": [
                {"item": "Notebook Novo", "valor": 450.00, "pagas": 3, "total": 10, "restantes": 7},
                {"item": "Curso Online", "valor": 190.00, "pagas": 7, "total": 12, "restantes": 5}
            ]
        }
    ]

    # 2. metas_poupanca.json (Simulado)
    mock_goals = {
        "Valor_Meta": 50000.00,
        "Valor_Acumulado": 12850.40,
        "Necessidade_Restante": 37149.60,
        "Percentual": 25.7,
        "Data_Alvo": "2026-12-31",
        "Status": "On Track"
    }

    # 3. resumo_mensal.json (Simulado para gráficos de barra/histórico)
    mock_resumo = [
        {"Mes_Sigla": "JAN", "Ano": "2026", "Total_Valor": 4200.00, "Total_Renda": 5500.00},
        {"Mes_Sigla": "FEV", "Ano": "2026", "Total_Valor": 5650.00, "Total_Renda": 5500.00},
        {"Mes_Sigla": "MAR", "Ano": "2026", "Total_Valor": 4249.25, "Total_Renda": 5500.00}
    ]

    # Salvando arquivos
    with open(os.path.join(PATHS["GOLD"], "indicadores_acao.json"), "w", encoding="utf-8") as f:
        json.dump(mock_indicators, f, indent=4, ensure_ascii=False)
    
    with open(os.path.join(PATHS["GOLD"], "metas_poupanca.json"), "w", encoding="utf-8") as f:
        json.dump([mock_goals], f, indent=4, ensure_ascii=False) # Espera array []

    with open(os.path.join(PATHS["GOLD"], "resumo_mensal.json"), "w", encoding="utf-8") as f:
        json.dump(mock_resumo, f, indent=4, ensure_ascii=False)

    print("Dados simulados gerados com sucesso na pasta Dados/3_Gold/")

if __name__ == "__main__":
    generate_mock_data()
