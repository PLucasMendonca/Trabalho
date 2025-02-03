import tkinter as tk
from tkinter import messagebox

class TelaFila:
    def __init__(self, dados_json):
        self.root = tk.Toplevel()
        self.root.title("Fila de Propostas")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Propostas Aceitas",
            font=('Helvetica', 18, 'bold')
        )
        titulo.pack(pady=20)
        
        # Frame para lista de propostas
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lista de propostas
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Helvetica', 10),
            selectmode=tk.SINGLE
        )
        self.listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Contador de propostas
        self.contador = tk.Label(
            main_frame,
            text="Total: 0 propostas",
            font=('Helvetica', 10)
        )
        self.contador.pack(pady=10)
        
        # Armazena os dados
        self.dados_json = dados_json
        self.propostas = []
        
        # Carregar propostas
        self.carregar_propostas()
        
    def carregar_propostas(self):
        """Carrega as propostas do JSON para a listbox"""
        try:
            self.propostas = []
            self.listbox.delete(0, tk.END)
            
            for empresa_id, info in self.dados_json.items():
                if 'etapas' in info and 'ACEITAS' in info['etapas']:
                    nome_empresa = info.get('nome_empresa', 'N/A')
                    for card in info['etapas']['ACEITAS']['cards']:
                        proposta = {
                            'pregao': card.get('Número do pregão', 'N/A'),
                            'portal': card.get('Portal', 'N/A'),
                            'empresa': nome_empresa,
                            'cidade': card.get('Cidade', 'N/A'),
                            'estado': card.get('Estado', 'N/A'),
                            'objeto': card.get('Objeto', 'N/A'),
                            'data': card.get('Data', 'N/A'),
                            'valor': card.get('AO ESTIMADO ÓRGÃO', 'N/A')
                        }
                        
                        # Texto para exibição
                        texto = f"Pregão: {proposta['pregao']} | Portal: {proposta['portal']} | Empresa: {proposta['empresa']}"
                        
                        self.propostas.append(proposta)
                        self.listbox.insert(tk.END, texto)
            
            # Atualizar contador
            total = len(self.propostas)
            self.contador.config(text=f"Total: {total} propostas")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar propostas: {str(e)}")
    
    def atualizar_lista(self, propostas):
        """Atualiza a lista de propostas"""
        self.listbox.delete(0, tk.END)
        self.propostas = propostas
        
        for proposta in propostas:
            texto = f"Pregão: {proposta['pregao']} | Portal: {proposta['portal']} | Empresa: {proposta['empresa']}"
            self.listbox.insert(tk.END, texto)
            
        self.contador.config(text=f"Total: {len(propostas)} propostas")