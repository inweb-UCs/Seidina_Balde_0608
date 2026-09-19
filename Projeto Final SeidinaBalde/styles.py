import tkinter as tk
from tkinter import ttk

# ==========================================================
# PALETA DE CORES
# ==========================================================

PRIMARY = "#2c3e50"
SECONDARY = "#34495e"
ACCENT = "#2980b9"
SUCCESS = "#27ae60"
WARNING = "#f39c12"
DANGER = "#c0392b"
LIGHT = "#ecf0f1"
WHITE = "#ffffff"
GRAY = "#bdc3c7"

FONT_TITLE = ("Arial", 20, "bold")
FONT_SUBTITLE = ("Arial", 16, "bold")
FONT_NORMAL = ("Arial", 12)
FONT_SMALL = ("Arial", 10)

# ==========================================================
# FUNÇÃO PARA APLICAR ESTILOS
# ==========================================================

def aplicar_estilos(root):
    style = ttk.Style(root)

    # Tema base
    style.theme_use("clam")

    # -----------------------------
    # BOTÕES
    # -----------------------------
    style.configure("TButton",
                    font=FONT_NORMAL,
                    padding=6,
                    background=ACCENT,
                    foreground=WHITE)
    style.map("TButton",
              background=[("active", PRIMARY)],
              foreground=[("active", WHITE)])

    # -----------------------------
    # TREEVIEW (TABELAS)
    # -----------------------------
    style.configure("Treeview",
                    font=FONT_NORMAL,
                    background=WHITE,
                    foreground=PRIMARY,
                    rowheight=28,
                    fieldbackground=WHITE)

    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    background=PRIMARY,
                    foreground=WHITE)

    style.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", WHITE)])

    # -----------------------------
    # LABELS
    # -----------------------------
    style.configure("TLabel",
                    font=FONT_NORMAL,
                    background=WHITE,
                    foreground=PRIMARY)

    # -----------------------------
    # ENTRY (CAIXAS DE TEXTO)
    # -----------------------------
    style.configure("TEntry",
                    padding=5,
                    font=FONT_NORMAL)

    # -----------------------------
    # NOTEBOOK (Separadores)
    # -----------------------------
    style.configure("TNotebook",
                    background=WHITE,
                    borderwidth=0)

    style.configure("TNotebook.Tab",
                    font=FONT_NORMAL,
                    padding=[10, 5],
                    background=SECONDARY,
                    foreground=WHITE)

    style.map("TNotebook.Tab",
              background=[("selected", PRIMARY)],
              foreground=[("selected", WHITE)])

    # -----------------------------
    # FRAMES
    # -----------------------------
    style.configure("TFrame", background=WHITE)

# ==========================================================
# FUNÇÕES DE UTILIDADE
# ==========================================================

def titulo(master, texto):
    return tk.Label(master, text=texto, font=FONT_TITLE, bg=WHITE, fg=PRIMARY)

def subtitulo(master, texto):
    return tk.Label(master, text=texto, font=FONT_SUBTITLE, bg=WHITE, fg=PRIMARY)

def label(master, texto):
    return tk.Label(master, text=texto, font=FONT_NORMAL, bg=WHITE, fg=PRIMARY)

def botao(master, texto, comando):
    return ttk.Button(master, text=texto, command=comando)

def entrada(master):
    return ttk.Entry(master, font=FONT_NORMAL)
