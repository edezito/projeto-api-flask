import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega variáveis de ambiente
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class BancoDados:
    # Configuração do banco de dados
    DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///gestao_escolar.db')
    
    engine = create_engine(
        DATABASE_URI,
        echo=os.getenv('SQL_ECHO', 'False').lower() in ('true', '1', 't'),
        pool_size=int(os.getenv('DB_POOL_SIZE', '5')),
        max_overflow=int(os.getenv('DB_MAX_OVERFLOW', '10')),
        pool_pre_ping=True,
        pool_recycle=3600
    )
    
    Base = declarative_base()
    
    # Configuração correta do sessionmaker
    Session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=True
    )

    @staticmethod
    def get_session():
        """Retorna uma nova sessão do banco de dados"""
        try:
            return BancoDados.Session()
        except Exception as e:
            BancoDados.engine.dispose()
            raise ConnectionError(f"Falha ao estabelecer sessão: {str(e)}")

class Config:
    # Configurações básicas
    HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    PORT = int(os.getenv('FLASK_PORT', '5000'))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Segurança
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.urandom(24).hex())
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = BancoDados.DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False