from flask import request
from service.turma_service import TurmaService, TurmaNaoEncontrada
from flask_restx import abort
from http import HTTPStatus

class TurmaController:
    """Controller para operações relacionadas a turmas"""

    @staticmethod
    def listar_turmas():
        """
        Lista todas as turmas com possibilidade de filtros via query params
        
        Returns:
            tuple: (dict, int) Dados das turmas e status code
        """
        try:
            # Obter filtros da query string
            filtros = {
                'ativo': request.args.get('ativo', type=lambda v: v.lower() == 'true'),
                'professor_id': request.args.get('professor_id', type=int)
            }
            # Remove filtros não informados
            filtros = {k: v for k, v in filtros.items() if v is not None}
            
            turmas = TurmaService.listar_turmas(filtros)
            return [turma.to_dict() for turma in turmas], HTTPStatus.OK
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 
                 message=f"Erro ao listar turmas: {str(e)}")

    @staticmethod
    def criar_turma():
        """
        Cria uma nova turma
        
        Returns:
            tuple: (dict, int) Dados da turma criada e status code
        """
        try:
            data = request.get_json()
            if not data:
                abort(HTTPStatus.BAD_REQUEST, message="Dados não fornecidos")
            
            # Validações básicas do controller
            if 'id' in data:
                abort(HTTPStatus.BAD_REQUEST, 
                     message="O ID não deve ser fornecido manualmente")
            
            turma = TurmaService.criar_turma(data)
            return turma.to_dict(), HTTPStatus.CREATED
            
        except ValueError as ve:
            abort(HTTPStatus.BAD_REQUEST, message=str(ve))
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 
                 message=f"Erro ao criar turma: {str(e)}")

    @staticmethod
    def buscar_por_id_turma(id_turma):
        """
        Obtém uma turma específica pelo ID
        
        Args:
            id_turma (int): ID da turma
            
        Returns:
            tuple: (dict, int) Dados da turma e status code
        """
        try:
            turma = TurmaService.buscar_turma_por_id(id_turma)
            return turma.to_dict(), HTTPStatus.OK
        except TurmaNaoEncontrada:
            abort(HTTPStatus.NOT_FOUND, message=f"Turma com ID {id_turma} não encontrada")
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 
                 message=f"Erro ao buscar turma: {str(e)}")

    @staticmethod
    def atualizar_turma(id_turma):
        """
        Atualiza os dados de uma turma
        
        Args:
            id_turma (int): ID da turma a ser atualizada
            
        Returns:
            tuple: (dict, int) Dados atualizados e status code
        """
        try:
            data = request.get_json()
            if not data:
                abort(HTTPStatus.BAD_REQUEST, message="Dados não fornecidos")
            
            turma = TurmaService.atualizar_turma(id_turma, data)
            return turma.to_dict(), HTTPStatus.OK
            
        except TurmaNaoEncontrada:
            abort(HTTPStatus.NOT_FOUND, message=f"Turma com ID {id_turma} não encontrada")
        except ValueError as ve:
            abort(HTTPStatus.BAD_REQUEST, message=str(ve))
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 
                 message=f"Erro ao atualizar turma: {str(e)}")

    @staticmethod
    def desativar_turma(id_turma):
        """
        Desativa uma turma (exclusão lógica)
        
        Args:
            id_turma (int): ID da turma a desativar
            
        Returns:
            tuple: (dict, int) Mensagem de sucesso e status code
        """
        try:
            turma = TurmaService.desativar_turma(id_turma)
            return {
                'mensagem': 'Turma desativada com sucesso',
                'turma_id': turma.id
            }, HTTPStatus.OK
        except TurmaNaoEncontrada:
            abort(HTTPStatus.NOT_FOUND, message=f"Turma com ID {id_turma} não encontrada")
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 
                 message=f"Erro ao desativar turma: {str(e)}")

    @staticmethod
    def excluir_turma(id_turma):
        """
        Remove permanentemente uma turma (exclusão física)
        
        Args:
            id_turma (int): ID da turma a excluir
            
        Returns:
            tuple: (dict, int) Mensagem de sucesso e status code
        """
        try:
            TurmaService.excluir_turma(id_turma)
            return {
                'mensagem': 'Turma excluída permanentemente',
                'turma_id': id_turma
            }, HTTPStatus.OK
        except TurmaNaoEncontrada:
            abort(HTTPStatus.NOT_FOUND, message=f"Turma com ID {id_turma} não encontrada")
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 
                 message=f"Erro ao excluir turma: {str(e)}")