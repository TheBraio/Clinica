from flask import request, redirect, jsonify, flash
from extensions import app, db
from models import Funcionario, Paciente, Doutor, Atendente
from views_recursos import Status
from views import session
from websocket import add_paciente, next_patient
from sqlalchemy.exc import IntegrityError

@app.route("/login", methods=["POST"])
def login_send():
    cpf = request.form['cpf']
    senha = request.form['senha']
    
    funcionario = Funcionario.query.filter(Funcionario.cpf == cpf).first()

    if funcionario:
        if funcionario.check_password(senha):
            session['privilegios'] = [ 'admin', 'atendente', 'doutor' ] if funcionario.admin else [funcionario.cargo]
            session['id'] = funcionario.id
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
    doutorId = data.get('doutor')
    
    status = Status("SUCESSO: Paciente cadastrado com sucesso!", 'sucess')

    if not nome or not cpf:
        status.message = "ERROR: Os campos Nome e CPF são obrigatórios."
        status.category = "error"
    else:
        novo_paciente = Paciente(nome=nome, descricao=descricao, cpf = cpf, doutor = doutorId)

        try:
            db.session.add(novo_paciente)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            status.message = "ERROR: Um paciente com esse CPF já está cadastrado."
            status.category = 'error'
    
    flash(status.message, status.category)
    return redirect('/atendente/cadastrar-paciente')

@app.route("/crud/pacientes/deletar/<int:id>", methods=["POST"])
def paciente_deletar(id):
    paciente = Paciente.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    status = Status("SUCESSO: Paciente deletado com sucesso!", 'sucess')
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
            "SUCESSO: Funcionario adicionado com sucesso", 
            'sucess'
        )
        if not nome or not cargo or not cpf:
            status.message = 'ERROR: Os campos Nome, Cargo e Cpf são obrigatórios!'
            status.category = 'error'
            return status
        
        if cargo == "doutor":
            consultorio = data.get("consultorio")
            if consultorio is None:
                status.message = 'ERROR: O campo Consultorio é obrigatório para cadastrar um doutor'
                status.category = 'error'
                return status
            
            novo_funcionario = Doutor(nome=nome, consultorio=consultorio, cpf = cpf, admin = admin)
                

        elif cargo == "atendente":
            setor = data.get("setor")
            if not setor:
                status.message = 'ERROR: O campo Setor é obrigatório para cadastrar um atendente.'
                status.category = 'error'
                return status
            
            novo_funcionario = Atendente(nome=nome, setor=setor, cpf = cpf, admin = admin)
        else:
            status.message = 'ERROR: Por favor forneça um cargo válido (doutor/atendente)'
            status.category = 'error'
            return status

        try:
            db.session.add(novo_funcionario)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            status.message = "ERROR: Um funcionário com esse CPF já está cadastrado."
            status.category = 'error'

        return status

    status = verify()
    flash(status.message, status.category)

    return redirect('/admin/cadastrar-funcionario')

@app.route("/crud/funcionarios/deletar/<int:id>", methods=["POST"])
def deletar_funcionario(id):
    funcionario = Funcionario.query.get(id)
    status = Status("[SUCESSO] Funcionário excluído com sucesso!", 'sucess')
    if not funcionario:
        return jsonify(
            {
                "status": "error",
                "message": "Funcionário não encontrado.",
            }
        ), 404
    elif funcionario.id == session['id']:
        status.message = '[ERROR] Você não pode excluir o próprio usuário.'
        status.category = 'error'
    else:
        db.session.delete(funcionario)
        db.session.commit()
        
    flash(status.message, status.category)

    return redirect("/admin/home")

###
### CRUD FUNCIONARIOS
###

@app.route('/trocar-senha-enviar', methods=['POST'])
def trocar_senha_enviar():
    data = request.get_json() if request.is_json else request.form
    senhaAntiga = data.get('senhaAntiga')
    novaSenha = data.get('novaSenha')
    novaSenha2 = data.get('novaSenha2')

    status = Status("[SUCESSO] Senha Alterada com sucesso!", 'sucess')


    if not (senhaAntiga and novaSenha and novaSenha2):
        status.message = "[ERROR] É necessário preencher todos os campos."
        status.category = "error"
    elif novaSenha != novaSenha2:
        status.message = "[ERROR] As senhas não coincidem."
        status.category = "error"
    else:
        funcionario = Funcionario.query.get(session['id'])
        if not funcionario.check_password(senhaAntiga):
            status.message = '[ERROR] A senha atual digitada não coincide com a senha cadastrada.'
            status.category = 'error'
        elif novaSenha == senhaAntiga:
            status.message = "[ERROR] A nova senha é igual a senha anterior."
            status.category = 'error'
        else:
            funcionario.change_password(novaSenha)

            db.session.commit()

    flash(status.message, status.category)

    return redirect('/trocar-senha')
