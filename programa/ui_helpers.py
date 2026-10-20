"""
Elementos visuais auxiliares do Gestão de Chamados Senatec:
imagens com cantos arredondados e os cartões de indicador do cabeçalho.
"""

import tkinter as tk

from PIL import Image, ImageDraw

from config import RAIO_CARTAO


def imagem_cantos_arredondados(caminho, tamanho, raio):
    """Abre uma imagem e devolve uma versão com cantos arredondados (com transparência)."""
    img = Image.open(caminho).convert("RGBA").resize(tamanho, Image.LANCZOS)
    mascara = Image.new("L", tamanho, 0)
    desenho = ImageDraw.Draw(mascara)
    desenho.rounded_rectangle([(0, 0), (tamanho[0] - 1, tamanho[1] - 1)], radius=raio, fill=255)
    img.putalpha(mascara)
    return img


def desenhar_retangulo_arredondado(canvas, x1, y1, x2, y2, raio, **kwargs):
    pontos = [
        x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
        x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
        x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1,
    ]
    return canvas.create_polygon(pontos, smooth=True, **kwargs)


class CartaoIndicador(tk.Canvas):
    """Cartãozinho colorido, com cantos arredondados, para os contadores do cabeçalho."""

    def __init__(self, parent, cor_fundo, cor_hex, largura=92, altura=56):
        super().__init__(parent, width=largura, height=altura, highlightthickness=0, bg=cor_fundo)
        desenhar_retangulo_arredondado(self, 1, 1, largura - 1, altura - 1, RAIO_CARTAO,
                                        fill=cor_hex, outline=cor_hex)
        self.item_valor = self.create_text(largura / 2, altura / 2 - 9, text="0",
                                            font=("Segoe UI", 14, "bold"), fill="white")
        self.item_label = self.create_text(largura / 2, altura / 2 + 12, text="",
                                            font=("Segoe UI", 8), fill="white")

    def set_valor(self, valor, texto_label):
        self.itemconfig(self.item_valor, text=str(valor))
        self.itemconfig(self.item_label, text=texto_label)
