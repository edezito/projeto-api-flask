from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from service.professor_service import ProfessorService
from config import BancoDados
from functools import wraps

class ProfessorController:
    def __init__(self, professor_service: ProfessorService = None):
        self.professor_service = professor_service or ProfessorService()

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
            session = BancoDados.get_session()
            try:
                result = func(self, session, *args, **kwargs)
                session.commit()
                return result
            except ValueError as e:
                session.rollback()
                return ProfessorController._handle_response(False, str(e), None, 400)
            except NoResultFound as e:
                session.rollback()
                return ProfessorController._handle_response(False, str(e), None, 404)
            except SQLAlchemyError as e:
                session.rollback()
                return ProfessorController._handle_response(False, f"Erro no banco de dados: {str(e)}", None, 500)
            except Exception as e:
                session.rollback()
                return ProfessorController._handle_response(False, f"Erro inesperado: {str(e)}", None, 500)
            finally:
                session.close()
        return wrapper

    @handle_db_errors
    def listar(self, session):
        filters = {
            'page': request.args.get('page', 1, type=int),
            'per_page': request.args.get('per_page', 20, type=int),
            'order_by': request.args.get('order_by', 'nome')
        }
        professores, total = self.professor_service.listar_professores(session, **filters)
        return self._handle_response(
            True,
            "Lista de professores recuperada com sucesso",
            {
                'professores': [prof.to_dict() for prof in professores],
                'total': total
            }
        )

    @handle_db_errors
    def criar(self, session):
        dados = request.get_json()

        # Validação simples
        campos_obrigatorios = ['nome', 'idade', 'materia']
        if not all(campo in dados and dados[campo] for campo in campos_obrigatorios):
            return self._handle_response(False, "Campos obrigatórios faltando: nome, idade, materia", None, 400)

        professor = self.professor_service.criar_professor(session, dados)
        return self._handle_response(
            True,
            "Professor criado com sucesso",
            {'professor': professor.to_dict()},
            201
        )

    @handle_db_errors
    def buscar_por_id(self, session, id_professor):
        professor = self.professor_service.buscar_professor_por_id(session, id_professor)
        return self._handle_response(
            True,
            "Professor encontrado com sucesso",
            {'professor': professor.to_dict()}
        )

    @handle_db_errors
    def atualizar(self, session, id_professor):
        dados = request.get_json()
        if not dados:
            return self._handle_response(False, "Dados para atualização não fornecidos", None, 400)

        professor = self.professor_service.atualizar_professor(session, id_professor, dados)
        return self._handle_response(
            True,
            "Professor atualizado com sucesso",
            {'professor': professor.to_dict()}
        )

    @handle_db_errors
    def excluir(self, session, id_professor):
        professor = self.professor_service.excluir_professor(session, id_professor)
        return self._handle_response(
            True,
            "Professor removido com sucesso",
            {'id': professor.id}
        )