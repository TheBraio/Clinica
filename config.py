import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Chave_que_ninguem_jamais_descobrira"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = '0.0.0.0'  # Permite acesso de qualquer dispositivo na rede

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dados.db"

class ProductionConfig(Config):
    DEBUG = False
    # Usando SQLite para simplicidade, mas considere migrar para um banco mais robusto
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///dados.db"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
