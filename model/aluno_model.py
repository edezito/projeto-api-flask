from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    nota_primeiro_semestre = Column(Float)
    nota_segundo_semestre = Column(Float)
    media = Column(Float)
    turma_id = Column(Integer, ForeignKey('turmas.id'))

    turma = relationship("Turma", back_populates="alunos")

    def to_dict(self, include_turma=False):
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
            aluno_dict['turma'] = self.turma.to_dict()  # Inclui os dados da turma
        return aluno_dict