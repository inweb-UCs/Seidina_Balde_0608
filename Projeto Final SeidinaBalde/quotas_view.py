import tkinter as tk
from tkinter import ttk, messagebox
import database_mysql as database


class QuotasView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Gestão de Quotas / Pagamentos",
                 font=("Arial", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        form = tk.Frame(self, bg="white")
        form.pack(pady=10)

        tk.Label(form, text="Membro ID:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.membro_id_entry = tk.Entry(form, font=("Arial", 12), width=20)
        self.membro_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Ano:", bg="white", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.ano_entry = tk.Entry(form, font=("Arial", 12), width=20)
        self.ano_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Mês:", bg="white", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.mes_entry = tk.Entry(form, font=("Arial", 12), width=20)
        self.mes_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Valor:", bg="white", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.valor_entry = tk.Entry(form, font=("Arial", 12), width=20)
        self.valor_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form, text="Registar Pagamento", command=self.registar_pagamento).grid(row=4, column=0, columnspan=2, pady=10)

        self.tabela = ttk.Treeview(self,
                                   columns=("id", "membro", "ano", "mes", "valor"),
                                   show="headings", height=12)
        self.tabela.pack(pady=20, fill="x")

        colunas = [
            ("id", 50),
            ("membro", 200),
            ("ano", 80),
            ("mes", 80),
            ("valor", 100)
        ]

        for nome, largura in colunas:
            self.tabela.heading(nome, text=nome.capitalize())
            self.tabela.column(nome, width=largura)

        self.carregar_pagamentos()

    def registar_pagamento(self):
        try:
            membro_id = int(self.membro_id_entry.get().strip())
            ano = int(self.ano_entry.get().strip())
            mes = int(self.mes_entry.get().strip())
            valor = float(self.valor_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Aviso", "Preencha os campos com valores válidos.")
            return

        sucesso = database.adicionar_pagamento(membro_id, ano, mes, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", "Pagamento registado com sucesso!")
            self.carregar_pagamentos()
        else:
            messagebox.showerror("Erro", "Falha ao registar pagamento.")

    def carregar_pagamentos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        dados = database.listar_pagamentos()
        for p in dados:
            self.tabela.insert("", tk.END, values=(
                p["id"], p["membro"], p["ano"], p["mes"], p["valor"]
            ))
