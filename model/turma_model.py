from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados
from model.professor_model import Professor 

Base = BancoDados.Base
Session = BancoDados.SessionLocal

class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento com a classe Aluno
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")

    # Relacionamento com a classe Professor
    professor = relationship("Professor", back_populates="turmas")

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    def to_dict(self):
        """Método para converter o objeto Turma em um dicionário"""
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": self.ativo,
            "professor": self.professor.to_dict() if self.professor else None,  # Evita erro caso professor seja None
            "quantidade_alunos": len(self.alunos) if self.alunos else 0  # Conta a quantidade de alunos
        }

    def __repr__(self):
        """Representação da classe para facilitar a leitura"""
        return f"<Turma(id={self.id}, descricao='{self.descricao}', ativo={self.ativo})>"

class TurmaNaoEncontrada(Exception):
    """Exceção personalizada para quando uma turma não for encontrada"""
    pass