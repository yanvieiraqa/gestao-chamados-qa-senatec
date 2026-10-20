GESTÃO DE CHAMADOS SENATEC
===========================

COMO RODAR (pelo VS Code / Python)
-----------------------------------
1. Deixe TODOS os arquivos desta pasta juntos, sem mover nenhum.
2. Instale as bibliotecas necessárias (uma vez só). No terminal, dentro
   desta pasta:

   pip install ttkbootstrap pillow reportlab winotify

3. Rode o programa:

   python chamados_app.py

   O banco de dados (chamados.db), a pasta de backups e a pasta de
   relatórios em PDF são criados automaticamente aqui do lado, na
   primeira vez que você salvar um chamado ou gerar um relatório.


COMO GERAR O .EXE (programa de duplo clique, sem precisar do VS Code)
-----------------------------------------------------------------------
1. Instale o PyInstaller:

   pip install pyinstaller

2. Dentro desta pasta, rode:

   pyinstaller --onefile --windowed --icon=senatec_logo.ico --name "GestaoChamadosSenatec" --collect-all ttkbootstrap chamados_app.py

3. Isso cria uma pasta "dist" com o GestaoChamadosSenatec.exe dentro.
4. Copie o senatec_logo.png, o senatec_logo.ico e o chamados.db (se já
   tiver chamados cadastrados) para DENTRO da pasta "dist", do lado do
   .exe.
5. Clique com o botão direito no .exe → Enviar para → Área de trabalho
   (criar atalho). Pronto, é só abrir por esse atalho dali em diante.


O QUE O PROGRAMA FAZ
----------------------
- Cadastro de chamados (cliente, contrato, local, equipamento,
  prioridade, técnico, status, data).
- Abas separadas de Pendentes, Atendidos, Cancelados e uma geral com
  filtro por bairro/região.
- Editar e excluir chamados direto nas listas.
- Exportar para CSV.
- Backup automático do banco de dados uma vez por dia (pasta backups/).
- Todo dia às 17h (ajustável em config.py, em HORA_RELATORIO), gera um
  PDF com os chamados em aberto (pasta relatorios/) e mostra uma
  notificação no Windows avisando que ficou pronto — depois é só você
  enviar esse PDF pra quem quiser, pelo WhatsApp por exemplo.
- Botão "Gerar Relatório em PDF" e "Abrir Pasta de Relatórios" no
  cabeçalho, pra gerar na hora e achar os arquivos rápido.


PRECISA MUDAR ALGUMA CONFIGURAÇÃO?
-------------------------------------
Abra o config.py — lá estão reunidas as coisas mais comuns de ajustar:
nome do app, horário do relatório automático, locais padrão, quantos
dias até um pendente virar "atrasado", etc.


Feito por Yan Vieira.
