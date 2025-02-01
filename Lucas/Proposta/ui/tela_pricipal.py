
class TelaPrincipal:
    # Lista de portais disponíveis
    PORTAIS_DISPONIVEIS = [
        'bll',
        'comprasnet',
        'compraspublicas',
        'bnc',
        'comprasbr',
        'licitanet'
    ]
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Propostas")
        self.root.state('zoomed')  # Maximiza a janela
        
        # Definir cores
        self.bg_color = "#f0f0f0"
        self.frame_bg = "#ffffff"
        self.highlight_color = "#f5f5f5"
        
        self.root.configure(bg=self.bg_color)
        
        # Frame principal que conterá os três painéis
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configurar o grid com pesos iguais
        self.main_frame.grid_columnconfigure(0, weight=1)  # Controle: 33%
        self.main_frame.grid_columnconfigure(1, weight=2)  # Fila: 33%
        self.main_frame.grid_columnconfigure(2, weight=2)  # Detalhes: 33%
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Inicializar processador de fila
        from fila_processor import FilaProcessor
        self.fila_processor = FilaProcessor()
        self.portal_processor = PortalProcessor()
        
        # Criar os três painéis
        self.criar_painel_controle()  # Painel esquerdo
        self.criar_painel_fila()      # Painel central
        self.criar_painel_detalhes()  # Painel direito
        
        # Inicializar dados
        self.dados_json = None
        self.cards_data = []
        self.output_buffer = []
        self.processando = False
        self.deve_parar = False
        
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        self.adicionar_log("Carregando dados do arquivo JSON...")
        self.dados_json = self.fila_processor.carregar_dados_json(callback_log=self.adicionar_log)
        
        if self.dados_json:
            self.cards_data = self.fila_processor.carregar_cards_aceitos(
                callback_log=self.adicionar_log
            )
            if self.cards_data:
                self.adicionar_log(f"\nTotal de cards aceitos: {len(self.cards_data)}")
                self.adicionar_log("Adicionando cards à fila de processamento...")
                
                # Limpar listbox antes de adicionar novos itens
                self.listbox.delete(0, tk.END)
                
                # Adicionar cada card à listbox
                for card in self.cards_data:
                    texto = f"Pregão: {card.get('pregao', 'N/A')} | Portal: {card.get('portal', 'N/A')} | Empresa: {card.get('empresa', 'N/A')}"
                    self.listbox.insert(tk.END, texto)
                    self.adicionar_log(f"Adicionado à fila: {texto}")
                
                self.atualizar_contador()
                self.iniciar_temporizador()
            else:
                self.finalizar_processamento("Nenhum card em estado 'ACEITAS' encontrado")
        else:
            self.finalizar_processamento("Erro ao carregar dados JSON")
            
    def carregar_cards_aceitos(self):
        if not self.dados_json:
            return
        
        self.cards_data = []
        for empresa_id, empresa_data in self.dados_json.items():
            etapas = empresa_data.get('etapas', {})
            if 'ACEITAS' in etapas:
                cards_aceitos = etapas['ACEITAS'].get('cards', [])
                for card in cards_aceitos:
                    card_processado = {
                        'id': card.get('ID', 'N/A'),
                        'pregao': card.get('Número do pregão', 'N/A'),
                        'portal': card.get('Portal', 'N/A'),
                        'empresa': empresa_data.get('nome_empresa', 'N/A'),
                        'empresa_id': empresa_id,
                        'status': 'ACEITAS',
                        'dados_completos': card
                    }
                    self.cards_data.append(card_processado)
        
        self.atualizar_lista_cards()
        self.atualizar_contador()

    def processar_proximo_item(self):
        """Processa o próximo item da fila"""
        if self.deve_parar:
            self.finalizar_processamento("Processamento interrompido pelo usuário")
            return

        if not self.cards_data:
            self.adicionar_log("Fila vazia. Recarregando todos os cards...")
            self.cards_data = self.fila_processor.carregar_cards_aceitos(self.adicionar_log)
            if not self.cards_data:
                self.finalizar_processamento("Não há mais itens para processar")
                return

        # Pegar o primeiro item
        proximo_item = self.cards_data[0]
        
        # Verificar se tem portal
        portal = proximo_item.get('portal', '').strip()
        
        if not portal or portal not in self.PORTAIS_DISPONIVEIS:
            # Se não tem portal ou não está na lista de portais disponíveis, mover para tela de resultados
            self.adicionar_log(f"Item {proximo_item.get('id', 'N/A')} não tem portal válido. Movendo para resultados...")
            self.adicionar_resultado(f"Item {proximo_item.get('id', 'N/A')} movido para resultados", "info")
            # Remover o item da fila
            self.cards_data = self.cards_data[1:]
        else:
            # Se tem portal válido, processar normalmente
            self.adicionar_log(f"Processando item {proximo_item.get('id', 'N/A')} no portal {portal}...")
            
            # Identificar o portal
            portal_info = self.portal_processor.identificar_portal(proximo_item)
            
            if not portal_info:
                self.adicionar_log(f"Não foi possível identificar o portal para o item {proximo_item.get('id', 'N/A')}")
                # Mover para o próximo item
                self.cards_data = self.cards_data[1:]
            else:
                # Mover o item processado para o final da fila
                self.cards_data = self.cards_data[1:] + [proximo_item]
                self.adicionar_log(f"Item {proximo_item.get('id', 'N/A')} movido para o final da fila")

        # Atualizar o contador
        self.atualizar_contador()
        
        # Continuar o processamento
        if not self.deve_parar:
            self.root.after(1000, self.processar_proximo_item)
    
    def finalizar_processamento(self, mensagem):
        """Finaliza o processamento e atualiza a interface"""
        self.processando = False
        self.deve_parar = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Aguardando")
        self.adicionar_log(mensagem)
            
    def executar_script_info_gerais(self):
        self.adicionar_log("Executando script de coleta de informações gerais...")
        script_path = os.path.join("bitrix", "pega_informacoes_gerais.py")
        
        try:
            # Limpar área de output
            self.output_area.delete('1.0', tk.END)
            self.adicionar_output("Iniciando execução do script...\n", "info")
            
            # Executar o script e capturar a saída em tempo real
            process = subprocess.Popen(
                ["python", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Função para ler a saída em tempo real
            def read_output():
                # Ler stdout
                stdout_line = process.stdout.readline()
                if stdout_line:
                    self.adicionar_output(stdout_line.rstrip(), "info")
                    self.root.after(10, read_output)
                    return
                
                # Ler stderr
                stderr_line = process.stderr.readline()
                if stderr_line:
                    self.adicionar_output(stderr_line.rstrip(), "error")
                    self.root.after(10, read_output)
                    return
                
                # Se não há mais saída, verificar se o processo terminou
                if process.poll() is not None:
                    # Processo terminou
                    if process.returncode == 0:
                        self.adicionar_output("\nScript executado com sucesso!", "success")
                        self.root.after(2000, self.carregar_dados)
                    else:
                        self.adicionar_output("\nErro ao executar o script!", "error")
                        self.btn_iniciar.config(state=tk.NORMAL)
                    return
                
                # Se o processo ainda está rodando, continuar lendo
                self.root.after(10, read_output)
            
            # Iniciar a leitura da saída
            self.root.after(10, read_output)
            return True
            
        except Exception as e:
            self.adicionar_log(f"Erro ao executar o script: {str(e)}")
            self.adicionar_output(f"Erro: {str(e)}", "error")
            return False

    def adicionar_log(self, mensagem):
        """Adiciona uma mensagem ao log"""
        if hasattr(self, 'output_area'):
            timestamp = datetime.now().strftime('[%H:%M:%S]')
            self.output_area.insert(tk.END, f"{timestamp} {mensagem}\n")
            self.output_area.see(tk.END)
            self.output_area.update_idletasks()

    def adicionar_output(self, texto, tag=None):
        """Adiciona texto à área de output com a tag especificada"""
        if hasattr(self, 'output_area'):
            timestamp = datetime.now().strftime('[%H:%M:%S]')
            self.output_area.insert(tk.END, f"{timestamp} {texto}\n", tag)
            self.output_area.see(tk.END)
            self.output_area.update_idletasks()

    def adicionar_resultado(self, mensagem, tipo):
        """Adiciona uma mensagem de resultado na área de output com a tag especificada"""
        # Adicionar timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        mensagem_formatada = f"[{timestamp}] {mensagem}\n"
        
        # Adicionar ao output com a tag apropriada
        self.output_area.insert(tk.END, mensagem_formatada, tipo)
        self.output_area.see(tk.END)  # Rolar para o final
        
        # Atualizar cores baseado no tipo
        self.output_area.tag_config('success', foreground='green')
        self.output_area.tag_config('error', foreground='red')
        
    def criar_painel_controle(self):
        # Painel de Controle (Esquerdo)
        controle_frame = tk.LabelFrame(
            self.main_frame,
            text="Controles",
            padx=10, pady=10,
            bg=self.frame_bg,
            font=('Helvetica', 10, 'bold')
        )
        controle_frame.grid(row=0, column=0, sticky='nsew', padx=5)
        
        # Status
        self.status_label = tk.Label(
            controle_frame,
            text="Status: Aguardando",
            font=('Helvetica', 10),
            bg=self.frame_bg
        )
        self.status_label.pack(pady=(0, 20))
        
        # Botões
        self.btn_iniciar = tk.Button(
            controle_frame,
            text="Iniciar Processamento",
            command=self.iniciar_processamento,
            width=20
        )
        self.btn_iniciar.pack(pady=5)
        
        self.btn_parar = tk.Button(
            controle_frame,
            text="Parar Processamento",
            command=self.parar_processamento_handler,
            width=20,
            state=tk.DISABLED
        )
        self.btn_parar.pack(pady=5)
        
        # Frame para resultados
        resultados_frame = tk.LabelFrame(
            controle_frame,
            text="Resultados",
            padx=10, pady=10,
            bg=self.frame_bg
        )
        resultados_frame.pack(fill='x', pady=(20, 0), expand=True)
        
        # Lista de resultados com scrollbar
        scrollbar = tk.Scrollbar(resultados_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resultados_list = tk.Listbox(
            resultados_frame,
            yscrollcommand=scrollbar.set,
            font=('Consolas', 9),
            bg='black',
            fg='white',
            height=10
        )
        self.resultados_list.pack(fill='both', expand=True)
        scrollbar.config(command=self.resultados_list.yview)
        
    def parar_processamento_handler(self):
        """Para o processamento atual"""
        self.deve_parar = True
        self.btn_parar.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Parando...")
        
    def criar_painel_fila(self):
        # Painel da Fila (Central)
        fila_frame = tk.LabelFrame(
            self.main_frame,
            text="Fila de Processos",
            padx=10, pady=10,
            bg=self.frame_bg,
            font=('Helvetica', 10, 'bold')
        )
        fila_frame.grid(row=0, column=1, sticky='nsew', padx=5)
        
        # Frame para cabeçalho
        header_frame = tk.Frame(fila_frame, bg=self.frame_bg)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Contador
        self.contador_label = tk.Label(
            header_frame,
            text="Total: 0",
            font=('Helvetica', 10),
            bg=self.frame_bg
        )
        self.contador_label.pack(side=tk.RIGHT, padx=5)
        
        # Lista de cards com scrollbar
        scrollbar = tk.Scrollbar(fila_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            fila_frame,
            yscrollcommand=scrollbar.set,
            font=('Helvetica', 10),
            bg=self.highlight_color,
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
    def criar_painel_detalhes(self):
        # Painel de Detalhes (Direito)
        detalhes_frame = tk.LabelFrame(
            self.main_frame,
            text="Resultados e Saída",
            padx=10, pady=10,
            bg=self.frame_bg,
            font=('Helvetica', 10, 'bold')
        )
        detalhes_frame.grid(row=0, column=2, sticky='nsew', padx=5)
        
        # Frame para o texto
        text_frame = tk.Frame(detalhes_frame, bg=self.frame_bg)
        text_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(text_frame, orient="vertical")
        hsb = ttk.Scrollbar(text_frame, orient="horizontal")
        
        # Área de texto para output
        self.output_area = tk.Text(
            text_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='white',  # Mudado para fundo branco
            fg='black',  # Texto preto para melhor legibilidade
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar as tags para diferentes tipos de mensagem
        self.output_area.tag_configure('error', foreground='red')
        self.output_area.tag_configure('success', foreground='green')
        self.output_area.tag_configure('info', foreground='blue')
        
        # Layout dos componentes
        self.output_area.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configurar o redimensionamento
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
    def iniciar_processamento(self):
        """Inicia o processamento dos cards"""
        if self.processando:
            return
            
        self.processando = True
        self.deve_parar = False
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Iniciando...")
        
        # Limpar áreas
        self.output_area.delete('1.0', tk.END)
        self.listbox.delete(0, tk.END)
        self.cards_data = []
        
        # Carregar dados
        self.carregar_dados()
    
    def parar_processamento(self):
        """Para o processamento atual"""
        self.deve_parar = True
        self.btn_parar.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Parando...")
        
    def processar_proximo_item(self):
        """Processa o próximo item da fila"""
        if self.deve_parar:
            self.finalizar_processamento("Processamento interrompido pelo usuário")
            return

        # Calcular o total de itens aceitos
        total_aceitos = len(self.cards_data)

        # Inicializar contador de iterações
        iteracoes = 0

        while iteracoes < total_aceitos:
            if not self.cards_data:
                self.adicionar_log("Fila vazia. Recarregando todos os cards...")
                self.cards_data = self.fila_processor.carregar_cards_aceitos(self.adicionar_log)
                if not self.cards_data:
                    self.finalizar_processamento("Não há mais itens para processar")
                    return

            # Pegar o primeiro item
            proximo_item = self.cards_data[0]
            
            # Verificar se tem portal
            portal = proximo_item.get('portal', '').strip()
            
            if not portal or portal not in self.PORTAIS_DISPONIVEIS:
                # Se não tem portal ou não está na lista de portais disponíveis, mover para tela de resultados
                self.adicionar_log(f"Item {proximo_item.get('id', 'N/A')} não tem portal válido. Movendo para resultados...")
                self.adicionar_resultado(f"Item {proximo_item.get('id', 'N/A')} movido para resultados", "info")
                # Remover o item da fila
                self.cards_data = self.cards_data[1:]
            else:
                # Se tem portal válido, processar normalmente
                self.adicionar_log(f"Processando item {proximo_item.get('id', 'N/A')} no portal {portal}...")
                # Mover o item processado para o final da fila
                self.cards_data = self.cards_data[1:] + [proximo_item]

            # Atualizar o contador
            self.atualizar_contador()

            # Incrementar contador de iterações
            iteracoes += 1

        # Continuar o processamento se necessário
        if not self.deve_parar and self.cards_data:
            self.root.after(1000, self.processar_proximo_item)
    
    def finalizar_processamento(self, mensagem):
        """Finaliza o processamento e atualiza a interface"""
        self.processando = False
        self.deve_parar = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Aguardando")
        self.adicionar_log(mensagem)
            
    def atualizar_contador(self):
        """Atualiza o contador de itens na fila"""
        if hasattr(self, 'contador_label'):
            total = len(self.cards_data) if self.cards_data else 0
            self.contador_label.config(text=f"Total: {total}")