from flask import request, render_template, redirect, jsonify
from extensions import app, db, socketio
from models import Pacientes
from queue import Queue


#Teste branch


class Rotas:
    @app.route("/", methods=["GET"])
    def ler(self):
        pacientes = Pacientes.query.all()
        return render_template("home.html", pacientes=pacientes)

rotas = Rotas()

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastrarPaciente.html")


@app.route("/doutor")
def doutor():
    return render_template("doutor.html")


@app.route("/cadastrar/enviar", methods=["POST"])
def cadastroEnviar():
    nome = request.form["nome"]
    descricao = request.form["descricao"]

    novo_Paciente = Pacientes(nome=nome, descricao=descricao)

    db.session.add(novo_Paciente)
    db.session.commit()

    return redirect("/")


@app.route("/teste", methods=["GET"])
def teste():
    return render_template("teste.html")


@app.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        db.session.delete(paciente)
        db.session.commit()

    return redirect("/")


# Fila de pacientes

queue = Queue()
paciente_atual = None


@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")


@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")


@app.route("/chamada")
def chamada():
    socketio.emit(
        "handshake",
        {
            "message": "Conexão estabelecida",
            "paciente": {"id": paciente_atual.id, "nome": paciente_atual.nome}
            if paciente_atual
            else None,
        },
    )
    return render_template("chamadaPaciente.html")


@app.route("/add_paciente/<int:id>", methods=["POST"])
def add_paciente(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        queue.put(paciente)
        socketio.emit("queue_updated", {"message": "Paciente adicionado à fila"})
        print("Paciente adicionado à fila, fila atual:")
        temp_queue = list(queue.queue)
        for i in temp_queue:
            print(i.nome)
        return jsonify(
            {"status": "success", "message": "Paciente adicionado à fila"}
        ), 200
    else:
        return jsonify({"status": "error", "message": "Paciente não encontrado"}), 404


@app.route("/next_patient", methods=["POST"])
def next_patient():
    global paciente_atual
    if not queue.empty():
        paciente_atual = queue.get()
        socketio.emit(
            "next_patient", {"id": paciente_atual.id, "nome": paciente_atual.nome}
        )
        return jsonify(
            {
                "status": "success",
                "message": "Próximo paciente chamado",
                "paciente": {"id": paciente_atual.id, "nome": paciente_atual.nome},
            }
        ), 200
    else:
        return jsonify({"status": "error", "message": "Fila vazia"}), 404
