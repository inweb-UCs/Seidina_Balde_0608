import tkinter as tk
from tkinter import ttk, messagebox
import database_mysql as database


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema da Associação Comunitária")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="white")

        # Título
        tk.Label(self, text="Login do Sistema",
                 font=("Arial", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        # Frame do formulário
        form = tk.Frame(self, bg="white")
        form.pack(pady=10)

        # Username
        tk.Label(form, text="Usuário:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(form, font=("Arial", 12), width=25)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Senha
        tk.Label(form, text="Senha:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.senha_entry = tk.Entry(form, font=("Arial", 12), width=25, show="*")
        self.senha_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botão de login
        ttk.Button(self, text="Entrar", command=self.fazer_login).pack(pady=20)

        # Evento Enter
        self.bind("<Return>", lambda event: self.fazer_login())

    def fazer_login(self):
        username = self.username_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if username == "" or senha == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        valido = database.verificar_login(username, senha)

        if valido:
            messagebox.showinfo("Bem-vindo", f"Login realizado com sucesso, {username}!")
            self.destroy()
            self.abrir_main()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def abrir_main(self):
        import main
        main.MainWindow()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
