import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import pandas as pd

class RecipientsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        
        # Variáveis
        self.contacts_path = ttk.StringVar()
        self.manual_name = ttk.StringVar()
        self.manual_email = ttk.StringVar()
        self.recipients = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets do frame de destinatários"""
        # Título
        title = ttk.Label(
            self,
            text="Lista de Destinatários",
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(fill=X, pady=(0, 20))
        
        # Frame para adicionar manualmente
        manual_frame = ttk.LabelFrame(
            self,
            text="Adicionar Destinatário",
            padding=10
        )
        manual_frame.pack(fill=X, pady=(0, 10))
        
        # Nome
        name_frame = ttk.Frame(manual_frame)
        name_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            name_frame,
            text="Nome:",
            width=10
        ).pack(side=LEFT)
        
        ttk.Entry(
            name_frame,
            textvariable=self.manual_name,
            width=40
        ).pack(side=LEFT, fill=X, expand=True)
        
        # Email
        email_frame = ttk.Frame(manual_frame)
        email_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            email_frame,
            text="Email:",
            width=10
        ).pack(side=LEFT)
        
        ttk.Entry(
            email_frame,
            textvariable=self.manual_email,
            width=40
        ).pack(side=LEFT, fill=X, expand=True)
        
        # Botão adicionar
        ttk.Button(
            manual_frame,
            text="Adicionar",
            command=self._add_manual_recipient,
            bootstyle="success-outline",
            width=15
        ).pack(pady=(10, 0))
        
        # Frame para importar arquivo
        import_frame = ttk.LabelFrame(
            self,
            text="Importar Lista",
            padding=10
        )
        import_frame.pack(fill=X, pady=10)
        
        # Caminho do arquivo
        file_frame = ttk.Frame(import_frame)
        file_frame.pack(fill=X, pady=5)
        
        ttk.Entry(
            file_frame,
            textvariable=self.contacts_path,
            width=50
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        ttk.Button(
            file_frame,
            text="Procurar",
            command=self._browse_file,
            bootstyle="secondary-outline",
            width=15
        ).pack(side=LEFT)
        
        # Botão importar
        ttk.Button(
            import_frame,
            text="Importar",
            command=self._import_contacts,
            bootstyle="info-outline",
            width=15
        ).pack(pady=(10, 0))
        
        # Lista de destinatários
        list_frame = ttk.LabelFrame(
            self,
            text="Destinatários",
            padding=10
        )
        list_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # Treeview para lista
        self.recipients_tree = ttk.Treeview(
            list_frame,
            columns=('nome', 'email'),
            show='headings'
        )
        
        self.recipients_tree.heading('nome', text='Nome')
        self.recipients_tree.heading('email', text='Email')
        
        self.recipients_tree.pack(fill=BOTH, expand=True)
        
        # Botões da lista
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Button(
            buttons_frame,
            text="Remover Selecionado",
            command=self._remove_selected,
            bootstyle="danger-outline",
            width=20
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Limpar Lista",
            command=self._clear_list,
            bootstyle="danger-outline",
            width=15
        ).pack(side=LEFT, padx=5)
    
    def _add_manual_recipient(self):
        """Adiciona um destinatário manualmente"""
        name = self.manual_name.get().strip()
        email = self.manual_email.get().strip()
        
        if name and email:
            self.recipients.append({'nome': name, 'email': email})
            self.recipients_tree.insert('', END, values=(name, email))
            self.manual_name.set('')
            self.manual_email.set('')
    
    def _browse_file(self):
        """Abre diálogo para selecionar arquivo"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ('Arquivos Excel', '*.xlsx'),
                ('Arquivos CSV', '*.csv'),
                ('Todos os arquivos', '*.*')
            ]
        )
        if file_path:
            self.contacts_path.set(file_path)
    
    def _import_contacts(self):
        """Importa contatos do arquivo selecionado"""
        file_path = self.contacts_path.get()
        if not file_path:
            return
        
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            for _, row in df.iterrows():
                name = str(row['nome']).strip()
                email = str(row['email']).strip()
                if name and email:
                    self.recipients.append({'nome': name, 'email': email})
                    self.recipients_tree.insert('', END, values=(name, email))
            
            self.contacts_path.set('')
            
        except Exception as e:
            # TODO: Melhorar tratamento de erro
            print(f"Erro ao importar arquivo: {e}")
    
    def _remove_selected(self):
        """Remove o destinatário selecionado"""
        selected = self.recipients_tree.selection()
        if selected:
            for item in selected:
                values = self.recipients_tree.item(item)['values']
                self.recipients.remove({'nome': values[0], 'email': values[1]})
                self.recipients_tree.delete(item)
    
    def _clear_list(self):
        """Limpa toda a lista de destinatários"""
        self.recipients.clear()
        for item in self.recipients_tree.get_children():
            self.recipients_tree.delete(item) 