"""
Notificação nativa do Windows avisando que o relatório está pronto.

Usa o winotify em vez do plyer: o plyer não conseguia mudar o nome que
aparece na notificação (sempre saía "Python"), porque o Windows exige um
"app id" registrado para mostrar um nome customizado. O winotify cuida
desse registro sozinho.

Requisitos: pip install winotify
"""

from config import NOME_APP, ICONE_PATH

try:
    from winotify import Notification
except ImportError:
    Notification = None


def notificar(titulo, mensagem):
    """Mostra uma notificação no PC, com o nome e a logo da Senatec.
    Se a biblioteca não estiver instalada, só imprime no terminal
    (não trava o programa)."""
    if Notification is None:
        print(f"[notificação indisponível — instale 'winotify'] {titulo}: {mensagem}")
        return
    try:
        toast = Notification(
            app_id=NOME_APP,
            title=titulo,
            msg=mensagem,
            icon=ICONE_PATH,
        )
        toast.show()
    except Exception as erro:
        print("[notificação] falha ao mostrar:", erro)
