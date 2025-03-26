from flask import request, redirect, jsonify
from extensions import app, db
from models import Funcionario, Paciente, Doutor, Atendente

from views import session


@app.route("/login", methods=["POST"])
def login_send():
    cpf = request.form['cpf']
    senha = request.form['senha']
    
    funcionario = Funcionario.query.filter(Funcionario.cpf == cpf).first()

    if funcionario:
        if funcionario.check_password(senha):
            session['privilegios'] = [
                'admin', 'atendente', 'doutor' if funcionario.admin else funcionario.cargo
            ]

    return redirect("/")


###
### CRUD PACIENTES
###


@app.route("/crud/pacientes/", methods=["GET"])
def pacientes():
    pacientes = Paciente.query.all()

    # Converter a lista de objetos Paciente para uma lista de dicionários
    pacientes_json = [
        {"id": p.id, "nome": p.nome, "descricao": p.descricao} for p in pacientes
    ]

    return jsonify(pacientes_json)


@app.route("/crud/pacientes/", methods=["POST"])
def paciente_cadastrar():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    nome = data.get("nome")  # Usa .get() para evitar erro se não existir
    descricao = data.get("descricao")

    if not nome:
        return jsonify(
            {"status": "error", "message": "O campo 'nome' é obrigatório."}
        ), 400

    novo_paciente = Paciente(nome=nome, descricao=descricao)

    db.session.add(novo_paciente)
    db.session.commit()

    return jsonify(
        {
            "status": "success",
            "message": "Paciente adicionado.",
            "paciente": {
                "id": novo_paciente.id,
                "nome": novo_paciente.nome,
                "descricao": novo_paciente.descricao,
            },
        }
    ), 200


@app.route("/crud/pacientes/deletar/<int:id>", methods=["POST"])
def paciente_deletar(id):
    paciente = Paciente.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    return jsonify(
        {
            "status": "success",
            "message": "Paciente deletado.",
        }
    ), 200


###
### CRUD PACIENTES
###


###
### CRUD FUNCIONÁRIOS
###
@app.route("/crud/funcionarios/", methods=["GET"])
def funcionarios():
    funcionarios = Funcionario.query.all()

    return jsonify(
        {
            "status": "success",
            "message": "Funcionários listados.",
            "funcionarios": [
                {
                    "id": funcionario.id,
                    "nome": funcionario.nome,
                    "cargo": funcionario.cargo,
                    **(
                        {"consultorio": funcionario.consultorio}
                        if funcionario.cargo == "doutor"
                        else {}
                    ),
                    **(
                        {"setor": funcionario.setor}
                        if funcionario.cargo == "atendente"
                        else {}
                    ),
                }
                for funcionario in funcionarios
            ],
        }
    ), 200


@app.route("/crud/funcionarios/", methods=["POST"])
def cadastrar_funcionario():
    data = request.get_json() if request.is_json else request.form
    nome = data.get("nome")
    cargo = data.get("cargo")

    if not nome or not cargo:
        return jsonify(
            {
                "status": "error",
                "message": "Os campos 'nome' e 'cargo' são obrigatórios.",
            }
        ), 400

    if cargo == "doutor":
        consultorio = data.get("consultorio")
        if consultorio is None:
            return jsonify(
                {
                    "status": "error",
                    "message": "O campo 'consultorio' é obrigatório para doutor.",
                }
            ), 400
        novo_funcionario = Doutor(nome=nome, consultorio=consultorio)

    elif cargo == "atendente":
        setor = data.get("setor")
        if not setor:
            return jsonify(
                {
                    "status": "error",
                    "message": "O campo 'setor' é obrigatório para atendente.",
                }
            ), 400
        novo_funcionario = Atendente(nome=nome, setor=setor)

    else:
        return jsonify(
            {
                "status": "error",
                "message": "Por favor forneça um cargo válido (doutor/atendente).",
            }
        ), 400

    db.session.add(novo_funcionario)
    db.session.commit()

    funcionario_data = {
        "id": novo_funcionario.id,
        "nome": novo_funcionario.nome,
        "cargo": novo_funcionario.cargo,
    }

    if cargo == "doutor":
        funcionario_data["consultorio"] = novo_funcionario.consultorio
    elif cargo == "atendente":
        funcionario_data["setor"] = novo_funcionario.setor

    return jsonify(
        {
            "status": "success",
            "message": "Funcionário adicionado.",
            "funcionario": funcionario_data,
        }
    ), 200


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

    return jsonify(
        {
            "status": "success",
            "message": "Funcionário deletado.",
        }
    ), 200
