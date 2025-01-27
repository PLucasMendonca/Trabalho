from datetime import datetime
import requests
import json

# URL da API do Bitrix24
url_api_bitrix24 = "https://smartsupply.bitrix24.com.br/rest/16/canbg9vx6rag1mox/"

# Mapeamento de etapas pelo ID e nome
etapas = {
    "C2:UC_ARBQO9": "CLIENTE",
    "C2:NEW": "PENDÊNCIA",
    "C2:UC_8ASL7Y": "ATENÇÃO",
    "C2:UC_1PKAEQ": "CERTIDÕES VENCIDAS",
    "C2:UC_SKP20T": "PRIMEIRA COBRANÇA",
    "C2:UC_OVHW9C": "SEGUNDA COBRANÇA",
    "C2:UC_GFPUC0": "TERCEIRA COBRANÇA",
    "C2:UC_HSOAJY": "GESTÃO CLIENTES - CERTIDÕES VENCIDAS",
    "C2:UC_V6IMZ5": "GESTÃO CLIENTES - DOCUMENTAÇÃO VENCIDA",
    "C6:UC_NMP27I": "INSERIDAS",
    "C6:UC_73IZ9I": "OPORTUNIDADES",
    "C6:UC_SHMHFO": "OPORTUNIDADES DA QUINZENA",
    "C6:NEW": "FAZER RESUMO",
    "C6:UC_X6QP0A": "RESUMO FEITO",
    "C6:UC_7243LR": "ENVIAR NO GRUPO",
    "C6:UC_33WJXA": "RESUMO ENVIADO NO GRUPO",
    "C6:UC_8T3IED": "PREGÃO PARA 72 HORAS",
    "C6:UC_5AH23H": "PREGÃO 72 HORAS - ENVIADO",
    "C6:LOSE": "OPORTUNIDADES RECUSADAS",
    "UC_581EPX": "NOVO",
    "UC_XAUYPM": "ARREMATADO",
    "NEW": "ATENÇÃO - CONVOCAÇÕES",
    "UC_66R6K6": "ENVIAR NO GRUPO (CONVOCAÇÕES)",
    "UC_3Z5RVG": "MONITORANDO",
    "UC_X338TJ": "ENVIAR NO GRUPO (MONITORANDO)",
    "UC_0OGO1V": "DESCLASSIFICAÇÃO",
    "UC_JDBE9Y": "ENVIAR NO GRUPO (DESCLASSIFICADO)",
    "UC_CCMBH5": "MANIFESTAR A INTENÇÃO DE RECURSO",
    "UC_CK5340": "EM RECURSO",
    "UC_MGU9UN": "ENVIAR NO GRUPO (EM RECURSO)",
    "UC_25NHAS": "EM CONTRARRAZÃO",
    "UC_XOO9XV": "ENVIAR NO GRUPO (CONTRARRAZÃO)",
    "UC_XA5EZ2": "REVOGADA",
    "UC_F5294Q": "ENVIAR NO GRUPO (REVOGADA)",
    "UC_HF9XZB": "AGUARDANDO HOMOLOGAÇÃO",
    "UC_13OWIY": "ENVIAR NO GRUPO (AGUARDANDO HOMOLOGAÇÃO)",
    "UC_9FXPA0": "LICITAÇÃO GANHA",
    "UC_0CUFM2": "ENVIAR NO GRUPO (GANHA)",
    "UC_26C4JA": "LICITAÇÃO PERDIDA",
    "UC_PE3GFT": "ENVIAR NO GRUPO (PERDIDA)"
}

# Método para obter informações dos cartões de negócio em várias etapas de um pipeline específico, com paginação
def obter_info_cartoes_na_etapa(id_pipeline, id_etapas):
    endpoint = "crm.deal.list"
    start = 0
    resultados_completos = []
    
    while True:
        parametros = {
            "filter": {
                "=CATEGORY_ID": id_pipeline,
                "STAGE_ID": id_etapas
            },
            "select": ["ID", "COMPANY_ID", "STAGE_ID", "DATE_CREATE", "DATE_MODIFY", "UF_CRM_1700081429"],
            "order": {"DATE_CREATE": "ASC"},
            "start": start  # Usado para paginar os resultados
        }
        response = requests.post(url_api_bitrix24 + endpoint, json=parametros)
        
        if response.status_code == 200:
            resultados = response.json().get("result", [])
            resultados_completos.extend(resultados)
            
            # Verifica se há mais resultados a serem carregados
            if len(resultados) < 50:
                break
            else:
                start += 50
        else:
            print(f"Erro ao obter informações dos cartões de negócio. Código de status: {response.status_code}")
            break

    return resultados_completos

