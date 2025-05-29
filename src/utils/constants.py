"""
Constantes utilizadas no projeto
"""

# Configurações padrão
DEFAULT_SMTP_SERVER = 'smtp.gmail.com'
DEFAULT_SMTP_PORT = 587

# Cores do tema
COLORS = {
    'light': {
        'bg': '#ffffff',
        'fg': '#333333',
        'accent': '#007bff',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'border': '#dee2e6'
    },
    'dark': {
        'bg': '#212529',
        'fg': '#f8f9fa',
        'accent': '#0d6efd',
        'success': '#198754',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'border': '#495057'
    }
}

# Fontes
FONTS = {
    'title': ('Segoe UI', 16, 'bold'),
    'text': ('Segoe UI', 10),
    'monospace': ('Consolas', 10)
}

# Mensagens
MESSAGES = {
    'connection_success': 'Conexão estabelecida com sucesso!',
    'connection_error': 'Erro ao conectar ao servidor: {}',
    'sending_success': 'Email enviado para {} ({})',
    'sending_error': 'Erro ao enviar para {}: {}',
    'file_error': 'Erro ao ler arquivo: {}',
    'invalid_file': 'Formato de arquivo não suportado',
    'missing_columns': 'O arquivo deve conter as colunas: nome, email',
    'log_exported': 'Log exportado para {}',
    'log_export_error': 'Erro ao exportar log: {}',
    'log_cleared': 'Log limpo'
} 