import pandas as pd
import os
import requests

def download_spreadsheet(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo baixado com sucesso e salvo em {file_path}.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a planilha: {e}")
        raise

def verify_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        
        issues = []
        if df['Date'].isnull().any():
            issues.append('Há datas ausentes na planilha.')
        if df.duplicated().any():
            issues.append('Há registros duplicados na planilha.')
        if (df['Value'] < 0).any():
            issues.append('Há valores negativos na planilha.')

        return issues
    except pd.errors.ParserError as e:
        print(f"Erro de análise: {e}")
        return []
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro ao verificar a planilha: {e}")
        return []

def generate_report(issues, report_path):
    try:
        with open(report_path, 'w') as file:
            if issues:
                file.write("Problemas encontrados:\n")
                for issue in issues:
                    file.write(f"- {issue}\n")
            else:
                file.write("Nenhum problema encontrado.")
        print(f"Relatório gerado com sucesso em {report_path}.")
    except Exception as e:
        print(f"Erro ao gerar o relatório: {e}")
        raise

spreadsheet_url = 'https://drive.google.com/uc?export=download&id=14bOzCd_cD6IDMu9_9gGLLqKaBL-_gqaA'
workspace_dir = '/var/lib/jenkins/workspace/IT Talent - Task 4'
spreadsheet_path = os.path.join(workspace_dir, 'consultas_previas.csv')
report_path = os.path.join(workspace_dir, 'relatorio.txt')

try:
    download_spreadsheet(spreadsheet_url, spreadsheet_path)

    issues = verify_data(spreadsheet_path)

    generate_report(issues, report_path)
finally:
    if os.path.exists(spreadsheet_path):
        os.remove(spreadsheet_path)
        print(f"Arquivo temporário {spreadsheet_path} removido.")
