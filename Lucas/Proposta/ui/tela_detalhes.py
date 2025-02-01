class TelaDetalhes:
    def __init__(self, dados_processo):
        self.root = tk.Toplevel()
        self.root.title("Detalhes do Processo")
        self.root.geometry("1000x600")
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Detalhes Completos do Processo",
            font=('Helvetica', 18, 'bold')
        )
        titulo.pack(pady=20)
        
        # Frame para a árvore de dados
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview para mostrar os dados em formato de árvore
        self.tree = ttk.Treeview(tree_frame, selectmode='browse',
                                yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set)
        
        # Configurar scrollbars
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Posicionar elementos
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)
        
        # Configurar colunas
        self.tree["columns"] = ("Valor",)
        self.tree.column("#0", width=300, stretch=tk.NO)
        self.tree.column("Valor", width=500, stretch=tk.NO)
        
        self.tree.heading("#0", text="Campo")
        self.tree.heading("Valor", text="Valor")
        
        # Preencher a árvore com os dados
        self.preencher_arvore(dados_processo)
    
    def preencher_arvore(self, dados, parent=""):
        if isinstance(dados, dict):
            for key, value in dados.items():
                item_id = self.tree.insert(parent, "end", text=str(key))
                if isinstance(value, (dict, list)):
                    self.preencher_arvore(value, item_id)
                else:
                    self.tree.insert(parent, "end", text=str(key), values=(str(value),))
        elif isinstance(dados, list):
            for i, item in enumerate(dados):
                item_id = self.tree.insert(parent, "end", text=f"Item {i+1}")
                if isinstance(item, (dict, list)):
                    self.preencher_arvore(item, item_id)
                else:
                    self.tree.insert(parent, "end", text=str(item))
