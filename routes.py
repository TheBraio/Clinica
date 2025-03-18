from flask import request, redirect
from extensions import app, db
from models import Pacientes

@app.route("/", methods=["GET"])
def ler():
    pacientes = Pacientes.query.all()
    return render_template("home.html", pacientes=pacientes)


####
#### Pacientes CRUD
####


@app.route("/pacientes")
def paciente_view():
    pacientes = Pacientes.query.all()
    return render_template("paciente_view.html", pacientes=pacientes)


@app.route("/pacientes/cadastrar")
def cadastrar():
    return render_template("cadastrarPaciente.html")


@app.route("/pacientes/cadastrar", methods=["POST"])
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

@app.route("/doutor")
def doutor():
    return render_template("doutor.html")


@app.route("/teste", methods=["GET"])
def teste():
    return render_template("teste.html")


# Fila de pacientes

queue = Queue()
paciente_atual = None
