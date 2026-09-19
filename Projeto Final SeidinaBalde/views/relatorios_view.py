import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database_mysql as database
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime


class RelatoriosView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Relatórios",
                 font=("Arial", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        ttk.Button(self, text="Exportar Membros para PDF", command=self.exportar_membros_pdf).pack(pady=10)
        ttk.Button(self, text="Exportar Pagamentos para PDF", command=self.exportar_pagamentos_pdf).pack(pady=10)
        ttk.Button(self, text="Exportar Documentos para PDF", command=self.exportar_documentos_pdf).pack(pady=10)

    def _criar_canvas(self, titulo):
        ficheiro = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Guardar relatório"
        )
        if not ficheiro:
            return None

        c = canvas.Canvas(ficheiro, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, titulo)
        c.setFont("Helvetica", 10)
        c.drawString(50, 785, f"Data: {datetime.date.today().strftime('%Y-%m-%d')}")
        return c

    def exportar_membros_pdf(self):
        dados = database.listar_membros()
        c = self._criar_canvas("Relatório de Membros")
        if c is None:
            return

        y = 760
        c.setFont("Helvetica", 10)
        for m in dados:
            linha = f"{m['id']} - {m['nome']} - {m['bi']} - {m['contacto']}"
            c.drawString(50, y, linha)
            y -= 15
            if y < 50:
                c.showPage()
                y = 800

        c.save()
        messagebox.showinfo("Sucesso", "Relatório de membros exportado para PDF.")

    def exportar_pagamentos_pdf(self):
        dados = database.listar_pagamentos()
        c = self._criar_canvas("Relatório de Pagamentos")
        if c is None:
            return

        y = 760
        c.setFont("Helvetica", 10)
        for p in dados:
            linha = f"{p['id']} - {p['membro']} - {p['ano']}/{p['mes']} - {p['valor']:.2f}€"
            c.drawString(50, y, linha)
            y -= 15
            if y < 50:
                c.showPage()
                y = 800

        c.save()
        messagebox.showinfo("Sucesso", "Relatório de pagamentos exportado para PDF.")

    def exportar_documentos_pdf(self):
        dados = database.listar_documentos()
        c = self._criar_canvas("Relatório de Documentos")
        if c is None:
            return

        y = 760
        c.setFont("Helvetica", 10)
        for d in dados:
            linha = f"{d['id']} - {d['titulo']} - {d['tipo']} - {d['data']} - {d['caminho']}"
            c.drawString(50, y, linha)
            y -= 15
            if y < 50:
                c.showPage()
                y = 800

        c.save()
        messagebox.showinfo("Sucesso", "Relatório de documentos exportado para PDF.")
