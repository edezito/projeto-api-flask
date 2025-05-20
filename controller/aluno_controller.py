from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from model.aluno_model import Aluno
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

        alunos_dict = [aluno.to_dict(include_turma=True) for aluno in alunos]
        
        pagination = {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page if total > 0 else 0
        }

        return self._handle_response(
            True,
            "Lista de alunos recuperada com sucesso",
            {
                'alunos': alunos_dict,
                'pagination': pagination
            }
        )


    @handle_db_errors
    def criar(self, session):
        dados = request.get_json()
        
        # Cria o aluno e obtém o objeto Aluno (não o dicionário ainda)
        aluno = self.aluno_service.criar_aluno(session, dados)
        
        # Converte para dicionário incluindo as informações da turma
        aluno_dict = aluno.to_dict(include_turma=True)
        
        # Calcula a média se necessário
        aluno_dict['media'] = self.aluno_service.calcular_media({
            'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
            'nota_segundo_semestre': aluno.nota_segundo_semestre
        })
        
        return self._handle_response(
            True,
            "Aluno criado com sucesso",
            aluno_dict,
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
        
        # Busca o aluno
        aluno = self.aluno_service.buscar_aluno_por_id(session, id)
        
        # Atualiza os dados (passando apenas dados e aluno)
        aluno_atualizado = self.aluno_service.atualizar_aluno(dados, aluno)
        
        # Confirma as alterações
        session.commit()
        
        return self._handle_response(
            True,
            "Aluno atualizado com sucesso",
            {
                "id": aluno_atualizado.id,
                "nome": aluno_atualizado.nome,
                "idade": aluno_atualizado.idade,
                "media": aluno_atualizado.media
            }
        )

    @handle_db_errors   
    def excluir(self, session, id_aluno):
        aluno = self.aluno_service.excluir_aluno(session, id_aluno)
        return self._handle_response(
            True,
            "Aluno removido com sucesso",
            aluno  # Já é um dicionário
        )