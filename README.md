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

1. **Cadastro de chamados**
2. **Listas por status e botões de ação**
3. **Edição de chamados**
4. **Exclusão de chamados**
5. **Visualização de chamados — Todos e Por Região**
6. **Relatórios, pastas, notificações e alertas**
7. **Gravação de dados e backup**

### Resultados da execução dos testes

| Indicador | Resultado |
|---|---:|
| Casos de teste executados | 44 |
| Testes aprovados | 35 |
| Testes reprovados | 9 |
| Bugs registrados | 9 |

Os resultados correspondem à execução inicial dos 44 casos de teste. Os casos reprovados deram origem a registros de bugs para documentar as falhas identificadas.

O CT
