from extensions import app
from flask import render_template
from models import Pacientes
from views_recursos import *




@app.route('/login', methods=["GET"])
def login():
    return render_template('login.html', links = links[session['nome']])


# Rotas do admin
@app.route('/admin-funcionarios')
@is_admin
def admin_funcionarios():
    return render_template('admin_funcionarios.html', links = links[session['nome']])
# Rotas do admin

# Rotas do atendente
@app.route("/atendente-pacientes", methods=["GET"])
def ler():
    pacientes = Pacientes.query.all()
    
    return render_template("home.html", pacientes=pacientes,)

@app.route("/atendente-cadastrar")
def cadastrar():
    return render_template("cadastrarPaciente.html")
# Rotas do atendente

# Rotas do doutor 
@app.route("/doutor-mainpage")
def doutor():
    return render_template("doutor.html")
# Rotas do doutor


@app.route("/chamada")
def chamada():
    return render_template("chamadaPaciente.html")