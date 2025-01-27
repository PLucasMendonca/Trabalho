import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from src.modules.certidoes.federal import iniciar_federal
from src.modules.certidoes.fgts import iniciar_fgts
from src.modules.certidoes.trabalhista import iniciar_trabalhista
from src.modules.certidoes.tcu import iniciar_tcu
from src.modules.certidoes.SINTEGRA.dif import iniciar_dif


DIRETORIO_CLIENTES = "src/data/empresas.json"


class TelaCliente:
    
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500")
        self.master.title("Clientes")

        self.dadosEmpresas = self.carregar_dados_json()

        self.mostrarApenasAtivos = BooleanVar()

        self.entry_busca = Entry(self.master)
        self.entry_busca.grid(row=0, column=0, columnspan=2, padx=10, pady=10, stick="ew")
        self.master = master
        self.master.geometry("1000x500")
        self.master.title("Clientes")

        self.dadosEmpresas = self.carregar_dados_json()

        self.mostrarApenasAtivos = BooleanVar()

        self.entry_busca = Entry(self.master)
        self.entry_busca.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", self.filtrar_dados)

        self.treeViewDados = ttk.Treeview(self.master, column=(1, 2, 3, 4), show="headings")
        self.configurar_treeview()

        self.labelNumeroRegistros = Label(self.master, text="Registros: ", font="Arial 12")
        self.labelNumeroRegistros.grid(row=3, column=0, columnspan=4, sticky="W")

        self.checkAtivos = Checkbutton(self.master, text="Mostrar apenas clientes ativos", variable=self.mostrarApenasAtivos, command=self.alternar_filtro)
        self.checkAtivos.grid(row=3, column=4, columnspan=4, sticky="E")
        
        self.automacao_opcoes = ["Federal", "FGTS", "TCU", "Trabalhista", "DIF"]
        self.combo_automacao = ttk.Combobox(self.master, values=self.automacao_opcoes, state="disabled")
        self.combo_automacao.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.botao_executar = ttk.Button(self.master, text="Iniciar", command=self.executar_automacao, state="disabled")
        self.botao_executar.grid(row=4, column=1, padx=10, pady=10)

        self.preencher_dados_treeview(self.dadosEmpresas)

    def carregar_dados_json(self):
        try:
            with open(DIRETORIO_CLIENTES, 'r', encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo JSON não encontrado!")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Erro ao decodificar o arquivo JSON!")
            return []

    def configurar_treeview(self):
        estiloDaTreeview = ttk.Style()
        estiloDaTreeview.theme_use("alt")
        estiloDaTreeview.configure(".", font="Arial 12")

        self.treeViewDados.column("1", anchor=CENTER, width="50")
        self.treeViewDados.heading("1", text="ID")

        self.treeViewDados.column("2", anchor=CENTER, width="600")
        self.treeViewDados.heading("2", text="Razão Social")

        self.treeViewDados.column("3", anchor=CENTER, width="150")
        self.treeViewDados.heading("3", text="CNPJ")

        self.treeViewDados.column("4", anchor=CENTER, width="100")
        self.treeViewDados.heading("4", text="Status")

        self.treeViewDados.grid(row=2, column=0, columnspan=8, stick="NSEW")
        self.treeViewDados.bind("<<TreeviewSelect>>", self.on_tree_select)
    
    def preencher_dados_treeview(self, dados, filtrar_ativos=False):
        for item in self.treeViewDados.get_children():
            self.treeViewDados.delete(item)
        for empresa in dados:
            if not filtrar_ativos or (filtrar_ativos and empresa.get("CLIENTE ATIVO")):
                self.treeViewDados.insert("", "end",
                    values=(
                        empresa.get("ID_Empresa"),
                        empresa.get("Nome_Empresa"),
                        empresa.get("CNPJ", "N/A"),
                        "Sim" if empresa.get("CLIENTE ATIVO") else "Não"
                    ))
        self.contar_registros()

    def contar_registros(self):
        numero = len(self.treeViewDados.get_children())
        self.labelNumeroRegistros.config(text="Registros: " + str(numero) + " encontrados.")

    def alternar_filtro(self):
        self.preencher_dados_treeview(self.dadosEmpresas, filtrar_ativos=self.mostrarApenasAtivos.get())

    def filtrar_dados(self, event):
        busca = self.entry_busca.get().lower()
        dados_filtrados = [empresa for empresa in self.dadosEmpresas if busca in empresa.get("Nome_Empresa", "").lower()]
        self.preencher_dados_treeview(dados_filtrados, filtrar_ativos=self.mostrarApenasAtivos.get())

    def on_tree_select(self, event):
        item = self.treeViewDados.selection()
        if item:
            self.combo_automacao.config(state="normal")
            self.botao_executar.config(state="normal")

    def executar_automacao(self):
        
        global janela_certidoes
        item = self.treeViewDados.selection()
        if item:
            cnpj = self.treeViewDados.item(item)["values"][2]
            automacao_selecionada = self.combo_automacao.get()
            messagebox.showinfo("Automação", f"Executando {automacao_selecionada} para o CNPJ: {cnpj}")

            self.master.withdraw()
            if automacao_selecionada == "Federal":
                iniciar_automacao_federal(cnpj)
            elif automacao_selecionada == "FGTS":
                self.iniciar_automacao_fgts(cnpj)
            elif automacao_selecionada == "TCU":
                self.iniciar_automacao_tcu(cnpj)
            elif automacao_selecionada == "Trabalhista":
                self.iniciar_automacao_trabalhista(cnpj)
            elif automacao_selecionada == "DIF":
                self.iniciar_automacao_dif(cnpj)
            else:
                messagebox.showerror("Erro", "Automação não encontrada.")
            
            self.master.deiconify()

def abrir_tela():
    root = Tk()
    app = TelaCliente(root)
    root.mainloop()
