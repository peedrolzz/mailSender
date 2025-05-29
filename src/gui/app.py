import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .components.email_config import EmailConfigFrame
from .components.recipients_list import RecipientsFrame
from .components.message_composer import MessageComposerFrame
from .components.log_viewer import LogViewerFrame
from .themes.custom_styles import apply_custom_styles

class MailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MailSender")
        self.root.geometry("1200x800")
        
        # Aplicar estilos personalizados
        self.style = ttk.Style()
        apply_custom_styles(self.style)
        
        # Container principal usando Notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Configurações
        self.config_tab = EmailConfigFrame(self.notebook)
        self.notebook.add(self.config_tab, text="Configurações")
        
        # Aba de Destinatários
        self.recipients_tab = RecipientsFrame(self.notebook)
        self.notebook.add(self.recipients_tab, text="Destinatários")
        
        # Aba de Composição
        self.composer_tab = MessageComposerFrame(self.notebook)
        self.notebook.add(self.composer_tab, text="Composição")
        
        # Aba de Log
        self.log_tab = LogViewerFrame(self.notebook)
        self.notebook.add(self.log_tab, text="Log")
        
        # Barra de status
        self.status_bar = ttk.Label(
            root,
            text="Pronto",
            relief=SUNKEN,
            padding=5
        )
        self.status_bar.pack(side=BOTTOM, fill=X)
    
    def update_status(self, message):
        """Atualiza a mensagem na barra de status"""
        self.status_bar.config(text=message)
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop() 