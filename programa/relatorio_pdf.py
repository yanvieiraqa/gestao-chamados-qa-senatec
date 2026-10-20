"""
Geração do relatório de chamados em aberto em PDF.

Requisitos: pip install reportlab
"""

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from config import PASTA_RELATORIOS, NOME_APP


def gerar_pdf_relatorio(pendentes):
    """Recebe a lista de chamados pendentes (linhas do banco) e gera um PDF.
    Devolve o caminho completo do arquivo criado."""
    os.makedirs(PASTA_RELATORIOS, exist_ok=True)

    hoje = datetime.now()
    nome_arquivo = f"relatorio_chamados_{hoje.strftime('%Y-%m-%d')}.pdf"
    caminho = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    estilos = getSampleStyleSheet()
    documento = SimpleDocTemplate(caminho, pagesize=A4,
                                   topMargin=2 * cm, bottomMargin=2 * cm,
                                   leftMargin=1.5 * cm, rightMargin=1.5 * cm)
    conteudo = []

    conteudo.append(Paragraph(NOME_APP, estilos["Title"]))
    conteudo.append(Paragraph(f"Relatório de Chamados em Aberto — {hoje.strftime('%d/%m/%Y')}",
                               estilos["Heading2"]))
    conteudo.append(Paragraph(f"Total de chamados pendentes: {len(pendentes)}", estilos["Normal"]))
    conteudo.append(Spacer(1, 16))

    if not pendentes:
        conteudo.append(Paragraph("Nenhum chamado em aberto no momento. ✅", estilos["Normal"]))
    else:
        cabecalho = ["ID", "Cliente", "Contrato", "Local", "Equipamento",
                     "Qtd", "Prioridade", "Técnico", "Aberto em"]
        linhas = [cabecalho]
        for row in pendentes:
            (cid, cliente, contrato, local, descricao, equipamento,
             quantidade, prioridade, tecnico, status, abertura) = row
            linhas.append([
                str(cid), cliente, contrato, local, equipamento,
                str(quantidade), prioridade, tecnico or "-", abertura or "-",
            ])

        tabela = Table(linhas, repeatRows=1)
        estilo_tabela = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ])
        # destaca em vermelho claro as linhas com prioridade Urgente
        for indice, linha in enumerate(linhas[1:], start=1):
            if linha[6] == "Urgente":
                estilo_tabela.add("BACKGROUND", (0, indice), (-1, indice), colors.HexColor("#fde2e2"))
        tabela.setStyle(estilo_tabela)
        conteudo.append(tabela)

    documento.build(conteudo)
    return caminho
