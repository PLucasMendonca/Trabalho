import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from queue import Queue
from src.utils.word_processor import criar_tabela_word

class ProcessadorAPI:
    # Mapeamento dos campos entre os JSONs
    MAPEAMENTO_CAMPOS = {
        'dados_operacao': {
            'numero_pregao': 'Número do pregão',
            'objeto': 'Objeto',
            'data': 'Data',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'validade_proposta': 'Validade da proposta',
            'modalidade': 'Modalidade de licitação',
            'orgao': 'AO ESTIMADO ÓRGÃO'
        },
        'comprasnet': {
            'numero_pregao': 'numeroCompra',
            'objeto': 'objetoCompra',
            'data': 'dataAberturaPropostaPncp',
            'cidade': 'unidadeOrgaoMunicipioNome',
            'estado': 'unidadeOrgaoUfSigla',
            'validade_proposta': 'dataEncerramentoPropostaPncp',
            'modalidade': 'modalidadeNome',
            'orgao': 'orgaoEntidadeRazaoSocial'
        },
        'pncp': {
            'numero_pregao': ['licitacao', 'numeroCompra'],
            'objeto': ['licitacao', 'objetoCompra'],
            'data': ['licitacao', 'dataAberturaProposta'],
            'cidade': ['licitacao', 'unidadeOrgao', 'municipioNome'],
            'estado': ['licitacao', 'unidadeOrgao', 'ufSigla'],
            'validade_proposta': ['licitacao', 'dataEncerramentoProposta'],
            'modalidade': ['licitacao', 'modalidadeNome'],
            'orgao': ['licitacao', 'orgaoEntidade', 'razaoSocial']
        }
    }

    def __init__(self, callback_log=None):
        self.callback_log = callback_log
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.pilha_processamento = []
        
    def log(self, mensagem: str, tipo: str = "info"):
        """Função auxiliar para logging"""
        if self.callback_log:
            self.callback_log(mensagem, tipo)
        else:
            print(mensagem)

    def get_nested_value(self, data: Dict, keys: str | list) -> Any:
        """Obtém valor de um dicionário aninhado usando uma lista de chaves ou uma única chave"""
        if isinstance(keys, str):
            return data.get(keys)
            
        current = data
        for key in keys:
            if current is None:
                return None
            current = current.get(key, {})
        return current if current != {} else None

    def carregar_json(self, nome_arquivo: str) -> Optional[Dict[str, Any]]:
        """Carrega um arquivo JSON do diretório data/json"""
        try:
            caminho_arquivo = os.path.join(self.base_dir, 'data', 'json', nome_arquivo)
            if not os.path.exists(caminho_arquivo):
                self.log(f"Arquivo {nome_arquivo} não encontrado", "error")
                return None
                
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Erro ao carregar {nome_arquivo}: {str(e)}", "error")
            return None

    def extrair_dados_normalizados(self, dados: Dict, tipo_json: str) -> Dict[str, Any]:
        """Extrai e normaliza os dados do JSON conforme o mapeamento"""
        mapeamento = self.MAPEAMENTO_CAMPOS[tipo_json]
        resultado = {}
        
        for campo_norm, campo_orig in mapeamento.items():
            if campo_orig is None:
                continue
            valor = self.get_nested_value(dados, campo_orig)
            resultado[campo_norm] = valor if valor is not None else 'N/A'
            
        return resultado

    def dados_correspondem(self, dados_card: Dict[str, Any], dados_api: Dict[str, Any]) -> bool:
        """
        Verifica se os dados do card correspondem aos dados da API.
        Retorna True se encontrar correspondência nos campos chave.
        """
        # Campos principais para comparação
        campos_chave = ['numero_pregao', 'objeto']
        campos_secundarios = ['cidade', 'estado']
        
        # Verificar campos principais (precisa corresponder pelo menos um)
        correspondencia_principal = False
        for campo in campos_chave:
            valor_card = str(dados_card.get(campo, '')).strip().lower()
            valor_api = str(dados_api.get(campo, '')).strip().lower()
            
            if valor_card and valor_api and (valor_card in valor_api or valor_api in valor_card):
                self.log(f"Correspondência encontrada no campo {campo}", "success")
                correspondencia_principal = True
                break
        
        if not correspondencia_principal:
            return False
            
        # Se encontrou correspondência principal, verifica campos secundários
        correspondencias_secundarias = 0
        for campo in campos_secundarios:
            valor_card = str(dados_card.get(campo, '')).strip().lower()
            valor_api = str(dados_api.get(campo, '')).strip().lower()
            
            if valor_card and valor_api and valor_card == valor_api:
                correspondencias_secundarias += 1
                self.log(f"Correspondência adicional encontrada no campo {campo}", "success")
        
        # Retorna True se encontrou pelo menos uma correspondência secundária
        return correspondencias_secundarias > 0

    def atualizar_dados_card(self, item: Dict[str, Any], dados_api: Dict[str, Any], tipo_origem: str):
        """Atualiza os dados do card com as informações encontradas na API"""
        mapeamento_reverso = {
            'numero_pregao': 'Número do pregão',
            'objeto': 'Objeto',
            'data': 'Data',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'validade_proposta': 'Validade da proposta',
            'modalidade': 'Modalidade de licitação',
            'orgao': 'AO ESTIMADO ÓRGÃO'
        }
        
        for campo_norm, campo_card in mapeamento_reverso.items():
            valor = dados_api.get(campo_norm)
            if valor and valor != 'N/A':
                item[campo_card] = valor
                self.log(f"Campo {campo_card} atualizado com valor do {tipo_origem}", "info")

    def processar_comprasnet(self, dados: Dict[str, Any], card_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados do ComprasNet e retorna os dados normalizados se houver correspondência
        """
        try:
            if not dados:
                return None
                
            dados_comp = self.extrair_dados_normalizados(dados, 'comprasnet')
            dados_card = self.extrair_dados_normalizados(card_info, 'dados_operacao')
            
            if self.dados_correspondem(dados_card, dados_comp):
                self.log("Dados encontrados no ComprasNet", "success")
                return dados_comp
                
        except Exception as e:
            self.log(f"Erro ao processar dados do ComprasNet: {str(e)}", "error")
            
        return None

    def processar_pncp(self, dados: Dict[str, Any], card_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados do PNCP e retorna os dados normalizados se houver correspondência
        """
        try:
            if not dados:
                return None
                
            dados_pncp = self.extrair_dados_normalizados(dados, 'pncp')
            dados_card = self.extrair_dados_normalizados(card_info, 'dados_operacao')
            
            if self.dados_correspondem(dados_card, dados_pncp):
                self.log("Dados encontrados no PNCP", "success")
                return dados_pncp
                
        except Exception as e:
            self.log(f"Erro ao processar dados do PNCP: {str(e)}", "error")
            
        return None

    def processar_portal(self, item: Dict[str, Any]) -> bool:
        """
        Processa um item da fila tentando primeiro via API/JSON.
        Retorna True se processado com sucesso, False se precisa usar Firefox.
        """
        self.log(f"\nProcessando item {item.get('ID', 'N/A')} via API/JSON...")
        
        # Tentar encontrar os dados nos JSONs
        dados_encontrados = None
        tipo_origem = None
        
        # Primeiro tenta no ComprasNet
        dados_comprasnet = self.carregar_json('dados_completos_comprasNet.json')
        dados_encontrados = self.processar_comprasnet(dados_comprasnet, item)
        if dados_encontrados:
            tipo_origem = 'ComprasNet'
            
        # Depois tenta no PNCP se não encontrou no ComprasNet
        if not dados_encontrados:
            dados_pncp = self.carregar_json('dados_completos_pncp.json')
            dados_encontrados = self.processar_pncp(dados_pncp, item)
            if dados_encontrados:
                tipo_origem = 'PNCP'
        
        if dados_encontrados and tipo_origem:
            self.atualizar_dados_card(item, dados_encontrados, tipo_origem)
            # Adiciona à pilha de processamento
            self.pilha_processamento.append(item)
            return True
                
        self.log("Dados não encontrados nos JSONs", "info")
        return False

    def processar_pilha_word(self, template_file=None):
        """
        Processa todos os itens da pilha usando o word_processor
        """
        if not self.pilha_processamento:
            self.log("Nenhum item na pilha para processar", "info")
            return
            
        self.log(f"Processando {len(self.pilha_processamento)} itens para o Word...", "info")
        
        # Cria um arquivo JSON temporário com os dados da pilha
        json_temp = os.path.join(self.base_dir, 'data', 'json', 'temp_word_data.json')
        try:
            with open(json_temp, 'w', encoding='utf-8') as f:
                json.dump(self.pilha_processamento, f, ensure_ascii=False, indent=2)
                
            # Processa o arquivo usando o word_processor
            output_file = criar_tabela_word(json_temp, template_file)
            if output_file:
                self.log(f"Documento Word criado com sucesso: {output_file}", "success")
            else:
                self.log("Erro ao criar documento Word", "error")
                
        except Exception as e:
            self.log(f"Erro ao processar pilha para Word: {str(e)}", "error")
        finally:
            # Limpa a pilha após o processamento
            self.pilha_processamento = []
            # Remove o arquivo temporário
            if os.path.exists(json_temp):
                os.remove(json_temp)

def criar_fila_processos() -> Queue:
    """
    Cria uma fila de processos com os portais a serem processados.
    """
    fila = Queue()
    # Adicione aqui a lógica para popular a fila com os portais
    # Por exemplo:
    portais = [{"portal": "portal1", "id_licitacao": "id1"}, {"portal": "portal2", "id_licitacao": "id2"}]  # Lista exemplo
    for portal in portais:
        fila.put(portal)
    return fila

def executar_processamento():
    """
    Função principal que executa o processamento dos portais.
    """
    processador = ProcessadorAPI()
    fila = criar_fila_processos()
    
    while not fila.empty():
        item = fila.get()
        print(f"\nProcessando portal: {item.get('portal', '')}")
        
        sucesso = processador.processar_portal(item)
        if not sucesso:
            print(f"Processamento JSON falhou para {item.get('portal', '')}. Será necessário usar Firefox")
        else:
            print(f"Portal {item.get('portal', '')} processado com sucesso via JSON")
            
    # Processa a pilha de itens para o Word
    processador.processar_pilha_word()

if __name__ == "__main__":
    executar_processamento()