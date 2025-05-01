from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from config import BancoDados
from sqlalchemy.orm.exc import NoResultFound

Base = BancoDados.Base
Session = BancoDados.Session

class Turma(Base):
    """
    Classe que representa uma turma no sistema.
    
    Atributos:
        id (int): Identificador único da turma (PK)
        descricao (str): Nome/descrição da turma
        professor_id (int): ID do professor responsável (FK)
        ativo (bool): Status da turma (ativo/inativo)
        alunos (relationship): Relacionamento com alunos
        professor (relationship): Relacionamento com professor
    """
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True, doc="ID único da turma")
    descricao = Column(String(100), nullable=False, doc="Nome/descrição da turma")
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False, doc="ID do professor responsável")
    ativo = Column(Boolean, default=True, doc="Status da turma (ativo/inativo)")

    # Relacionamentos
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan", doc="Lista de alunos da turma")
    professor = relationship("Professor", back_populates="turmas", doc="Professor responsável pela turma")

    def to_dict(self):
        """Converte o objeto Turma para um dicionário serializável"""
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


class TurmaService:
    """Classe de serviço para operações relacionadas a turmas"""
    
    @staticmethod
    def listar_turmas(apenas_ativas=False):
        """
        Lista todas as turmas cadastradas
        
        Args:
            apenas_ativas (bool): Se True, retorna apenas turmas ativas
            
        Returns:
            list: Lista de turmas no formato de dicionário
            
        Raises:
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            query = session.query(Turma)
            if apenas_ativas:
                query = query.filter(Turma.ativo == True)
                
            turmas = query.all()
            return [t.to_dict() for t in turmas]
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar turmas: {e}")
        finally:
            session.close()

    @staticmethod
    def turma_por_id(id_turma):
        """
        Busca uma turma pelo ID
        
        Args:
            id_turma (int): ID da turma a ser buscada
            
        Returns:
            dict: Dados da turma no formato de dicionário
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com id {id_turma} não encontrada.")
            return turma.to_dict()
        except NoResultFound:
            raise TurmaNaoEncontrada(f"Turma com id {id_turma} não encontrada.")
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar turma: {e}")
        finally:
            session.close()

    @staticmethod
    def validar_dados(dados):
        """
        Valida os dados fornecidos para criação/atualização de turma
        
        Args:
            dados (dict): Dicionário com os dados da turma
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        campos_obrigatorios = ["descricao", "professor_id"]
        
        # Verifica campos obrigatórios
        if not all(campo in dados for campo in campos_obrigatorios):
            raise ValueError("Faltam campos obrigatórios: descricao e professor_id")
        
        # Valida descrição
        if not isinstance(dados["descricao"], str) or not dados["descricao"].strip():
            raise ValueError("Descrição deve ser um texto não vazio")
            
        # Valida professor_id
        if not isinstance(dados["professor_id"], int) or dados["professor_id"] <= 0:
            raise ValueError("ID do professor deve ser um número positivo")
            
        # Valida ativo (se fornecido)
        if "ativo" in dados and not isinstance(dados["ativo"], bool):
            raise ValueError("Status 'ativo' deve ser verdadeiro ou falso")

    @staticmethod
    def criar_turma(dados):
        """
        Cria uma nova turma no sistema
        
        Args:
            dados (dict): Dados da turma a ser criada
            
        Returns:
            tuple: (dict, int) Dados da turma criada e status code
            
        Raises:
            ValueError: Se os dados forem inválidos
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            # Valida os dados recebidos
            TurmaService.validar_dados(dados)
            
            # Verifica se o professor existe
            professor = session.query(Professor).get(dados["professor_id"])
            if not professor:
                raise ValueError("Professor não encontrado")

            # Cria a nova turma
            nova_turma = Turma(
                descricao=dados["descricao"].strip(),
                professor_id=dados["professor_id"],
                ativo=dados.get("ativo", True)
            )
            
            session.add(nova_turma)
            session.commit()
            
            return nova_turma.to_dict(), 201
        except ValueError as ve:
            session.rollback()
            return {"erro": str(ve)}, 400
        except SQLAlchemyError as e:
            session.rollback()
            return {"erro": f"Erro ao criar turma: {e}"}, 500
        finally:
            session.close()

    @staticmethod
    def atualizar_turma(id_turma, dados):
        """
        Atualiza os dados de uma turma existente
        
        Args:
            id_turma (int): ID da turma a ser atualizada
            dados (dict): Dados a serem atualizados
            
        Returns:
            tuple: (dict, int) Dados atualizados e status code
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            ValueError: Se os dados forem inválidos
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com id {id_turma} não encontrada.")

            # Validações específicas para atualização
            if "descricao" in dados:
                if not isinstance(dados["descricao"], str) or not dados["descricao"].strip():
                    raise ValueError("Descrição inválida")
                turma.descricao = dados["descricao"].strip()
                
            if "professor_id" in dados:
                if not isinstance(dados["professor_id"], int) or dados["professor_id"] <= 0:
                    raise ValueError("ID do professor inválido")
                turma.professor_id = dados["professor_id"]
                
            if "ativo" in dados:
                if not isinstance(dados["ativo"], bool):
                    raise ValueError("Status 'ativo' deve ser verdadeiro ou falso")
                turma.ativo = dados["ativo"]

            session.commit()
            return turma.to_dict(), 200
        except TurmaNaoEncontrada:
            session.rollback()
            raise
        except ValueError as ve:
            session.rollback()
            return {"erro": str(ve)}, 400
        except SQLAlchemyError as e:
            session.rollback()
            return {"erro": f"Erro ao atualizar turma: {e}"}, 500
        finally:
            session.close()

    @staticmethod
    def excluir_turma(id_turma):
        """
        Exclui uma turma do sistema (exclusão física)
        
        Args:
            id_turma (int): ID da turma a ser excluída
            
        Returns:
            tuple: (dict, int) Mensagem de sucesso e status code
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com id {id_turma} não encontrada.")

            session.delete(turma)
            session.commit()
            return {"mensagem": "Turma excluída com sucesso"}, 200
        except TurmaNaoEncontrada:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            return {"erro": f"Erro ao excluir turma: {e}"}, 500
        finally:
            session.close()