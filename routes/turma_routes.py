from functools import wraps
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from autenticacao import login_requerido
from model.turma_model import TurmaService, TurmaNaoEncontrada

# Create the Namespace for turmas
turmas_ns = Namespace('turmas', description='Operações de gerenciamento de turmas')

# Data models for Swagger documentation
turma_model = turmas_ns.model('Turma', {
    'id': fields.Integer(readOnly=True, description='ID único da turma'),
    'descricao': fields.String(required=True, description='Nome da turma'),
    'professor_id': fields.Integer(required=True, description='ID do professor'),
    'ativo': fields.Boolean(required=True, description='Turma está ativa ou inativa')
})

success_response = turmas_ns.model('SuccessResponse', {
    'message': fields.String(description='Mensagem de sucesso'),    
    'data': fields.Raw(description='Dados retornados')  
})

error_response = turmas_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

# Error handling decorator
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TurmaNaoEncontrada:
            return {'error': 'Turma não encontrada'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Erro interno: {str(e)}'}, 500
    return wrapper

@turmas_ns.route('/')
class ListaTurmas(Resource):
    @turmas_ns.doc(security='Bearer Auth')
    @turmas_ns.marshal_list_with(turma_model)
    @turmas_ns.response(404, 'Nenhuma turma encontrada', error_response)
    @turmas_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def get(self):
        '''Lista todas as turmas cadastradas'''
        turmas = TurmaService.listar_turmas()
        if not turmas:
            turmas_ns.abort(404, 'Nenhuma turma encontrada')
        return turmas, 200

    @turmas_ns.doc(security='Bearer Auth')
    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_model, code=201)
    @turmas_ns.response(400, 'Dados inválidos', error_response)
    @turmas_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def post(self):
        '''Cria uma nova turma'''
        data = request.get_json()
        if not data:
            turmas_ns.abort(400, 'Dados não fornecidos')
        
        turma = TurmaService.criar_turma(data)
        return turma, 201

@turmas_ns.route('/<int:id_turma>')
@turmas_ns.param('id_turma', 'ID da turma')
class TurmaResource(Resource):
    @turmas_ns.doc(security='Bearer Auth')
    @turmas_ns.marshal_with(turma_model)
    @turmas_ns.response(404, 'Turma não encontrada', error_response)
    @turmas_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def get(self, id_turma):
        '''Obtém detalhes de uma turma específica'''
        turma = TurmaService.turma_por_id(id_turma)
        return turma, 200

    @turmas_ns.doc(security='Bearer Auth')
    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_model)
    @turmas_ns.response(400, 'Dados inválidos', error_response)
    @turmas_ns.response(404, 'Turma não encontrada', error_response)
    @turmas_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def put(self, id_turma):
        '''Atualiza os dados de uma turma'''
        data = request.get_json()
        if not data:
            turmas_ns.abort(400, 'Dados não fornecidos')
        
        turma = TurmaService.atualizar_turma(id_turma, data)
        return turma, 200

    @turmas_ns.doc(security='Bearer Auth')
    @turmas_ns.response(200, 'Turma removida', success_response)
    @turmas_ns.response(404, 'Turma não encontrada', error_response)
    @turmas_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def delete(self, id_turma):
        '''Remove uma turma do sistema'''
        TurmaService.excluir_turma(id_turma)
        return {'message': 'Turma removida com sucesso'}, 200