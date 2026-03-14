---
name: SempreFazerCommit
description: Diretriz rigorosa para realizar commits no Git após finalizar tarefas ou processos no projeto.
---

# Diretriz de Versionamento (Git)

Você está trabalhando em um projeto onde o versionamento de código é essencial. 

**Regra de Ouro:** A cada processo concluído, alteração significativa, ou funcionalidade finalizada (como a criação de um novo KPI, ajuste em scripts Python, etc.), você **DEVE** realizar um commit no Git antes de passar para a próxima tarefa ou encerrar a sessão.

## Instruções:
1. Ao finalizar um bloco lógico de trabalho, verifique os arquivos modificados usando `git status`.
2. Adicione os arquivos relevantes usando `git add <arquivos>`.
3. Escreva uma mensagem de commit clara e descritiva do que foi feito usando `git commit -m "sua mensagem"`.
4. (Opcional) Confirme com o usuário se ele deseja fazer o `git push` caso haja um repositório remoto configurado.

**CUIDADO:** Nunca permita que várias alterações se acumulem indefinidamente sem commit. O rastreamento contínuo é obrigatório.
