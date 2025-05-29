# MailSender

Aplicação para envio de emails em lote com interface gráfica moderna usando Python e ttkbootstrap.

## Funcionalidades

- Interface moderna com tema escuro/claro
- Envio de emails em lote
- Suporte a mensagens HTML
- Importação de contatos via CSV/Excel
- Adição manual de destinatários
- Log detalhado de envio
- Visualização prévia de emails
- Configuração de servidor SMTP personalizado

## Requisitos

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/mailsender.git
cd mailsender
```

2. Crie um ambiente virtual (opcional mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute o programa:
```bash
python main.py
```

2. Configure suas credenciais de email:
   - Para Gmail, use sua senha de app (https://myaccount.google.com/apppasswords)
   - Para outros serviços, configure o servidor SMTP e porta apropriados

3. Adicione destinatários:
   - Manualmente através do formulário
   - Importando um arquivo CSV/Excel com colunas 'nome' e 'email'

4. Componha sua mensagem:
   - Digite diretamente na área de texto
   - Ou carregue um arquivo HTML

5. Envie e monitore o progresso através do log

## Estrutura do Projeto

```
mailSender/
├── src/
│   ├── gui/
│   │   ├── components/      # Componentes da interface
│   │   └── themes/          # Configurações de tema
│   ├── services/            # Serviços (email, arquivos)
│   └── utils/               # Utilitários e constantes
├── assets/                  # Recursos (ícones, etc)
├── main.py                  # Ponto de entrada
└── requirements.txt         # Dependências
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request
