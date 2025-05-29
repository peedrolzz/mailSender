"""
Estilos personalizados para a interface do MailSender
"""

def apply_custom_styles(style):
    """
    Aplica estilos personalizados ao tema atual
    
    Args:
        style: Objeto ttk.Style
    """
    # Cores para modo claro
    LIGHT_COLORS = {
        'bg': '#ffffff',
        'fg': '#333333',
        'accent': '#007bff',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'border': '#dee2e6'
    }
    
    # Cores para modo escuro
    DARK_COLORS = {
        'bg': '#212529',
        'fg': '#f8f9fa',
        'accent': '#0d6efd',
        'success': '#198754',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'border': '#495057'
    }
    
    # Configurações comuns
    style.configure(
        'TFrame',
        background=DARK_COLORS['bg']
    )
    
    style.configure(
        'TLabel',
        background=DARK_COLORS['bg'],
        foreground=DARK_COLORS['fg']
    )
    
    style.configure(
        'TEntry',
        fieldbackground=DARK_COLORS['bg'],
        foreground=DARK_COLORS['fg'],
        insertcolor=DARK_COLORS['fg']
    )
    
    style.configure(
        'TButton',
        background=DARK_COLORS['accent'],
        foreground=DARK_COLORS['fg']
    )
    
    style.configure(
        'Danger.TButton',
        background=DARK_COLORS['danger']
    )
    
    style.configure(
        'Success.TButton',
        background=DARK_COLORS['success']
    )
    
    # Configurações do Notebook
    style.configure(
        'TNotebook',
        background=DARK_COLORS['bg'],
        tabmargins=[2, 5, 2, 0]
    )
    
    style.configure(
        'TNotebook.Tab',
        background=DARK_COLORS['bg'],
        foreground=DARK_COLORS['fg'],
        padding=[10, 5]
    )
    
    style.map(
        'TNotebook.Tab',
        background=[
            ('selected', DARK_COLORS['accent']),
            ('!selected', DARK_COLORS['bg'])
        ],
        foreground=[
            ('selected', '#ffffff'),
            ('!selected', DARK_COLORS['fg'])
        ]
    ) 