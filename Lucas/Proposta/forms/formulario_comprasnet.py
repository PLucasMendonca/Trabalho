class FormularioComprasNet(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_compra = self.criar_campo(self.campos_frame, "N° da Compra:")
        self.uasg = self.criar_campo(self.campos_frame, "UASG:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Compra: {registro['numero_compra']} - UASG: {registro['uasg']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_compra": self.numero_compra.get(),
            "uasg": self.uasg.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_compra.delete(0, tk.END)
        self.uasg.delete(0, tk.END)
        self.modalidade.set('Selecione a modalidade')