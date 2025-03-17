from extensions import app, db, socketio
from routes import *  # noqa: F403


if __name__ == "__main__":  # teste teste mudança linha 4
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)

#Teste de branch