import tkinter as tk
from tkinter import ttk
from styles import aplicar_estilos
from views.dashboard_view import DashboardView
from views.membros_view import MembrosView
from views.quotas_view import QuotasView
from views.documentos_view import DocumentosView
from views.relatorios_view import RelatoriosView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("Associação Comunitária")
        self.geometry("1200x700")
        self.configure(bg="white")

        # Aplicar estilos
        aplicar_estilos(self)

        # Frame principal
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        # Criar layout
        self.criar_layout()

    def criar_layout(self):
        # Menu lateral
        menu_frame = tk.Frame(self.container, bg="#2c3e50", width=200)
        menu_frame.pack(side="left", fill="y")

        # Área de conteúdo
        self.content_frame = tk.Frame(self.container, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Botões do menu
        botoes = [
            ("🏠 Dashboard", self.mostrar_dashboard),
            ("👥 Membros", self.mostrar_membros),
            ("💰 Quotas", self.mostrar_quotas),
            ("📄 Documentos", self.mostrar_documentos),
            ("📊 Relatórios", self.mostrar_relatorios),
            ("🚪 Sair", self.sair)
        ]

        for texto, comando in botoes:
            btn = ttk.Button(menu_frame, text=texto, command=comando)
            btn.pack(fill="x", pady=5, padx=10)

        # Mostrar dashboard por padrão
        self.mostrar_dashboard()

    # Funções para trocar de view
    def limpar_conteudo(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpar_conteudo()
        DashboardView(self.content_frame, self).pack(fill="both", expand=True)

    def mostrar_membros(self):
        self.limpar_conteudo()
        MembrosView(self.content_frame, self).pack(fill="both", expand=True)

    def mostrar_quotas(self):
        self.limpar_conteudo()
        QuotasView(self.content_frame, self).pack(fill="both", expand=True)

    def mostrar_documentos(self):
        self.limpar_conteudo()
        DocumentosView(self.content_frame, self).pack(fill="both", expand=True)

    def mostrar_relatorios(self):
        self.limpar_conteudo()
        RelatoriosView(self.content_frame, self).pack(fill="both", expand=True)

    def sair(self):
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
