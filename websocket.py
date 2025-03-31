from queue import Queue
from extensions import socketio, app
from flask import jsonify, flash, redirect, session
from models import Paciente
from views_recursos import Status
from collections import deque

fila_pacientes: Queue[Paciente] = Queue()
ultimos_chamados: deque[Paciente] = deque(maxlen=5)
paciente_atual: Paciente | None = None

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")
    socketio.emit(
        "handshake",
        {
            "message": "Conexão estabelecida",
            "paciente": {"id": paciente_atual[0].id, "nome": paciente_atual[0].nome}
            if paciente_atual
            else None,
        },
    )


@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")


@app.route("/add_paciente/<int:id>", methods=["POST"])
def add_paciente(id):
    paciente = Paciente.query.get(id)

    status = Status("Paciente adicionado na fila com sucesso!", 'sucess')

    
    if paciente:
        fila_pacientes.put(paciente)
        fila_pacientes_list = [pac.nome for pac in fila_pacientes.queue]
        socketio.emit(
            "queue_updated",
            fila_pacientes_list,
        )
    else:
        status.message = "Paciente não encontrado!"
        status.category = "error"
    
    flash(status.message, status.category)

    return redirect('/atendente/home')


@app.route("/next_patient", methods=["POST"])
def next_patient():
    if not fila_pacientes.empty():
        global paciente_atual
        if paciente_atual:
            ultimos_chamados.append(paciente_atual)
        ultimos_chamados_list = [{'nome':chamado.nome, 'consultorio':consultorio} for chamado, consultorio in ultimos_chamados]
        paciente_atual = (fila_pacientes.get(), session['consultorio'])
        socketio.emit(
            "next_patient", {
                "paciente": paciente_atual[0].nome, 
                "doutor": session['nome'], 
                'consultorio': session['consultorio'],
                'chamadas': ultimos_chamados_list
            }
        )
        session['paciente'] = {'nome': paciente_atual[0].nome, 'descricao': paciente_atual[0].descricao}
        return redirect('/doutor/home')
    else:
        return jsonify({"status": "error", "message": "Fila vazia"}), 404
