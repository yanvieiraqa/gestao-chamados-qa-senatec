
# Gestão de Chamados Senatec — Sistema e Projeto de QA

Projeto de desenvolvimento de um sistema de Gestão de Chamados em Python, com banco de dados SQLite, acompanhado de um projeto de Garantia da Qualidade de Software (QA) organizado no Jira.

O objetivo é apresentar tanto a aplicação desenvolvida quanto as atividades de planejamento, execução, registro de falhas e documentação dos testes.

## Sobre o sistema

A aplicação permite cadastrar e acompanhar chamados, organizar registros por status e região, editar e excluir informações, exportar dados em CSV e gerar relatórios em PDF.

O sistema utiliza Python para a aplicação, SQLite para armazenamento local e Tkinter com ttkbootstrap para a interface gráfica.

## Tecnologias e ferramentas

- Python
- SQLite
- Tkinter e ttkbootstrap
- Pillow
- ReportLab
- winotify
- Jira
- GitHub
- PyInstaller para empacotamento do executável Windows

## Projeto de QA

O planejamento e o acompanhamento dos testes foram organizados no Jira, contemplando sete grupos funcionais:

1. Cadastro de chamados
2. Listas por status e botões de ação
3. Edição de chamados
4. Exclusão de chamados
5. Visualização de chamados — Todos e Por Região
6. Relatórios, pastas, notificações e alertas
7. Gravação de dados e backup

### Resultados da primeira execução

| Indicador | Resultado |
|---|---:|
| Casos de teste executados | 44 |
| Testes aprovados | 36 |
| Testes reprovados | 8 |
| Bugs registrados | 8 |

Os oito bugs foram registrados e relacionados aos casos de teste correspondentes. A Sprint 2 — Reteste foi preparada, mas permanece sem iniciar até que os problemas sejam corrigidos.

Os resultados representam a primeira execução dos testes. Os bugs ainda não são considerados resolvidos.

## Navegação pelo repositório

- [Programa — código-fonte](./programa/)
- [Projeto de QA](./qa/)
- [Documentação](./documentacao/)
- [Evidências](./evidencias/)

## Documentação disponível

A pasta de documentação reúne os materiais de planejamento e análise de QA, incluindo o Plano de Testes e as Regras de Negócio.

O catálogo dos 44 casos de teste será adicionado após a atualização do documento e a organização das evidências correspondentes.

## Projeto de QA no Jira

O Jira foi utilizado para organizar e acompanhar os casos de teste, os resultados da execução, o registro de bugs, o dashboard e o planejamento do reteste.

**Acessar o projeto:** [QA — Gestão de Chamados Senatec](https://yanvieiradecarvalho.atlassian.net/jira/software/projects/QGDCS/boards/35?filter=&groupBy=none)

O acesso ao Jira depende das permissões configuradas no projeto. Os materiais deste repositório complementam os registros disponíveis na ferramenta.

## Objetivos do projeto

Este projeto reúne prática de desenvolvimento em Python e testes manuais de software, incluindo planejamento, execução, registro de resultados, identificação de falhas, rastreabilidade e documentação de QA.

O repositório está em preparação para apresentação em portfólio profissional.
