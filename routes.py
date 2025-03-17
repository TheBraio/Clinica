from flask import request, redirect
from extensions import app, db
from models import Pacientes

from views import *
from websocket import *


@app.route("/cadastrar/enviar", methods=["POST"])
def cadastroEnviar():
    nome = request.form["nome"]
    descricao = request.form["descricao"]

    novo_Paciente = Pacientes(nome=nome, descricao=descricao)

    db.session.add(novo_Paciente)
    db.session.commit()

    return redirect("/")


@app.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    return redirect("/")




