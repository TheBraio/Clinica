from flask import request, render_template, redirect
from main import app
from models import *


@app.route('/cadastrar')
def cadastrar():
    return render_template("cadastrarPaciente.html")

@app.route('/doutor')
def doutor():
    return render_template('doutor.html')

@app.route('/chamada')
def chamada():
    return render_template('chamadaPaciente.html')


#Cadastro de pacientes.
@app.route('/cadastrar/enviar', methods=['POST'])
def cadastroEnviar():
    nome = request.form['nome']
    descricao = request.form['descricao']

    novo_Paciente = Pacientes(nome = nome, descricao = descricao)

    db.session.add(novo_Paciente)
    db.session.commit()

    return redirect('/')

#Le todos os pacientes.
@app.route('/', methods = ['GET'])
def ler():
    pacientes = Pacientes.query.all()
 
    return render_template('home.html', pacientes = pacientes)

#Deleta um paciente.
@app.route('/deletar/<int:id>', methods = ['POST'])
def deletar(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    return redirect('/')
