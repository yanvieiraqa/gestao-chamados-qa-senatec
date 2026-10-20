
# Projeto de Garantia da Qualidade (QA)

Esta pasta reúne os materiais relacionados aos testes de software da aplicação Gestão de Chamados Senatec, desenvolvida em Python com banco de dados SQLite.

## Objetivo

Avaliar as principais funcionalidades do sistema por meio de testes manuais, registrar os resultados, identificar falhas e manter a rastreabilidade entre casos de teste e bugs.

## Escopo dos testes

O projeto contempla sete grupos funcionais:

1. Cadastro de chamados
2. Listas por status e botões de ação
3. Edição de chamados
4. Exclusão de chamados
5. Visualização de chamados por região
6. Relatórios, notificações e alertas
7. Gravação de dados e backup

## Resultados da primeira execução

| Indicador | Resultado |
|---|---:|
| Casos de teste executados | 44 |
| Aprovados | 36 |
| Reprovados | 8 |
| Bugs registrados | 8 |

Os resultados correspondem à primeira execução dos testes. Os oito bugs foram registrados no Jira e relacionados aos respectivos casos de teste.

## Reteste

A Sprint 2 — Reteste foi preparada para organizar a verificação futura das correções. Ela permanece sem iniciar, e os bugs continuam com status "A fazer", pois ainda aguardam correção.

## Ferramentas utilizadas

- Jira: gerenciamento dos casos de teste, resultados, bugs e planejamento do reteste.
- GitHub: organização e apresentação dos materiais do projeto.
- Python e SQLite: tecnologias utilizadas na aplicação testada.

## Materiais relacionados

- [Código-fonte da aplicação](../programa/)
- [Documentação do projeto](../documentacao/)
- [Evidências do projeto](../evidencias/)

O catálogo atualizado dos 44 casos de teste e as evidências selecionadas serão adicionados ao repositório após a conclusão dessa etapa.
