from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash




class Funcionario(db.Model):
    __tablename__ = "funcionario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), unique = True, nullable=False)
    senha = db.Column(db.String(255), default=generate_password_hash('123'), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    cargo = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "funcionario",
        "polymorphic_on": cargo,
        "with_polymorphic": "*",
    }

    def __init__(self, nome, cargo, cpf, admin):
        self.nome = nome
        self.cargo = cargo
        self.cpf = cpf
        self.admin = admin

    def __repr__(self):
        return f"<Funcionario {self.nome} - {self.cargo}>"
    
    def change_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)


class Doutor(Funcionario):
    __tablename__ = "doutor"

    id = db.Column(db.Integer, db.ForeignKey("funcionario.id"), primary_key=True)
    consultorio = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "doutor"}

    pacientes = db.relationship('Paciente', backref='responsavel', lazy=True)

    def __init__(self, nome, cpf, consultorio, admin=False):
        super().__init__(nome=nome, cargo="doutor", cpf=cpf, admin=admin)
        self.consultorio = consultorio

    def __repr__(self):
        return f"<Doutor {self.nome}, Consultório {self.consultorio}>"


class Atendente(Funcionario):
    __tablename__ = "atendente"

    id = db.Column(db.Integer, db.ForeignKey("funcionario.id"), primary_key=True)
    setor = db.Column(db.String(50))

    __mapper_args__ = {"polymorphic_identity": "atendente"}

    def __init__(self, nome, cpf, setor, admin=False):
        super().__init__(nome=nome, cpf = cpf, cargo="atendente", admin = admin)
        self.setor = setor


    def __repr__(self):
        return f"<Atendente {self.nome}, Setor {self.setor}>"

class Paciente(db.Model):
    __tablename__ = "paciente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100))
    cpf = db.Column(db.String(11), unique=True)

    doutor = db.Column(db.Integer, db.ForeignKey('doutor.id'))
    def __init__(self, nome, descricao, cpf, doutor):
        self.nome = nome
        self.descricao = descricao
        self.cpf = cpf
        self.doutor = doutor

    def __repr__(self):
        return f"<Paciente {self.nome}>"