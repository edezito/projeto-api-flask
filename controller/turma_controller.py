from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from service.turma_service import TurmaService
from functools import wraps

class TurmaController:
    def __init__(self, turma_service: TurmaService = None):
        self.turma_service = turma_service or TurmaService()

    @staticmethod
    def _handle_response(success, message, data=None, status_code=200):
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return response, status_code  # Agora usando o status_code

    def _turma_response(self, turma, mensagem, status_code=200):
        return self._handle_response(
            True,
            mensagem,
            turma.to_dict(),
            status_code
        )

    @staticmethod
    def handle_db_errors(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                if hasattr(self.turma_service, 'session'):
                    self.turma_service.session.commit()
                return result
            except ValueError as e:
                self._rollback()
                return TurmaController._handle_response(False, str(e), None, 400)
            except NoResultFound:
                self._rollback()
                return TurmaController._handle_response(False, "Registro não encontrado.", None, 404)
            except SQLAlchemyError as e:
                self._rollback()
                return TurmaController._handle_response(False, "Erro ao acessar o banco de dados.", str(e), 500)
            except Exception as e:
                self._rollback()
                return TurmaController._handle_response(False, "Erro inesperado.", str(e), 500)
        return wrapper

    def _rollback(self):
        if hasattr(self.turma_service, 'session'):
            self.turma_service.session.rollback()

    @handle_db_errors
    def listar_turmas(self):
        filtros = {
            'ativo': request.args.get('ativo', type=bool),
            'professor_id': request.args.get('professor_id', type=int)
        }
        filtros = {k: v for k, v in filtros.items() if v is not None}

        turmas, total = self.turma_service.listar_turmas(filtros)
        return self._handle_response(
            True,
            "Lista de turmas recuperada com sucesso.",
            {
                'turmas': [turma.to_dict() for turma in turmas],
                'total': total
            }
        )

    @handle_db_errors
    def criar_turma(self):
        dados = request.get_json()
        if not dados:
            return self._handle_response(False, "Nenhum dado fornecido.", None, 400)

        campos_obrigatorios = ['descricao', 'professor_id']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return self._handle_response(False, f"Campo obrigatório faltando: {campo}", None, 400)

        # Remove a necessidade de passar session, pois o service já gerencia isso
        turma = self.turma_service.criar_turma(dados)
        return self._turma_response(turma, "Turma criada com sucesso.", 201)

    # 🔸 Buscar turma por ID
    @handle_db_errors
    def buscar_turma_por_id(self, session, id_turma):
        turma = self.turma_service.buscar_turma_por_id(session, id_turma)
        return self._turma_response(turma, "Turma encontrada com sucesso.")

    @handle_db_errors
    def atualizar_turma(self, id_turma):
        """Atualiza uma turma existente"""
        dados = request.get_json()
        if not dados:
            return self._handle_response(False, "Dados inválidos para atualização.", None, 400)

        turma_atualizada = self.turma_service.atualizar_turma(id_turma, dados)
        return self._turma_response(turma_atualizada, "Turma atualizada com sucesso.")

    # 🔸 Excluir turma
    @handle_db_errors
    def excluir_turma(self, session, id_turma):
        self.turma_service.excluir_turma(session, id_turma)
        return '', 204  # Sem conteúdo, padrão para deleção bem-sucedida

    # 🔸 Atualizar status (ativo/inativo) da turma
    @handle_db_errors
    def atualizar_status_turma(self, session, id_turma):
        turma = self.turma_service.atualizar_status_turma(session, id_turma)
        return self._turma_response(turma, "Status da turma atualizado com sucesso.")