from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base

class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    materia = Column(String(100), nullable=False)
    observacoes = Column(Text, nullable=True)

    turmas = relationship("Turma", back_populates="professor", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "materia": self.materia,
            "observacoes": self.observacoes
        }

    def __repr__(self):
        return f"<Professor(id={self.id}, nome='{self.nome}', materia='{self.materia}')>"