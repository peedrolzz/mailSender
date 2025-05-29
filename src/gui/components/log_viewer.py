import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext, filedialog
from datetime import datetime

class LogViewerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets do frame de log"""
        # Título
        title = ttk.Label(
            self,
            text="Log de Envio",
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(fill=X, pady=(0, 20))
        
        # Área de log
        self.log_text = scrolledtext.ScrolledText(
            self,
            wrap=WORD,
            height=20,
            font=('Consolas', 10)
        )
        self.log_text.pack(fill=BOTH, expand=True, pady=10)
        
        # Botões
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Button(
            buttons_frame,
            text="Exportar Log",
            command=self._export_log,
            bootstyle="info-outline",
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Limpar Log",
            command=self._clear_log,
            bootstyle="danger-outline",
            width=15
        ).pack(side=LEFT, padx=5)
    
    def add_log(self, message, level='INFO'):
        """
        Adiciona uma mensagem ao log
        
        Args:
            message (str): Mensagem a ser adicionada
            level (str): Nível do log (INFO, ERROR, SUCCESS)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{timestamp}] [{level}] {message}\n'
        
        self.log_text.insert(END, log_entry)
        self.log_text.see(END)
        
        # Aplica tag de cor baseado no nível
        last_line = self.log_text.get('end-2c linestart', 'end-1c')
        line_start = f'end-{len(last_line)+1}c linestart'
        line_end = 'end-1c'
        
        if level == 'ERROR':
            self.log_text.tag_add('error', line_start, line_end)
            self.log_text.tag_config('error', foreground='red')
        elif level == 'SUCCESS':
            self.log_text.tag_add('success', line_start, line_end)
            self.log_text.tag_config('success', foreground='green')
    
    def _export_log(self):
        """Exporta o log para um arquivo"""
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[
                ('Arquivos de Texto', '*.txt'),
                ('Todos os arquivos', '*.*')
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get('1.0', END))
                self.add_log(f'Log exportado para {file_path}', 'SUCCESS')
            except Exception as e:
                self.add_log(f'Erro ao exportar log: {e}', 'ERROR')
    
    def _clear_log(self):
        """Limpa o conteúdo do log"""
        self.log_text.delete('1.0', END)
        self.add_log('Log limpo', 'INFO') 