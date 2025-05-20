from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from service.turma_service import TurmaService
from config import BancoDados
from functools import wraps

class TurmaController:
    def __init__(self, turma_service: TurmaService):
        self.turma_service = turma_service

    @staticmethod
    def _handle_response(success, message, data=None, status_code=200):
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return jsonify(response), status_code

    @staticmethod
    def handle_db_errors(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            session = BancoDados.SessionLocal()
            try:
                result = func(self, session, *args, **kwargs)
                session.commit()
                return result
            except ValueError as e:
                session.rollback()
                return TurmaController._handle_response(False, str(e), None, 400)
            except NoResultFound as e:
                session.rollback()
                return TurmaController._handle_response(False, str(e), None, 404)
            except SQLAlchemyError as e:
                session.rollback()
                return TurmaController._handle_response(False, f"Erro no banco de dados: {str(e)}", None, 500)
            except Exception as e:
                session.rollback()
                return TurmaController._handle_response(False, f"Erro inesperado: {str(e)}", None, 500)
            finally:
                session.close()
        return wrapper

    @handle_db_errors
    def listar_turmas(self, session):
        turmas, total = self.turma_service.listar_turmas(session)
        turmas_dict = [turma.to_dict() for turma in turmas]

        return self._handle_response(
            True,
            "Lista de turmas recuperada com sucesso",
            {
                'turmas': turmas_dict,
                'total': total
            }
        )

    @handle_db_errors
    def criar_turma(self, session):
        dados = request.get_json()
        turma = self.turma_service.criar_turma(session, dados)
        return self._handle_response(
            True,
            "Turma criada com sucesso",
            turma.to_dict(),
            201
        )

    @handle_db_errors
    def buscar_turma_por_id(self, session, id_turma):
        turma = self.turma_service.buscar_turma_por_id(session, id_turma)
        return self._handle_response(
            True,
            "Turma encontrada com sucesso",
            turma.to_dict()
        )

    @handle_db_errors
    def atualizar_turma(self, session, id_turma):
        dados = request.get_json()
        turma_atualizada = self.turma_service.atualizar_turma(session, id_turma, dados)
        return self._handle_response(
            True,
            "Turma atualizada com sucesso",
            turma_atualizada.to_dict()
        )

    @handle_db_errors
    def excluir_turma(self, session, id_turma):
        turma = self.turma_service.excluir_turma(session, id_turma)
        return self._handle_response(
            True,
            "Turma removida com sucesso",
            {'id': turma.id}
        )