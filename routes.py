from flask import request, jsonify, render_template
from main import app
from models import *

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cadastrar')
def cadastrar():
    return render_template("cadastrarPaciente.html")

#Cadastro de pacientes.
@app.route('/cadastrar/enviar', methods=['POST'])
def cadastroEnviar():
    nome = request.form['nome']
    descricao = request.form['descricao']

    novo_Paciente = Pacientes(nome = nome, descricao = descricao)

    db.session.add(novo_Paciente)
    db.session.commit()

    return "Certinho"

#Le todos os pacientes.
@app.route('/ler', methods = ['GET'])
def ler():
    pacientes = Pacientes.query.all()
    
    pacientes_json = [
        {
            'id' : paciente.id,
            'nome' : paciente.nome,
            'descricao' : paciente.descricao
        } for paciente in pacientes
    ]
    return jsonify(pacientes_json)

#Deleta um paciente.
@app.route('/deletar/<int:id>', methods = ['DELETE'])
def deletar(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()
    else:
        return "Esse cara existe nao"
    return "Deletado com sucesso."
