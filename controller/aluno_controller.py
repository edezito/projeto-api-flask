from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from service.aluno_service import AlunoService
from model.turma_model import Turma
from config import BancoDados
from functools import wraps

class AlunoController:
    def __init__(self, aluno_service: AlunoService):
        self.aluno_service = aluno_service

    @staticmethod
    def _handle_response(success, message, data=None, status_code=200):
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return jsonify(response), status_code

    @staticmethod
    def _get_turma_info(session, turma_id):
        if not turma_id:
            return None
        turma = session.query(Turma).get(turma_id)
        return turma.to_dict() if turma else None

    @staticmethod
    def handle_db_errors(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = BancoDados.SessionLocal()
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except ValueError as e:
                session.rollback()
                return AlunoController._handle_response(False, str(e), None, 400)
            except NoResultFound as e:
                session.rollback()
                return AlunoController._handle_response(False, str(e), None, 404)
            except SQLAlchemyError as e:
                session.rollback()
                return AlunoController._handle_response(False, f"Erro no banco de dados: {str(e)}", None, 500)
            except Exception as e:
                session.rollback()
                return AlunoController._handle_response(False, f"Erro inesperado: {str(e)}", None, 500)
            finally:
                session.close()
        return wrapper

    @handle_db_errors
    def listar(self, session, page=1, per_page=20, order_by='nome'):
        alunos, total = self.aluno_service.listar_alunos(
            session,
            page=page,
            per_page=per_page,
            order_by=order_by
        )

        alunos_dict = []
        for aluno in alunos:
            turma_info = self._get_turma_info(session, aluno.turma_id)
            aluno_dict = aluno.to_dict(include_turma=True)
            aluno_dict['turma'] = turma_info
            aluno_dict['media'] = self.aluno_service.calcular_media({
                'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
                'nota_segundo_semestre': aluno.nota_segundo_semestre
            })
            alunos_dict.append(aluno_dict)

        return self._handle_response(
            True,
            "Lista de alunos recuperada com sucesso",
            {
                'alunos': alunos_dict,
                'pagination': {
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'total_pages': (total + per_page - 1) // per_page
                }
            }
        )

    @handle_db_errors
    def criar(self, session):
        dados = request.get_json()
        aluno = self.aluno_service.criar_aluno(session, dados)
        turma_info = self._get_turma_info(session, aluno.turma_id)
        return self._handle_response(
            True,
            "Aluno criado com sucesso",
            {
                'aluno': aluno.to_dict(include_turma=True),
                'turma': turma_info
            },
            201
        )

    @handle_db_errors
    def buscar_por_id(self, session, id_aluno):
        aluno = self.aluno_service.buscar_aluno_por_id(session, id_aluno)
        turma_info = self._get_turma_info(session, aluno.turma_id)
        aluno_dict = aluno.to_dict(include_turma=True)
        aluno_dict['media'] = self.aluno_service.calcular_media({
            'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
            'nota_segundo_semestre': aluno.nota_segundo_semestre
        })
        aluno_dict['turma'] = turma_info
        return self._handle_response(
            True,
            "Aluno encontrado com sucesso",
            aluno_dict
        )

    @handle_db_errors
    def atualizar(self, session, id):
        dados = request.get_json()
        aluno_atualizado = self.aluno_service.atualizar_aluno(session, id, dados)
        return self._handle_response(
            True,
            "Aluno atualizado com sucesso",
            {'aluno': aluno_atualizado.to_dict()}
        )

    @handle_db_errors
    def excluir(self, session, id_aluno):
        aluno = self.aluno_service.excluir_aluno(session, id_aluno)
        return self._handle_response(
            True,
            "Aluno removido com sucesso",
            {'id': aluno.id}
        )