from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    nota_primeiro_semestre = Column(Float, nullable=True)
    nota_segundo_semestre = Column(Float, nullable=True)
    media = Column(Float, nullable=True)
    turma_id = Column(Integer, ForeignKey('turmas.id'))

    turma = relationship("Turma", back_populates="alunos")

    def __init__(self, nome, idade, nota_primeiro_semestre=None, nota_segundo_semestre=None, turma_id=None):
        self.nome = nome
        self.idade = idade
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.turma_id = turma_id

    def calcular_media(self):
        """Calcula a média do aluno com base nas notas dos dois semestres."""
        if self.nota_primeiro_semestre and self.nota_segundo_semestre:
            self.media = (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        else:
            self.media = None

    def to_dict(self, include_turma=False):
        """Converte o objeto Aluno para um dicionário, incluindo informações da turma se solicitado."""
        aluno_dict = {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media": self.media,
            "turma_id": self.turma_id
        }
        if include_turma and self.turma:
            aluno_dict['turma'] = self.turma.to_dict()  # Inclui os dados da turma, se solicitado
        return aluno_dict

    def __repr__(self):
        return f"<Aluno(id={self.id}, nome='{self.nome}', media={self.media})>"