from queue import Queue
from extensions import socketio, app
from flask import jsonify, flash, redirect, session, request
from models import Paciente
from views_recursos import Status
from collections import deque

fila_pacientes: dict[int, Queue[Paciente]] = {}
ultimos_chamados: deque[Paciente] = deque(maxlen=2)
paciente_atual: Paciente | None = None
socketDoutor: dict[int, str] = {}

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado: ", request.sid)
    
@socketio.on("doutorConnect")
def doutorConnect(data):
    doutorID = int(data)
    if not fila_pacientes.get(doutorID):
        fila_pacientes[doutorID] = Queue()
    socketDoutor[doutorID] = request.sid


@socketio.on("disconnect")
def handle_disconnect():
    for id, sid in socketDoutor.items():
        if sid == request.sid:
            del socketDoutor[id]
            print('Removido')
            break

@app.route("/add_paciente/<int:id>", methods=["POST"])
def add_paciente(id):
    paciente = Paciente.query.get(id)
    doutor = paciente.doutor
    status = Status("Paciente adicionado na fila com sucesso!", 'sucess')

    if paciente:
        if not fila_pacientes.get(doutor):
            fila_pacientes[doutor] = Queue()
            
        fila_pacientes[doutor].put(paciente)
        fila_pacientes_list = [pac.nome for pac in fila_pacientes[doutor].queue]
        try:
            socketio.emit(
                "queue_updated",
                fila_pacientes_list,to=socketDoutor[doutor]
            )
        except:
            pass
            
    else:
        status.message = "ERROR: Paciente não encontrado!"
        status.category = "error"
    
    flash(status.message, status.category)

    return redirect('/atendente/home')


@app.route("/next_patient/<int:id>", methods=["POST"])
def next_patient(id):
    if not fila_pacientes[id].empty():
        global paciente_atual
        if paciente_atual:
            ultimos_chamados.append(paciente_atual)
        ultimos_chamados_list = [{'nome':chamado.nome, 'consultorio':consultorio} for chamado, consultorio in ultimos_chamados]
        paciente_atual = (fila_pacientes[id].get(), session['consultorio'])
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
