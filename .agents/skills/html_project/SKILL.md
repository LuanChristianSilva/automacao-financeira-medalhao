---
name: Desenvolvimento Web com HTML
description: Melhores práticas e diretrizes para a construção de projetos HTML
---

# Skill de Projeto HTML

Esta skill fornece diretrizes e melhores práticas para trabalhar em projetos HTML, focando em padrões modernos e eficiência.

## 1. Princípios Fundamentais

* **HTML Semântico**: Utilize tags estruturais (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`, `<aside>`) em vez de `<div>` genéricas. Isso melhora a acessibilidade e o SEO.
* **Acessibilidade (a11y)**:
    * Tags `<img>` devem ter atributos `alt` descritivos (ou `alt=""` se for decorativa).
    * Mantenha a hierarquia de títulos (`<h1>` a `<h6>`) sem pular níveis. Apenas um `<h1>` por página.
    * Use `<button>` para ações e `<a>` para navegação.
    * Elementos `<input>` devem ter `<label>` associados.
* **Design Responsivo**:
    * Inclua a meta tag viewport: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
    * Aplique a estratégia **Mobile-First** com media queries para telas maiores.
* **Performance & SEO**:
    * Sempre inclua as tags `<title>` e `<meta name="description">` no `<head>`.
    * Carregue o CSS no `<head>` e o JavaScript ao final do `<body>` (ou use `defer`/`async`).

* **REGRAS_1*:
    * NÃO utilize outra ferramenta sem ser JS, HTML e CSS5
    * Sempre apos um bloco de codigo, adicione um comentario explicativo
    * Não faça coisas sem nescessidade
---

## 2. Estrutura de Arquivos Recomendada

Um projeto HTML padrão deve seguir esta organização de diretórios:

```text
index.html
css/
  style.css
js/
  main.js
assets/
  images/
  fonts/