import smtplib
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image, ImageTk

# Ícone padrão em base64 (um ícone de email simples)
ICON_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAA
7AAAAOwBeShxvQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAMASURBVFiF7ZZN
aBNpGMd/M5PJJGk+mqSxX2lttYpFxYMiIh4E8bB4UAQFQYMXQVhY8OzN0+JBT3qUBXHxIF4EQQ9+HEVB
LFoVRVu1VWyVftgPkzRNMslMMu+OB7XYJk0nk4MH/zDwznue5//7v8/zvO8MjEUr5CvkAR3QgM3rQzM0
dB0MHYyVn5qGjqalQNVAVUDXQNXWjsuy3JXJZGZkWS5s2LCh2el0FhRFcauqWgYUTdMcgANQVgKs+wWS
JNnT6fS2QqHQK0nSVjNzTNOMGIbxwDAMSZblz4lEYj4SiUw5nc5ZwzA+2Gy2b4ABqGvGWLcDsixvTKVS
+4vF4i5Zlr2SJDkWFxcbZFn2SJLkLRQKzfl8fqvX6x0MBoNTfr//k8/n+9DU1DQqSdKYqqrfAXUtgHUB
LMvyxmQyeahYLHYXCoUGRVG8iqK4VVV1qKrqUBTFrShKQ6FQaM7n81sDgcBgKBSa9Pl8Yz6f733I7/cP
K4oyqijKd13XV1XDugDZbHZzMpk8XCwWu/L5fIOiKF5VVd2qqjpVVXUqiuJWFMWbz+ebc7ncVr/fPxgM
Bqf8fv+Y1+t9HwqF3hqG8VZV1e+GYawbYF0OZLPZLclk8lCxWOzO5/ONiqJ4NE1zappWpWmaU9M0t6Zp
3lKp1FwqlbbYbLaBYDA4GQgExr1e7/twOPzG6XS+1nV9XFXVVQHWdSCbzW5NJpMHi8Vid6FQaFQUxaNp
mkvXdaeqqk5N01yqqnoURfEWi8WWUqm0xW63D4RCoYlAIDDm8XjehcPhEafT+UrX9QlVVVesgnUBstns
tmQyeaBYLO4sFAqNiqJ4dF136bru0nXdqWmaS9d1j6qqvmKx2FIsFrcYhjEQCoUmgsHgB4/H8y4SiQw7
nc6Xuq5PrqWGdQHWOv4/AZDNZrcnk8n9xWJxZ6lU8mm67tZ13aVpmkvXdbeu655SqeQvFovbDMMYCAaD
E6FQaNztdr+NRCLDLpfrhaZpU2up8acAVjPTNL8ZhvHVMIyvhmF8AfKGYaQ0TZvRNA1N0+b/BsCvqQKl
1bZmAD8AJBc0h1wXRxwAAAAASUVORK5CYII=
"""

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MailSender")
        self.root.geometry("1800x900")
        
        # Variáveis
        self.email_var = ttk.StringVar()
        self.password_var = ttk.StringVar()
        self.subject_var = ttk.StringVar()
        self.contacts_path = ttk.StringVar()
        self.contacts_df = pd.DataFrame(columns=['nome', 'email'])
        self.is_html = ttk.BooleanVar(value=False)
        self.manual_recipient_name = ttk.StringVar()
        self.manual_recipient_email = ttk.StringVar()
        self.html_file_path = ttk.StringVar()
        self.is_dark_mode = ttk.BooleanVar(value=True)
        self.smtp_server = ttk.StringVar(value='smtp.gmail.com')
        self.smtp_port = ttk.StringVar(value='587')
        
        # Configurar tema inicial
        self.style = ttk.Style()
        self.style.theme_use('darkly')
        
        # Configurar ícone
        try:
            icon_data = base64.b64decode(ICON_BASE64)
            icon_image = Image.open(BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
        except:
            pass
        
        # Container principal
        main_container = ttk.Frame(root, padding=10)
        main_container.pack(fill=BOTH, expand=True)
        
        # Barra superior
        top_bar = ttk.Frame(main_container)
        top_bar.pack(fill=X, pady=(0, 10))
        
        # Controles de tema e tela cheia
        controls = ttk.Frame(top_bar)
        controls.pack(side=RIGHT)
        
        ttk.Checkbutton(
            controls,
            text="Modo Claro",
            variable=self.is_dark_mode,
            command=self.toggle_theme,
            bootstyle="round-toggle"
        ).pack(side=RIGHT, padx=5)
        
        # Configurações de Email
        email_frame = ttk.LabelFrame(main_container, text="Configurações de Email", padding=10)
        email_frame.pack(fill=X, pady=(0, 10))
        
        # Grid de configurações
        settings_grid = ttk.Frame(email_frame)
        settings_grid.pack(fill=X, padx=5, pady=5)
        
        # Linha 1: Email e Senha
        ttk.Label(settings_grid, text="Email:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        ttk.Entry(settings_grid, textvariable=self.email_var, width=40).grid(row=0, column=1, sticky=W, padx=5, pady=5)
        
        ttk.Label(settings_grid, text="Senha:").grid(row=0, column=2, sticky=W, padx=5, pady=5)
        ttk.Entry(settings_grid, textvariable=self.password_var, show="•", width=40).grid(row=0, column=3, sticky=W, padx=5, pady=5)
        
        ttk.Button(
            settings_grid,
            text="Testar Conexão",
            command=self.test_connection,
            bootstyle="info-outline"
        ).grid(row=0, column=4, padx=5, pady=5)
        
        # Linha 2: SMTP e Porta
        ttk.Label(settings_grid, text="SMTP:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        ttk.Entry(settings_grid, textvariable=self.smtp_server, width=40).grid(row=1, column=1, sticky=W, padx=5, pady=5)
        
        ttk.Label(settings_grid, text="Porta:").grid(row=1, column=2, sticky=W, padx=5, pady=5)
        ttk.Entry(settings_grid, textvariable=self.smtp_port, width=10).grid(row=1, column=3, sticky=W, padx=5, pady=5)
        
        ttk.Button(
            settings_grid,
            text="Restaurar Padrão",
            command=self.restore_smtp_default,
            bootstyle="secondary-outline"
        ).grid(row=1, column=4, padx=5, pady=5)
        
        # Container central
        central_container = ttk.Frame(main_container)
        central_container.pack(fill=BOTH, expand=True, pady=10)
        
        # Frame esquerdo - Lista de destinatários
        recipients_frame = ttk.LabelFrame(central_container, text="Lista de Destinatários", padding=10)
        recipients_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        # Adicionar destinatário manualmente
        manual_add = ttk.Frame(recipients_frame)
        manual_add.pack(fill=X, pady=(0, 10))
        
        ttk.Label(manual_add, text="Nome:").pack(side=LEFT, padx=2)
        ttk.Entry(manual_add, textvariable=self.manual_recipient_name, width=20).pack(side=LEFT, padx=2)
        
        ttk.Label(manual_add, text="Email:").pack(side=LEFT, padx=2)
        ttk.Entry(manual_add, textvariable=self.manual_recipient_email, width=30).pack(side=LEFT, padx=2)
        
        ttk.Button(
            manual_add,
            text="Adicionar",
            command=self.add_manual_recipient,
            bootstyle="success-outline"
        ).pack(side=LEFT, padx=5)
        
        # Importar lista
        import_frame = ttk.Frame(recipients_frame)
        import_frame.pack(fill=X, pady=5)
        
        ttk.Label(import_frame, text="Arquivo:").pack(side=LEFT, padx=2)
        ttk.Entry(import_frame, textvariable=self.contacts_path, width=40).pack(side=LEFT, padx=2)
        
        ttk.Button(
            import_frame,
            text="Procurar",
            command=self.browse_file,
            bootstyle="secondary-outline"
        ).pack(side=LEFT, padx=2)
        
        ttk.Button(
            import_frame,
            text="Carregar",
            command=self.load_contacts,
            bootstyle="secondary-outline"
        ).pack(side=LEFT, padx=2)
        
        # Lista de destinatários
        self.recipients_text = scrolledtext.ScrolledText(
            recipients_frame,
            width=40,
            height=15,
            font=("Segoe UI", 10)
        )
        self.recipients_text.pack(fill=BOTH, expand=True, pady=5)
        
        # Botões da lista
        list_buttons = ttk.Frame(recipients_frame)
        list_buttons.pack(fill=X, pady=5)
        
        ttk.Button(
            list_buttons,
            text="Limpar Lista",
            command=self.clear_recipients,
            bootstyle="danger-outline"
        ).pack(side=RIGHT)
        
        # Frame direito - Composição do email
        compose_frame = ttk.LabelFrame(central_container, text="Composição do Email", padding=10)
        compose_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        # Assunto
        subject_frame = ttk.Frame(compose_frame)
        subject_frame.pack(fill=X, pady=(0, 5))
        
        ttk.Label(subject_frame, text="Assunto:").pack(side=LEFT, padx=5)
        ttk.Entry(subject_frame, textvariable=self.subject_var).pack(side=LEFT, fill=X, expand=True, padx=5)
        
        # Controles HTML
        html_frame = ttk.Frame(compose_frame)
        html_frame.pack(fill=X, pady=5)
        
        ttk.Checkbutton(
            html_frame,
            text="Usar HTML",
            variable=self.is_html,
            bootstyle="round-toggle"
        ).pack(side=LEFT, padx=5)
        
        ttk.Label(html_frame, text="Arquivo HTML:").pack(side=LEFT, padx=5)
        ttk.Entry(html_frame, textvariable=self.html_file_path, width=40).pack(side=LEFT, padx=5)
        
        ttk.Button(
            html_frame,
            text="Carregar HTML",
            command=self.load_html_file,
            bootstyle="info-outline"
        ).pack(side=LEFT, padx=5)
        
        # Área de mensagem
        self.message_text = scrolledtext.ScrolledText(
            compose_frame,
            width=50,
            height=15,
            font=("Segoe UI", 10)
        )
        self.message_text.pack(fill=BOTH, expand=True, pady=5)
        
        # Frame inferior
        bottom_container = ttk.Frame(main_container)
        bottom_container.pack(fill=X, pady=(10, 0))
        
        # Log
        log_frame = ttk.LabelFrame(bottom_container, text="Log de Envio", padding=10)
        log_frame.pack(fill=X)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            width=80,
            height=6,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=BOTH, expand=True, pady=5)
        
        # Botões do log
        log_buttons = ttk.Frame(log_frame)
        log_buttons.pack(fill=X)
        
        ttk.Button(
            log_buttons,
            text="Limpar Log",
            command=self.clear_log,
            bootstyle="danger-outline"
        ).pack(side=RIGHT, padx=5)
        
        ttk.Button(
            log_buttons,
            text="Exportar Log",
            command=self.export_log,
            bootstyle="info-outline"
        ).pack(side=RIGHT, padx=5)
        
        # Botões de ação
        action_buttons = ttk.Frame(main_container)
        action_buttons.pack(fill=X, pady=10)
        
        ttk.Button(
            action_buttons,
            text="Enviar Emails",
            command=self.send_emails,
            bootstyle="success"
        ).pack(side=RIGHT, padx=5)
        
        ttk.Button(
            action_buttons,
            text="Visualizar",
            command=self.preview_email,
            bootstyle="info"
        ).pack(side=RIGHT, padx=5)
        
        # Barra de status
        self.status_var = ttk.StringVar(value="Pronto para enviar emails")
        status_bar = ttk.Label(
            main_container,
            textvariable=self.status_var,
            relief=SUNKEN,
            padding=5
        )
        status_bar.pack(side=BOTTOM, fill=X)
        
        # Aplicar tema inicial
        self.apply_theme()

    def apply_theme(self):
        """Aplica as cores do tema atual"""
        is_dark = self.is_dark_mode.get()
        bg_color = '#2b2b2b' if is_dark else '#ffffff'
        fg_color = '#ffffff' if is_dark else '#000000'
        
        # Configurar cores dos widgets ScrolledText
        text_config = {
            'bg': bg_color,
            'fg': fg_color,
            'insertbackground': fg_color
        }
        
        for widget in [self.message_text, self.recipients_text, self.log_text]:
            widget.configure(**text_config)
        
        # Atualizar tema do ttkbootstrap
        self.style.theme_use('darkly' if is_dark else 'litera')

    def toggle_theme(self):
        """Alterna entre os temas claro e escuro"""
        self.apply_theme()

    def add_manual_recipient(self):
        nome = self.manual_recipient_name.get().strip()
        email = self.manual_recipient_email.get().strip()
        
        if not nome or not email:
            messagebox.showerror("Erro", "Preencha o nome e o email do destinatário.")
            return
        
        # Adicionar à lista
        new_row = pd.DataFrame({'nome': [nome], 'email': [email]})
        self.contacts_df = pd.concat([self.contacts_df, new_row], ignore_index=True)
        
        # Atualizar visualização
        self.update_recipients_list()
        
        # Limpar campos
        self.manual_recipient_name.set("")
        self.manual_recipient_email.set("")
        
        self.status_var.set(f"Destinatário adicionado: {nome} ({email})")

    def update_recipients_list(self):
        self.recipients_text.delete("1.0", ttk.END)
        for _, row in self.contacts_df.iterrows():
            self.recipients_text.insert(ttk.END, f"{row['nome']} - {row['email']}\n")

    def clear_recipients(self):
        if messagebox.askyesno("Confirmar", "Deseja limpar toda a lista de destinatários?"):
            self.contacts_df = pd.DataFrame(columns=['nome', 'email'])
            self.update_recipients_list()
            self.status_var.set("Lista de destinatários limpa")

    def load_html_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivos HTML", "*.html"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                self.message_text.delete("1.0", ttk.END)
                self.message_text.insert("1.0", html_content)
                self.html_file_path.set(file_path)
                self.is_html.set(True)
                self.status_var.set("Arquivo HTML carregado com sucesso")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo HTML: {str(e)}")

    def load_contacts(self):
        file_path = self.contacts_path.get()
        if not file_path:
            messagebox.showerror("Erro", "Selecione um arquivo de contatos primeiro.")
            return
        
        try:
            self.status_var.set("Carregando contatos...")
            self.root.update()
            
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, header=None)
            else:
                df = pd.read_excel(file_path, header=None)
            
            # Renomear colunas
            df.columns = ['nome', 'email'] + [f'col_{i}' for i in range(2, len(df.columns))]
            
            # Manter apenas as colunas necessárias
            df = df[['nome', 'email']]
            
            # Concatenar com a lista existente
            self.contacts_df = pd.concat([self.contacts_df, df], ignore_index=True)
            
            # Atualizar visualização
            self.update_recipients_list()
            
            num_contacts = len(df)
            messagebox.showinfo("Sucesso", f"{num_contacts} contatos foram carregados com sucesso!")
            self.status_var.set(f"{num_contacts} contatos carregados")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o arquivo: {str(e)}")
            self.status_var.set("Erro ao carregar contatos")

    def send_emails(self):
        if not self.email_var.get() or not self.password_var.get():
            messagebox.showerror("Erro", "Configure seu email e senha primeiro.")
            return
        
        if self.contacts_df.empty:
            messagebox.showerror("Erro", "Adicione pelo menos um destinatário.")
            return
        
        if not self.subject_var.get():
            messagebox.showerror("Erro", "Digite o assunto do email.")
            return
        
        message_body = self.message_text.get("1.0", ttk.END).strip()
        if not message_body:
            messagebox.showerror("Erro", "A mensagem não pode estar vazia.")
            return
        
        # Confirmar envio
        total_emails = len(self.contacts_df)
        if not messagebox.askyesno("Confirmar Envio", f"Você está prestes a enviar {total_emails} emails. Deseja continuar?"):
            return
        
        # Criar janela de progresso
        progress_window = ttk.Toplevel(self.root)
        progress_window.title("Progresso do Envio")
        progress_window.geometry("400x150")
        
        progress_frame = ttk.Frame(progress_window, padding=15, style='Custom.TFrame')
        progress_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(progress_frame, text="Enviando emails...", 
                 font=("Helvetica", 12)).pack(pady=(0, 10))
        
        progress_var = ttk.DoubleVar()
        progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=progress_var, 
            maximum=total_emails,
            style='Custom.Horizontal.TProgressbar'
        )
        progress_bar.pack(fill=X, pady=10)
        
        status_label = ttk.Label(progress_frame, text="Iniciando...")
        status_label.pack(pady=5)
        
        try:
            server = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
            server.starttls()
            server.login(self.email_var.get(), self.password_var.get())
            
            success_count = 0
            error_count = 0
            
            for index, row in self.contacts_df.iterrows():
                try:
                    nome = row['nome']
                    email = row['email']
                    
                    status_label.config(text=f"Enviando para: {nome} ({email})")
                    progress_window.update()
                    
                    # Personalizar mensagem
                    personalized_message = message_body.replace("{nome}", nome).replace("{email}", email)
                    
                    msg = MIMEMultipart()
                    msg['From'] = self.email_var.get()
                    msg['To'] = email
                    msg['Subject'] = self.subject_var.get()
                    
                    if self.is_html.get():
                        msg.attach(MIMEText(personalized_message, 'html'))
                    else:
                        msg.attach(MIMEText(personalized_message, 'plain'))
                    
                    server.send_message(msg)
                    success_count += 1
                    
                    self.log_text.insert(ttk.END, f"✓ Email enviado para: {nome} ({email})\n")
                    self.log_text.see(ttk.END)
                    
                    progress_var.set(index + 1)
                    progress_window.update()
                    
                except Exception as e:
                    error_count += 1
                    self.log_text.insert(ttk.END, f"✗ ERRO ao enviar para {email}: {str(e)}\n")
                    self.log_text.see(ttk.END)
                    progress_window.update()
            
            server.quit()
            
            status_label.config(text=f"Concluído! {success_count} enviados, {error_count} falhas")
            progress_window.update()
            
            self.log_text.insert(ttk.END, f"\nEnvio concluído! {success_count} emails enviados com sucesso, {error_count} falhas.\n")
            self.log_text.see(ttk.END)
            self.status_var.set(f"Envio concluído: {success_count} enviados, {error_count} falhas")
            
            ttk.Button(progress_frame, text="Fechar", 
                      command=progress_window.destroy,
                      style='Custom.TButton').pack(pady=10)
            
            messagebox.showinfo("Concluído", f"Envio concluído!\n{success_count} emails enviados com sucesso.\n{error_count} falhas.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar emails: {str(e)}")
            self.log_text.insert(ttk.END, f"ERRO GERAL: {str(e)}\n")
            self.log_text.see(ttk.END)
            self.status_var.set("Erro ao enviar emails")
            progress_window.destroy()

    def preview_email(self):
        if self.contacts_df.empty:
            messagebox.showerror("Erro", "Adicione pelo menos um destinatário para visualizar.")
            return
        
        if not self.subject_var.get():
            messagebox.showerror("Erro", "Digite o assunto do email.")
            return
        
        preview_window = ttk.Toplevel(self.root)
        preview_window.title("Visualização do Email")
        preview_window.geometry("600x500")
        
        preview_frame = ttk.Frame(preview_window, padding=20)
        preview_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(preview_frame, text="Visualização do Email", 
                 font=("Helvetica", 14, "bold")).pack(pady=(0, 20))
        
        # Usar o primeiro destinatário como exemplo
        primeiro_dest = self.contacts_df.iloc[0]
        
        ttk.Label(preview_frame, text=f"De: {self.email_var.get()}", 
                 anchor=W).pack(fill=X, pady=2)
        ttk.Label(preview_frame, text=f"Para: {primeiro_dest['nome']} ({primeiro_dest['email']})", 
                 anchor=W).pack(fill=X, pady=2)
        ttk.Label(preview_frame, text=f"Assunto: {self.subject_var.get()}", 
                 anchor=W).pack(fill=X, pady=2)
        
        ttk.Separator(preview_frame, orient=HORIZONTAL).pack(fill=X, pady=10)
        
        message_preview = scrolledtext.ScrolledText(
            preview_frame, 
            width=70, 
            height=15,
            font=("Segoe UI", 10),
            bd=1,
            relief="solid",
            padx=5,
            pady=5
        )
        message_preview.pack(fill=BOTH, expand=True, pady=10)
        
        # Configurar cores baseado no tema atual
        if self.is_dark_mode.get():
            message_preview.configure(
                bg='#2b2b2b',
                fg='#ffffff',
                insertbackground='#ffffff'
            )
        else:
            message_preview.configure(
                bg='#ffffff',
                fg='#000000',
                insertbackground='#000000'
            )
        
        # Personalizar mensagem com dados do primeiro destinatário
        message_body = self.message_text.get("1.0", ttk.END)
        personalized_message = message_body.replace("{nome}", primeiro_dest['nome']).replace("{email}", primeiro_dest['email'])
        
        message_preview.insert(ttk.END, personalized_message)
        message_preview.config(state=ttk.DISABLED)
        
        ttk.Label(preview_frame, text="(Visualização usando o primeiro destinatário como exemplo)", 
                 font=("Helvetica", 10, "italic")).pack(pady=5)
        
        ttk.Button(preview_frame, text="Fechar", 
                  command=preview_window.destroy).pack(pady=10)

    def test_connection(self):
        if not self.email_var.get() or not self.password_var.get():
            messagebox.showerror("Erro", "Preencha seu email e senha primeiro.")
            return
        
        try:
            self.status_var.set("Testando conexão...")
            self.root.update()
            
            server = smtplib.SMTP(self.smtp_server.get(), int(self.smtp_port.get()))
            server.starttls()
            server.login(self.email_var.get(), self.password_var.get())
            server.quit()
            
            messagebox.showinfo("Sucesso", "Conexão estabelecida com sucesso!")
            self.status_var.set("Conexão testada com sucesso")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar: {str(e)}")
            self.status_var.set("Falha na conexão")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.contacts_path.set(file_path)

    def clear_log(self):
        if messagebox.askyesno("Confirmar", "Deseja limpar o log?"):
            self.log_text.delete("1.0", ttk.END)
            self.status_var.set("Log limpo")

    def export_log(self):
        log_content = self.log_text.get("1.0", ttk.END).strip()
        if not log_content:
            messagebox.showinfo("Aviso", "O log está vazio. Nada para exportar.")
            return
            
        # Obter data e hora atual para o nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"log_envio_{timestamp}.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialfile=default_filename,
            title="Exportar Log"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    # Adicionar cabeçalho com data/hora
                    file.write(f"Log de Envio - Exportado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                    file.write("="*50 + "\n\n")
                    file.write(log_content)
                
                messagebox.showinfo("Sucesso", "Log exportado com sucesso!")
                self.status_var.set("Log exportado com sucesso")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar log: {str(e)}")
                self.status_var.set("Erro ao exportar log")

    def restore_smtp_default(self):
        self.smtp_server.set('smtp.gmail.com')
        self.smtp_port.set('587')
        messagebox.showinfo("Sucesso", "Servidor SMTP e porta restaurados para os padrões.")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  # Iniciando com tema escuro
    app = EmailSenderApp(root)
    root.mainloop()
    
