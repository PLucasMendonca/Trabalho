import requests
import pandas as pd

# URL da API do Bitrix24
url_api_bitrix24 = "https://smartsupply.bitrix24.com.br/rest/16/canbg9vx6rag1mox/"

# Método para obter todos os cartões de negócio filtrados por pipeline e etapa
def listar_todos_cartoes(id_pipeline, id_etapa):
    endpoint = "crm.deal.list"
    parametros = {
        "filter": {"=STAGE_ID": id_etapa, "=CATEGORY_ID": id_pipeline},
        "select": [
            "ID",
            "COMPANY_ID",  # Código da empresa
            "UF_CRM_1657389026", "UF_CRM_1657388991", "UF_CRM_1657389005",
            "UF_CRM_1700081429", "UF_CRM_1657480523844", "UF_CRM_1703860124684",
            "UF_CRM_1657480073676", "UF_CRM_1657480058163", "UF_CRM_1704052564",
            "UF_CRM_1680611704914", "UF_CRM_1663253782486", "UF_CRM_1704052561",
            "UF_CRM_1704052938", "UF_CRM_1704052658", "UF_CRM_1695820797444",
            "UF_CRM_1657394383051", "UF_CRM_1657480087357", "UF_CRM_1704052771",
            "UF_CRM_1704052692", "UF_CRM_1704052644", "UF_CRM_1680044112142",
            "UF_CRM_1657480114363", "UF_CRM_1706878527"
        ]
    }
    response = requests.post(url_api_bitrix24 + endpoint, json=parametros)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Erro ao listar cartões de negócio. Código de status: {response.status_code}")
        return []

# Método para obter detalhes da empresa com base no COMPANY_ID
def obter_detalhes_empresa(company_id):
    endpoint = "crm.company.get"
    parametros = {"ID": company_id}
    response = requests.post(url_api_bitrix24 + endpoint, json=parametros)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Erro ao obter detalhes da empresa. Código de status: {response.status_code}")
        return None

# Função para salvar as informações dos cartões em um arquivo CSV
def salvar_informacoes_csv(cartoes, output_file):
    for cartao in cartoes:
        company_id = cartao.get("COMPANY_ID")
        if company_id:
            detalhes_empresa = obter_detalhes_empresa(company_id)
            if detalhes_empresa:
                cartao["COMPANY_NAME"] = detalhes_empresa.get("TITLE")
    
    df = pd.DataFrame(cartoes)
    df.to_csv(output_file, index=False)
    print(f"Informações salvas com sucesso em {output_file}")

# Exemplo de uso
id_pipeline = "32"  # ID da pipeline
id_etapa = "C32:NEW"  # ID da etapa
output_file = r'C:\Users\MSI Pulse\Documents\Chatpdf\Effecti\Boletim Resumo - Info Excel\Resumo_pronto.csv'  # Caminho do arquivo de saída CSV

# Obter todos os cartões filtrados por pipeline e etapa
cartoes = listar_todos_cartoes(id_pipeline, id_etapa)

# Salvar informações em um arquivo CSV
salvar_informacoes_csv(cartoes, output_file)
