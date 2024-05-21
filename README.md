### Análise de Planilha Automatizada com Jenkins

## Objetivo

Esta atividade tem como objetivo configurar um job no Jenkins para automatizar a análise de uma planilha de dados usando um script em Python. O job será agendado para rodar a cada 2 horas utilizando a sintaxe CRON.

## Passo a Passo

### 1. Configuração Inicial

- **Certifique-se de ter o Jenkins instalado e funcionando.**
- **Instale o plugin "Email Extension Plugin" no Jenkins para enviar e-mails com relatórios.**

### 2. Configurar o Script Python

Crie um script Python com o seguinte código e salve-o como `verify_spreadsheet.py`. Se desejar, pode criar seu próprio script de automação em cima de um arquivo `.csv` de sua preferência. Este script em Python realiza três principais funções relacionadas ao processamento de uma planilha de dados:

#### Download da Planilha

Função `download_spreadsheet(url, file_path)`: Baixa uma planilha a partir de uma URL fornecida e salva no caminho especificado.

```python
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
```

### 3. Configurar Jenkins

#### Criar um Novo Job

1. No Jenkins, clique em "New Item" para criar um novo job.
2. Dê um nome ao job, selecione "Freestyle project" e clique em "OK".

#### Configurar o Job

1. Em "General", adicione uma breve descrição do job.
2. Em "Build Triggers", marque a opção "Build periodically" e insira a expressão CRON `H */2 * * *` para executar o job a cada 2 horas.
3. Em "Build", clique em "Add build step" e selecione "Execute shell".
4. No campo de comando, insira:

   ```sh
   python3 /caminho/para/seu/script/verify_spreadsheet.py
   ```

5. Aplique e salve.

### 4. Configurar Notificação por E-mail

#### Configuração Global

1. Vá para "Gerenciar Jenkins" > "Configurar o sistema".
2. Encontre a seção "Extended E-mail Notification" e configure:

   - **SMTP server**: o servidor SMTP do seu provedor de e-mail (Exemplo: `smtp.gmail.com`).
   - **Default Recipients**: e-mails que devem receber notificações.
   - **Default Content**: O job `$PROJECT_NAME - Build # $BUILD_NUMBER` foi concluído com status `$BUILD_STATUS`.

3. Clique em "Salvar" para aplicar as configurações.

#### Configuração no Job

1. Vá para o job que você criou.
2. Clique em "Configurar".
3. Adicione uma ação de pós-construção "Editable Email Notification".
4. Configure:

   - **Project Recipient List**: `gabriel.lopes@irede.org.br`
   - **Content Type**: Default Content Type
   - **Default Subject**: Relatório do Excel gerado com sucesso (adicione seu nome completo)
   - **Default Content**: O job `$PROJECT_NAME - Build # $BUILD_NUMBER` foi concluído com status `$BUILD_STATUS`.
   - **Attachments**: `*/relatorio.txt`

5. Salve as configurações.

### Resultado Esperado

Forma de avaliação:

- **3 Pontos** pela entrega antes do dia 27/05/2024. Após essa data, a atividade vale no máximo **7 pontos**.
- **7 pontos** pelo funcionamento correto.

Nota máxima: **10**

Nota: É necessário que você coloque o seu nome completo no campo Default Subject pois caso contrário não haverá como comprovar a conclusão. Caso não consiga enviar para os e-mails listados, pode enviar um relatório resumido com a imagem da conclusão do JOB, e de suas dificuldades. Se não entregar a atividade até 31/05/2024 a atividade é zerada.