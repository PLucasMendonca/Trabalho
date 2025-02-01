class TelaFila:
    def __init__(self, dados_json):
        self.root = tk.Toplevel()
        self.root.title("Fila de Processos")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Fila de Processos Aceitos",
            font=('Helvetica', 18, 'bold')
        )
        titulo.pack(pady=20)
        
        # Frame para lista de cards
        self.cards_frame = tk.Frame(main_frame)
        self.cards_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Lista de cards com scrollbar
        cards_scrollbar = tk.Scrollbar(self.cards_frame)
        cards_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cards_listbox = tk.Listbox(
            self.cards_frame,
            height=10,
            width=50,
            yscrollcommand=cards_scrollbar.set,
            font=('Helvetica', 10)
        )
        self.cards_listbox.pack(fill='both', expand=True)
        cards_scrollbar.config(command=self.cards_listbox.yview)
        
        # Botão para ver detalhes
        self.btn_detalhes = tk.Button(
            main_frame,
            text="Ver Detalhes",
            command=self.ver_detalhes,
            font=('Helvetica', 12),
            width=20,
            height=2
        )
        self.btn_detalhes.pack(pady=20)
        
        # Armazena os dados JSON
        self.dados_json = dados_json
        self.cards_data = []  # Armazena os dados completos dos cards
        
        # Carregar cards aceitos
        self.carregar_cards_aceitos()
        
        # Bind do duplo clique
        self.cards_listbox.bind('<Double-Button-1>', lambda e: self.ver_detalhes())
    
    def carregar_cards_aceitos(self):
        
        try:
            self.cards_data = []  # Limpa os dados anteriores
            
            for empresa_id, info in self.dados_json.items():
                etapas = info.get('etapas', {})
                if 'ACEITAS' in etapas:
                    nome_empresa = info["nome_empresa"]
                    for card in info["etapas"]["ACEITAS"]["cards"]:
                        numero_pregao = card.get("Número do pregão", "N/A")
                        portal = card.get("Portal", "N/A")
                        # Armazena o card completo e o texto para display
                        self.cards_data.append({
                            'texto': f"{nome_empresa} - Pregão: {numero_pregao} - Portal: {portal}",
                            'dados': {
                                'empresa_id': empresa_id,
                                'empresa': info,
                                'card': card
                            }
                        })
            
            # Limpa a lista atual
            self.cards_listbox.delete(0, tk.END)
            
            # Adiciona os cards encontrados
            for card in self.cards_data:
                self.cards_listbox.insert(tk.END, card['texto'])
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar cards: {str(e)}")
    
    def ver_detalhes(self):
        selection = self.cards_listbox.curselection()
        if selection:
            index = selection[0]
            dados_card = self.cards_data[index]['dados']
            TelaDetalhes(dados_card)