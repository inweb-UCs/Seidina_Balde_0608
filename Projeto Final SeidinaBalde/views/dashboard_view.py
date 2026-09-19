import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database_mysql as database


class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Dashboard – Estatísticas Gerais",
                 font=("Arial", 22, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        # ============================
        # CONTADORES
        # ============================
        cards_frame = tk.Frame(self, bg="white")
        cards_frame.pack(pady=10)

        self.total_membros_label = tk.Label(cards_frame, text="Membros: 0",
                                            font=("Arial", 16, "bold"), bg="white", fg="#27ae60")
        self.total_membros_label.grid(row=0, column=0, padx=40, pady=10)

        self.total_pagamentos_label = tk.Label(cards_frame, text="Pagamentos: 0",
                                               font=("Arial", 16, "bold"), bg="white", fg="#2980b9")
        self.total_pagamentos_label.grid(row=0, column=1, padx=40, pady=10)

        self.total_documentos_label = tk.Label(cards_frame, text="Documentos: 0",
                                               font=("Arial", 16, "bold"), bg="white", fg="#8e44ad")
        self.total_documentos_label.grid(row=0, column=2, padx=40, pady=10)

        # ============================
        # FILTROS INTERATIVOS
        # ============================
        filtros_frame = tk.Frame(self, bg="white")
        filtros_frame.pack(pady=10)

        tk.Label(filtros_frame, text="Ano:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.ano_var = tk.StringVar()
        self.ano_combo = ttk.Combobox(filtros_frame, textvariable=self.ano_var, width=10)
        self.ano_combo.grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Mês:", bg="white", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.mes_var = tk.StringVar()
        self.mes_combo = ttk.Combobox(filtros_frame, textvariable=self.mes_var, width=10)
        self.mes_combo.grid(row=0, column=3, padx=5)

        ttk.Button(filtros_frame, text="Aplicar Filtros", command=self.aplicar_filtros).grid(row=0, column=4, padx=10)

        # ============================
        # ÁREA DOS GRÁFICOS
        # ============================
        self.graficos_frame = tk.Frame(self, bg="white")
        self.graficos_frame.pack(fill="both", expand=True, pady=20)

        self.atualizar_dashboard()

    # ==========================================================
    # ATUALIZAR DADOS E GRÁFICOS
    # ==========================================================
    def atualizar_dashboard(self):
        membros = database.listar_membros()
        pagamentos = database.listar_pagamentos()
        documentos = database.listar_documentos()

        self.total_membros_label.config(text=f"Membros: {len(membros)}")
        self.total_pagamentos_label.config(text=f"Pagamentos: {len(pagamentos)}")
        self.total_documentos_label.config(text=f"Documentos: {len(documentos)}")

        # Preencher filtros com anos e meses existentes
        anos_set = set()
        for m in membros:
            data = m.get("data_entrada")
            if not data:
                continue
            data_str = str(data)
            if "/" in data_str:  # DD/MM/YYYY
                partes = data_str.split("/")
                try:
                    ano = int(partes[-1])
                    anos_set.add(ano)
                except ValueError:
                    continue
            elif "-" in data_str:  # YYYY-MM-DD
                try:
                    ano = int(data_str[:4])
                    anos_set.add(ano)
                except ValueError:
                    continue

        meses_set = {p["mes"] for p in pagamentos}

        self.ano_combo["values"] = sorted(anos_set)
        self.mes_combo["values"] = sorted(meses_set)

        for widget in self.graficos_frame.winfo_children():
            widget.destroy()

        self.criar_grafico_pagamentos(pagamentos)
        self.criar_grafico_funcoes(membros)
        self.criar_grafico_membros_ano(membros)

    # ==========================================================
    # APLICAR FILTROS
    # ==========================================================
    def aplicar_filtros(self):
        ano_filtro = self.ano_var.get()
        mes_filtro = self.mes_var.get()

        pagamentos = database.listar_pagamentos()
        membros = database.listar_membros()

        if ano_filtro:
            pagamentos = [p for p in pagamentos if p["ano"] == int(ano_filtro)]

        if mes_filtro:
            pagamentos = [p for p in pagamentos if p["mes"] == int(mes_filtro)]

        if ano_filtro:
            membros_filtrados = []
            for m in membros:
                data = m.get("data_entrada")
                if not data:
                    continue
                data_str = str(data)
                try:
                    if "/" in data_str:  # DD/MM/YYYY
                        partes = data_str.split("/")
                        ano = int(partes[-1])
                    elif "-" in data_str:  # YYYY-MM-DD
                        ano = int(data_str[:4])
                    else:
                        continue
                    if ano == int(ano_filtro):
                        membros_filtrados.append(m)
                except ValueError:
                    continue
            membros = membros_filtrados

        for widget in self.graficos_frame.winfo_children():
            widget.destroy()

        self.criar_grafico_pagamentos(pagamentos)
        self.criar_grafico_funcoes(membros)
        self.criar_grafico_membros_ano(membros)

    # ==========================================================
    # GRÁFICO 1 — PAGAMENTOS POR MÊS (BARRAS)
    # ==========================================================
    def criar_grafico_pagamentos(self, pagamentos):
        if not pagamentos:
            tk.Label(self.graficos_frame, text="Sem dados de pagamentos.",
                     font=("Arial", 12), bg="white", fg="#7f8c8d").pack(side="left", padx=20)
            return

        meses = [p["mes"] for p in pagamentos]
        valores = [float(p["valor"]) for p in pagamentos]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(meses, valores, color="#2980b9")
        ax.set_title("Pagamentos por Mês")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Valor (€)")
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", padx=20)

    # ==========================================================
    # GRÁFICO 2 — DISTRIBUIÇÃO DE FUNÇÕES (PIZZA)
    # ==========================================================
    def criar_grafico_funcoes(self, membros):
        if not membros:
            tk.Label(self.graficos_frame, text="Sem dados de membros.",
                     font=("Arial", 12), bg="white", fg="#7f8c8d").pack(side="left", padx=20)
            return

        funcoes = {}
        for m in membros:
            f = m["funcao"] if m["funcao"] else "Indefinido"
            funcoes[f] = funcoes.get(f, 0) + 1

        labels = list(funcoes.keys())
        valores = list(funcoes.values())

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(valores, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Distribuição de Funções")

        canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", padx=20)

    # ==========================================================
    # GRÁFICO 3 — MEMBROS POR ANO (LINHA)
    # ==========================================================
    def criar_grafico_membros_ano(self, membros):
        if not membros:
            tk.Label(self.graficos_frame, text="Sem dados de membros.",
                     font=("Arial", 12), bg="white", fg="#7f8c8d").pack(side="left", padx=20)
            return

        anos = {}
        for m in membros:
            data = m.get("data_entrada")
            if not data:
                continue
            try:
                data_str = str(data)
                if "/" in data_str:  # DD/MM/YYYY
                    partes = data_str.split("/")
                    ano = int(partes[-1])
                elif "-" in data_str:  # YYYY-MM-DD
                    ano = int(data_str[:4])
                else:
                    continue
                anos[ano] = anos.get(ano, 0) + 1
            except (ValueError, TypeError):
                continue

        if not anos:
            tk.Label(self.graficos_frame, text="Sem dados válidos de datas.",
                     font=("Arial", 12), bg="white", fg="#7f8c8d").pack(side="left", padx=20)
            return

        anos_ordenados = sorted(anos.keys())
        valores = [anos[a] for a in anos_ordenados]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(anos_ordenados, valores, marker="o", color="#27ae60", linewidth=2)
        ax.set_title("Crescimento de Membros por Ano")
        ax.set_xlabel("Ano")
        ax.set_ylabel("Total de Membros")
        ax.grid(True, linestyle="--", alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", padx=20)
