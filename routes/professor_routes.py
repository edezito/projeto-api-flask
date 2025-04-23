from functools import wraps
from flask import request
from flask_restx import Namespace, Resource, fields
from autenticacao import login_requerido
from model.professor_model import ProfessorService, ProfessorNaoEncontrado

# Criar o Namespace para professores
professores_ns = Namespace('professores', description='Operações de gerenciamento de professores')

# Modelo de dados do professor para documentação Swagger
professor_model = professores_ns.model('Professor', {
    'id': fields.Integer(readOnly=True, description='ID único do professor'),
    'nome': fields.String(required=True, description='Nome completo do professor'),
    'email': fields.String(required=True, description='Email do professor'),
    'disciplina': fields.String(required=True, description='Disciplina que o professor leciona')
})

# Modelo para respostas de sucesso
success_response = professores_ns.model('SuccessResponse', {
    'message': fields.String(description='Mensagem de sucesso'),
    'data': fields.Raw(description='Dados retornados')
})

# Modelo para respostas de erro
error_response = professores_ns.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro')
})

# Função para tratar erros
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProfessorNaoEncontrado:
            return {'error': 'Professor não encontrado'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Erro interno: {str(e)}'}, 500
    return wrapper

@professores_ns.route('/')
class ListaProfessores(Resource):
    @professores_ns.doc(security='Bearer Auth')
    @professores_ns.marshal_list_with(professor_model)
    @professores_ns.response(404, 'Nenhum professor encontrado', error_response)
    @professores_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def get(self):
        '''Lista todos os professores cadastrados'''
        professores = ProfessorService.listar_professores()
        if not professores:
            professores_ns.abort(404, 'Nenhum professor encontrado')
        return professores, 200

    @professores_ns.doc(security='Bearer Auth')
    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_model, code=201)
    @professores_ns.response(400, 'Dados inválidos', error_response)
    @professores_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def post(self):
        '''Cria um novo professor'''
        data = request.get_json()
        if not data:
            professores_ns.abort(400, 'Dados não fornecidos')
        
        professor = ProfessorService.criar_professor(data)
        return professor, 201

@professores_ns.route('/<int:id_professor>')
@professores_ns.param('id_professor', 'ID do professor')
class ProfessorResource(Resource):
    @professores_ns.doc(security='Bearer Auth')
    @professores_ns.marshal_with(professor_model)
    @professores_ns.response(404, 'Professor não encontrado', error_response)
    @professores_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def get(self, id_professor):
        '''Obtém detalhes de um professor específico'''
        professor = ProfessorService.professor_por_id(id_professor)
        return professor, 200

    @professores_ns.doc(security='Bearer Auth')
    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_model)
    @professores_ns.response(400, 'Dados inválidos', error_response)
    @professores_ns.response(404, 'Professor não encontrado', error_response)
    @professores_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def put(self, id_professor):
        '''Atualiza os dados de um professor'''
        data = request.get_json()
        if not data:
            professores_ns.abort(400, 'Dados não fornecidos')
        
        professor = ProfessorService.atualizar_professor(id_professor, data)
        return professor, 200

    @professores_ns.doc(security='Bearer Auth')
    @professores_ns.response(200, 'Professor removido', success_response)
    @professores_ns.response(404, 'Professor não encontrado', error_response)
    @professores_ns.response(500, 'Erro interno', error_response)
    @login_requerido
    @handle_errors
    def delete(self, id_professor):
        '''Remove um professor do sistema'''
        ProfessorService.excluir_professor(id_professor)
        return {'message': 'Professor removido com sucesso'}, 200