# Método para obter informações de uma empresa específica
def obter_info_empresa_por_id(id_empresa):
    endpoint = "crm.company.get"
    response = requests.get(url_api_bitrix24 + endpoint, params={"ID": id_empresa})
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Erro ao obter informações da empresa (ID: {id_empresa}). Código de status: {response.status_code}")
        return None

# Função para formatar a data no formato dia-mês-ano
def formatar_data(data_str):
    try:
        data = datetime.fromisoformat(data_str)
        return data.strftime('%d-%m-%Y')
    except ValueError:
        return "Data inválida"

# Função para calcular a diferença de dias entre a data atual e a data de modificação
def calcular_dias_desde_modificacao(data_str):
    try:
        data_modificacao = datetime.fromisoformat(data_str).replace(tzinfo=None)
        data_atual = datetime.now()
        diferenca_dias = (data_atual.date() - data_modificacao.date()).days
        return f"{diferenca_dias} dias atrás" if diferenca_dias > 0 else "Hoje"
    except ValueError:
        return "Data inválida"

# Função para calcular quantos dias faltam para uma data futura
def calcular_dias_para_futuro(data_str):
    try:
        data_sessao = datetime.fromisoformat(data_str).replace(tzinfo=None)
        data_atual = datetime.now()
        diferenca_dias = (data_sessao.date() - data_atual.date()).days
        return f"Faltam {diferenca_dias} dias" if diferenca_dias > 0 else "Hoje"
    except ValueError:
        return "Data inválida"

# Exemplo de uso com vários pipelines e etapas
pipelines_e_etapas = {
    "2": ["C2:UC_HSOAJY", "C2:UC_V6IMZ5"],
    "6": ["C6:UC_SHMHFO", "C6:UC_33WJXA", "C6:UC_8T3IED"],
    "0": ["UC_9FXPA0", "UC_26C4JA"]
}

dados_agrupados = {}

for id_pipeline, id_etapas in pipelines_e_etapas.items():
    cartoes_na_etapa = obter_info_cartoes_na_etapa(id_pipeline, id_etapas)

    if cartoes_na_etapa:
        for cartao in cartoes_na_etapa:
            id_cartao = cartao['ID']
            etapa_id = cartao['STAGE_ID']
            id_empresa = cartao.get('COMPANY_ID')
            data_criacao = formatar_data(cartao.get('DATE_CREATE', "Não disponível"))
            data_modificacao = formatar_data(cartao.get('DATE_MODIFY', "Não disponível"))
            dias_desde_modificacao = calcular_dias_desde_modificacao(cartao.get('DATE_MODIFY', "Não disponível"))
            data_sessao = formatar_data(cartao.get('UF_CRM_1700081429', "Não disponível"))
            dias_para_sessao = calcular_dias_para_futuro(cartao.get('UF_CRM_1700081429', "Não disponível"))

            if id_empresa:
                if id_empresa not in dados_agrupados:
                    info_empresa = obter_info_empresa_por_id(id_empresa)
                    nome_empresa = info_empresa.get("TITLE", "Nome da Empresa Desconhecido") if info_empresa else "Nome da Empresa Desconhecido"
                    dados_agrupados[id_empresa] = {
                        "nome_empresa": nome_empresa,
                        "etapas": {}
                    }

                etapa_nome = etapas.get(etapa_id, "Etapa Desconhecida")
                if etapa_nome not in dados_agrupados[id_empresa]["etapas"]:
                    dados_agrupados[id_empresa]["etapas"][etapa_nome] = {
                        "total_cards": 0,
                        "cards": []
                    }

                dados_agrupados[id_empresa]["etapas"][etapa_nome]["total_cards"] += 1

                dados_agrupados[id_empresa]["etapas"][etapa_nome]["cards"].append({
                    "ID": id_cartao,
                    "Data de Criação": data_criacao,
                    "Data de Modificação": data_modificacao,
                    "Última Modificação": dias_desde_modificacao,
                    "Data da Sessão": data_sessao,
                    "Dias para Sessão": dias_para_sessao
                })

