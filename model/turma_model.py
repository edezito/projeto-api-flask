from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from config import BancoDados

Base = BancoDados.Base
Session = BancoDados.Session
class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False)
    ativo = Column(Boolean, default=True)

    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")

    professor = relationship("Professor", back_populates="turmas")

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": self.ativo
        }
class TurmaNaoEncontrada(Exception):
    pass
class TurmaService:

    @staticmethod
    def listar_turmas():
        session = Session()
        try:
            turmas = session.query(Turma).all()
            return [t.to_dict() for t in turmas]
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar turmas: {e}")
        finally:
            session.close()

    @staticmethod
    def turma_por_id(id_turma):
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada()
            return turma.to_dict()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar turma: {e}")
        finally:
            session.close()

    @staticmethod
    def validar_dados(dados):
        campos_obrigatorios = ["descricao", "professor_id"]
        if not all(c in dados for c in campos_obrigatorios):
            raise ValueError("Faltam campos obrigatórios")
        if not isinstance(dados["descricao"], str) or not dados["descricao"].strip():
            raise ValueError("Descrição inválida")
        if not isinstance(dados["professor_id"], int) or dados["professor_id"] <= 0:
            raise ValueError("Professor_id inválido")
        if "ativo" in dados and not isinstance(dados["ativo"], bool):
            raise ValueError("Campo 'ativo' deve ser booleano")

    @staticmethod
    def criar_turma(dados):
        session = Session()
        try:
            TurmaService.validar_dados(dados)
            nova = Turma(
                descricao=dados["descricao"].strip(),
                professor_id=dados["professor_id"],
                ativo=dados.get("ativo", True)
            )
            session.add(nova)
            session.commit()
            return nova.to_dict(), 201
        except ValueError as ve:
            session.rollback()
            return {"error": str(ve)}, 400
        except SQLAlchemyError as e:
            session.rollback()
            return {"error": f"Erro ao criar turma: {e}"}, 500
        finally:
            session.close()

    @staticmethod
    def atualizar_turma(id_turma, dados):
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada()

            # validações pontuais
            if "descricao" in dados and (not isinstance(dados["descricao"], str) or not dados["descricao"].strip()):
                raise ValueError("Descrição inválida")
            if "professor_id" in dados and (not isinstance(dados["professor_id"], int) or dados["professor_id"] <= 0):
                raise ValueError("Professor_id inválido")
            if "ativo" in dados and not isinstance(dados["ativo"], bool):
                raise ValueError("Campo 'ativo' deve ser booleano")

            # aplicação de updates
            turma.descricao = dados.get("descricao", turma.descricao).strip()
            turma.professor_id = dados.get("professor_id", turma.professor_id)
            turma.ativo = dados.get("ativo", turma.ativo)

            session.commit()
            return turma.to_dict(), 200
        except TurmaNaoEncontrada:
            raise
        except ValueError as ve:
            session.rollback()
            return {"error": str(ve)}, 400
        except SQLAlchemyError as e:
            session.rollback()
            return {"error": f"Erro ao atualizar turma: {e}"}, 500
        finally:
            session.close()

    @staticmethod
    def excluir_turma(id_turma):
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada()

            session.delete(turma)
            session.commit()
            return {"message": "Turma excluída com sucesso"}, 200
        except TurmaNaoEncontrada:
            raise
        except SQLAlchemyError as e:
            session.rollback()
            return {"error": f"Erro ao excluir turma: {e}"}, 500
        finally:
            session.close()
