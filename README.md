# Automação de Extração Financeira - Arquitetura Medalhão 🥇

Este projeto automatiza a extração, limpeza e consolidação de dados financeiros a partir de planilhas Excel complexas, utilizando uma arquitetura de dados em camadas (Bronze e Silver) para garantir qualidade e rastreabilidade.

## 🚀 Arquitetura do Projeto

O projeto segue o padrão **Medallion Architecture**:

1.  **Bronze (Raw)**: Dados brutos extraídos diretamente do Excel sem transformações. Salvos em `.csv`.
2.  **Silver (Refined)**: Dados limpos, tipados e padronizados via SQL (DuckDB). Salvos em `.parquet` para performance e integração com ferramentas de BI (Power BI).

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem core para automação.
- **Pandas & Openpyxl**: Extração dinâmica de blocos de dados do Excel.
- **DuckDB**: Engine SQL em processo para transformações ultra-rápidas na camada Silver.
- **Parquet**: Formato de arquivo colunar para armazenamento eficiente na camada Silver.

## 📁 Estrutura de Pastas

```bash
📂 Dados/
├── 📂 1_Bronze/       # Arquitetos brutos (CSV)
└── 📂 2_Silver/       # Fatos refinados (Parquet)
📂 .agents/            # Definições de Skills e regras de negócio
├── extractor.py       # Script de extração Excel -> Bronze
└── silver_transform.py # Script de transformação Bronze -> Silver
```

## ⚙️ Como Executar

### 1. Requisitos
Instale as dependências necessárias:
```bash
pip install pandas openpyxl duckdb
```

### 2. Extração para Bronze
Execute o script para varrer as abas do Excel e gerar os consolidados brutos:
```bash
python extractor.py
```

### 3. Transformação para Silver (SQL Engine)
Execute o script que utiliza DuckDB para aplicar as regras de limpeza, tratar datas PT-BR e gerar os arquivos Parquet:
```bash
python silver_transform.py
```

## 📊 Diferenciais Técnicos (Silver Layer)
- **Unificação Inteligente**: Uso de `COALESCE` para priorizar colunas de valor real sobre valores previstos.
- **BI Ready**: Criação automática de `Data_Competencia` (dia 1 do mês) para inteligência de tempo no Power BI.
- **Data Cleaning**: Aplicação de `TRIM` em todos os campos de texto para evitar erros de filtro.

---
*Desenvolvido como parte do projeto de estudos de Engenharia de Dados.*
