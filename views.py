from extensions import app
from flask import render_template
from models import Pacientes

@app.route("/", methods=["GET"])
def ler():
    pacientes = Pacientes.query.all()
    return render_template("home.html", pacientes=pacientes)


@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastrarPaciente.html")


@app.route("/doutor")
def doutor():
    return render_template("doutor.html")

@app.route("/teste", methods=["GET"])
def teste():
    return render_template("teste.html")

@app.route("/chamada")
def chamada():
    return render_template("chamadaPaciente.html")