# Consumo de Dados

## Objetivo
Este projeto tem como objetivo construir um pipeline simples de dados que realiza:

1. Extração de dados a partir de um arquivo Excel
2. Padronização e transformação dos dados
3. Persistência em múltiplas camadas de armazenamento
4. Disponibilização de dados consolidados em formato JSON
5. Consumo desses dados por um site estático publicado via GitHub Pages

O pipeline segue uma arquitetura inspirada em **Data Lake Medallion (Bronze → Silver → Gold)**.

---

# Arquitetura Geral

Fluxo de dados:

Excel → CSV → Parquet → Gold (JSON) → Site

---

# Consumo de Dados

## Objetivo

Esta etapa do pipeline é responsável por disponibilizar os dados consolidados para consumo da aplicação web.

Os dados são expostos em formato **JSON**, permitindo leitura direta pelo front-end do site hospedado no GitHub Pages.

Esta camada **não realiza transformações complexas**. Seu objetivo é apenas:

* receber dados já tratados da camada anterior
* estruturar os dados para consumo web
* disponibilizar o arquivo final utilizado pelo site

---

# Entrada de Dados

Esta etapa recebe dados da camada anterior no seguinte formato:

Formato esperado:

```
Parquet
```

Local esperado no repositório:

```
Dados/2_Silver/
```

Arquivos esperados:

```
fato_despesa.parquet
fato_renda.parquet
```

---

# Processamento

O processamento desta etapa consiste em:

1. leitura dos arquivos parquet (Renda e Despesa)
2. agregação de valores por competência e categoria
3. conversão para arquivos JSON otimizados

Script responsável:

```
gold_load.py
```

Fluxo desta etapa:

```
Parquet (Silver) → JSON (Gold)
```

---

# Saída de Dados

Os dados gerados nesta etapa serão armazenados no seguinte local:

```
Dados/3_Gold/
```

Este arquivo representa a **fonte de dados utilizada pelo site**.

---

# Estrutura Esperada do JSON

O JSON deve ser estruturado de forma otimizada para leitura no navegador.

Exemplo:

```json
[
  {
    "categoria": "Produto A",
    "valor": 120,
    "data": "2026-03-01"
  },
  {
    "categoria": "Produto B",
    "valor": 95,
    "data": "2026-03-01"
  }
]
```

A estrutura deve priorizar:

* baixo tamanho de arquivo
* leitura rápida no navegador
* compatibilidade com bibliotecas de gráficos

---

# Localização no Repositório

Estrutura relacionada a esta etapa:

```
teste_antgravity/
│
├── Dados/3_Gold/
│   └── *
│
├── pipeline/
│   └── load.py
│
└── site/
    ├── index.html
    ├── script.js
    └── style.css
```

---

# Consumo pelo Site

O site consome os dados diretamente da pasta Gold.

Exemplo de leitura no JavaScript:

```javascript
// Ajustado para a estrutura do projeto
fetch("../Dados/3_Gold/resumo_mensal.json")
  .then(response => response.json())
  .then(data => {
      console.log("Dados Gold carregados:", data);
  });
```

Sempre que o pipeline atualizar o arquivo JSON, o site automaticamente passará a consumir os novos dados.

---

# Responsabilidades desta Camada

Esta camada é responsável por:

* disponibilizar dados finais para consumo
* garantir formato compatível com web
* manter baixo volume de dados
* facilitar atualização automática via pipeline

Não é responsabilidade desta camada:

* realizar limpeza de dados
* corrigir inconsistências
* aplicar regras de negócio complexas

