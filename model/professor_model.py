from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config import BancoDados
from sqlalchemy.exc import SQLAlchemyError


Base = BancoDados.Base
Session = BancoDados.Session
class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    materia = Column(String(100), nullable=False)
    observacoes = Column(Text)

    turmas = relationship("Turma", back_populates="professor", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "materia": self.materia,
            "observacoes": self.observacoes
        }


class ProfessorNaoEncontrado(Exception):
    pass
class ProfessorService:

    @staticmethod
    def listar_professores():
        session = Session()
        try:
            professores = session.query(Professor).all()
            return [prof.to_dict() for prof in professores]
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar professores: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def professor_por_id(id_professor):
        session = Session()
        try:
            professor = session.query(Professor).filter(Professor.id == id_professor).first()
            if not professor:
                raise ProfessorNaoEncontrado()
            return professor.to_dict()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar professor: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def validar_dados(dados):
        campos_obrigatorios = ["nome", "idade", "materia"]
        if not all(campo in dados for campo in campos_obrigatorios):
            raise ValueError("Faltam campos obrigatórios")

        if not isinstance(dados["idade"], int) or dados["idade"] < 0:
            raise ValueError("Idade inválida")

    @staticmethod
    def criar_professor(dados):
        session = Session()
        try:
            ProfessorService.validar_dados(dados)

            novo_professor = Professor(
                nome=dados["nome"],
                idade=dados["idade"],
                materia=dados["materia"],
                observacoes=dados.get("observacoes")
            )

            session.add(novo_professor)
            session.commit()
            return novo_professor.to_dict(), 201
        except ValueError as e:
            session.rollback()
            return {"error": str(e)}, 400
        except SQLAlchemyError as e:
            session.rollback()
            return {"error": f"Erro ao criar professor: {str(e)}"}, 500
        finally:
            session.close()

    @staticmethod
    def atualizar_professor(id_professor, dados):
        session = Session()
        try:
            professor = session.query(Professor).filter(Professor.id == id_professor).first()
            if not professor:
                raise ProfessorNaoEncontrado()

            if "idade" in dados:
                if not isinstance(dados["idade"], int) or dados["idade"] < 0:
                    raise ValueError("Idade inválida")

            professor.nome = dados.get("nome", professor.nome)
            professor.idade = dados.get("idade", professor.idade)
            professor.materia = dados.get("materia", professor.materia)
            professor.observacoes = dados.get("observacoes", professor.observacoes)

            session.commit()
            return professor.to_dict(), 200
        except ValueError as e:
            session.rollback()
            return {"error": str(e)}, 400
        except SQLAlchemyError as e:
            session.rollback()
            return {"error": f"Erro ao atualizar professor: {str(e)}"}, 500
        finally:
            session.close()

    @staticmethod
    def excluir_professor(id_professor):
        session = Session()
        try:
            professor = session.query(Professor).filter(Professor.id == id_professor).first()
            if not professor:
                raise ProfessorNaoEncontrado()

            session.delete(professor)
            session.commit()
            return {"message": "Professor excluído com sucesso"}, 200
        except SQLAlchemyError as e:
            session.rollback()
            return {"error": f"Erro ao excluir professor: {str(e)}"}, 500
        finally:
            session.close()
