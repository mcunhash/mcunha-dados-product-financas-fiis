# Databricks notebook source
# scripts/extract_sql.py
import json
import sys

def extract_sql_from_notebook(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sql_commands = []
        for cell in data.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                cell_text = ''.join(source).strip()
                if cell_text.startswith('%sql'):
                    # Remove o '%sql' e limpa os espaços nas pontas
                    clean_sql = cell_text.replace('%sql', '', 1).strip()
                    
                    # Se o comando individual já termina com ';', remove para termos controle da junção
                    if clean_sql.endswith(';'):
                        clean_sql = clean_sql[:-1].strip()
                        
                    if clean_sql:
                        sql_commands.append(clean_sql)
        
        # Junta os comandos usando ';\n' para o Databricks saber onde termina um e começa o outro.
        # Não adiciona ';' no final do último elemento, evitando o erro de "EMPTY STATEMENT".
        return ';\n'.join(sql_commands)
    except Exception as e:
        print(f"Erro ao ler o arquivo {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_sql.py <caminho_do_notebook.ipynb>", file=sys.stderr)
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    print(extract_sql_from_notebook(notebook_path))