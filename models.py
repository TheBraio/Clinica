from main import db


class Pacientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100))

    def __repr__(self):
        return f"<Paciente {self.nome}>"
