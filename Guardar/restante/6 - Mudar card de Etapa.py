import requests
import json

# URL da API do Bitrix24
url_api_bitrix24 = "https://smartsupply.bitrix24.com.br/rest/16/canbg9vx6rag1mox/"

# Método para mover um cartão de negócio para uma nova etapa
def mover_cartao_para_nova_etapa(id_cartao, nova_etapa):
    endpoint = "crm.deal.update"
    parametros = {
        "ID": id_cartao,
        "fields": {
            "STAGE_ID": nova_etapa
        }
    }
    response = requests.post(url_api_bitrix24 + endpoint, json=parametros)
    if response.status_code == 200:
        print(f"Cartão de negócio (ID: {id_cartao}) movido para a etapa {nova_etapa} com sucesso.")
    else:
        print(f"Erro ao mover o cartão de negócio (ID: {id_cartao}). Código de status: {response.status_code}")
        print(response.json())

# Carregar o arquivo JSON com os IDs dos cartões
caminho_arquivo = r"C:\Users\MSI Pulse\Documents\Chatpdf\Clonador de Voz\id_audio\dados_cartoes.json"
with open(caminho_arquivo, 'r', encoding="utf-8") as arquivo_json:
    dados_cartoes = json.load(arquivo_json)

# Definir a nova etapa
nova_etapa = "C42:UC_HYFEI4"

# Mover cada cartão para a nova etapa
for cartao in dados_cartoes:
    id_cartao = cartao['ID']
    mover_cartao_para_nova_etapa(id_cartao, nova_etapa)

print("Todos os cartões foram movidos para a nova etapa.")
