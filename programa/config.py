"""
Configurações gerais do Gestão de Chamados Senatec.
Todas as constantes ajustáveis do programa ficam neste arquivo.
"""

import os
import sys

DB_PATH = "chamados.db"
TEMA = "flatly"  # tema claro e profissional. Alternativas: "darkly", "superhero", "cosmo"
NOME_APP = "Gestão de Chamados Senatec"

# Caminho da pasta do programa: quando rodando como .py normal, é a pasta
# deste arquivo; quando vira um .exe (gerado com o PyInstaller), é a pasta
# onde o .exe está. Sem essa diferença, o banco de dados e a logo não seriam
# encontrados depois de "empacotado".
if getattr(sys, "frozen", False):
    PASTA_APP = os.path.dirname(sys.executable)
else:
    PASTA_APP = os.path.dirname(os.path.abspath(__file__))

LOGO_PATH = os.path.join(PASTA_APP, "senatec_logo.png")
ICONE_PATH = os.path.join(PASTA_APP, "senatec_logo.ico")
BACKUP_DIR = os.path.join(PASTA_APP, "backups")
PASTA_RELATORIOS = os.path.join(PASTA_APP, "relatorios")

LOGO_TAMANHO = (56, 56)
RAIO_LOGO = 16          # arredondamento dos cantos da logo
RAIO_CARTAO = 12        # arredondamento dos cartões de indicador
ALTURA_LINHA_TABELA = 34  # altura de cada linha nas listas (padrão do ttk é ~20)
DIAS_ALERTA_PENDENTE = 7  # a partir de quantos dias um pendente vira "atrasado"

LOCAIS_PADRAO = ["Barra da Tijuca", "Leblon", "Copacabana"]
PRIORIDADES = ["Normal", "Urgente"]

# Geração automática do relatório em PDF, todo dia no horário abaixo
HORA_RELATORIO = 17   # 17h
MINUTO_RELATORIO = 0
ARQUIVO_ULTIMO_RELATORIO = os.path.join(PASTA_APP, "ultimo_relatorio_gerado.txt")

# status: (nome da cor bootstyle, cor de fundo clara para a linha da tabela)
STATUS_INFO = {
    "Pendente": ("warning", "#fff3cd"),
    "Atendido": ("success", "#d4edda"),
    "Cancelado": ("danger", "#f8d7da"),
}

COLUNAS = ("ID", "Cliente", "Contrato", "Local", "Descrição", "Equipamento",
           "Qtd", "Prioridade", "Técnico", "Status", "Abertura")
