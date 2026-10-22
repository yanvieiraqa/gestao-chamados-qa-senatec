# Gestão de Chamados Senatec — Sistema e Projeto de QA

Projeto de desenvolvimento de um sistema de Gestão de Chamados em Python, acompanhado de um projeto de Garantia da Qualidade de Software (QA), organizado no Jira e documentado neste repositório.

O objetivo é apresentar tanto a aplicação desenvolvida quanto as atividades de planejamento, execução de testes, identificação de falhas, registro de bugs e documentação dos resultados.

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

1. **Grupo A — Cadastro de chamados**
2. **Grupo B — Listas por status e botões de ação**
3. **Grupo C — Edição de chamados**
4. **Grupo D — Exclusão de chamados**
5. **Grupo E — Visualização de chamados: Todos e Por Região**
6. **Grupo F — Relatórios, pastas, notificações e alertas**
7. **Grupo G — Gravação de dados e backup**

### Resultados da execução dos testes

| Indicador | Resultado |
|---|---:|
| Casos de teste executados | 44 |
| Testes aprovados | 35 |
| Testes reprovados | 9 |
| Bugs registrados | 9 |

Os resultados correspondem à execução inicial dos 44 casos de teste. As falhas identificadas foram documentadas por meio de registros de bugs no Jira.

O CT-006 também foi reprovado após a identificação de um comportamento inesperado na validação do campo **“Data que o chamado chegou”**, permitindo a criação de chamados com dados inválidos.

Os testes foram executados e documentados no Jira. O reteste das falhas ainda não foi realizado.

### Atividades de QA realizadas

- Organização dos casos de teste em grupos funcionais.
- Planejamento e documentação dos testes.
- Execução dos 44 casos de teste.
- Registro dos resultados obtidos.
- Identificação e documentação de bugs.
- Organização de evidências por meio de capturas de tela e vídeos.
- Anexação das evidências às respectivas tarefas no Jira.
- Elaboração do plano de testes, das regras de negócio e do resumo executivo de QA.

## Documentação

A pasta [`documentacao`](./documentacao/) reúne os documentos utilizados para planejar, executar e apresentar os resultados do projeto, incluindo:

- Plano de Testes.
- Regras de Negócio.
- Resumo Executivo de QA.
- Documentação dos casos de teste.

## Evidências

As evidências estão organizadas em duas pastas:

- [`evidencias-jira`](./evidencias-jira/) — materiais relacionados à documentação e ao acompanhamento do projeto no Jira.
- [`evidencias-casos-de-teste`](./evidencias-casos-de-teste/) — capturas de tela e vídeos dos casos de teste, organizados por grupos funcionais de A a G.

As evidências individuais dos casos de teste também estão anexadas às respectivas tarefas no Jira.

## Programa

A pasta [`programa`](./programa/) contém os arquivos disponibilizados da aplicação Gestão de Chamados Senatec.

## Ferramenta de gerenciamento

O Jira foi utilizado para organizar os casos de teste, acompanhar os resultados, registrar bugs e centralizar a documentação e as evidências.

[**Acessar o projeto QA Senatec no Jira**](https://yanvieiradecarvalho.atlassian.net/jira/software/projects/QGDCS/boards/35)

## Objetivo do portfólio

Este projeto demonstra a aplicação prática de conceitos de Garantia da Qualidade de Software, incluindo planejamento, execução de testes funcionais, documentação de resultados, identificação de falhas e registro de bugs.

O repositório foi organizado para apresentar o sistema desenvolvido e o processo de QA de forma clara, facilitando a análise do projeto por recrutadores e profissionais da área de tecnologia.
