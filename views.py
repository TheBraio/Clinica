from extensions import app
from models import Pacientes
from views_recursos import *

# Rotas do admin
@app.route('/admin-funcionarios')
@is_admin
def admin_funcionarios():
    return render_template_nav('admin_funcionarios.html')
# Rotas do admin

# Rotas do atendente
@app.route("/atendente-pacientes", methods=["GET"])
def atendente_pacientes():
    pacientes = Pacientes.query.all()
    
    return render_template_nav("atendente_pacientes.html", pacientes=pacientes, )

@app.route("/atendente-cadastrar-paciente")
def cadastrar():
    return render_template_nav("atendente_cadastrar_paciente.html")
# Rotas do atendente

# Rotas do doutor 
@app.route("/doutor-mainpage")
def doutor():
    return render_template_nav("doutor_mainpage.html")
# Rotas do doutor 


# Rotas Gerais
@app.route('/login', methods=["GET"])
@app.route('/', methods=["GET"])
def login():
    return render_template_nav('login.html')

@app.route("/chamada")
def chamada():
    return render_template("chamadaPaciente.html")
# Rotas Gerais