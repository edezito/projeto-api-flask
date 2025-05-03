from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config import BancoDados
from sqlalchemy.exc import SQLAlchemyError


Base = BancoDados.Base
Session = BancoDados.SessionLocal
class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    materia = Column(String(100), nullable=False)
    observacoes = Column(Text)

    turmas = relationship("Turma", back_populates="professor", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "materia": self.materia,
            "observacoes": self.observacoes
        }