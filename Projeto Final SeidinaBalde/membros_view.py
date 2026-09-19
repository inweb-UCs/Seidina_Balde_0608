import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database_mysql as database
import datetime
import os

class MembrosView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Gestão de Membros",
                 font=("Arial", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        # ============================
        # FORMULÁRIO DE REGISTO
        # ============================

        form = tk.Frame(self, bg="white")
        form.pack(pady=10)

        # Nome
        tk.Label(form, text="Nome:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # BI
        tk.Label(form, text="BI:", bg="white", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.bi_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.bi_entry.grid(row=1, column=1, padx=5, pady=5)

        # Data de nascimento
        tk.Label(form, text="Data de Nascimento:", bg="white", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.data_nasc_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.data_nasc_entry.insert(0, "2000-01-01")
        self.data_nasc_entry.grid(row=2, column=1, padx=5, pady=5)

        # Função
        tk.Label(form, text="Função:", bg="white", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.funcao_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.funcao_entry.grid(row=3, column=1, padx=5, pady=5)

        # Morada
        tk.Label(form, text="Morada:", bg="white", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
        self.morada_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.morada_entry.grid(row=4, column=1, padx=5, pady=5)

        # Contacto
        tk.Label(form, text="Contacto:", bg="white", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5)
        self.contacto_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.contacto_entry.grid(row=5, column=1, padx=5, pady=5)

        # Data de entrada
        tk.Label(form, text="Data de Entrada:", bg="white", font=("Arial", 12)).grid(row=6, column=0, padx=5, pady=5)
        self.data_entrada_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.data_entrada_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.data_entrada_entry.grid(row=6, column=1, padx=5, pady=5)

        # Foto
        tk.Label(form, text="Foto:", bg="white", font=("Arial", 12)).grid(row=7, column=0, padx=5, pady=5)
        self.foto_entry = tk.Entry(form, font=("Arial", 12), width=40)
        self.foto_entry.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(form, text="Escolher Foto", command=self.escolher_foto).grid(row=7, column=2, padx=5)
        ttk.Button(form, text="Salvar Membro", command=self.salvar_membro).grid(row=8, column=0, columnspan=3, pady=10)

        # ============================
        # TABELA DE MEMBROS
        # ============================

        self.tabela = ttk.Treeview(self,
                                   columns=("id", "nome", "bi", "data_nascimento", "funcao",
                                            "morada", "contacto", "data_entrada", "foto"),
                                   show="headings", height=12)
        self.tabela.pack(pady=20, fill="x")

        colunas = [
            ("id", 50),
            ("nome", 200),
            ("bi", 120),
            ("data_nascimento", 120),
            ("funcao", 150),
            ("morada", 200),
            ("contacto", 120),
            ("data_entrada", 120),
            ("foto", 200)
        ]

        for nome, largura in colunas:
            self.tabela.heading(nome, text=nome.capitalize())
            self.tabela.column(nome, width=largura)

        # Botão eliminar
        ttk.Button(self, text="Eliminar Membro Selecionado", command=self.eliminar_membro).pack(pady=10)

        self.carregar_membros()

    # ==========================================================
    # FUNÇÕES
    # ==========================================================

    def escolher_foto(self):
        caminho = filedialog.askopenfilename(
            title="Escolher Foto",
            filetypes=[("Imagens", "*.jpg *.png *.jpeg"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.foto_entry.delete(0, tk.END)
            self.foto_entry.insert(0, caminho)

    def salvar_membro(self):
        nome = self.nome_entry.get().strip()
        bi = self.bi_entry.get().strip()
        data_nasc = self.data_nasc_entry.get().strip()
        funcao = self.funcao_entry.get().strip()
        morada = self.morada_entry.get().strip()
        contacto = self.contacto_entry.get().strip()
        data_entrada = self.data_entrada_entry.get().strip()
        foto = self.foto_entry.get().strip()

        if not nome or not bi or not contacto:
            messagebox.showwarning("Aviso", "Nome, BI e Contacto são obrigatórios.")
            return

        sucesso = database.adicionar_membro(
            nome, bi, data_nasc, funcao, morada, contacto, data_entrada, foto
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Membro salvo com sucesso!")
            self.carregar_membros()
            self.limpar_formulario()
        else:
            messagebox.showerror("Erro", "Falha ao salvar membro.")

    def carregar_membros(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        dados = database.listar_membros()
        for m in dados:
            self.tabela.insert("", tk.END, values=(
                m["id"], m["nome"], m["bi"], m["data_nascimento"],
                m["funcao"], m["morada"], m["contacto"],
                m["data_entrada"], m["foto"]
            ))

    def eliminar_membro(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um membro para eliminar.")
            return

        item = selecao[0]
        valores = self.tabela.item(item, "values")
        id_membro = valores[0]

        if messagebox.askyesno("Confirmar", "Deseja eliminar este membro?"):
            sucesso = database.eliminar_membro(id_membro)
            if sucesso:
                messagebox.showinfo("Sucesso", "Membro eliminado.")
                self.carregar_membros()
            else:
                messagebox.showerror("Erro", "Não foi possível eliminar o membro.")

    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
        self.bi_entry.delete(0, tk.END)
        self.data_nasc_entry.delete(0, tk.END)
        self.funcao_entry.delete(0, tk.END)
        self.morada_entry.delete(0, tk.END)
        self.contacto_entry.delete(0, tk.END)
        self.data_entrada_entry.delete(0, tk.END)
        self.foto_entry.delete(0, tk.END)
