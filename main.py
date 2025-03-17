from extensions import app, db, socketio
from routes import *  # noqa: F403
<<<<<<< HEAD
#Teste
if __name__ == "__main__":
=======

if __name__ == "__main__":  # teste teste mudança linha 4
>>>>>>> 9b48a80ee10f4fd28d2dfd96a315269fbf5c6834
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
