from queue import Queue
from collections import deque
from flask import jsonify, flash, redirect, session, request
from models import Paciente
from views_recursos import Status
from extensions import socketio

fila_pacientes = {}
ultimos_chamados = deque(maxlen=3)  # Aumentando para 3 últimos chamados
paciente_atual = None
socketDoutor = {}

@socketio.on("connect")
def handle_connect():
    """Lida com conexões de clientes"""
    print("Cliente conectado: ", request.sid)

@socketio.on("doutorConnect")
def doutorConnect(data):
    """Conecta doutor ao websocket e inicializa sua fila se necessário"""
    try:
        doutorID = int(data)
        if not fila_pacientes.get(doutorID):
            fila_pacientes[doutorID] = Queue()
        socketDoutor[doutorID] = request.sid
        # Enviar estado atual da fila para o doutor recém-conectado
        if doutorID in fila_pacientes:
            fila_pacientes_list = [pac.nome for pac in fila_pacientes[doutorID].queue]
            socketio.emit("queue_updated", fila_pacientes_list, to=request.sid)
        print(f"Doutor {doutorID} conectado")
    except (ValueError, TypeError) as e:
        print(f"Erro ao conectar doutor: {e}")

@socketio.on("disconnect")
def handle_disconnect():
    """Remove doutor da lista de conectados quando ele desconecta"""
    sid = request.sid
    for id, doctor_sid in list(socketDoutor.items()):
        if doctor_sid == sid:
            del socketDoutor[id]
            print(f'Doutor {id} desconectado')
            break

def add_paciente(id, app):
    """Adiciona paciente à fila de um doutor"""
    with app.app_context():
        paciente = Paciente.query.get(id)
        if not paciente:
            status = Status("ERROR: Paciente não encontrado!", 'error')
            flash(status.message, status.category)
            return redirect('/atendente/home')

        doutor = paciente.doutor
        status = Status("Paciente adicionado na fila com sucesso!", 'success')

        if not fila_pacientes.get(doutor):
            fila_pacientes[doutor] = Queue()

        fila_pacientes[doutor].put(paciente)
        fila_pacientes_list = [pac.nome for pac in fila_pacientes[doutor].queue]

        try:
            if doutor in socketDoutor:
                socketio.emit("queue_updated", fila_pacientes_list, to=socketDoutor[doutor])
        except Exception as e:
            print(f"Erro ao atualizar fila: {e}")

        flash(status.message, status.category)
        return redirect('/atendente/home')

def next_patient(id, app):
    """Chama o próximo paciente da fila"""
    global paciente_atual

    with app.app_context():
        if id not in fila_pacientes or fila_pacientes[id].empty():
            return jsonify({"status": "error", "message": "Fila vazia"}), 404

        if paciente_atual:
            ultimos_chamados.append((paciente_atual[0], paciente_atual[1]))

        ultimos_chamados_list = [{'nome': chamado[0].nome, 'consultorio': chamado[1]}
                                for chamado in ultimos_chamados]

        paciente_atual = (fila_pacientes[id].get(), session.get('consultorio', 'N/A'))

        # Emitir para todos os clientes conectados
        socketio.emit(
            "next_patient", {
                "paciente": paciente_atual[0].nome,
                "doutor": session.get('nome', 'Médico'),
                'consultorio': paciente_atual[1],
                'chamadas': ultimos_chamados_list
            }
        )

        session['paciente'] = {'nome': paciente_atual[0].nome, 'descricao': paciente_atual[0].descricao}

        # Atualize a fila do doutor
        if id in socketDoutor:
            fila_pacientes_list = [pac.nome for pac in fila_pacientes[id].queue]
            socketio.emit("queue_updated", fila_pacientes_list, to=socketDoutor[id])

        return redirect('/doutor/home')
