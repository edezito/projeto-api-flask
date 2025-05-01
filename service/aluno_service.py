from sqlalchemy.exc import SQLAlchemyError

from model.aluno_model import Aluno

class AlunoService:
    @staticmethod
    def listar_alunos(session):
        try:
            alunos = session.query(Aluno).all()
            return [aluno.to_dict() for aluno in alunos]
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar alunos: {str(e)}")

    @staticmethod
    def buscar_aluno_por_id(session, id_aluno):
        try:
            aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
            if not aluno:
                raise Exception("Aluno não encontrado")
            return aluno.to_dict()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar aluno: {str(e)}")

    @staticmethod
    def validar_dados(dados):
        if not all(key in dados for key in ["nome", "idade", "turma_id"]):
            raise ValueError("Faltam campos obrigatórios")
        
        if not isinstance(dados["idade"], int) or not 0 <= dados["idade"] <= 120:
            raise ValueError("Idade inválida")

    @staticmethod
    def calcular_media(dados):
        nota_primeiro = dados.get("nota_primeiro_semestre", 0.0)
        nota_segundo = dados.get("nota_segundo_semestre", 0.0)
        return (nota_primeiro + nota_segundo) / 2

    @staticmethod
    def criar_aluno(session, dados):
        try:
            AlunoService.validar_dados(dados)
            media = AlunoService.calcular_media(dados)
            
            aluno = Aluno(
                nome=dados["nome"],
                idade=dados["idade"],
                turma_id=dados["turma_id"],
                nota_primeiro_semestre=dados.get("nota_primeiro_semestre", 0.0),
                nota_segundo_semestre=dados.get("nota_segundo_semestre", 0.0),
                media=media
            )
            
            session.add(aluno)
            session.commit()
            return aluno.to_dict()
        except ValueError as e:
            session.rollback()
            raise ValueError(str(e))
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao criar aluno: {str(e)}")

    @staticmethod
    def atualizar_aluno(session, id_aluno, dados):
        try:
            aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
            if not aluno:
                raise Exception("Aluno não encontrado")

            if "idade" in dados:
                if not isinstance(dados["idade"], int) or not 0 <= dados["idade"] <= 120:
                    raise ValueError("Idade inválida")

            aluno.nome = dados.get("nome", aluno.nome)
            aluno.idade = dados.get("idade", aluno.idade)
            aluno.turma_id = dados.get("turma_id", aluno.turma_id)

            if "nota_primeiro_semestre" in dados:
                aluno.nota_primeiro_semestre = dados["nota_primeiro_semestre"]
            if "nota_segundo_semestre" in dados:
                aluno.nota_segundo_semestre = dados["nota_segundo_semestre"]
                
            aluno.media = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2

            session.commit()
            return aluno.to_dict()
        except ValueError as e:
            session.rollback()
            raise ValueError(str(e))
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar aluno: {str(e)}")

    @staticmethod
    def excluir_aluno(session, id_aluno):
        try:
            aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
            if not aluno:
                raise Exception("Aluno não encontrado")

            session.delete(aluno)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao excluir aluno: {str(e)}")