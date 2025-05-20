from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from service.turma_service import TurmaService
from config import BancoDados
from functools import wraps

class TurmaController:
    def __init__(self, turma_service: TurmaService = None):
        self.turma_service = turma_service or TurmaService()

    @staticmethod
    def _handle_response(success, message, data=None, status_code=200):
        """Método auxiliar para formatar respostas consistentes"""
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return jsonify(response), status_code

    def _turma_response(self, turma, mensagem, status_code=200):
        """Formata a resposta com uma turma"""
        return self._handle_response(True, mensagem, turma.to_dict(), status_code)

    @staticmethod
    def handle_db_errors(func):
        """Decorator para tratamento centralizado de erros de banco de dados"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            session = BancoDados.get_session()
            try:
                result = func(self, session, *args, **kwargs)
                session.commit()
                return result
            except ValueError as e:
                session.rollback()
                return TurmaController._handle_response(False, str(e), None, 400)
            except NoResultFound:
                session.rollback()
                return TurmaController._handle_response(False, "Registro não encontrado.", None, 404)
            except SQLAlchemyError as e:
                session.rollback()
                return TurmaController._handle_response(False, "Erro ao acessar o banco de dados.", None, 500)
            except Exception as e:
                session.rollback()
                return TurmaController._handle_response(False, "Erro inesperado ao processar a solicitação.", None, 500)
            finally:
                session.close()
        return wrapper

    @handle_db_errors
    def listar_turmas(self, session):
        """Lista todas as turmas com suporte a filtros"""
        filtros = {
            'ativo': request.args.get('ativo', type=lambda x: x.lower() == 'true'),
            'professor_id': request.args.get('professor_id', type=int)
        }
        filtros = {k: v for k, v in filtros.items() if v is not None}

        turmas, total = self.turma_service.listar_turmas(session, filtros)
        return self._handle_response(
            True,
            "Lista de turmas recuperada com sucesso",
            {
                'turmas': [turma.to_dict() for turma in turmas],
                'total': total
            }
        )

    @handle_db_errors
    def criar_turma(self, session):
        """Cria uma nova turma"""
        try:
            dados = request.get_json()
            if not dados:
                return {"success": False, "message": "Nenhum dado fornecido"}, 400
                
            campos_obrigatorios = ['descricao', 'professor_id']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    return {
                        "success": False,
                        "message": f"Campo obrigatório faltando: {campo}"
                    }, 400

            turma = self.turma_service.criar_turma(session, dados)
            return {
                "success": True,
                "message": "Turma criada com sucesso",
                "data": turma.to_dict()
            }, 201
            
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception as e:
            return {
                "success": False,
                "message": "Erro interno ao criar turma",
                "error": str(e)
            }, 500

    @handle_db_errors
    def buscar_turma_por_id(self, session, id_turma):
        turma = self.turma_service.buscar_turma_por_id(session, id_turma)
        return self._turma_response(turma, "Turma encontrada com sucesso")

    @handle_db_errors
    def atualizar_turma(self, session, id_turma):
        dados = request.get_json()
        if not dados:
            return self._handle_response(False, "Dados inválidos para atualização da turma.", None, 400)

        turma_atualizada = self.turma_service.atualizar_turma(session, id_turma, dados)
        return self._turma_response(turma_atualizada, "Turma atualizada com sucesso")

    @handle_db_errors
    def excluir_turma(self, session, id_turma):
        """Remove uma turma do sistema"""
        turma = self.turma_service.excluir_turma(session, id_turma)
        return self._handle_response(
            True,
            "Turma removida com sucesso",
            {'id': turma.id}
        )
