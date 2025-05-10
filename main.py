import os
from extensions import create_app, db, socketio

# Determina o ambiente baseado em variável de ambiente
env = os.environ.get('FLASK_ENV', 'default')
app = create_app(env)

# Importa as rotas depois de criar a aplicação
import routes  # noqa: F401
import views  # noqa: F401
import websocket  # noqa: F401

def create_admin():
    """Cria um usuário admin se não existir"""
    from models import Doutor
    with app.app_context():
        if not Doutor.query.filter_by(cpf='000').first():
            admin = Doutor(nome="admin", cpf='000', admin=True, consultorio=0)
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

    # Para produção, use o host 0.0.0.0 para permitir acesso pela rede local
    host = app.config.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))

    print(f"Servidor rodando em http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=app.config.get('DEBUG', False))
