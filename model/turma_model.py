from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.orm import attributes
from config import BancoDados
from model.professor_model import Professor

Base = BancoDados.Base
Session = BancoDados.SessionLocal

class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    alunos = relationship(
        "Aluno", 
        back_populates="turma", 
        cascade="all, delete-orphan",
        lazy="dynamic"  # Melhor para performance quando há muitos alunos
    )
    
    professor = relationship(
        "Professor", 
        back_populates="turmas",
        lazy="joined"  # Carrega automaticamente o professor
    )

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    @validates('descricao')
    def valida_descricao(self, key, descricao):
        """Validação automática para a descrição"""
        if not descricao or len(descricao.strip()) < 3:
            raise ValueError("Descrição deve ter pelo menos 3 caracteres")
        return descricao.strip()

    @validates('professor_id')
    def valida_professor_id(self, key, professor_id):
        """Validação automática para o ID do professor"""
        if not isinstance(professor_id, int) or professor_id <= 0:
            raise ValueError("ID do professor deve ser um número positivo")
        return professor_id

    def to_dict(self):
        """Converte o objeto Turma em um dicionário de forma segura"""
        # Verifica se os relacionamentos estão carregados
        professor_loaded = attributes.instance_state(self).loaded_attrs.get('professor', None)
        alunos_loaded = attributes.instance_state(self).loaded_attrs.get('alunos', None)

        professor_dict = None
        if professor_loaded:
            professor_dict = self.professor.to_dict() if self.professor else None
        
        quantidade_alunos = 0
        if alunos_loaded:
            if self.alunos and hasattr(self.alunos, 'count'):
                quantidade_alunos = self.alunos.count()
            elif self.alunos:
                quantidade_alunos = len(self.alunos)

        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": self.ativo,
            "professor": professor_dict,
            "quantidade_alunos": quantidade_alunos
        }

    def ativar(self):
        """Ativa a turma"""
        self.ativo = True

    def desativar(self):
        """Desativa a turma"""
        self.ativo = False

    def __repr__(self):
        return (f"<Turma(id={self.id}, descricao='{self.descricao}', "
                f"professor_id={self.professor_id}, ativo={self.ativo})>")

class TurmaNaoEncontrada(Exception):
    """Exceção personalizada para quando uma turma não for encontrada"""
    def __init__(self, turma_id):
        self.turma_id = turma_id
        super().__init__(f"Turma com ID {turma_id} não encontrada")