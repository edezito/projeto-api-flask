from functools import wraps
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm.exc import NoResultFound
from config import BancoDados
from model.aluno_model import AlunoService
from model.turma_model import Turma
from autenticacao import login_requerido

# Criando o Namespace para alunos
alunos_namespace = Namespace('alunos', description='Operações de gerenciamento de alunos')

# Modelo de dados para documentação Swagger
aluno_model = alunos_namespace.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID único do aluno'),
    'nome': fields.String(required=True, description='Nome completo do aluno'),
    'email': fields.String(required=True, description='Email do aluno'),
    'turma_id': fields.Integer(required=True, description='ID da turma do aluno')
})

# Modelo para resposta de sucesso
success_model = alunos_namespace.model('SuccessResponse', {
    'mensagem': fields.String(description='Mensagem de sucesso'),
    'aluno': fields.Nested(aluno_model),
    'turma': fields.Raw(description='Dados da turma do aluno')
})

# Função para tratamento de erros
def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = BancoDados.Session()
        try:
            return func(session, *args, **kwargs)
        except ValueError as e:
            return {'erro': str(e)}, 400
        except NoResultFound:
            return {'erro': 'Registro não encontrado'}, 404
        except Exception as e:
            session.rollback()
            return {'erro': str(e)}, 500
        finally:
            session.close()
    return wrapper

@alunos_namespace.route('/')
class ListaAlunos(Resource):
    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.marshal_list_with(aluno_model)
    @login_requerido
    @handle_db_errors
    def get(self, session):
        '''Lista todos os alunos cadastrados'''
        return AlunoService.listar_alunos(session), 200

    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.expect(aluno_model)
    @alunos_namespace.marshal_with(success_model, code=201)
    @login_requerido
    @handle_db_errors
    def post(self, session):
        '''Cria um novo aluno'''
        data = request.get_json()
        if not data:
            raise ValueError("Dados não fornecidos")
        
        if 'id' in data:
            raise ValueError("O ID não deve ser fornecido manualmente")

        aluno = AlunoService.criar_aluno(session, data)
        turma = session.query(Turma).get(data['turma_id'])
        
        return {
            "mensagem": "Aluno criado com sucesso",
            "aluno": aluno,
            "turma": turma.to_dict() if turma else None
        }, 201

@alunos_namespace.route('/<int:id_aluno>')
@alunos_namespace.param('id_aluno', 'ID do aluno')
class AlunoResource(Resource):
    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.marshal_with(aluno_model)
    @login_requerido
    @handle_db_errors
    def get(self, session, id_aluno):
        '''Obtém detalhes de um aluno específico'''
        aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
        turma = session.query(Turma).get(aluno['turma_id'])
        aluno['turma'] = turma.to_dict() if turma else None
        return aluno, 200

    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.expect(aluno_model)
    @alunos_namespace.marshal_with(success_model)
    @login_requerido
    @handle_db_errors
    def put(self, session, id_aluno):
        '''Atualiza os dados de um aluno'''
        data = request.get_json()
        if not data:
            raise ValueError("Dados não fornecidos")

        aluno = AlunoService.atualizar_aluno(session, id_aluno, data)
        turma = session.query(Turma).get(aluno['turma_id'])
        
        return {
            "mensagem": "Aluno atualizado com sucesso",
            "aluno": aluno,
            "turma": turma.to_dict() if turma else None
        }, 200

    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.response(200, 'Aluno removido com sucesso')
    @login_requerido
    @handle_db_errors
    def delete(self, session, id_aluno):
        '''Remove um aluno do sistema'''
        aluno = AlunoService.excluir_aluno(session, id_aluno)
        return {
            "mensagem": "Aluno removido com sucesso",
            "aluno_removido": aluno
        }, 200