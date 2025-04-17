import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

class BancoDados:
    engine = create_engine('sqlite:///gestao_escolar.db', echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)

class Config:
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'projeto-escola')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///gestao_escolar.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False