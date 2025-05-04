from flask import request, jsonify
from http import HTTPStatus
from flask_restx import abort
from model.turma_model import TurmaNaoEncontrada
from service.turma_service import TurmaService

class TurmaController:
    @staticmethod
    def listar_turmas():
        try:
            filtros = {
                'ativo': request.args.get('ativo', type=lambda v: v.lower() == 'true'),
                'professor_id': request.args.get('professor_id', type=int)
            }
            filtros = {k: v for k, v in filtros.items() if v is not None}
            
            turmas = TurmaService.listar_turmas(filtros)
            return [turma.to_dict() for turma in turmas], HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def criar_turma():
        data = request.get_json()
        if not data:
            return {'message': "Dados não fornecidos"}, HTTPStatus.BAD_REQUEST
        
        if 'id' in data:
            return {'message': "O ID não deve ser fornecido manualmente"}, HTTPStatus.BAD_REQUEST
        
        try:
            turma = TurmaService.criar_turma(data)
            return turma.to_dict(), HTTPStatus.CREATED
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def buscar_por_id_turma(id_turma):
        try:
            turma = TurmaService.buscar_turma_por_id(id_turma)
            return turma.to_dict(), HTTPStatus.OK
        except TurmaNaoEncontrada as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def atualizar_turma(id_turma):
        data = request.get_json()
        if not data:
            return {'message': "Dados não fornecidos"}, HTTPStatus.BAD_REQUEST
        
        try:
            turma = TurmaService.atualizar_turma(id_turma, data)
            return turma.to_dict(), HTTPStatus.OK
        except TurmaNaoEncontrada as e:
            return {'message': str(e)}, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def desativar_turma(id_turma):
        try:
            turma = TurmaService.desativar_turma(id_turma)
            return {
                'mensagem': 'Turma desativada com sucesso',
                'turma_id': turma.id
            }, HTTPStatus.OK
        except TurmaNaoEncontrada:
            abort(HTTPStatus.NOT_FOUND, message=f"Turma com ID {id_turma} não encontrada")
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Erro ao desativar turma: {str(e)}")

    @staticmethod
    def excluir_turma(id_turma):
        try:
            TurmaService.excluir_turma(id_turma)
            return {
                'mensagem': 'Turma excluída permanentemente',
                'turma_id': id_turma
            }, HTTPStatus.OK
        except TurmaNaoEncontrada:
            abort(HTTPStatus.NOT_FOUND, message=f"Turma com ID {id_turma} não encontrada")
        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Erro ao excluir turma: {str(e)}")
