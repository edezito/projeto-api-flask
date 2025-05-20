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
        """Garante que retorna valores padrão mesmo se o objeto não estiver carregado"""
        return {
            "id": self.id if self.id is not None else 0,
            "nome": self.nome if self.nome is not None else "",
            "idade": self.idade if self.idade is not None else 0,
            "materia": self.materia if self.materia is not None else "",
            "observacoes": self.observacoes if self.observacoes is not None else ""
        }

    def __repr__(self):
        return f"<Professor(id={self.id}, nome='{self.nome}', materia='{self.materia}')>"