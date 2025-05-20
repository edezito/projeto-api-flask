from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from model import aluno_model, professor_model, turma_model
from config import BancoDados
from functools import wraps

class SistemaController:

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
        def wrapper(*args, **kwargs):
            session = BancoDados.get_session()
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except ValueError as e:
                session.rollback()
                return SistemaController._handle_response(False, str(e), None, 400)
            except NoResultFound as e:
                session.rollback()
                return SistemaController._handle_response(False, str(e), None, 404)
            except SQLAlchemyError as e:
                session.rollback()
                return SistemaController._handle_response(False, f"Erro no banco de dados: {str(e)}", None, 500)
            except Exception as e:
                session.rollback()
                return SistemaController._handle_response(False, f"Erro inesperado: {str(e)}", None, 500)
            finally:
                session.close()
        return wrapper

    @handle_db_errors
    def resetar_dados(self, session):
        session.query(aluno_model.Aluno).delete()
        session.query(turma_model.Turma).delete()
        session.query(professor_model.Professor).delete()
        return self._handle_response(True, "Dados resetados com sucesso.")
