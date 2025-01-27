import tkinter as tk
from tkinter import messagebox
from src.federal import iniciar_federal
from src.fgts import iniciar_fgts  # Certifique-se de que o arquivo fgts.py esteja no mesmo diretório

def rodar_automacao(tipo):
    """Chama a automação federal ou FGTS com o CNPJ fornecido."""
    cnpj = entry_cnpj.get().replace('.', '').replace('/', '').replace('-', '')
    if not validar_cnpj(cnpj):
        messagebox.showerror("Erro", "Por favor, insira um CNPJ válido.")
        return

    # Fecha a janela principal
    janela.destroy()

    try:
        if tipo == 'federal':
            iniciar_federal(cnpj)
        elif tipo == 'fgts':
            iniciar_fgts(cnpj)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar a automação: {e}")
    finally:
        # Reabre a janela principal após a automação
        criar_interface()

def validar_cnpj(cnpj):
    """Valida se o CNPJ informado possui 14 dígitos."""
    return len(cnpj) == 14

def criar_interface():
    """Cria a interface gráfica para a automação."""
    global janela  # Declare a janela como global
    janela = tk.Tk()
    janela.title("Automação")
    janela.geometry("600x400")

    label = tk.Label(janela, text="Digite o CNPJ para iniciar a automação")
    label.pack(pady=10)

    global entry_cnpj
    label_cnpj = tk.Label(janela, text="Digite o CNPJ:")
    label_cnpj.pack(pady=10)
    entry_cnpj = tk.Entry(janela)
    entry_cnpj.pack(pady=5)

    # Botão para a automação Federal
    botao_federal = tk.Button(janela, text="Federal", command=lambda: rodar_automacao('federal'))
    botao_federal.pack(pady=20)

    # Botão para a automação FGTS
    botao_fgts = tk.Button(janela, text="FGTS", command=lambda: rodar_automacao('fgts'))
    botao_fgts.pack(pady=20)

    janela.mainloop()

# Executa a criação da interface
if __name__ == "__main__":
    criar_interface()
 