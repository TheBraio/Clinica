from functools import wraps
from flask import session

class Link:
    def __init__(self, rota, icone, texto):
        self.rota = rota
        self.icone = icone
        self.texto = texto

links : dict = {
    'admin': [
        Link("/admin-funcionarios", "", "Funcionários"),
        Link("/admin-lucros", "", "Lucros"),
    ],
    'atendente': [
        Link('/atendente-pacientes', 'fa-solid fa-user', 'Pacientes'),
        Link('/atendente-calculo', '', 'Calculos'),
    ],
    '': [Link('/login', "fa-solid fa-arrow-right-to-bracket", "Logar")]
}

def is_admin(func):
    @wraps(func)
    def wrapper():
        if session and 'nome' in session:
            if session['nome'] == 'admin':
                return func()        
            else:
                return "Você Não é admin manow"
        else:
            return "Nem logado ce ta."

    return wrapper
