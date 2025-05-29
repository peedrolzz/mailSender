import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional, Callable

class EmailService:
    def __init__(
        self,
        smtp_server: str = 'smtp.gmail.com',
        smtp_port: int = 587,
        on_progress: Optional[Callable[[str, str], None]] = None
    ):
        """
        Inicializa o serviço de email
        
        Args:
            smtp_server (str): Servidor SMTP
            smtp_port (int): Porta do servidor
            on_progress (callable): Callback para progresso do envio
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.on_progress = on_progress or (lambda msg, level: None)
    
    def test_connection(self, email: str, password: str) -> bool:
        """
        Testa a conexão com o servidor SMTP
        
        Args:
            email (str): Email do remetente
            password (str): Senha do remetente
            
        Returns:
            bool: True se a conexão foi bem sucedida
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(email, password)
                return True
        except Exception as e:
            self.on_progress(f'Erro ao testar conexão: {e}', 'ERROR')
            return False
    
    def send_emails(
        self,
        sender_email: str,
        sender_password: str,
        recipients: List[Dict[str, str]],
        subject: str,
        message: str,
        is_html: bool = False
    ) -> bool:
        """
        Envia emails em lote
        
        Args:
            sender_email (str): Email do remetente
            sender_password (str): Senha do remetente
            recipients (list): Lista de destinatários (dicts com 'nome' e 'email')
            subject (str): Assunto do email
            message (str): Corpo do email
            is_html (bool): Se True, o email será enviado como HTML
            
        Returns:
            bool: True se todos os emails foram enviados com sucesso
        """
        try:
            # Conecta ao servidor
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                
                self.on_progress('Conectado ao servidor SMTP', 'SUCCESS')
                
                # Envia para cada destinatário
                for recipient in recipients:
                    try:
                        # Prepara o email
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = recipient['email']
                        msg['Subject'] = subject
                        
                        # Adiciona o corpo
                        body = MIMEText(message, 'html' if is_html else 'plain')
                        msg.attach(body)
                        
                        # Envia
                        server.send_message(msg)
                        
                        self.on_progress(
                            f'Email enviado para {recipient["nome"]} ({recipient["email"]})',
                            'SUCCESS'
                        )
                        
                    except Exception as e:
                        self.on_progress(
                            f'Erro ao enviar para {recipient["email"]}: {e}',
                            'ERROR'
                        )
                        return False
                
                self.on_progress('Todos os emails foram enviados', 'SUCCESS')
                return True
                
        except Exception as e:
            self.on_progress(f'Erro ao conectar ao servidor: {e}', 'ERROR')
            return False 