# Exibir as informações agrupadas por empresa e etapa
for id_empresa, info_empresa in dados_agrupados.items():
    nome_empresa = info_empresa["nome_empresa"]
    print(f"ID da Empresa: {id_empresa}, Nome da Empresa: {nome_empresa}")
    for etapa, detalhes in info_empresa["etapas"].items():
        total_cards = detalhes["total_cards"]
        print(f"  - Etapa: {etapa}, Total de Cards: {total_cards}")
        for card in detalhes["cards"]:
            print(f"    - ID do Card: {card['ID']}, Data de Criação: {card['Data de Criação']}, Data de Modificação: {card['Data de Modificação']}, Última Modificação: {card['Última Modificação']}, Data da Sessão: {card['Data da Sessão']}, Dias para Sessão: {card['Dias para Sessão']}")

# Salvar a lista em um arquivo JSON
caminho_arquivo = "dados_operação.json"
with open(caminho_arquivo, 'w', encoding="utf-8") as arquivo_json:
    json.dump(dados_agrupados, arquivo_json, ensure_ascii=False, indent=4)
    print("Arquivo salvo com sucesso")

    
# Pipeline: PARTICIPANDO (ID: 4)
#   ID da Etapa: C4:UC_N6MUH1, Nome da Etapa: BUSCAR EDITAL
#   ID da Etapa: C4:UC_XIMF55, Nome da Etapa: EDITAL ENCONTRADO
#   ID da Etapa: C4:UC_CZG1NZ, Nome da Etapa: CADASTRAR PROPOSTA IMPERIO
#   ID da Etapa: C4:UC_FES7FE, Nome da Etapa: ACEITAS
#   ID da Etapa: C4:UC_0231Y5, Nome da Etapa: CADASTRAR EMPRESA NO PORTAL
#   ID da Etapa: C4:UC_CRXOB7, Nome da Etapa: PROPOSTA /DECLARAÇÃO
#   ID da Etapa: C4:UC_0ZCNCX, Nome da Etapa: SOLICITAR MINIMO/PROPOSTA
#   ID da Etapa: C4:UC_U84BPI, Nome da Etapa: CADATRAR NO PORTAL NORMAL
#   ID da Etapa: C4:UC_5WLYQ7, Nome da Etapa: NÃO HABILITA
#   ID da Etapa: C4:UC_HL0SGA, Nome da Etapa: PROPOSTA CADASTRADA
#   ID da Etapa: C4:UC_AM8OOQ, Nome da Etapa: AGUARDANDO PLANILHA- FACILITIES
#   ID da Etapa: C4:UC_EIRAYY, Nome da Etapa: AGUARDANDO MINIMO
#   ID da Etapa: C4:UC_G1LXBQ, Nome da Etapa: CADASTRADO NO ESTIMADO
#   ID da Etapa: C4:UC_BV3I0I, Nome da Etapa: REVISANDO
#   ID da Etapa: C4:UC_KQ1E9E, Nome da Etapa: REVISADO
#   ID da Etapa: C4:UC_V6TS9O, Nome da Etapa: CADASTRADA  NO ROBÔ
#   ID da Etapa: C4:UC_NOGANH, Nome da Etapa: OPERAÇÃO MANUAL
#   ID da Etapa: C4:UC_4BHAIW, Nome da Etapa: SUSPENSA
#   ID da Etapa: C4:UC_7TZMTQ, Nome da Etapa: ARREMATADO
#   ID da Etapa: C4:UC_AQ2IFD, Nome da Etapa: DISPUTA PERDIDA
#   ID da Etapa: C4:UC_IXEQVA, Nome da Etapa: vazio
#   ID da Etapa: C4:NEW, Nome da Etapa: INVALIDO
#   ID da Etapa: C4:WON, Nome da Etapa: Negócios Ganhos
#   ID da Etapa: C4:LOSE, Nome da Etapa: Negócios Perdidos
#   ID da Etapa: C4:APOLOGY, Nome da Etapa: Analisar falha