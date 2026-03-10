# Estrutura de Publicação e Execução do Site

## Objetivo

Definir a estrutura necessária para manter o site publicado no GitHub, integrado ao pipeline em Python, com atualização automática dos dados e execução recorrente **duas vezes por semana**.

Esta documentação cobre:

* organização do repositório
* ferramentas necessárias
* integração entre pipeline e site
* automação de execução
* publicação do front-end
* atualização automática dos dados

---

# Stack Utilizada

## Hospedagem

* GitHub Pages

## Automação

* GitHub Actions

## Processamento de dados

* Python

## Bibliotecas Python

* pandas
* openpyxl
* pyarrow

## Front-end

* HTML
* CSS
* JavaScript

---

# Requisitos para Funcionamento

Para que o projeto funcione corretamente é necessário:

* repositório criado no GitHub
* GitHub Pages habilitado
* GitHub Actions habilitado
* scripts Python organizados
* arquivo `requirements.txt`
* workflow `.yml` para automação
* arquivo final de dados em JSON
* front-end preparado para ler o JSON

---

# Estrutura do Repositório

```
consumo_dados/
│
├── data/
│   ├── input/
│   │   └── dados.xlsx
│   │
│   └── gold/
│       └── dados_site.json
│
├── pipeline/
│   ├── main.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── site/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .github/
│   └── workflows/
│       └── deploy_site.yml
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Papel de Cada Pasta

## data/input

Contém o arquivo de entrada do pipeline.

Exemplo:

```
data/input/dados.xlsx
```

---

## data/gold

Contém o arquivo final utilizado pelo site.

Exemplo:

```
data/gold/dados_site.json
```

---

## pipeline

Contém os scripts responsáveis por:

* leitura do Excel
* transformação dos dados
* geração do JSON final

---

## site

Contém o front-end que será publicado no GitHub Pages.

Arquivos típicos:

```
index.html
script.js
style.css
```

---

## .github/workflows

Contém o workflow responsável pela automação do pipeline e publicação do site.

---

# Fluxo de Funcionamento

```
Excel
 ↓
Pipeline Python
 ↓
Geração do JSON final
 ↓
Site lê o JSON
 ↓
GitHub Pages publica o site
```

Fluxo automatizado:

```
Agendamento ou push
 ↓
GitHub Actions executa o pipeline
 ↓
Atualiza JSON
 ↓
Publica site atualizado
```

---

# Ferramentas e Responsabilidades

## GitHub Pages

Responsável por:

* hospedar o site
* disponibilizar HTML, CSS e JavaScript
* tornar o projeto acessível publicamente

---

## GitHub Actions

Responsável por:

* instalar o ambiente Python
* instalar dependências
* executar o pipeline
* gerar o JSON final
* publicar o site

---

## Python

Responsável por:

* ler o Excel
* tratar dados
* gerar o arquivo JSON consumido pelo site

---

## JavaScript

Responsável por:

* ler o JSON
* renderizar tabelas ou gráficos
* atualizar os dados exibidos no site

---

# Arquivos Obrigatórios

## requirements.txt

Lista de dependências do projeto.

Exemplo:

```
pandas
openpyxl
pyarrow
```

---

## pipeline/main.py

Arquivo principal responsável por executar o pipeline completo.

Responsabilidade:

* chamar extract
* chamar transform
* chamar load

---

## data/gold/dados_site.json

Arquivo final que será consumido pelo site.

---

## site/index.html

Página principal do site.

---

## site/script.js

Script responsável por ler o JSON e exibir os dados.

---

## .github/workflows/deploy_site.yml

Workflow responsável por executar o pipeline e publicar o site automaticamente.

---

# Integração entre Pipeline e Site

A integração ocorre através do arquivo JSON.

Pipeline gera:

```
data/gold/dados_site.json
```

O site consome:

```
../data/gold/dados_site.json
```

Exemplo de leitura no JavaScript:

```javascript
fetch("../data/gold/dados_site.json")
  .then(response => response.json())
  .then(data => {
      console.log(data);
  });
```

---

# Agendamento de Execução

O pipeline será executado **duas vezes por semana**.

Dias recomendados:

* terça-feira
* sexta-feira

Horário sugerido:

06:00 (horário de Brasília)

---

# Responsabilidade do Workflow

O workflow deve executar:

1. baixar o código do repositório
2. configurar ambiente Python
3. instalar dependências
4. executar pipeline Python
5. validar geração do JSON
6. publicar o site

---

# Publicação do Site

O GitHub Pages será configurado para publicar o site utilizando **GitHub Actions** como fonte de deploy.

Processo:

1. workflow executa pipeline
2. JSON é atualizado
3. site é publicado com os novos dados

---

# Configurações Necessárias no GitHub

## Pages

Configurar no repositório:

```
Settings → Pages
```

Definir:

```
Source: GitHub Actions
```

---

## Actions

Garantir que:

* workflows estejam habilitados
* permissões permitam deploy do Pages

---

# Estrutura de Execução

Entrada:

```
data/input/dados.xlsx
```

Processamento:

```
pipeline/main.py
```

Saída:

```
data/gold/dados_site.json
```

Consumo:

```
site/script.js
```

Automação:

```
.github/workflows/deploy_site.yml
```

---

# Critérios de Funcionamento

O projeto será considerado funcional quando:

* pipeline executar sem intervenção manual
* JSON for atualizado automaticamente
* site ler o JSON corretamente
* GitHub Pages publicar o site
* execução ocorrer duas vezes por semana
* execução manual também for possível

---

# Boas Práticas

* manter o JSON final leve
* separar pipeline e front-end
* manter apenas um ponto de saída de dados
* centralizar execução no `main.py`
* validar geração do JSON antes do deploy

---

# Resultado Esperado

A arquitetura permitirá:

* pipeline versionado no GitHub
* atualização automática dos dados
* site publicado sem custo de hospedagem
* execução automática duas vezes por semana
* integração simples entre dados e front-end

---

# Resumo da Arquitetura

```
GitHub Repository
 ├── Pipeline Python
 ├── JSON final
 ├── Site estático
 └── Workflow de automação

GitHub Actions
 ├── Executa pipeline
 ├── Atualiza dados
 └── Publica site

GitHub Pages
 └── Exibe o site atualizado
```
