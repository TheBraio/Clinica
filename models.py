from main import db


class Pacientes(db.Model):
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100))

    def __repr__(self):
        return f"<Paciente {self.nome}>"


class Funcionario(db.Model):
    def __init__(self, nome, cargo):
        self.nome = nome
        self.cargo = cargo

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(50))

    __mapper_args__ = {"polymorphic_on": cargo, "with_polymorphic": "*"}

    def __repr__(self):
        return f"<Funcionario {self.nome}>"


class Doutor(Funcionario):
    __tablename__ = "doutor"
    id = db.Column(db.Integer, db.ForeignKey("funcionario.id"), primary_key=True)
    consultorio = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "doutor"  # Identificador único para a classe Doutor
    }

    def __init__(self, nome, consultorio):
        super().__init__(nome)
        self.consultorio = consultorio

    def __repr__(self):
        return f"<Doutor {self.nome}>"


class Atendente(Funcionario):
    __tablename__ = "atendente"
    id = db.Column(db.Integer, db.ForeignKey("funcionario.id"), primary_key=True)
    setor = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "atendente"  # Identificador único para a classe Atendente
    }

    def __init__(self, nome, setor):
        super().__init__(nome)
        self.setor = setor

    def __repr__(self):
        return f"<Atendente {self.nome}>"
