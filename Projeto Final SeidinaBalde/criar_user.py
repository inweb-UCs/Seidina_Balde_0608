def criar_usuario(username, senha, perfil=None):
    conexao = conectar()
    if not conexao:
        return False

    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, senha) VALUES (%s, %s)",
            (username, senha)
        )
        conexao.commit()
        return True

    except Error as erro:
        print(f"Erro ao criar usuário: {erro}")
        return False

    finally:
        cursor.close()
        conexao.close()

