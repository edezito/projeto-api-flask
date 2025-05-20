from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    nota_primeiro_semestre = Column(Float, nullable=True)
    nota_segundo_semestre = Column(Float, nullable=True)
    media = Column(Float, nullable=True)
    turma_id = Column(Integer, ForeignKey('turmas.id'), nullable=True)

    turma = relationship("Turma", back_populates="alunos", lazy='select')

    def __init__(self, nome, idade, nota_primeiro_semestre=None, nota_segundo_semestre=None, turma_id=None):
        self.nome = nome.strip()
        self.idade = idade
        self.nota_primeiro_semestre = self._validar_nota(nota_primeiro_semestre)
        self.nota_segundo_semestre = self._validar_nota(nota_segundo_semestre)
        self.turma_id = turma_id
        self.calcular_media()

    def _validar_nota(self, nota):
        """Valida se a nota está entre 0 e 10 ou é None"""
        if nota is not None:
            if not isinstance(nota, (int, float)) or not 0 <= nota <= 10:
                raise ValueError("Notas devem ser números entre 0 e 10")
        return nota

    def calcular_media(self):
        """Calcula a média do aluno com base nas notas dos dois semestres."""
        if None not in (self.nota_primeiro_semestre, self.nota_segundo_semestre):
            self.media = round((self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2, 2)
        else:
            self.media = None

    def to_dict(self, include_turma=False):
        """Converte o objeto Aluno para um dicionário de forma segura."""
        try:
            aluno_dict = {
                "id": self.id,
                "nome": self.nome,
                "idade": self.idade,
                "nota_primeiro_semestre": self.nota_primeiro_semestre,
                "nota_segundo_semestre": self.nota_segundo_semestre,
                "media": self.media,
                "turma_id": self.turma_id
            }

            if include_turma:
                aluno_dict['turma'] = self._get_turma_dict()
            
            return aluno_dict
        except Exception as e:
            # Fallback seguro em caso de erro inesperado
            return {
                "id": self.id,
                "nome": self.nome,
                "error": f"Erro na serialização: {str(e)}"
            }

    def _get_turma_dict(self):
        """Método auxiliar para serialização segura da turma"""
        if not hasattr(self, 'turma') or self.turma is None:
            return None
        
        # Verifica se a turma já foi carregada
        if self.turma in (None, {}, ''):
            return None
            
        # Versão segura que não depende do método to_dict da Turma
        return {
            "id": getattr(self.turma, 'id', None),
            "nome": getattr(self.turma, 'nome', None),
            # Adicione outros campos necessários
        }

    def __repr__(self):
        return f"<Aluno(id={self.id}, nome='{self.nome}', media={self.media})>"