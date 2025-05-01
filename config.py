import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class BancoDados:
    # Configuração otimizada do SQLAlchemy
    DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///gestao_escolar.db')
    engine = create_engine(
        DATABASE_URI,
        echo=True,  # Log de queries (desativar em produção)
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True  # Verifica conexões antes de usar
    )
    
    Base = declarative_base()
    
    Session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=True
    )

    @staticmethod
    def get_session():
        """Retorna uma nova sessão do banco de dados"""
        return BancoDados.Session()

class Config:
    # Configurações básicas
    HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    PORT = int(os.getenv('FLASK_PORT', '5000'))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Segurança
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.urandom(24).hex())
    
    # Configurações do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = BancoDados.DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
    
    # Configurações adicionais
    API_TITLE = "Gestão Escolar API"
    API_VERSION = "1.0"
    OPENAPI_VERSION = "3.0.3"