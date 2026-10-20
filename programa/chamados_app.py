"""
Gestão de Chamados Senatec
---------------------------
Aplicativo de cadastro e acompanhamento de chamados de atendimento,
organizados por status e localização.

Requisitos: pip install ttkbootstrap pillow reportlab plyer

Arquivos que trabalham junto com este (todos precisam estar na mesma pasta):
  config.py          -> configurações e constantes
  database.py        -> acesso ao banco de dados (ChamadosDB)
  ui_helpers.py       -> logo arredondada e cartões do cabeçalho
  relatorio_pdf.py    -> gera o relatório de chamados em aberto em PDF
  notificacao.py      -> mostra o aviso no PC quando o relatório fica pronto
  senatec_logo.png   -> logo da empresa
"""

import os 
import csv
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets import DateEntry
from PIL import ImageTk

from config import (
    TEMA, NOME_APP, LOGO_PATH, ICONE_PATH, LOGO_TAMANHO, RAIO_LOGO, ALTURA_LINHA_TABELA,
    DIAS_ALERTA_PENDENTE, PRIORIDADES, STATUS_INFO, COLUNAS,
    PASTA_RELATORIOS, HORA_RELATORIO, MINUTO_RELATORIO, ARQUIVO_ULTIMO_RELATORIO,
)
from database import ChamadosDB
from ui_helpers import imagem_cantos_arredondados, CartaoIndicador
from relatorio_pdf import gerar_pdf_relatorio
from notificacao import notificar


# ----------------------------------------------------------------------
# INTERFACE
# ----------------------------------------------------------------------

