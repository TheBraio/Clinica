from queue import Queue
from extensions import socketio, app
from flask import jsonify
from models import Pacientes

queue : Queue = Queue() 
paciente_atual = None


@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")
    socketio.emit(
        "handshake",
        {
            "message": "Conexão estabelecida",
            "paciente": {"id": paciente_atual.id, "nome": paciente_atual.nome}
            if paciente_atual
            else None,
        },
    )


@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")


@app.route("/add_paciente/<int:id>", methods=["POST"])
def add_paciente(id):
    paciente = Pacientes.query.get(id)

    if paciente:
        queue.put(paciente)
        socketio.emit("queue_updated", {"message": "Paciente adicionado à fila", 'queue':queue.queue})
        return jsonify(
            {"status": "success", "message": "Paciente adicionado à fila"}
        ), 200
    else:
        return jsonify({"status": "error", "message": "Paciente não encontrado"}), 404


@app.route("/next_patient", methods=["POST"])
def next_patient():
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
