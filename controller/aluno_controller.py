from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from service.aluno_service import AlunoService
from model.turma_model import Turma
from config import BancoDados
from functools import wraps

class AlunoController:
    
    @staticmethod
    def _handle_response(success, message, data=None, status_code=200):
        """Padroniza todas as respostas da API"""
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return response, status_code

    @staticmethod
    def _get_turma_info(session, turma_id):
        """Obtém informações da turma de forma segura"""
        if not turma_id:
            return None
        turma = session.query(Turma).get(turma_id)
        return turma.to_dict() if turma else None

    @staticmethod
    def _validate_aluno_data(data, is_update=False):
        """Validação centralizada dos dados do aluno"""
        if not data:
            raise ValueError("Dados não fornecidos")
        
        required_fields = ['nome', 'matricula', 'turma_id']
        if not is_update:
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Campo obrigatório faltando: {field}")
        
        if 'id' in data:
            raise ValueError("O ID não deve ser fornecido manualmente")

    @staticmethod
    def handle_db_errors(func):
        """Decorator para tratamento centralizado de erros"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = BancoDados.Session()
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except ValueError as e:
                session.rollback()
                return AlunoController._handle_response(False, str(e), None, 400)
            except NoResultFound:
                session.rollback()
                return AlunoController._handle_response(False, "Registro não encontrado", None, 404)
            except SQLAlchemyError as e:
                session.rollback()
                return AlunoController._handle_response(False, f"Erro no banco de dados: {str(e)}", None, 500)
            except Exception as e:
                session.rollback()
                return AlunoController._handle_response(False, f"Erro inesperado: {str(e)}", None, 500)
            finally:
                session.close()
        return wrapper

    @staticmethod
    @handle_db_errors
    def listar(session, page=1, per_page=20, order_by='nome'):
        """Lista alunos com paginação"""
        alunos, total = AlunoService.listar_alunos(
            session, 
            page=page, 
            per_page=per_page, 
            order_by=order_by
        )
        
        return AlunoController._handle_response(
            True,
            "Lista de alunos recuperada com sucesso",
            {
                'alunos': alunos,
                'pagination': {
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'total_pages': (total + per_page - 1) // per_page
                }
            }
        )

    @staticmethod
    @handle_db_errors
    def criar(session):
        """Cria um novo aluno"""
        data = request.get_json()
        AlunoController._validate_aluno_data(data)
        
        aluno = AlunoService.criar_aluno(session, data)
        turma_info = AlunoController._get_turma_info(session, aluno['turma_id'])
        
        return AlunoController._handle_response(
            True,
            "Aluno criado com sucesso",
            {
                'aluno': aluno,
                'turma': turma_info
            },
            201
        )

    @staticmethod
    @handle_db_errors
    def buscar_por_id(session, id_aluno):
        """Busca um aluno por ID"""
        aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
        turma_info = AlunoController._get_turma_info(session, aluno['turma_id'])
        
        aluno['turma'] = turma_info
        return AlunoController._handle_response(
            True,
            "Aluno encontrado com sucesso",
            aluno
        )

    @staticmethod
    @handle_db_errors
    def atualizar(session, id_aluno):
        """Atualiza um aluno existente"""
        data = request.get_json()
        AlunoController._validate_aluno_data(data, is_update=True)
        
        aluno = AlunoService.atualizar_aluno(session, id_aluno, data)
        turma_info = AlunoController._get_turma_info(session, aluno['turma_id'])
        
        return AlunoController._handle_response(
            True,
            "Aluno atualizado com sucesso",
            {
                'aluno': aluno,
                'turma': turma_info
            }
        )

    @staticmethod
    @handle_db_errors
    def excluir(session, id_aluno):
        """Remove um aluno"""
        aluno = AlunoService.excluir_aluno(session, id_aluno)
        return AlunoController._handle_response(
            True,
            "Aluno removido com sucesso",
            {'id': aluno['id']}
        )