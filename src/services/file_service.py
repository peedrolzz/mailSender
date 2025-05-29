import pandas as pd
from typing import List, Dict, Optional
import os

class FileService:
    @staticmethod
    def load_contacts(file_path: str) -> Optional[List[Dict[str, str]]]:
        """
        Carrega contatos de um arquivo CSV ou Excel
        
        Args:
            file_path (str): Caminho do arquivo
            
        Returns:
            list: Lista de dicionários com nome e email dos contatos
            None: Se houver erro na leitura
        """
        try:
            # Determina o tipo de arquivo
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError('Formato de arquivo não suportado')
            
            # Verifica as colunas necessárias
            required_columns = {'nome', 'email'}
            if not required_columns.issubset(df.columns):
                raise ValueError(
                    'O arquivo deve conter as colunas: nome, email'
                )
            
            # Converte para lista de dicionários
            contacts = []
            for _, row in df.iterrows():
                name = str(row['nome']).strip()
                email = str(row['email']).strip()
                if name and email:  # Ignora linhas vazias
                    contacts.append({
                        'nome': name,
                        'email': email
                    })
            
            return contacts
            
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return None
    
    @staticmethod
    def load_html_template(file_path: str) -> Optional[str]:
        """
        Carrega um template HTML de um arquivo
        
        Args:
            file_path (str): Caminho do arquivo
            
        Returns:
            str: Conteúdo do arquivo HTML
            None: Se houver erro na leitura
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao ler arquivo HTML: {e}")
            return None
    
    @staticmethod
    def save_log(file_path: str, content: str) -> bool:
        """
        Salva o conteúdo do log em um arquivo
        
        Args:
            file_path (str): Caminho do arquivo
            content (str): Conteúdo a ser salvo
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            return False 