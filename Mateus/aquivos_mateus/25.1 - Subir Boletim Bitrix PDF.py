import os
import json
import requests
import base64

# URL da API do Bitrix24
url_api_bitrix24 = "https://smartsupply.bitrix24.com.br/rest/16/canbg9vx6rag1mox/"

def upload_file_to_deal(webhook_url, deal_id, file_path):
    # Lendo o arquivo e convertendo para base64
    with open(file_path, 'rb') as file:
        file_content = file.read()
    file_base64 = base64.b64encode(file_content).decode('utf-8')

    # Nome do arquivo
    file_name = os.path.basename(file_path)

    # Parâmetros para atualizar o card com o arquivo em base64
    params = {
        'ID': deal_id,
        'fields': {
            'UF_CRM_1707937255628': {
                'fileData': [file_name, file_base64]
            }
        }
    }

    # Faz a chamada para a API
    response = requests.post(webhook_url + 'crm.deal.update.json', json=params)

    # Verifica se a chamada foi bem-sucedida
    if response.status_code == 200:
        print(f'Arquivo {file_name} anexado com sucesso ao card {deal_id}.')
    else:
        print(f'Erro ao anexar arquivo ao card {deal_id}: {response.status_code}')
        print(response.text)

def processar_dados_cartoes(pasta_indexar):
    # Iterando sobre todas as subpastas dentro da pasta principal
    for subdir in os.listdir(pasta_indexar):
        full_subdir_path = os.path.join(pasta_indexar, subdir)
        if os.path.isdir(full_subdir_path):
            for file_name in os.listdir(full_subdir_path):
                # Verifica se o nome do arquivo corresponde a um ID de card
                if file_name.endswith('.pdf'):
                    deal_id = os.path.splitext(file_name)[0]
                    file_path = os.path.join(full_subdir_path, file_name)
                    upload_file_to_deal(url_api_bitrix24, deal_id, file_path)

# Caminho da pasta principal onde os arquivos estão indexados
pasta_indexar = r'C:\Users\MSI Pulse\Documents\Chatpdf\Effecti\Boletim Resumo - Envio'

# Processar os dados dos cartões e subir os arquivos para o Bitrix24
processar_dados_cartoes(pasta_indexar)