class App(ttk.Window): 
    def __init__(self):
        super().__init__(themename=TEMA)
        self.title(NOME_APP)
        self.geometry("1300x780")
        self.minsize(1050, 640)
        self._abrir_maximizado()
        self._definir_icone()

        self.db = ChamadosDB()
        self.db.backup()
        self.chamado_em_edicao = None  # id do chamado sendo editado, ou None

        self._configurar_estilo_tabela()
        self._montar_layout()
        self.atualizar_tudo()
        self._verificar_envio_automatico()  # liga o "relógio" que checa a hora de gerar o relatório

    # ------------------------------------------------------------------
    # ESTILO
    # ------------------------------------------------------------------

    def _configurar_estilo_tabela(self):
        """Deixa as linhas das listas mais altas e mais fáceis de ler."""
        estilo = self.style
        estilo.configure("Treeview", rowheight=ALTURA_LINHA_TABELA, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # ------------------------------------------------------------------
    # LAYOUT GERAL
    # ------------------------------------------------------------------

    def _montar_layout(self):
        self._montar_cabecalho()

        self._montar_rodape()  # empacotado antes para reservar o espaço embaixo

        self.notebook = ttk.Notebook(self, bootstyle=PRIMARY)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.frame_form = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.frame_form, text="  Novo Chamado  ")
        self._montar_formulario(self.frame_form)

        self.trees = {}
        self._montar_aba_listagem("Pendente", "  Pendentes  ")
        self._montar_aba_listagem("Atendido", "  Atendidos  ")
        self._montar_aba_listagem("Cancelado", "  Cancelados  ")
        self._montar_aba_regiao()

    def _montar_rodape(self):
        rodape = ttk.Frame(self, padding=(20, 2, 20, 14))
        rodape.pack(side="bottom", fill="x")
        ttk.Label(
            rodape, text="Feito por Yan Vieira", font=("Segoe UI", 9, "bold"), bootstyle=SECONDARY
        ).pack(side="right")

    def _montar_cabecalho(self):
        topo = ttk.Frame(self, padding=(20, 16, 20, 8))
        topo.pack(fill="x")
        cor_fundo = str(self.style.colors.bg)

        titulo_frame = ttk.Frame(topo)
        titulo_frame.pack(side="left")
        self._carregar_logo(titulo_frame)

        texto_frame = ttk.Frame(titulo_frame)
        texto_frame.pack(side="left")
        ttk.Label(texto_frame, text=NOME_APP, font=("Segoe UI", 20, "bold")).pack(anchor="w")
        self.label_alerta = ttk.Label(texto_frame, text="", font=("Segoe UI", 9), bootstyle=DANGER)
        self.label_alerta.pack(anchor="w")

        self.cards_frame = ttk.Frame(topo)
        self.cards_frame.pack(side="right")
        self.card_widgets = {}
        for status, (cor_nome, _tint) in STATUS_INFO.items():
            cor_hex = self.style.colors.get(cor_nome)
            cartao = CartaoIndicador(self.cards_frame, cor_fundo, cor_hex)
            cartao.pack(side="left", padx=6)
            self.card_widgets[status] = cartao

        ttk.Button(topo, text="Abrir Pasta de Relatórios", bootstyle=(SECONDARY, OUTLINE),
                   command=self._abrir_pasta_relatorios).pack(side="right", padx=(0, 8))

        ttk.Button(topo, text="Gerar Relatório em PDF", bootstyle=(SECONDARY, OUTLINE),
                   command=lambda: self._gerar_relatorio(automatico=False)).pack(side="right", padx=(0, 8))

        ttk.Separator(self).pack(fill="x")

    def _carregar_logo(self, container):
        """Mostra a logo da Senatec (com cantos arredondados) no cabeçalho, se existir."""
        if not os.path.exists(LOGO_PATH):
            print(f"[logo] arquivo não encontrado em: {LOGO_PATH}")
            print("[logo] coloque o 'senatec_logo.png' na mesma pasta do chamados_app.py")
            return
        try:
            imagem = imagem_cantos_arredondados(LOGO_PATH, LOGO_TAMANHO, RAIO_LOGO)
            self.logo_img = ImageTk.PhotoImage(imagem)  # referência guardada para não sumir
            ttk.Label(container, image=self.logo_img).pack(side="left", padx=(0, 12))
        except Exception as erro:
            print("[logo] falha ao carregar a imagem:", erro)

    def _abrir_maximizado(self):
        """Abre o programa já ocupando a tela toda, pra não cortar os botões
        de baixo das listas quando a janela abre pequena."""
        try:
            self.state("zoomed")  # funciona no Windows
        except Exception:
            try:
                self.attributes("-zoomed", True)  # alternativa para Linux
            except Exception:
                pass  # se nada funcionar, fica no tamanho padrão mesmo

    def _definir_icone(self):
        """Coloca a logo da Senatec como ícone da janela e da barra de tarefas."""
        if os.path.exists(ICONE_PATH):
            try:
                self.iconbitmap(ICONE_PATH)
            except Exception as erro:
                print("[ícone] não foi possível aplicar o senatec_logo.ico:", erro)
        else:
            print(f"[ícone] arquivo não encontrado em: {ICONE_PATH}")

    def _abrir_pasta_relatorios(self):
        """Abre a pasta 'relatorios' no explorador de arquivos do sistema."""
        os.makedirs(PASTA_RELATORIOS, exist_ok=True)
        try:
            sistema = platform.system()
            if sistema == "Windows":
                os.startfile(PASTA_RELATORIOS)
            elif sistema == "Darwin":
                subprocess.Popen(["open", PASTA_RELATORIOS])
            else:
                subprocess.Popen(["xdg-open", PASTA_RELATORIOS])
        except Exception as erro:
            Messagebox.show_error(f"Não foi possível abrir a pasta:\n\n{erro}", "Erro")

    # ------------------------------------------------------------------
    # ABA: NOVO CHAMADO / EDIÇÃO
    # ------------------------------------------------------------------

    def _montar_formulario(self, frame):
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        self.form_title = ttk.Label(frame, text="Novo Chamado", font=("Segoe UI", 14, "bold"))
        self.form_title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 16))

        def campo(label, row, col, widget, colspan=1):
            ttk.Label(frame, text=label, font=("Segoe UI", 9, "bold")).grid(
                row=row, column=col, sticky="w", padx=(0, 8), pady=(8, 2))
            widget.grid(row=row + 1, column=col, columnspan=colspan, sticky="ew", padx=(0, 24), pady=(0, 4))

        self.entry_cliente = ttk.Entry(frame)
        campo("Cliente", 1, 0, self.entry_cliente)
        self.entry_cliente.bind("<FocusOut>", self._preencher_local_automatico)

        self.entry_contrato = ttk.Entry(frame)
        campo("Contrato", 1, 1, self.entry_contrato)
        self.entry_contrato.bind("<FocusOut>", self._preencher_local_automatico)

        self.combo_local = ttk.Combobox(frame, values=self.db.locais_conhecidos())
        campo("Local / Bairro / Cidade", 3, 0, self.combo_local)

        self.data_chegada = DateEntry(frame, dateformat="%d/%m/%Y", bootstyle=PRIMARY)
        campo("Data que o chamado chegou", 3, 1, self.data_chegada)

        self.combo_prioridade = ttk.Combobox(frame, values=PRIORIDADES, state="readonly")
        self.combo_prioridade.set("Normal")
        campo("Prioridade", 5, 0, self.combo_prioridade)

        self.entry_tecnico = ttk.Entry(frame)
        campo("Técnico responsável (opcional)", 5, 1, self.entry_tecnico)

        self.entry_equipamento = ttk.Entry(frame)
        campo("Equipamento", 7, 0, self.entry_equipamento)

        self.entry_quantidade = ttk.Entry(frame)
        campo("Quantidade", 7, 1, self.entry_quantidade)

        self.entry_descricao = ttk.Entry(frame)
        campo("Descrição do chamado", 9, 0, self.entry_descricao, colspan=2)

        self.combo_status = ttk.Combobox(frame, values=list(STATUS_INFO), state="readonly")
        self.combo_status.set("Pendente")
        campo("Status", 11, 0, self.combo_status)

        botoes = ttk.Frame(frame)
        botoes.grid(row=13, column=0, columnspan=2, sticky="w", pady=(20, 0))

        self.btn_salvar = ttk.Button(botoes, text="Salvar Chamado", bootstyle=SUCCESS, command=self._salvar)
        self.btn_salvar.pack(side="left", padx=(0, 8))

        self.btn_cancelar_edicao = ttk.Button(
            botoes, text="Cancelar Edição", bootstyle=(SECONDARY, OUTLINE), command=self._cancelar_edicao
        )
        # só aparece durante edição (pack é chamado em _carregar_para_edicao)

    def _preencher_local_automatico(self, event=None):
        cliente = self.entry_cliente.get().strip()
        contrato = self.entry_contrato.get().strip()
        if cliente and contrato and not self.combo_local.get():
            local = self.db.ultimo_local(cliente, contrato)
            if local:
                self.combo_local.set(local)

    def _ler_formulario(self):
        return {
            "cliente": self.entry_cliente.get().strip(),
            "contrato": self.entry_contrato.get().strip(),
            "local": self.combo_local.get().strip(),
            "descricao": self.entry_descricao.get().strip(),
            "equipamento": self.entry_equipamento.get().strip(),
            "quantidade": self.entry_quantidade.get().strip(),
            "prioridade": self.combo_prioridade.get().strip() or "Normal",
            "tecnico": self.entry_tecnico.get().strip(),
            "status": self.combo_status.get().strip(),
            "data_abertura": self.data_chegada.entry.get().strip(),
        }

    def _salvar(self):
        dados = self._ler_formulario()

        obrigatorios = ["cliente", "contrato", "local", "descricao", "equipamento",
                         "quantidade", "status", "data_abertura"]
        if not all(dados[campo] for campo in obrigatorios):
            Messagebox.show_error("Preencha todos os campos obrigatórios antes de salvar.", "Campos obrigatórios")
            return

        try:
            dados["quantidade"] = int(dados["quantidade"])
        except ValueError:
            Messagebox.show_error("Quantidade deve ser um número inteiro.", "Valor inválido")
            return

        if self.chamado_em_edicao is None:
            self.db.inserir(dados)
            Messagebox.show_info("Chamado cadastrado com sucesso.", "Sucesso")
        else:
            self.db.atualizar(self.chamado_em_edicao, dados)
            Messagebox.show_info("Chamado atualizado com sucesso.", "Sucesso")
            self._cancelar_edicao()

        self._limpar_formulario()
        self.atualizar_tudo()

    def _limpar_formulario(self):
        self.entry_cliente.delete(0, "end")
        self.entry_contrato.delete(0, "end")
        self.combo_local.set("")
        self.entry_descricao.delete(0, "end")
        self.entry_equipamento.delete(0, "end")
        self.entry_quantidade.delete(0, "end")
        self.entry_tecnico.delete(0, "end")
        self.combo_prioridade.set("Normal")
        self.combo_status.set("Pendente")
        self.data_chegada.entry.delete(0, "end")
        self.data_chegada.entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.combo_local["values"] = self.db.locais_conhecidos()

    def _carregar_para_edicao(self, chamado):
        (cid, cliente, contrato, local, descricao, equipamento, quantidade,
         prioridade, tecnico, status, abertura) = chamado

        self.chamado_em_edicao = cid
        self.entry_cliente.delete(0, "end"); self.entry_cliente.insert(0, cliente)
        self.entry_contrato.delete(0, "end"); self.entry_contrato.insert(0, contrato)
        self.combo_local.set(local)
        self.entry_descricao.delete(0, "end"); self.entry_descricao.insert(0, descricao)
        self.entry_equipamento.delete(0, "end"); self.entry_equipamento.insert(0, equipamento)
        self.entry_quantidade.delete(0, "end"); self.entry_quantidade.insert(0, quantidade)
        self.entry_tecnico.delete(0, "end"); self.entry_tecnico.insert(0, tecnico or "")
        self.combo_prioridade.set(prioridade or "Normal")
        self.combo_status.set(status)
        self.data_chegada.entry.delete(0, "end")
        self.data_chegada.entry.insert(0, abertura or datetime.now().strftime("%d/%m/%Y"))

        self.form_title.config(text=f"Editando Chamado #{cid}")
        self.btn_cancelar_edicao.pack(side="left")
        self.notebook.select(self.frame_form)

    def _cancelar_edicao(self):
        self.chamado_em_edicao = None
        self.form_title.config(text="Novo Chamado")
        self.btn_cancelar_edicao.pack_forget()
        self._limpar_formulario()

    # ------------------------------------------------------------------
    # ABAS DE STATUS (Pendentes / Atendidos / Cancelados)
    # ------------------------------------------------------------------

    def _montar_aba_listagem(self, status, titulo):
        frame = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(frame, text=titulo)

        barra = ttk.Frame(frame)
        barra.pack(fill="x", pady=(0, 10))
        ttk.Label(barra, text="Buscar:").pack(side="left", padx=(0, 6))
        busca_var = ttk.StringVar()
        ttk.Entry(barra, textvariable=busca_var, width=40).pack(side="left")
        busca_var.trace_add("write", lambda *_: self._atualizar_tabela(status, tree, busca_var.get()))

        tree = self._criar_tabela(frame)
        tree.bind("<Double-1>", lambda e, t=tree: self._editar_selecionado(t))
        self.trees[status] = tree

        acoes = ttk.Frame(frame)
        acoes.pack(fill="x", pady=(10, 0))

        ttk.Button(acoes, text="Editar", bootstyle=(INFO, OUTLINE),
                   command=lambda t=tree: self._editar_selecionado(t)).pack(side="left", padx=(0, 6))

        if status != "Atendido":
            ttk.Button(acoes, text="Marcar como Atendido", bootstyle=SUCCESS,
                       command=lambda t=tree: self._marcar_status(t, "Atendido")).pack(side="left", padx=6)
        if status != "Cancelado":
            ttk.Button(acoes, text="Marcar como Cancelado", bootstyle=DANGER,
                       command=lambda t=tree: self._marcar_status(t, "Cancelado")).pack(side="left", padx=6)

        ttk.Button(acoes, text="Excluir", bootstyle=(SECONDARY, OUTLINE),
                   command=lambda t=tree: self._excluir_selecionado(t)).pack(side="right")

    def _criar_tabela(self, frame):
        tree = ttk.Treeview(frame, columns=COLUNAS, show="headings", bootstyle=PRIMARY, height=16)
        larguras = {"ID": 40, "Cliente": 130, "Contrato": 85, "Local": 120, "Descrição": 190,
                    "Equipamento": 120, "Qtd": 45, "Prioridade": 80, "Técnico": 100,
                    "Status": 85, "Abertura": 100}
        for col in COLUNAS:
            tree.heading(col, text=col, anchor="w")
            tree.column(col, width=larguras.get(col, 100), anchor="w")
        for status, (_cor, tint) in STATUS_INFO.items():
            tree.tag_configure(status, background=tint)
        tree.pack(fill="both", expand=True)
        return tree

    # ------------------------------------------------------------------
    # ABA: TODOS / FILTRO POR REGIÃO
    # ------------------------------------------------------------------

    def _montar_aba_regiao(self):
        frame = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(frame, text="  Todos / Por Região  ")

        painel_esquerda = ttk.Frame(frame)
        painel_esquerda.pack(side="left", fill="y", padx=(0, 16))

        ttk.Label(painel_esquerda, text="Bairros / Regiões", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(painel_esquerda, text="Selecione os bairros da rota do dia:",
                  font=("Segoe UI", 8), bootstyle=SECONDARY).pack(anchor="w", pady=(0, 6))

        self.lista_bairros = tk.Listbox(painel_esquerda, selectmode="multiple", exportselection=False,
                                         height=16, width=24, activestyle="none")
        self.lista_bairros.pack(fill="y")
        self._recarregar_lista_bairros()

        ttk.Button(painel_esquerda, text="Aplicar Filtro", bootstyle=PRIMARY,
                   command=self._aplicar_filtro_regiao).pack(fill="x", pady=(8, 4))
        ttk.Button(painel_esquerda, text="Limpar Filtro", bootstyle=(SECONDARY, OUTLINE),
                   command=self._limpar_filtro_regiao).pack(fill="x")

        painel_direita = ttk.Frame(frame)
        painel_direita.pack(side="left", fill="both", expand=True)

        barra = ttk.Frame(painel_direita)
        barra.pack(fill="x", pady=(0, 10))
        ttk.Label(barra, text="Buscar:").pack(side="left", padx=(0, 6))
        self.busca_regiao_var = ttk.StringVar()
        ttk.Entry(barra, textvariable=self.busca_regiao_var, width=30).pack(side="left", padx=(0, 12))
        self.busca_regiao_var.trace_add("write", lambda *_: self._aplicar_filtro_regiao())

        ttk.Button(barra, text="Exportar CSV", bootstyle=(SUCCESS, OUTLINE),
                   command=lambda: self._exportar_csv(self.tree_regiao)).pack(side="right")

        tree = self._criar_tabela(painel_direita)
        tree.bind("<Double-1>", lambda e, t=tree: self._editar_selecionado(t))
        self.tree_regiao = tree
        self.trees[None] = tree  # None = sem filtro de status, usado no atualizar_tudo()

        acoes = ttk.Frame(painel_direita)
        acoes.pack(fill="x", pady=(10, 0))
        ttk.Button(acoes, text="Editar", bootstyle=(INFO, OUTLINE),
                   command=lambda: self._editar_selecionado(tree)).pack(side="left", padx=(0, 6))
        ttk.Button(acoes, text="Excluir", bootstyle=(SECONDARY, OUTLINE),
                   command=lambda: self._excluir_selecionado(tree)).pack(side="left")

    def _recarregar_lista_bairros(self):
        self.lista_bairros.delete(0, "end")
        for local in self.db.locais_conhecidos():
            self.lista_bairros.insert("end", local)

    def _bairros_selecionados(self):
        return [self.lista_bairros.get(i) for i in self.lista_bairros.curselection()]

    def _aplicar_filtro_regiao(self):
        bairros = self._bairros_selecionados()
        termo = self.busca_regiao_var.get()
        self._atualizar_tabela(None, self.tree_regiao, termo=termo, locais=bairros or None)

    def _limpar_filtro_regiao(self):
        self.lista_bairros.selection_clear(0, "end")
        self.busca_regiao_var.set("")
        self._atualizar_tabela(None, self.tree_regiao)

    def _exportar_csv(self, tree):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")],
            initialfile="chamados.csv",
            title="Exportar chamados para CSV"
        )
        if not caminho:
            return
        linhas = [tree.item(i)["values"] for i in tree.get_children()]
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(COLUNAS)
            escritor.writerows(linhas)
        Messagebox.show_info(f"{len(linhas)} chamado(s) exportado(s) com sucesso.", "Exportação concluída")

    # ------------------------------------------------------------------
    # AÇÕES SOBRE LINHAS SELECIONADAS
    # ------------------------------------------------------------------

    def _linha_selecionada_id(self, tree):
        selecionado = tree.selection()
        if not selecionado:
            Messagebox.show_warning("Selecione um chamado na lista primeiro.", "Nenhum chamado selecionado")
            return None
        return tree.item(selecionado)["values"][0]

    def _editar_selecionado(self, tree):
        chamado_id = self._linha_selecionada_id(tree)
        if chamado_id is None:
            return
        row = self.db.conn.execute(
            """SELECT id, cliente, contrato, local, descricao, equipamento, quantidade,
                      prioridade, tecnico, status, data_abertura FROM chamados WHERE id=?""",
            (chamado_id,)
        ).fetchone()
        if row:
            self._carregar_para_edicao(row)

    def _marcar_status(self, tree, novo_status):
        chamado_id = self._linha_selecionada_id(tree)
        if chamado_id is None:
            return
        self.db.alterar_status(chamado_id, novo_status)
        self.atualizar_tudo()

    def _excluir_selecionado(self, tree):
        chamado_id = self._linha_selecionada_id(tree)
        if chamado_id is None:
            return
        if Messagebox.yesno(f"Excluir o chamado #{chamado_id} permanentemente?", "Confirmar exclusão") == "Yes":
            self.db.excluir(chamado_id)
            self.atualizar_tudo()

    # ------------------------------------------------------------------
    # ATUALIZAÇÃO DE DADOS NA TELA
    # ------------------------------------------------------------------

    def _atualizar_tabela(self, status, tree, termo="", locais=None):
        for item in tree.get_children():
            tree.delete(item)
        for row in self.db.buscar(status=status, termo=termo or None, locais=locais):
            tree.insert("", "end", values=row, tags=(row[9],))  # row[9] = status, define a cor da linha

    def _atualizar_cartoes(self):
        contagem = self.db.contagem_por_status()
        for status, cartao in self.card_widgets.items():
            cartao.set_valor(contagem.get(status, 0), status)

        atrasados = self.db.pendentes_atrasados()
        if atrasados:
            self.label_alerta.config(
                text=f"⚠ {atrasados} chamado(s) pendente(s) há mais de {DIAS_ALERTA_PENDENTE} dias")
        else:
            self.label_alerta.config(text="")

    def atualizar_tudo(self):
        for status, tree in self.trees.items():
            if tree is self.tree_regiao:
                continue  # a aba de região respeita o filtro de bairro escolhido
            self._atualizar_tabela(status, tree)
        self._aplicar_filtro_regiao()
        self._atualizar_cartoes()
        self._recarregar_lista_bairros()

    # ------------------------------------------------------------------
    # RELATÓRIO DIÁRIO EM PDF (chamados em aberto, todo dia às 17h)
    # ------------------------------------------------------------------

    def _ja_gerado_hoje(self):
        if not os.path.exists(ARQUIVO_ULTIMO_RELATORIO):
            return False
        with open(ARQUIVO_ULTIMO_RELATORIO, encoding="utf-8") as arquivo:
            return arquivo.read().strip() == datetime.now().strftime("%Y-%m-%d")

    def _marcar_gerado_hoje(self):
        with open(ARQUIVO_ULTIMO_RELATORIO, "w", encoding="utf-8") as arquivo:
            arquivo.write(datetime.now().strftime("%Y-%m-%d"))

    def _verificar_envio_automatico(self):
        """Roda a cada minuto; às 17h gera o PDF do relatório automaticamente."""
        agora = datetime.now()
        se_e_hora = agora.hour == HORA_RELATORIO and agora.minute >= MINUTO_RELATORIO
        if se_e_hora and not self._ja_gerado_hoje():
            self._gerar_relatorio(automatico=True)
        self.after(60_000, self._verificar_envio_automatico)  # checa de novo em 1 minuto

    def _gerar_relatorio(self, automatico=True):
        pendentes = self.db.buscar(status="Pendente")

        def tarefa():
            try:
                caminho_pdf = gerar_pdf_relatorio(pendentes)
                self._marcar_gerado_hoje()
                notificar(
                    "Relatório de chamados pronto",
                    f"{len(pendentes)} chamado(s) em aberto. Já pode enviar pelo WhatsApp.",
                )
                if not automatico:
                    self.after(0, lambda: Messagebox.show_info(
                        f"Relatório gerado em:\n{caminho_pdf}", "Relatório pronto"
                    ))
            except Exception as erro:
                print("Erro ao gerar o relatório em PDF:", erro)
                self.after(0, lambda: Messagebox.show_error(
                    f"Não foi possível gerar o relatório:\n\n{erro}", "Erro"
                ))

        # roda em segundo plano para não travar a janela do app
        threading.Thread(target=tarefa, daemon=True).start()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
