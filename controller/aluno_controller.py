from flask import request
from sqlalchemy.orm.exc import NoResultFound
from model.aluno_model import AlunoService
from model.turma_model import Turma
from config import BancoDados
from functools import wraps

# Tratamento de erros do banco
def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = BancoDados.Session()
        try:
            return func(session, *args, **kwargs)
        except ValueError as e:
            return {'erro': str(e)}, 400
        except NoResultFound:
            return {'erro': 'Registro não encontrado'}, 404
        except Exception as e:
            session.rollback()
            return {'erro': str(e)}, 500
        finally:
            session.close()
    return wrapper

class AlunoController:

    @staticmethod
    @handle_db_errors
    def listar(session):
        return AlunoService.listar_alunos(session), 200

    @staticmethod
    @handle_db_errors
    def criar(session):
        data = request.get_json()
        if not data:
            raise ValueError("Dados não fornecidos")
        if 'id' in data:
            raise ValueError("O ID não deve ser fornecido manualmente")

        aluno = AlunoService.criar_aluno(session, data)
        turma = session.query(Turma).get(data['turma_id'])

        return {
            "mensagem": "Aluno criado com sucesso",
            "aluno": aluno,
            "turma": turma.to_dict() if turma else None
        }, 201

    @staticmethod
    @handle_db_errors
    def buscar_por_id(session, id_aluno):
        aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
        turma = session.query(Turma).get(aluno['turma_id'])
        aluno['turma'] = turma.to_dict() if turma else None
        return aluno, 200

    @staticmethod
    @handle_db_errors
    def atualizar(session, id_aluno):
        data = request.get_json()
        if not data:
            raise ValueError("Dados não fornecidos")

        aluno = AlunoService.atualizar_aluno(session, id_aluno, data)
        turma = session.query(Turma).get(aluno['turma_id'])

        return {
            "mensagem": "Aluno atualizado com sucesso",
            "aluno": aluno,
            "turma": turma.to_dict() if turma else None
        }, 200

    @staticmethod
    @handle_db_errors
    def excluir(session, id_aluno):
        aluno = AlunoService.excluir_aluno(session, id_aluno)
        return {
            "mensagem": "Aluno removido com sucesso",
            "aluno_removido": aluno
        }, 200