from flask import request, redirect
from extensions import app, db
from models import Pacientes

from views import *
from websocket import *



@app.route("/login", methods=['POST'])
def login_send():
    nome = request.form['nome']
    senha = request.form['senha']
    
    if nome == 'admin':
        session["nome"] = nome
        return redirect("/admin-funcionarios")
    if nome == 'atendente':
        session['nome'] = nome
        return redirect('/atendente-pacientes')
    if nome == 'doutor':
        session['nome'] = nome
        return redirect('/doutor-mainpage')
    return redirect("/")


# CRUD pacientes
@app.route("/cadastrar/enviar", methods=["POST"])
def paciente_cadastrar():
    nome = request.form["nome"]
    descricao = request.form["descricao"]

    novo_Paciente = Pacientes(nome=nome, descricao=descricao)

    db.session.add(novo_Paciente)
    db.session.commit()

    return redirect("/")

@app.route("/deletar/<int:id>", methods=["POST"])
def paciente_deletar(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    return redirect("/")
# CRUD pacientes
