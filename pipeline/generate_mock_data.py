import json
import os
import random
from datetime import datetime

PATHS = {
    "GOLD": os.path.join("Dados", "3_Gold"),
}

def generate_mock_data():
    print("Gerando dados simulados diversificados v3 para demonstracao online...")
    
    if not os.path.exists(PATHS["GOLD"]):
        os.makedirs(PATHS["GOLD"])

    # Configurações de variabilidade
    CATEGORIES = ["Supermercado", "Lazer", "Restaurante", "Educação", "Transporte", "Saúde", "Viagem", "Assinaturas", "Manutenção Casa"]
    INSTALLMENTS_POOL = [
        {"item": "iPhone 15 Pro", "valor": 650.00, "total": 12, "inicio_mes": 1},
        {"item": "Seguro Auto Porto", "valor": 185.40, "total": 10, "inicio_mes": 1},
        {"item": "Sofá Retrátil", "valor": 320.00, "total": 8, "inicio_mes": 3},
        {"item": "Academia BlueFit", "valor": 119.90, "total": 12, "inicio_mes": 1},
        {"item": "MBA Finanças", "valor": 450.00, "total": 24, "inicio_mes": 1},
        {"item": "Geladeira Samsung", "valor": 289.90, "total": 10, "inicio_mes": 2},
        {"item": "MacBook Air M2", "valor": 550.00, "total": 12, "inicio_mes": 5}
    ]

    mock_resumo = []
    meses_siglas = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    
    # Geramos 13 meses
    for i in range(1, 14):
        ano = "2025" if i <= 12 else "2026"
        mes_val = i if i <= 12 else 1
        mes_num = f"{mes_val:02d}"
        data_comp = f"{ano}-{mes_num}-01"
        
        # Variabilidade na Renda e Despesa (±8%)
        renda_base = 5500.00 + (i * 25)
        despesa_base = 3800.00 + (i * 20)
        
        renda = round(renda_base * random.uniform(0.92, 1.08), 2)
        despesa = round(despesa_base * random.uniform(0.92, 1.08), 2)
        
        mock_resumo.append({
            "Data_Competencia": data_comp,
            "Mes_Sigla": meses_siglas[mes_val-1],
            "Ano": ano,
            "Total_Renda": renda,
            "Total_Despesa": despesa,
            "Saldo": round(renda - despesa, 2)
        })

    # 2. indicadores_acao.json
    mock_indicators = []
    for idx, item in enumerate(mock_resumo):
        i = idx + 1 # Mês atual no loop (1-13)
        
        # Gerar Top Gastos Variados e Ordenados
        categories_sample = random.sample(CATEGORIES, 2)
        top_gastos = [
            {"item": "Aluguel Fixo", "valor": 2200.00}, # Valor alto para garantir ser o #1
            {"item": categories_sample[0], "valor": round(random.uniform(200, 800), 2)},
            {"item": categories_sample[1], "valor": round(random.uniform(50, 400), 2)}
        ]
        # Ordenação explícita
        top_gastos.sort(key=lambda x: x["valor"], reverse=True)

        # Gerar Parcelas que evoluem com o tempo
        parcelas_mes = []
        for p in INSTALLMENTS_POOL:
            if i >= p["inicio_mes"]:
                pagas = i - p["inicio_mes"] + 1
                if pagas <= p["total"]:
                    parcelas_mes.append({
                        "item": p["item"],
                        "valor": p["valor"],
                        "pagas": pagas,
                        "total": p["total"],
                        "restantes": p["total"] - pagas
                    })

        mock_indicators.append({
            "Mes_Referencia": item["Data_Competencia"],
            "Receita_Disponivel": item["Saldo"],
            "Dias_Restantes": random.randint(25, 30) if item["Saldo"] > 0 else 0,
            "Risco_Saldo_Negativo": "Baixo" if item["Saldo"] > 500 else ("Médio" if item["Saldo"] > 0 else "Alto"),
            "Impacto_Divida_Pct": round(random.uniform(25, 45), 2),
            "Valor_Comprometido": round(sum(p["valor"] for p in parcelas_mes), 2),
            "Renda_Base": item["Total_Renda"],
            "Global_Min_Divida": 1500.0,
            "Global_Max_Divida": 4500.0,
            "Meses_Para_Quitar": max([p["restantes"] for p in parcelas_mes]) if parcelas_mes else 0,
            "Top_Gastos": top_gastos,
            "Detalhe_Parcelas": parcelas_mes
        })

    # 3. detalhado_despesa.json
    mock_despesas = []
    for item in mock_resumo:
        num_gastos = random.randint(8, 15)
        for j in range(1, num_gastos):
            valor = round(random.uniform(20, 500), 2)
            mock_despesas.append({
                "Data_Competencia": item["Data_Competencia"],
                "Data_Referencia": f"{item['Data_Competencia'][:8]}{random.randint(1,28):02d}",
                "Item": f"Gasto {random.choice(CATEGORIES)} {j}",
                "Valor": valor,
                "Status": random.choice(["Pago", "Pago", "Pendente"]),
                "Credor": random.choice(["Amazon", "Mercado Livre", "Posto Shell", "iFood", "Netflix", "Localiza"]),
                "Tipo_Pagamento": random.choice(["Cartão de Crédito", "PIX", "Boleto"])
            })

    # 4. detalhado_renda.json
    mock_rendas = []
    for item in mock_resumo:
        mock_rendas.append({"Data_Competencia": item["Data_Competencia"], "Item": "Salário Mensal", "Valor": round(item["Total_Renda"] * 0.9, 2)})
        mock_rendas.append({"Data_Competencia": item["Data_Competencia"], "Item": "Renda Extra/Investimentos", "Valor": round(item["Total_Renda"] * 0.1, 2)})

    # 5. metas_poupanca.json
    mock_goals = {
        "Valor_Meta": 50000.00,
        "Valor_Acumulado": round(random.uniform(12000, 18000), 2),
        "Necessidade_Restante": 35000.00,
        "Percentual": 32.5,
        "Data_Alvo": "2026-12-31",
        "Status": "On Track"
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

    print(f"Dados simulados v3 gerados com variabilidade e ordenação em Dados/3_Gold/")

if __name__ == "__main__":
    generate_mock_data()
