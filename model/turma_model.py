from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base
Session = BancoDados.SessionLocal

class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True, doc="ID único da turma")
    descricao = Column(String(100), nullable=False, doc="Nome/descrição da turma")
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False, doc="ID do professor responsável")
    ativo = Column(Boolean, default=True, doc="Status da turma (ativo/inativo)")

    # Relacionamentos
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan", doc="Lista de alunos da turma")
    professor = relationship("Professor", back_populates="turmas", doc="Professor responsável pela turma")

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": self.ativo,
            "professor": self.professor.to_dict() if self.professor else None,
            "quantidade_alunos": len(self.alunos) if self.alunos else 0
        }

    def __repr__(self):
        return f"<Turma(id={self.id}, descricao='{self.descricao}', ativo={self.ativo})>"


class TurmaNaoEncontrada(Exception):
    """Exceção personalizada para quando uma turma não é encontrada"""
    pass