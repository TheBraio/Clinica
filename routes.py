from flask import request, redirect, jsonify, flash
from extensions import app, db
from models import Funcionario, Paciente, Doutor, Atendente
from views_recursos import Status
from views import session
from websocket import add_paciente, next_patient

@app.route("/login", methods=["POST"])
def login_send():
    cpf = request.form['cpf']
    senha = request.form['senha']
    
    funcionario = Funcionario.query.filter(Funcionario.cpf == cpf).first()

    if funcionario:
        if funcionario.check_password(senha):
            session['privilegios'] = [ 'admin', 'atendente', 'doutor' ] if funcionario.admin else [funcionario.cargo]
            if funcionario.cargo == 'doutor':
                session['nome'] = funcionario.nome
                session['consultorio'] = funcionario.consultorio

    return redirect("/")

@app.route('/desconectar')
def desconectar():
    session.clear()
    return redirect('/login')
###
### CRUD PACIENTES
###
@app.route("/crud/pacientes/", methods=["POST"])
def paciente_cadastrar():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    nome = data.get("nome")  # Usa .get() para evitar erro se não existir
    cpf = data.get("CPF")
    descricao = data.get("descricao")

    
    status = Status("Paciente cadastrado com sucesso!", 'sucess')

    if not nome or not cpf:
        status.message = "Os campos Nome e CPF são obrigatórios."
        status.category = "error"
    else:
        novo_paciente = Paciente(nome=nome, descricao=descricao, cpf = cpf)

        db.session.add(novo_paciente)
        db.session.commit()
    
    flash(status.message, status.category)
    return redirect('/atendente/cadastrar-paciente')

@app.route("/crud/pacientes/deletar/<int:id>", methods=["POST"])
def paciente_deletar(id):
    paciente = Paciente.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    status = Status("Paciente deletado com sucesso!", 'sucess')
    flash(status.message, status.category)

    return redirect('/atendente/home')
###
### CRUD PACIENTES
###

###
### CRUD FUNCIONÁRIOS
###
@app.route("/crud/funcionarios/", methods=["POST"])
def cadastrar_funcionario():
    data = request.get_json() if request.is_json else request.form
    nome = data.get("nome")
    cargo = data.get("cargo")
    cpf = data.get('CPF')
    admin = bool(data.get('admin'))

    def verify():
        status = Status(
            "Funcionario adicionado com sucesso", 
            'sucess'
        )
        if not nome or not cargo or not cpf:
            status.message = 'Os campos Nome, Cargo e Cpf são obrigatórios!'
            status.category = 'error'
            return status
        
        if cargo == "doutor":
            consultorio = data.get("consultorio")
            if consultorio is None:
                status.message = 'O campo Consultorio é obrigatório para cadastrar um doutor'
                status.category = 'error'
                return status
            
            novo_funcionario = Doutor(nome=nome, consultorio=consultorio, cpf = cpf, admin = admin)
                

        elif cargo == "atendente":
            setor = data.get("setor")
            if not setor:
                status.message = 'O campo Setor é obrigatório para cadastrar um atendente.'
                status.category = 'error'
                return status
            
            novo_funcionario = Atendente(nome=nome, setor=setor, cpf = cpf, admin = admin)
        else:
            status.message = 'Por favor forneça um cargo válido (doutor/atendente)'
            status.category = 'error'
            return status


        db.session.add(novo_funcionario)
        db.session.commit()


        return status

    status = verify()
    flash(status.message, status.category)

    return redirect('/admin/cadastrar-funcionario')

@app.route("/crud/funcionarios/deletar/<int:id>", methods=["POST"])
def deletar_funcionario(id):
    funcionario = Funcionario.query.get(id)
    if not funcionario:
        return jsonify(
            {
                "status": "error",
                "message": "Funcionário não encontrado.",
            }
        ), 404

    db.session.delete(funcionario)
    db.session.commit()


    return redirect("/admin/home")

###
### CRUD FUNCIONARIOS
###
