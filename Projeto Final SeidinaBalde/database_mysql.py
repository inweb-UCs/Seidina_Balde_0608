import mysql.connector
from mysql.connector import Error

# ==========================================================
# CONEXÃO COM A BASE DE DADOS
# ==========================================================

def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="associacao_comunitaria"
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# ==========================================================
# CRIAR TABELAS
# ==========================================================

def criar_tabelas():
    conn = conectar()
    if not conn:
        return
    c = conn.cursor()

    # Tabela de membros
    c.execute("""
        CREATE TABLE IF NOT EXISTS membros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(200),
            bi VARCHAR(50),
            data_nascimento DATE,
            funcao VARCHAR(100),
            morada VARCHAR(200),
            contacto VARCHAR(50),
            data_entrada DATE,
            foto VARCHAR(255)
        )
    """)

    # Tabela de pagamentos (quotas)
    c.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            membro_id INT,
            ano INT,
            mes INT,
            valor DECIMAL(10,2),
            FOREIGN KEY (membro_id) REFERENCES membros(id)
        )
    """)

    conn.commit()
    conn.close()

# ==========================================================
# TABELA DE DOCUMENTOS
# ==========================================================

def criar_tabela_documentos():
    conn = conectar()
    if not conn:
        return
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(200),
            tipo VARCHAR(50),
            data DATE,
            caminho VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

# ==========================================================
# FUNÇÕES DE MEMBROS
# ==========================================================

def adicionar_membro(nome, bi, data_nascimento, funcao, morada, contacto, data_entrada, foto):
    conn = conectar()
    if not conn:
        return False
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO membros (nome, bi, data_nascimento, funcao, morada, contacto, data_entrada, foto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, bi, data_nascimento, funcao, morada, contacto, data_entrada, foto))
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao adicionar membro: {e}")
        return False
    finally:
        conn.close()

def listar_membros():
    conn = conectar()
    if not conn:
        return []
    c = conn.cursor(dictionary=True)
    c.execute("""
        SELECT id, nome, bi, data_nascimento, funcao, morada, contacto, data_entrada, foto
        FROM membros
        ORDER BY id DESC
    """)
    dados = c.fetchall()
    conn.close()
    return dados

def eliminar_membro(id_membro):
    conn = conectar()
    if not conn:
        return False
    c = conn.cursor()
    try:
        c.execute("DELETE FROM membros WHERE id = %s", (id_membro,))
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao eliminar membro: {e}")
        return False
    finally:
        conn.close()

# ==========================================================
# FUNÇÕES DE PAGAMENTOS
# ==========================================================

def adicionar_pagamento(membro_id, ano, mes, valor):
    conn = conectar()
    if not conn:
        return False
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO pagamentos (membro_id, ano, mes, valor)
            VALUES (%s, %s, %s, %s)
        """, (membro_id, ano, mes, valor))
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao adicionar pagamento: {e}")
        return False
    finally:
        conn.close()

def listar_pagamentos():
    conn = conectar()
    if not conn:
        return []
    c = conn.cursor(dictionary=True)
    c.execute("""
        SELECT p.id, m.nome AS membro, p.ano, p.mes, p.valor
        FROM pagamentos p
        JOIN membros m ON p.membro_id = m.id
        ORDER BY p.id DESC
    """)
    dados = c.fetchall()
    conn.close()
    return dados

def eliminar_pagamento(id_pagamento):
    conn = conectar()
    if not conn:
        return False
    c = conn.cursor()
    try:
        c.execute("DELETE FROM pagamentos WHERE id = %s", (id_pagamento,))
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao eliminar pagamento: {e}")
        return False
    finally:
        conn.close()

# ==========================================================
# FUNÇÕES DE DOCUMENTOS
# ==========================================================

def adicionar_documento(titulo, tipo, data, caminho):
    conn = conectar()
    if not conn:
        return False
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO documentos (titulo, tipo, data, caminho)
            VALUES (%s, %s, %s, %s)
        """, (titulo, tipo, data, caminho))
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao adicionar documento: {e}")
        return False
    finally:
        conn.close()

def listar_documentos():
    conn = conectar()
    if not conn:
        return []
    c = conn.cursor(dictionary=True)
    c.execute("""
        SELECT id, titulo, tipo, data, caminho
        FROM documentos
        ORDER BY id DESC
    """)
    dados = c.fetchall()
    conn.close()
    return dados

def eliminar_documento(id_doc):
    conn = conectar()
    if not conn:
        return False
    c = conn.cursor()
    try:
        c.execute("DELETE FROM documentos WHERE id = %s", (id_doc,))
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao eliminar documento: {e}")
        return False
    finally:
        conn.close()
