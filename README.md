
# Gestão de Chamados — Sistema e Projeto de QA

Projeto de desenvolvimento de uma aplicação de Gestão de Chamados em Python e SQLite, acompanhado de um projeto de Garantia da Qualidade de Software (QA), organizado no Jira.

O objetivo é apresentar tanto o sistema desenvolvido quanto o processo de planejamento, execução e documentação dos testes realizados.

## Sobre o projeto

A aplicação foi desenvolvida em Python, utiliza SQLite para armazenamento de dados e possui distribuição por executável para Windows.

O trabalho de QA foi organizado no Jira, contemplando o planejamento dos testes, a definição dos casos de teste, a execução, o registro de bugs, a rastreabilidade e o planejamento de retestes.

## Tecnologias e ferramentas

- Python
- SQLite
- Jira
- GitHub
- PyInstaller para empacotamento do aplicativo Windows

## Escopo dos testes

Os testes foram organizados em sete grupos funcionais:

1. Cadastro de chamados
2. Listas por status e botões de ação
3. Edição de chamados
4. Exclusão de chamados
5. Visualização de chamados — Todos e Por Região
6. Relatórios, pastas, notificações e alertas
7. Gravação de dados e backup

## Resultados da primeira execução

| Indicador | Resultado |
|---|---:|
| Casos de teste executados | 44 |
| Testes aprovados | 36 |
| Testes reprovados | 8 |
| Bugs registrados | 8 |

Os oito bugs foram registrados no Jira e relacionados aos respectivos casos de teste. A Sprint 2 — Reteste foi preparada para uma execução futura, após a correção dos problemas identificados.

**Observação:** os resultados apresentados correspondem à primeira execução dos testes. Os bugs permanecem registrados como pendentes de correção; portanto, não são considerados resolvidos.

## Documentação de QA

O projeto contempla:

- Plano de testes
- Catálogo de casos de teste
- Regras de negócio
- Registro e acompanhamento de bugs
- Resumo executivo de QA
- Evidências de execução e resultados

Os arquivos e as evidências serão organizados neste repositório à medida que a preparação do portfólio avançar.

## Estrutura planejada

```text
gestao-chamados-qa-senatec/
├── programa/
├── qa/
├── documentacao/
├── evidencias/
└── README.md
```

## Objetivos de aprendizagem

Este projeto demonstra a prática de organização de testes manuais, registro de resultados, identificação de falhas, rastreabilidade entre testes e bugs e documentação de QA utilizando ferramentas de gestão de projetos.

O desenvolvimento do aplicativo também envolve programação em Python, persistência de dados com SQLite e empacotamento para Windows.

## Status do projeto

- Aplicação desenvolvida.
- Primeiro ciclo de testes registrado.
- Bugs identificados e documentados.
- Documentação de QA organizada no Jira.
- Preparação do portfólio no GitHub em andamento.
