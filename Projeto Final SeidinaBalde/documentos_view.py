import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database_mysql as database
import datetime
import os


class DocumentosView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Gestão de Documentos",
                 font=("Arial", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        form = tk.Frame(self, bg="white")
        form.pack(pady=10)

        tk.Label(form, text="Título:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.titulo_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Tipo:", bg="white", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.tipo_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.tipo_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Data:", bg="white", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.data_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.data_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.data_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Caminho:", bg="white", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.caminho_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.caminho_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form, text="Escolher Arquivo", command=self.escolher_arquivo).grid(row=3, column=2, padx=5)
        ttk.Button(form, text="Guardar Documento", command=self.guardar_documento).grid(row=4, column=0, columnspan=3, pady=10)

        self.tabela = ttk.Treeview(self,
                                   columns=("id", "titulo", "tipo", "data", "caminho"),
                                   show="headings", height=12)
        self.tabela.pack(pady=20, fill="x")

        colunas = [
            ("id", 50),
            ("titulo", 200),
            ("tipo", 100),
            ("data", 120),
            ("caminho", 300)
        ]

        for nome, largura in colunas:
            self.tabela.heading(nome, text=nome.capitalize())
            self.tabela.column(nome, width=largura)

        self.tabela.bind("<Double-1>", self.abrir_documento)

        self.carregar_documentos()

    def escolher_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Escolher Documento",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.caminho_entry.delete(0, tk.END)
            self.caminho_entry.insert(0, caminho)

    def guardar_documento(self):
        titulo = self.titulo_entry.get().strip()
        tipo = self.tipo_entry.get().strip()
        data = self.data_entry.get().strip()
        caminho = self.caminho_entry.get().strip()

        if not titulo or not tipo or not caminho:
            messagebox.showwarning("Aviso", "Preencha título, tipo e caminho.")
            return

        sucesso = database.adicionar_documento(titulo, tipo, data, caminho)
        if sucesso:
            messagebox.showinfo("Sucesso", "Documento guardado com sucesso!")
            self.carregar_documentos()
            self.titulo_entry.delete(0, tk.END)
            self.tipo_entry.delete(0, tk.END)
            self.caminho_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Falha ao guardar documento.")

    def carregar_documentos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        dados = database.listar_documentos()
        for d in dados:
            self.tabela.insert("", tk.END, values=(
                d["id"], d["titulo"], d["tipo"], d["data"], d["caminho"]
            ))

    def abrir_documento(self, event):
        selecao = self.tabela.selection()
        if not selecao:
            return

        item = selecao[0]
        valores = self.tabela.item(item, "values")
        caminho = valores[4]

        if os.path.exists(caminho):
            os.startfile(caminho)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
