from sqlalchemy import Column, String
from config import BancoDados

class Usuario(BancoDados.Base):
    __tablename__ = 'usuarios'
    
    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    nickname = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

    def to_dict(self):
        return {
            "nome": self.nome,
            "nickname": self.nickname,
        }