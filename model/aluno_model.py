from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    nota_primeiro_semestre = Column(Float, default=0.0)
    nota_segundo_semestre = Column(Float, default=0.0)
    media = Column(Float, default=0.0)

    turma_id = Column(Integer, ForeignKey('turmas.id', ondelete="CASCADE"), nullable=False)
    turma = relationship("Turma", back_populates="alunos")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media": self.media,
            "turma_id": self.turma_id
        }