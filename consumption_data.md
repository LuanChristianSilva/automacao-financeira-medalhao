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
data/silver/
```

Arquivo esperado:

```
dados_tratados.parquet
```

Os dados recebidos devem possuir:

* estrutura tabular
* tipos de dados já padronizados
* colunas finais já definidas
* ausência de registros inválidos

A camada de consumo **não deve realizar limpeza ou tratamento de dados**.

---

# Processamento

O processamento desta etapa consiste em:

1. leitura do arquivo parquet
2. agregação ou seleção de colunas necessárias
3. conversão para JSON otimizado para leitura web

Script responsável:

```
pipeline/load.py
```

Fluxo desta etapa:

```
Parquet → JSON
```

---

# Saída de Dados

Os dados gerados nesta etapa serão armazenados no seguinte local:

```
data/gold/
```

Arquivo gerado:

```
dados_site.json
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
consumo_dados/
│
├── data/
│   └── gold/
│       └── dados_site.json
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

O site consome os dados diretamente do arquivo JSON.

Exemplo de leitura no JavaScript:

```javascript
fetch("../data/gold/dados_site.json")
  .then(response => response.json())
  .then(data => {
      console.log(data);
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

