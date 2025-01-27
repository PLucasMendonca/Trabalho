import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def extrair_itens_da_pagina(driver):
    """Extrai itens da página atual usando BeautifulSoup."""
    # Aguardar elemento estar presente
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "app-cadastro-propostas-itens"))
    )
    
    # Capturar HTML da página atual
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Selecionar todos os itens na página
    itens = []
    for item in soup.select(".cp-itens-card"):
        numero = item.select_one(".dots.cp-item-bold").text.strip() if item.select_one(".dots.cp-item-bold") else None
        descricao = item.select_one(".text-uppercase").text.strip() if item.select_one(".text-uppercase") else None
        quantidade = item.select_one(".cp-texto-item .mb-half-half").text.strip() if item.select_one(".cp-texto-item .mb-half-half") else None
        valor_estimado = item.select_one(".cp-valor-item span").text.strip() if item.select_one(".cp-valor-item span") else None
        
        itens.append({
            "Número": numero,
            "Descrição": descricao,
            "Quantidade": quantidade,
            "Valor Estimado": valor_estimado
        })
    return itens

class InterfaceItens:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Itens do Pregão")
        
        # Criar Treeview
        self.tree = ttk.Treeview(root, columns=("Número", "Descrição", "Quantidade", "Valor Estimado"), show="headings")
        
        # Definir cabeçalhos
        self.tree.heading("Número", text="Número")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Valor Estimado", text="Valor Estimado")
        
        # Configurar larguras das colunas
        self.tree.column("Número", width=100)
        self.tree.column("Descrição", width=300)
        self.tree.column("Quantidade", width=100)
        self.tree.column("Valor Estimado", width=150)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def atualizar_itens(self, itens):
        # Limpar itens existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Inserir novos itens
        for item in itens:
            self.tree.insert("", "end", values=(
                item["Número"],
                item["Descrição"],
                item["Quantidade"],
                item["Valor Estimado"]
            ))

def main():
    root = tk.Tk()
    interface = InterfaceItens(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()
