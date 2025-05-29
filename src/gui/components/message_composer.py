import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext, filedialog

class MessageComposerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        
        # Variáveis
        self.subject_var = ttk.StringVar()
        self.is_html = ttk.BooleanVar(value=False)
        self.html_file_path = ttk.StringVar()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets do frame de composição"""
        # Título
        title = ttk.Label(
            self,
            text="Composição da Mensagem",
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(fill=X, pady=(0, 20))
        
        # Frame do assunto
        subject_frame = ttk.Frame(self)
        subject_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Label(
            subject_frame,
            text="Assunto:",
            width=10
        ).pack(side=LEFT)
        
        ttk.Entry(
            subject_frame,
            textvariable=self.subject_var
        ).pack(side=LEFT, fill=X, expand=True)
        
        # Frame HTML
        html_frame = ttk.Frame(self)
        html_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Checkbutton(
            html_frame,
            text="Usar HTML",
            variable=self.is_html,
            command=self._toggle_html,
            bootstyle="round-toggle"
        ).pack(side=LEFT)
        
        self.html_entry = ttk.Entry(
            html_frame,
            textvariable=self.html_file_path,
            state=DISABLED
        )
        self.html_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        
        self.browse_button = ttk.Button(
            html_frame,
            text="Procurar",
            command=self._browse_html,
            state=DISABLED,
            bootstyle="info-outline",
            width=15
        )
        self.browse_button.pack(side=LEFT)
        
        # Área de texto
        self.message_text = scrolledtext.ScrolledText(
            self,
            wrap=WORD,
            height=20,
            font=('Segoe UI', 10)
        )
        self.message_text.pack(fill=BOTH, expand=True, pady=10)
        
        # Botões
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Button(
            buttons_frame,
            text="Visualizar",
            command=self._preview_message,
            bootstyle="info-outline",
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Limpar",
            command=self._clear_message,
            bootstyle="danger-outline",
            width=15
        ).pack(side=LEFT, padx=5)
    
    def _toggle_html(self):
        """Alterna entre modo HTML e texto plano"""
        if self.is_html.get():
            self.html_entry.configure(state=NORMAL)
            self.browse_button.configure(state=NORMAL)
        else:
            self.html_entry.configure(state=DISABLED)
            self.browse_button.configure(state=DISABLED)
            self.html_file_path.set('')
    
    def _browse_html(self):
        """Abre diálogo para selecionar arquivo HTML"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ('Arquivos HTML', '*.html'),
                ('Todos os arquivos', '*.*')
            ]
        )
        if file_path:
            self.html_file_path.set(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.message_text.delete('1.0', END)
                    self.message_text.insert('1.0', f.read())
            except Exception as e:
                # TODO: Melhorar tratamento de erro
                print(f"Erro ao ler arquivo HTML: {e}")
    
    def _preview_message(self):
        """Abre janela de preview da mensagem"""
        # TODO: Implementar preview
        pass
    
    def _clear_message(self):
        """Limpa todos os campos da mensagem"""
        self.subject_var.set('')
        self.is_html.set(False)
        self.html_file_path.set('')
        self.message_text.delete('1.0', END)
        self._toggle_html() 