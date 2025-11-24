#!/usr/bin/env python3
import cgi
import cgitb
import html
import sqlite3   # <-- IMPORT NECESSÁRIO

cgitb.enable()

print("Content-Type: text/html\n")

form = cgi.FieldStorage()

nome = html.escape(form.getvalue("nome", ""))
sobrenome = html.escape(form.getvalue("sobrenome", ""))
cpf = html.escape(form.getvalue("cpf", ""))
telefone = html.escape(form.getvalue("telefone", ""))
data_nasc = form.getvalue("data", "")
email = html.escape(form.getvalue("email", ""))
senha = form.getvalue("senha", "")
confirmar_senha = form.getvalue("confirmar_senha", "")

# --- validações ---
if not (nome and sobrenome and cpf and telefone and data_nasc and email and senha and confirmar_senha):
    print("<h1>Erro: Preencha todos os campos!</h1>")
    exit()

if senha != confirmar_senha:
    print("<h1>Erro: As senhas não coincidem!</h1>")
    exit()

# --- cria / abre o banco ---
conn = sqlite3.connect("usuarios.db")  # será criado na mesma pasta do CGI
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    sobrenome TEXT,
    cpf TEXT UNIQUE,
    telefone TEXT,
    data_nasc TEXT,
    email TEXT UNIQUE,
    senha TEXT
)
""")

c.execute("""
INSERT INTO usuarios (nome, sobrenome, cpf, telefone, data_nasc, email, senha)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (nome, sobrenome, cpf, telefone, data_nasc, email, senha))

conn.commit()
conn.close()

print("<h1>Cadastro realizado com sucesso!</h1>")
print("<a href='login.html'>Ir para login</a>")
