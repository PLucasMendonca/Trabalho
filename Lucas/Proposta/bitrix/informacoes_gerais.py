import requests
import json
from datetime import datetime
import pytz

class APIBitrix:
    def __init__(self):
        # URL da API do Bitrix24
        url_api_bitrix24 = "https://smartsupply.bitrix24.com.br/rest/16/canbg9vx6rag1mox/"

    # Mapeamento de etapas pelo ID e nome para os pipelines "PARTICIPANDO" (ID: 4) e "PIPELINE_0" (ID: 0)
    etapas = {
        # Pipeline 4: PARTICIPANDO
        
        "C4:UC_FES7FE": "ACEITAS",
        "C4:UC_0231Y5": "CADASTRAR NO PORTAL",

        # Pipeline 2: GESTÃO DOCUMENTAL
        "C2:UC_ARBQO9": "CLIENTE",
        "C2:UC_TS3N3O": "JUNTAR DOC'S",
        "C2:NEW": "PENDÊNCIA",
        "C2:UC_8ASL7Y": "ATENÇÃO",
        "C2:UC_1PKAEQ": "CERTIDÕES VENCIDAS",
        "C2:UC_SKP20T": "PRIMEIRA COBRANÇA",
        "C2:UC_OVHW9C": "SEGUNDA COBRANÇA",
        "C2:UC_GFPUC0": "TERCEIRA COBRANÇA",
        "C2:UC_HSOAJY": "GESTÃO CLIENTES - CERTIDÕES VENCIDAS",
        "C2:UC_V6IMZ5": "GESTÃO CLIENTES - DOCUMENTAÇÃO VENCIDA",

    }

    pipelines_e_etapas = {
        "4": [  # Pipeline: PARTICIPANDO (ID: 4)
            "C4:UC_FES7FE",
            "C4:UC_0231Y5",
        ],

        "2": [  # Pipeline: GESTÃO DOCUMENTAL (ID: 2)
            "C2:UC_ARBQO9",
            "C2:UC_TS3N3O",
            "C2:NEW",
            "C2:UC_8ASL7Y",
            "C2:UC_1PKAEQ",
            "C2:UC_SKP20T",
            "C2:UC_OVHW9C",
            "C2:UC_GFPUC0",
            "C2:UC_HSOAJY",
            "C2:UC_V6IMZ5",
        ]
    }

    # Campos adicionais a serem obtidos
    campos_adicionais = [
        "UF_CRM_1657389026",      # Número do pregão
        "UF_CRM_1657401479",      # Cidade
        "UF_CRM_1657401492",      # Estado
        "UF_CRM_1657480523844",   # Objeto
        "UF_CRM_1737564045",      # login - bnc
        "UF_CRM_1737564060",      # senha - bnc
        "UF_CRM_1737564076",      # login - bll
        "UF_CRM_1737564324",      # senha - bll
        "UF_CRM_1737564007",      # login - comprasnet
        "UF_CRM_1737564024",      # senha - comprasnet
        "UF_CRM_1737564347",      # login - compras publicas
        "UF_CRM_1737564362",      # senha - compras publicas
        "UF_CRM_1657389005",      # portal
        "UF_CRM_1697549977",      # idlicitacao
        "UF_CRM_1700081429",      # Data
        "UF_CRM_1657388991",      # AO ESTIMADO ÓRGÃO
        "UF_CRM_1661536398",      # Validade da proposta
    ]

    # Campos da empresa a serem obtidos
    campos_empresa = [
        "UF_CRM_1677019095",      # RAZÃO SOCIAL
        "UF_CRM_1657467136849",   # CNPJ
        "UF_CRM_1684363050",      # ENDEREÇO
        "UF_CRM_1657470593970",   # DADOS BANCÁRIOS
        "UF_CRM_1657474180077",   # Campo adicional
        "UF_CRM_1657474218468",   # Campo adicional
    ]

    # Método para obter informações dos cartões de negócio em várias etapas de um pipeline específico, com paginação
    def obter_info_cartoes_na_etapa(id_pipeline, id_etapas):
        endpoint = "crm.deal.list"
        start = 0
        resultados_completos = []
        total_fetched = 0

        print(f"Iniciando a obtenção de cartões para o Pipeline ID: {id_pipeline} com {len(id_etapas)} etapas.")

        while True:
            parametros = {
                "filter": {
                    "=CATEGORY_ID": id_pipeline,
                    "STAGE_ID": id_etapas
                },
                "select": [
                    "ID",
                    "COMPANY_ID",
                    "STAGE_ID",
                    "DATE_CREATE",
                    "DATE_MODIFY",
                    "UF_CRM_1700081429"  # Data e hora da sessão
                ] + campos_adicionais,
                "order": {"DATE_CREATE": "ASC"},
                "start": start  # Usado para paginar os resultados
            }

            print(f"Fazendo requisição para obter cartões com start={start}...")
            try:
                response = requests.post(url_api_bitrix24 + endpoint, json=parametros)
                response.raise_for_status()
                resultados = response.json().get("result", [])
                fetched_count = len(resultados)
                print(f"Obtidos {fetched_count} cartões na requisição com start={start}.")
                
                if fetched_count == 0:
                    print("Nenhum cartão encontrado na requisição atual.")
                    break

                resultados_completos.extend(resultados)
                total_fetched += fetched_count

                if fetched_count < 50:
                    print("Última página de cartões alcançada.")
                    break
                else:
                    start += 50

            except requests.RequestException as e:
                print(f"Erro ao obter informações dos cartões de negócio: {e}")
                break

        print(f"Total de cartões obtidos para Pipeline ID {id_pipeline}: {total_fetched}")
        return resultados_completos

    # Método para obter informações de uma empresa específica
    def obter_info_empresa_por_id(id_empresa):
        endpoint = "crm.company.get"
        print(f"Obtendo informações da empresa com ID: {id_empresa}")
        try:
            response = requests.get(url_api_bitrix24 + endpoint, params={"ID": id_empresa})
            response.raise_for_status()
            result = response.json().get("result", {})
            
            # Extrair campos específicos da empresa
            dados_empresa = {
                "nome_empresa": result.get("TITLE", "Nome da Empresa Desconhecido"),
                "razao_social": result.get("UF_CRM_1677019095", "Não disponível"),
                "cnpj": result.get("UF_CRM_1657467136849", "Não disponível"),
                "endereco": result.get("UF_CRM_1684363050", "Não disponível"),
                "dados_bancarios": result.get("UF_CRM_1657470593970", "Não disponível"),
                "nome": result.get("UF_CRM_1657474180077", "Não disponível"),
                "cpf": result.get("UF_CRM_1657474218468", "Não disponível")
            }
            
            if result:
                print(f"Informações obtidas para a empresa ID {id_empresa}.")
            else:
                print(f"Nenhuma informação encontrada para a empresa ID {id_empresa}.")
            return dados_empresa
        except requests.RequestException as e:
            print(f"Erro ao obter informações da empresa (ID: {id_empresa}): {e}")
            return None

    # Função para formatar a data no formato dia-mês-ano hora:minuto:segundo
    def formatar_data_e_hora(data_str):
        if not data_str:
            return "Data inválida"
        try:
            # Usa fromisoformat para lidar com o formato ISO 8601
            data = datetime.fromisoformat(data_str)
            data_formatada = data.strftime('%d-%m-%Y %H:%M:%S')
            print(f"Data formatada: {data_formatada}")
            return data_formatada
        except (ValueError, TypeError):
            print(f"Erro ao parsear a data: {data_str}")
            return "Data inválida"

    # Função para calcular a diferença de dias entre a data atual e a data de modificação
    def calcular_dias_desde_modificacao(data_str):
        if not data_str:
            return "Data inválida"
        try:
            data_modificacao = datetime.fromisoformat(data_str).replace(tzinfo=None)
            data_atual = datetime.now()
            diferenca_dias = (data_atual.date() - data_modificacao.date()).days
            resultado = f"{diferenca_dias} dias atrás" if diferenca_dias > 0 else "Hoje"
            print(f"Dias desde modificação: {resultado}")
            return resultado
        except (ValueError, TypeError):
            print(f"Erro ao calcular dias desde modificação para a data: {data_str}")
            return "Data inválida"

    # Função para calcular quantos dias faltam para uma data futura
    def calcular_dias_para_futuro(data_str):
        if not data_str:
            return "Data inválida"
        try:
            data_sessao = datetime.fromisoformat(data_str).replace(tzinfo=None)
            data_atual = datetime.now()
            diferenca_dias = (data_sessao.date() - data_atual.date()).days
            resultado = f"Faltam {diferenca_dias} dias" if diferenca_dias > 0 else ("Hoje" if diferenca_dias == 0 else "Sessão já ocorreu")
            print(f"Dias para sessão: {resultado}")
            return resultado
        except (ValueError, TypeError):
            print(f"Erro ao calcular dias para futuro para a data: {data_str}")
            return "Data inválida"

    # Função para processar os cartões e agrupar os dados
    def processar_cartoes(dados_agrupados, cartoes, etapas):
        total_cartoes = len(cartoes)
        print(f"Iniciando processamento de {total_cartoes} cartões.")
        
        for index, cartao in enumerate(cartoes, start=1):
            print(f"Processando cartão {index}/{total_cartoes} (ID: {cartao.get('ID')})...")
            id_cartao = cartao.get('ID')
            etapa_id = cartao.get('STAGE_ID')
            id_empresa = cartao.get('COMPANY_ID')
            
            etapa_nome = etapas.get(etapa_id, "Etapa Desconhecida")
            
            # Define as informações do cartão com base na etapa
            if etapa_nome == "CLIENTE":
                info_cartao = {
                    "ID": id_cartao,
                    "Credenciais": {
                        "bnc": {
                            "login": cartao.get('UF_CRM_1737564045', "Não disponível"),
                            "senha": cartao.get('UF_CRM_1737564060', "Não disponível")
                        },
                        "bll": {
                            "login": cartao.get('UF_CRM_1737564076', "Não disponível"),
                            "senha": cartao.get('UF_CRM_1737564324', "Não disponível")
                        },
                        "comprasnet": {
                            "login": cartao.get('UF_CRM_1737564007', "Não disponível"),
                            "senha": cartao.get('UF_CRM_1737564024', "Não disponível")
                        },
                        "compras_publicas": {
                            "login": cartao.get('UF_CRM_1737564347', "Não disponível"),
                            "senha": cartao.get('UF_CRM_1737564362', "Não disponível")
                        }
                    }
                }
            else:
                info_cartao = {
                    "ID": id_cartao,
                    "Número do pregão": cartao.get('UF_CRM_1657389026', "Não disponível"),
                    "Cidade": cartao.get('UF_CRM_1657401479', "Não disponível"),
                    "Estado": cartao.get('UF_CRM_1657401492', "Não disponível"),
                    "Objeto": cartao.get('UF_CRM_1657480523844', "Não disponível"),
                    "Portal": cartao.get('UF_CRM_1657389005', "Não disponível"),
                    "ID Licitação": cartao.get('UF_CRM_1697549977', "Não disponível"),
                    "Data": cartao.get('UF_CRM_1700081429', "Não disponível"),
                    "AO ESTIMADO ÓRGÃO": cartao.get('UF_CRM_1657388991', "Não disponível"),
                    "Validade da proposta": cartao.get('UF_CRM_1661536398', "Não disponível")
                }

            # Adiciona credenciais apenas se não for a etapa "CADASTRAR NO PORTAL" ou "ACEITAS"
            if etapa_nome not in ["CADASTRAR NO PORTAL", "ACEITAS"] and etapa_nome != "CLIENTE":
                info_cartao["Credenciais"] = {
                    "bnc": {
                        "login": cartao.get('UF_CRM_1737564045', "Não disponível"),
                        "senha": cartao.get('UF_CRM_1737564060', "Não disponível")
                    },
                    "bll": {
                        "login": cartao.get('UF_CRM_1737564076', "Não disponível"),
                        "senha": cartao.get('UF_CRM_1737564324', "Não disponível")
                    },
                    "comprasnet": {
                        "login": cartao.get('UF_CRM_1737564007', "Não disponível"),
                        "senha": cartao.get('UF_CRM_1737564024', "Não disponível")
                    },
                    "compras_publicas": {
                        "login": cartao.get('UF_CRM_1737564347', "Não disponível"),
                        "senha": cartao.get('UF_CRM_1737564362', "Não disponível")
                    }
                }

            if id_empresa:
                if id_empresa not in dados_agrupados:
                    info_empresa = obter_info_empresa_por_id(id_empresa)
                    dados_agrupados[id_empresa] = {
                        **info_empresa,
                        "etapas": {}
                    }

                if etapa_nome not in dados_agrupados[id_empresa]["etapas"]:
                    dados_agrupados[id_empresa]["etapas"][etapa_nome] = {
                        "total_cards": 0,
                        "cards": []
                    }

                dados_agrupados[id_empresa]["etapas"][etapa_nome]["total_cards"] += 1
                dados_agrupados[id_empresa]["etapas"][etapa_nome]["cards"].append(info_cartao)
            else:
                print(f"Cartão ID {id_cartao} não possui ID de empresa associado.")

        print("Processamento de cartões concluído.")
        return dados_agrupados

    # Função principal
    def main():
        print("Iniciando o script de processamento de cartões do Bitrix24.")
        dados_agrupados = {}
        total_pipelines = len(pipelines_e_etapas)
        print(f"Total de pipelines a serem processados: {total_pipelines}")

        for idx_pipeline, (id_pipeline, id_etapas) in enumerate(pipelines_e_etapas.items(), start=1):
            nome_pipeline = "PARTICIPANDO" if id_pipeline == "4" else ("PIPELINE_0" if id_pipeline == "0" else "Outro Pipeline")
            print(f"\nProcessando Pipeline {idx_pipeline}/{total_pipelines} - ID: {id_pipeline} ({nome_pipeline})")
            cartoes_na_etapa = obter_info_cartoes_na_etapa(id_pipeline, id_etapas)

            if cartoes_na_etapa:
                print(f"{len(cartoes_na_etapa)} cartões encontrados no Pipeline ID {id_pipeline}.")
                dados_agrupados = processar_cartoes(dados_agrupados, cartoes_na_etapa, etapas)
            else:
                print(f"Nenhum cartão encontrado no Pipeline ID {id_pipeline}.")

        # Exibir as informações agrupadas por empresa e etapa
        print("\nExibindo informações agrupadas por empresa e etapa:")
        for id_empresa, info_empresa in dados_agrupados.items():
            nome_empresa = info_empresa["nome_empresa"]
            print(f"\nID da Empresa: {id_empresa}, Nome da Empresa: {nome_empresa}")
            for etapa, detalhes in info_empresa["etapas"].items():
                total_cards = detalhes["total_cards"]
                print(f"  - Etapa: {etapa}, Total de Cards: {total_cards}")
                for card in detalhes["cards"]:
                    if etapa == "CLIENTE":
                        info_card = f"    - ID do Card: {card['ID']}"
                        if "Credenciais" in card:
                            info_card += f", Credenciais: {card['Credenciais']}"
                    else:
                        info_card = (f"    - ID do Card: {card['ID']}, "
                                f"Número do pregão: {card.get('Número do pregão', 'N/A')}, "
                                f"Cidade: {card.get('Cidade', 'N/A')}, "
                                f"Estado: {card.get('Estado', 'N/A')}, "
                                f"Portal: {card.get('Portal', 'N/A')}, "
                                f"ID Licitação: {card.get('ID Licitação', 'N/A')}, "
                                f"Objeto: {card.get('Objeto', 'N/A')}")
                    
                    print(info_card)

        # Salvar a lista em um arquivo JSON
        caminho_arquivo = "dados_operacao4.json"
        print(f"\nSalvando os dados agrupados em '{caminho_arquivo}'...")
        try:
            with open(caminho_arquivo, 'w', encoding="utf-8") as arquivo_json:
                json.dump(dados_agrupados, arquivo_json, ensure_ascii=False, indent=4)
                print(f"Arquivo salvo com sucesso em '{caminho_arquivo}'.")
        except IOError as e:
            print(f"Erro ao salvar o arquivo JSON: {e}")

        print("Script concluído.")
