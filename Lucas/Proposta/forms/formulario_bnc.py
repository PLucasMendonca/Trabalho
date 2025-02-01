class FormularioBNC(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_edital = self.criar_campo(self.campos_frame, "N° do Edital:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        # Configurar as opções da modalidade
        if isinstance(self.modalidade, ttk.Combobox):
            self.modalidade['values'] = MODALIDADES.get(self.portal_id, [])
            self.modalidade.set('Selecione a modalidade')  # Valor padrão
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Edital: {registro['numero_edital']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_edital": self.numero_edital.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_edital.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('Selecione a modalidade')