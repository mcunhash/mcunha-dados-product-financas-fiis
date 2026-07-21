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
                    # Remove o '%sql' e remove espaços/quebras de linha nas pontas
                    clean_sql = cell_text.replace('%sql', '', 1).strip()
                    
                    # Remove ponto e vírgula se estiver no final do comando para evitar que o parser envie statement vazio
                    if clean_sql.endswith(';'):
                        clean_sql = clean_sql[:-1].strip()
                        
                    if clean_sql: # Só adiciona se o comando não estiver vazio
                        sql_commands.append(clean_sql)
        
        # Junta os comandos válidos usando uma quebra de linha normal.
        # O dbsqlcli consegue rodar múltiplos statements separados por quebra de linha.
        return '\n'.join(sql_commands)
    except Exception as e:
        print(f"Erro ao ler o arquivo {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_sql.py <caminho_do_notebook.ipynb>", file=sys.stderr)
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    print(extract_sql_from_notebook(notebook_path))