"""
MailSender - Aplicação para envio de emails em lote
"""

import ttkbootstrap as ttk
from src.gui.app import MailSenderApp

def main():
    """Função principal da aplicação"""
    root = ttk.Window(
        title="MailSender",
        themename="darkly",
        size=(1200, 800),
        resizable=(True, True)
    )
    
    app = MailSenderApp(root)
    app.run()

if __name__ == '__main__':
    main() 