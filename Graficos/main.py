import tkinter as tk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------
# Função de ligação à BD
# ---------------------------
def ligar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # coloca a tua password se tiver
        database="escola"
    )

# ---------------------------
# Carregar dados e mostrar gráfico
# ---------------------------
def carregar_dados():
    try:
        conn = ligar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, nota FROM alunos")
        dados = cursor.fetchall()

        if not dados:
            messagebox.showinfo("Informação", "Não existem alunos na tabela.")
            return

        nomes = [d[0] for d in dados]
        notas = [d[1] for d in dados]

        # Criar figura
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(nomes, notas, color="cornflowerblue")
        ax.set_title("Notas dos Alunos")
        ax.set_ylabel("Nota")
        ax.set_xlabel("Aluno")
        ax.set_ylim(0, 20)

        # Limpar gráfico anterior
        for widget in frame_grafico.winfo_children():
            widget.destroy()

        # Inserir gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

        cursor.close()
        conn.close()

    except Exception as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

# ---------------------------
# Melhor aluno
# ---------------------------
def melhor_aluno():
    try:
        conn = ligar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, nota FROM alunos ORDER BY nota DESC LIMIT 1")
        melhor = cursor.fetchone()

        if melhor:
            nome, nota = melhor
            messagebox.showinfo("Melhor Aluno",
                                f"O melhor aluno é {nome} com nota {nota}.")
        else:
            messagebox.showinfo("Informação", "Não existem alunos na tabela.")

        cursor.close()
        conn.close()

    except Exception as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

# ---------------------------
# Interface Tkinter
# ---------------------------
janela = tk.Tk()
janela.title("Notas dos Alunos")
janela.geometry("800x600")

# Título
titulo = tk.Label(janela, text="Notas dos Alunos",
                  font=("Arial", 18, "bold"))
titulo.pack(pady=10)

# Área do gráfico
frame_grafico = tk.Frame(janela)
frame_grafico.pack(pady=20)

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

btn_carregar = tk.Button(frame_botoes, text="Carregar Dados",
                         font=("Arial", 12), width=15,
                         command=carregar_dados)
btn_carregar.grid(row=0, column=0, padx=10)

btn_melhor = tk.Button(frame_botoes, text="Melhor Aluno",
                       font=("Arial", 12), width=15,
                       command=melhor_aluno)
btn_melhor.grid(row=0, column=1, padx=10)

btn_sair = tk.Button(frame_botoes, text="Sair",
                     font=("Arial", 12), width=15,
                     command=janela.destroy)
btn_sair.grid(row=0, column=2, padx=10)

janela.mainloop()
