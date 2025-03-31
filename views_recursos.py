from functools import wraps
from flask import session, render_template

class Link:
    def __init__(self, rota, icone, texto):
        self.rota = rota
        self.icone = icone
        self.texto = texto

desloga = Link('/deslogar', '', 'Desconectar')
links : dict = {
    'admin': [
        Link("/admin/home", "fa-solid fa-user-tie", "Funcionários"),
        Link("/admin/cadastrar-funcionario", "fa-solid fa-user-plus", "Cadastrar Funcionário")
    ],
    'atendente': [
        Link('/atendente/home', 'fa-solid fa-user', 'Pacientes'),
        Link('/atendente/cadastrar-paciente', 'fa-solid fa-user-plus', 'Cadastrar Pacientes'),
    ],
    'doutor': [
        Link('/doutor/home', 'fa-solid fa-user-doctor', 'Área do Doutor')
    ],
    '': [Link('/login', "fa-solid fa-arrow-right-to-bracket", "Logar")]
}

links['admin'] += links['atendente']
links['admin'] += links['doutor']

class Status:
    def __init__(self, message: str, category: str):
        self.message = message
        self.category = category

# Retornos de erro
# 450 = não logado
# 451 = não é admin
# 452 = não é doutor
# 453 = não é atendente

def render_template_nav(arq, links=links, **kwargs):
    return render_template(arq, 
                           links=links[''] if 'privilegios' not in session else links[session['privilegios'][0]], 
                           **kwargs)


def logged(func):
    @wraps(func)
    def wrapper():
        if session and 'privilegios' in session:
            return func()
        else:
            return '450'
        
    return wrapper

def is_admin(func):
    @wraps(func)
    def wrapper():
        if 'admin' in session['privilegios']:
            return func()        
        else:
            return "451"

    return wrapper

def is_doutor(func):
    @wraps(func)
    def wrapper():
        if 'doutor' in session['privilegios']:
            return func()
        else:
            return "452"
    
    return wrapper
        
def is_atendente(func):
    @wraps(func)
    def wrapper():
        if 'atendente' in session['privilegios']:
            return func()
        else:
            return "453"

    return wrapper


lista_pacientes: list = []