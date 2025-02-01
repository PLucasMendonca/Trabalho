import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from bnc_automation import wait_for_login
import pandas as pd
import win32com.client
from pywinauto import Application
import time

class ItemDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cadastro de Item")
        self.items_data = {}
        self.parent = parent
        
        # Checkbox Selecionar Todos
        self.select_all_var = tk.BooleanVar()
        self.select_all_check = ttk.Checkbutton(self, text="Marcar todos como próprio", variable=self.select_all_var, command=self.on_select_all_changed)
        self.select_all_check.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Campos do formulário
        ttk.Label(self, text="Item:").grid(row=1, column=0, padx=5, pady=5)
        self.item_entry = ttk.Entry(self)
        self.item_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Valor:").grid(row=2, column=0, padx=5, pady=5)
        self.valor_entry = ttk.Entry(self)
        self.valor_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Marca:").grid(row=3, column=0, padx=5, pady=5)
        self.marca_entry = ttk.Entry(self)
        self.marca_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Modelo:").grid(row=4, column=0, padx=5, pady=5)
        self.modelo_entry = ttk.Entry(self)
        self.modelo_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botões
        ttk.Button(self, text="Adicionar Item", command=self.add_item).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Finalizar", command=self.finish).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Lista de itens
        self.tree = ttk.Treeview(self, columns=("Item", "Valor", "Marca", "Modelo"), show="headings", selectmode="extended")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
        # Configurar cabeçalhos
        self.tree.heading("Item", text="Item")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Modelo", text="Modelo")
        
        # Configurar larguras das colunas
        for col in ("Item", "Valor", "Marca", "Modelo"):
            self.tree.column(col, width=100)
        
        # Ajustar o tamanho da janela
        self.geometry("400x600")
        
        self.grab_set()  # Torna a janela modal
    
    def add_item(self):
        item = self.item_entry.get().strip()
        valor = self.valor_entry.get().strip()
        marca = self.marca_entry.get().strip()
        modelo = self.modelo_entry.get().strip()
        
        if not all([item, valor]):
            messagebox.showerror("Erro", "Item e Valor são obrigatórios!")
            return

        # Se o checkbox "Selecionar Todos" estiver marcado, usa "proprio" para marca e modelo
        if self.select_all_var.get():
            marca = "proprio"
            modelo = "proprio"
        elif not all([marca, modelo]):
            messagebox.showerror("Erro", "Marca e Modelo são obrigatórios quando não estiver marcado 'Marcar todos como próprio'!")
            return
        
        try:
            # Tenta converter o item para número
            item_num = int(item.lstrip('0')) # Remove zeros à esquerda antes de converter
            # Formata o item como número com 2 dígitos
            item = str(item_num).zfill(2)
            
            # Converte o valor para float
            valor = float(valor.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "O item deve ser um número e o valor deve ser um número válido!")
            return
        
        # Adiciona à lista e ao dicionário
        self.items_data[item] = {
            "valor": valor,
            "marca": marca,
            "modelo": modelo
        }
        
        # Adiciona à árvore
        self.tree.insert("", "end", values=(f"Item {item}", valor, marca, modelo))
        
        # Limpa os campos
        for entry in (self.item_entry, self.valor_entry, self.marca_entry, self.modelo_entry):
            entry.delete(0, tk.END)
    
    def on_select_all_changed(self):
        if self.select_all_var.get():
            messagebox.showinfo("Configuração Salva",
                             "Todos os itens serão cadastrados com marca e modelo 'proprio'.\n"
                             "Esta configuração será usada ao processar o arquivo xlsx.")
            # Salvar a configuração para uso posterior
            self.parent.set_mark_all_as_proprio(True)
        else:
            self.parent.set_mark_all_as_proprio(False)

    def finish(self):
        if not self.items_data:
            if not messagebox.askyesno("Confirmar", "Nenhum item foi cadastrado. Deseja continuar mesmo assim?"):
                return
        
        # Salva os dados em um arquivo JSON
        project_dir = os.path.dirname(os.path.abspath(__file__))
        config = {
            "items_data": self.items_data,
            "mark_all_as_proprio": self.select_all_var.get()
        }
        with open(os.path.join(project_dir, "items_data.json"), 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        
        self.destroy()

class DocumentsDialog(tk.Toplevel):
    def __init__(self, parent, documents_data):
        super().__init__(parent)
        self.title("Documentos")
        self.documents_data = documents_data
        self.geometry("800x600")

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        if not documents_data:
            ttk.Label(
                scrollable_frame,
                text="Nenhum documento encontrado.",
                font=("Arial", 12)
            ).pack(pady=20)
        else:
            for doc in documents_data:
                frame = ttk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, padx=5, pady=5)

                doc_name = doc.get("name", "")
                is_required = doc.get("required", False)
                required_text = "* Obrigatório" if is_required else "Opcional"

                ttk.Label(
                    frame,
                    text=f"{doc_name} ({required_text})",
                    font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=5)

                ttk.Button(
                    frame,
                    text="Anexar Arquivo",
                    command=lambda d=doc: self.attach_file(d)
                ).pack(side=tk.LEFT, padx=5)

                if not is_required:
                    ttk.Radiobutton(
                        frame,
                        text="Não possui",
                        value=True
                    ).pack(side=tk.LEFT, padx=5)

                ttk.Label(frame, text="").pack(side=tk.LEFT, padx=5)
                ttk.Separator(scrollable_frame).pack(fill=tk.X, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="Enviar Documentos",
            command=self.submit_documents
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.grab_set()

    def attach_file(self, document):
        file_path = filedialog.askopenfilename(
            title=f"Selecione o arquivo para {document.get('name', '')}",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            document["file_path"] = file_path

    def submit_documents(self):
        missing_required = [
            doc.get("name", "")
            for doc in self.documents_data
            if doc.get("required", False) and not doc.get("file_path")
        ]
        if missing_required:
            messagebox.showerror(
                "Erro",
                f"Os seguintes documentos obrigatórios não foram anexados:\n\n" +
                "\n".join(missing_required)
            )
            return

        messagebox.showinfo("Sucesso", "Documentos enviados com sucesso!")
        self.destroy()


class AutomationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automação BNC")
        self.mark_all_as_proprio = False
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos de login
        ttk.Label(main_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame)
        self.email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(main_frame, text="Senha:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Botão de Cadastro de Itens
        ttk.Button(main_frame, text="Cadastrar Itens", command=self.open_item_dialog).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Campos existentes
        ttk.Label(main_frame, text="Número do Processo:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.number_entry = ttk.Entry(main_frame)
        self.number_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        self.number_entry.insert(0, "999")
        
        ttk.Label(main_frame, text="Estado:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.state_entry = ttk.Entry(main_frame)
        self.state_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        self.state_entry.insert(0, "DF")
        
        ttk.Label(main_frame, text="Cidade:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.city_entry = ttk.Entry(main_frame)
        self.city_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Radio buttons para ME/EPP
        self.is_me = tk.BooleanVar(value=True)
        ttk.Radiobutton(main_frame, text="ME/EPP - Sim", variable=self.is_me, value=True).grid(row=6, column=0, pady=5)
        ttk.Radiobutton(main_frame, text="ME/EPP - Não", variable=self.is_me, value=False).grid(row=6, column=1, pady=5)
        
         # Radio buttons para participar em todos os itens ou não
        self.all_itens_participate = tk.BooleanVar(value=True)
        # ttk.Radiobutton(main_frame, text="Vai participar de todos os itens - Sim", variable=self.all_itens_participate, value=True).grid(row=4, column=0, pady=5)
        # ttk.Radiobutton(main_frame, text="Vai participar de todos os itens - Não", variable=self.all_itens_participate, value=False).grid(row=4, column=1, pady=5)

        
        
        # Botão de início
        ttk.Button(main_frame, text="Iniciar Automação", command=self.start_automation).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Configura o grid
        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)
        
        # Centraliza a janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def open_item_dialog(self):
        ItemDialog(self.root)
    
    def set_mark_all_as_proprio(self, value):
        self.mark_all_as_proprio = value
    
    def start_automation(self):
        # Verificar se email e senha foram preenchidos
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Erro", "Por favor, preencha o email e a senha!")
            return
        
        driver = None
        try:
            # Iniciar automação BLL
            from bll import start_bll_automation
            driver = start_bll_automation(email, password)
            
            if driver:
                # Se o login no BLL foi bem sucedido, continuar com BNC
                from bnc_automation import wait_for_login
                
                # Pegar os valores dos campos
                process_number = self.number_entry.get()
                state = self.state_entry.get()
                city = self.city_entry.get()
                is_me = self.is_me.get()
                all_itens = self.all_itens_participate.get()
                
                # Chamar a automação do BNC
                wait_for_login(driver, process_number, state, city, is_me)
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a automação: {str(e)}")
        finally:
            if driver:
                driver.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AutomationGUI()
    app.run()
