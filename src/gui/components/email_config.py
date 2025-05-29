import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class EmailConfigFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        
        # Variáveis
        self.email_var = ttk.StringVar()
        self.password_var = ttk.StringVar()
        self.smtp_server = ttk.StringVar(value='smtp.gmail.com')
        self.smtp_port = ttk.StringVar(value='587')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets do frame de configuração"""
        # Título
        title = ttk.Label(
            self,
            text="Configurações de Email",
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(fill=X, pady=(0, 20))
        
        # Container para os campos
        fields = ttk.Frame(self)
        fields.pack(fill=X)
        
        # Email
        email_frame = ttk.Frame(fields)
        email_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            email_frame,
            text="Email:",
            width=15
        ).pack(side=LEFT)
        
        ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            width=40
        ).pack(side=LEFT, fill=X, expand=True)
        
        # Senha
        password_frame = ttk.Frame(fields)
        password_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            password_frame,
            text="Senha:",
            width=15
        ).pack(side=LEFT)
        
        ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="•",
            width=40
        ).pack(side=LEFT, fill=X, expand=True)
        
        # Servidor SMTP
        smtp_frame = ttk.Frame(fields)
        smtp_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            smtp_frame,
            text="Servidor SMTP:",
            width=15
        ).pack(side=LEFT)
        
        ttk.Entry(
            smtp_frame,
            textvariable=self.smtp_server,
            width=40
        ).pack(side=LEFT, fill=X, expand=True)
        
        # Porta
        port_frame = ttk.Frame(fields)
        port_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            port_frame,
            text="Porta:",
            width=15
        ).pack(side=LEFT)
        
        ttk.Entry(
            port_frame,
            textvariable=self.smtp_port,
            width=10
        ).pack(side=LEFT)
        
        # Botões
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=X, pady=20)
        
        ttk.Button(
            buttons_frame,
            text="Testar Conexão",
            command=self._test_connection,
            bootstyle="info-outline",
            width=20
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Restaurar Padrão",
            command=self._restore_defaults,
            bootstyle="secondary-outline",
            width=20
        ).pack(side=LEFT, padx=5)
    
    def _test_connection(self):
        """Testa a conexão com o servidor SMTP"""
        # TODO: Implementar teste de conexão
        pass
    
    def _restore_defaults(self):
        """Restaura as configurações padrão"""
        self.smtp_server.set('smtp.gmail.com')
        self.smtp_port.set('587') 