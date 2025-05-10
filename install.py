import os
import sys
import subprocess
import socket
import venv
from pathlib import Path

def criar_ambiente_virtual():
    """Cria um ambiente virtual Python para o projeto"""
    print("Criando ambiente virtual Python...")
    venv_dir = os.path.join(os.getcwd(), "venv")

    # Se a venv já existir, não tenta recriar
    if os.path.exists(venv_dir):
        print(f"Ambiente virtual já existe em: {venv_dir}")
        return True

    try:
        venv.create(venv_dir, with_pip=True)
        print(f"Ambiente virtual criado em: {venv_dir}")
        return True
    except Exception as e:
        print(f"Erro ao criar ambiente virtual: {e}")
        return False

def testar_venv():
    """Testa se a venv foi criada corretamente"""
    venv_activate = os.path.join(os.getcwd(), "venv", "Scripts", "activate.bat")
    if not os.path.exists(venv_activate):
        print("ERRO: O arquivo de ativação da venv não foi encontrado!")
        print(f"Esperado em: {venv_activate}")
        return False

    python_venv = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    if not os.path.exists(python_venv):
        print("ERRO: O executável Python da venv não foi encontrado!")
        print(f"Esperado em: {python_venv}")
        return False

    print("Ambiente virtual verificado com sucesso.")
    return True

def instalar_dependencias():
    """Instala as dependências necessárias usando pip dentro da venv"""
    python_venv = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    pip_venv = os.path.join(os.getcwd(), "venv", "Scripts", "pip.exe")

    print(f"Instalando dependências usando: {pip_venv}")

    requirements = [
        "flask",
        "flask-sqlalchemy",
        "flask-socketio",
        "flask-cors",
        "flask-migrate",
        "eventlet"
    ]

    try:
        # Atualiza pip primeiro
        subprocess.check_call([python_venv, "-m", "pip", "install", "--upgrade", "pip"])

        # Instala cada dependência
        for req in requirements:
            print(f"Instalando {req}...")
            subprocess.check_call([pip_venv, "install", req])

        print("Todas as dependências foram instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        return False

def criar_arquivo_bat():
    """Cria um arquivo .bat para iniciar o sistema usando a venv"""
    bat_path = os.path.join(os.getcwd(), "iniciar_sistema.bat")

    bat_content = f"""@echo off
echo ===== Iniciando Sistema da Clinica Odontologica =====
cd /d "{os.getcwd()}"
echo Ativando ambiente virtual...
call venv\\Scripts\\activate.bat
echo Servidor iniciando...
echo.
echo Use este endereco para acessar: http://{obter_ip_local()}:5000
echo.
python main.py
pause
"""

    with open(bat_path, 'w') as f:
        f.write(bat_content)

    print(f"Arquivo batch criado: {bat_path}")
    print("Clique duas vezes neste arquivo para iniciar o sistema")

def criar_bat_backup():
    """Cria um arquivo .bat para fazer backup do banco de dados"""
    bat_path = os.path.join(os.getcwd(), "fazer_backup.bat")

    # Cria pasta de backups se não existir
    backup_dir = os.path.join(os.getcwd(), "backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    bat_content = f"""@echo off
echo ===== Backup do Banco de Dados =====
cd /d "{os.getcwd()}"
call venv\\Scripts\\activate.bat
set data=%date:~6,4%%date:~3,2%%date:~0,2%
set hora=%time:~0,2%%time:~3,2%%time:~6,2%
set hora=%hora: =0%
set arquivo=backups\\backup_%data%_%hora%.db
echo Criando backup em: %arquivo%
copy dados.db %arquivo%
echo Backup concluido!
pause
"""

    with open(bat_path, 'w') as f:
        f.write(bat_content)

    print(f"Arquivo de backup criado: {bat_path}")
    print("Execute este arquivo quando quiser fazer um backup do sistema")

def obter_ip_local():
    """Obtém o endereço IP local da máquina"""
    try:
        # Cria socket para determinar o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except:
        return "localhost"

def modificar_main():
    """Modifica o arquivo main.py para iniciar com IP 0.0.0.0"""
    original_path = os.path.join(os.getcwd(), "main.py")

    with open(original_path, 'r') as f:
        conteudo = f.read()

    # Verifica se já foi modificado
    if "host='0.0.0.0'" in conteudo:
        print("Arquivo main.py já está configurado para rede local.")
        return

    # Adiciona código para mostrar o IP local
    novo_conteudo = conteudo.replace(
        "socketio.run(app, debug=True)",
        "print(f'Servidor iniciado! Acesse: http://" + obter_ip_local() + ":5000')\n"
        "    socketio.run(app, host='0.0.0.0', debug=False)"
    )

    with open(original_path, 'w') as f:
        f.write(novo_conteudo)

    print("Arquivo main.py modificado para permitir acesso pela rede local")

def criar_readme():
    """Cria um arquivo README com instruções"""
    readme_path = os.path.join(os.getcwd(), "INSTRUCOES.txt")

    readme_content = f"""SISTEMA DE CLÍNICA ODONTOLÓGICA - INSTRUÇÕES
=============================================

INFORMAÇÕES DE ACESSO:
----------------------
Endereço: http://{obter_ip_local()}:5000
Login admin padrão: CPF 000, senha 123

ARQUIVOS IMPORTANTES:
--------------------
- iniciar_sistema.bat: Inicia o sistema da clínica
- fazer_backup.bat: Cria uma cópia de segurança do banco de dados

PARA INICIAR O SISTEMA:
----------------------
1. Clique duas vezes no arquivo "iniciar_sistema.bat"
2. Aguarde a mensagem "Servidor iniciado!"
3. Acesse o endereço http://{obter_ip_local()}:5000 nos computadores da clínica

PARA FAZER BACKUP:
-----------------
1. Clique duas vezes no arquivo "fazer_backup.bat"
2. Será criado um arquivo na pasta "backups" com a data e hora atual

DICAS:
-----
- Mantenha este computador sempre ligado enquanto a clínica estiver em funcionamento
- Faça backups regularmente para evitar perda de dados
- Não mova ou renomeie os arquivos do sistema

SUPORTE:
-------
Em caso de problemas, entre em contato com o administrador do sistema.

INFORMAÇÕES TÉCNICAS:
-------------------
Este sistema usa um ambiente virtual Python (venv) que contém todas as
dependências necessárias isoladas do sistema. Isso garante que o sistema
funcione corretamente independentemente de outras instalações Python.
"""

    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"Arquivo de instruções criado: {readme_path}")

def main():
    print("===== Instalação do Sistema de Clínica Odontológica =====")
    print(f"Endereço IP local: {obter_ip_local()}")

    if criar_ambiente_virtual() and testar_venv() and instalar_dependencias():
        criar_arquivo_bat()
        criar_bat_backup()
        modificar_main()
        criar_readme()

        print("\nInstalação concluída com sucesso!")
        print("O sistema está pronto para uso.")
        print(f"Endereço de acesso: http://{obter_ip_local()}:5000")
        print("Para iniciar o servidor, clique duas vezes em 'iniciar_sistema.bat'")
    else:
        print("Falha na instalação. Verifique os erros acima.")

if __name__ == "__main__":
    main()
