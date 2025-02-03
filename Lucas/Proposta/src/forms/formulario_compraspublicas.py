
class FormularioComprasPublicas(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_processo = self.criar_campo(self.campos_frame, "N° do Processo:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Processo: {registro['numero_processo']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_processo": self.numero_processo.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_processo.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('Selecione a modalidade')