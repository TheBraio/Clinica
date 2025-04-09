from extensions import app, db
from flask import render_template, redirect, session
from models import Paciente, Funcionario, Doutor
from views_recursos import *


# Rotas do admin
@app.route("/admin/home")
@logged
@is_admin
def admin_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template_nav('admin_funcionarios.html', funcionarios = funcionarios)

@app.route('/admin/cadastrar-funcionario', methods=['GET'])
@logged
@is_admin
def admin_cadastrar_funcionario():
    return render_template_nav('admin_cadastrar_funcionario.html')
# Rotas do admin


# Rotas do atendente
@app.route("/atendente/home", methods=["GET"])
@logged
@is_atendente
def atendente_pacientes():
    pacientes = Paciente.query.all()
    
    return render_template_nav("atendente_home.html", pacientes=pacientes)

@app.route("/atendente/cadastrar-paciente")
@logged
@is_atendente
def cadastrar():
    doutores = Doutor.query.all()
    return render_template_nav("atendente_cadastrar_paciente.html", doutores = doutores)
# Rotas do atendente


# Rotas do doutor
@app.route("/doutor/home")
@logged
@is_doutor
def doutor():
    from websocket import fila_pacientes, Queue
    if fila_pacientes.get(session['id']):
        fila_pacientes_list = [pac.nome for pac in fila_pacientes[session['id']].queue]
    else:
        fila_pacientes_list = []
    return render_template_nav("doutor_home.html", fila=fila_pacientes_list, paciente=session['paciente'] if 'paciente' in session else False, doutorID = session['id'])
# Rotas do doutor 


# Rotas Gerais
@app.route('/login', methods=["GET"])
def login():
    return render_template_nav('login.html')

@app.route('/', methods=["GET"])
def home():
    # db.session.add(Doutor(nome="admin", cpf='000', admin=True, consultorio=0))
    # db.session.commit()
    if 'privilegios' in session:
        return redirect(f"/{session['privilegios'][0]}/home")
    return redirect('/login')

@app.route("/chamada")
def chamada():
    return render_template("chamadaPaciente.html")

@app.route('/trocar-senha', methods=['GET'])
def trocar_senha():
    return render_template_nav('troca-senha.html')
# Rotas Gerais
