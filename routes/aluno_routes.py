from flask_restx import Resource
from flask import request
from config import BancoDados
from service.aluno_service import AlunoService
from service.login_requerido import login_requerido
from swagger.namespaces.alunos_namespace import alunos_namespace, aluno_model

@alunos_namespace.route('/')
class AlunoListResource(Resource):
    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.marshal_list_with(aluno_model)
    @login_requerido
    def get(self):
        """Lista todos os alunos"""
        filters = {
            'page': request.args.get('page', 1, type=int),
            'per_page': request.args.get('per_page', 20, type=int),
            'order_by': request.args.get('order_by', 'nome')
        }
        with BancoDados.SessionLocal() as session:
            return AlunoService.listar_alunos(session, **filters)

    @alunos_namespace.expect(aluno_model, validate=True)
    @alunos_namespace.marshal_with(aluno_model, code=201)
    @login_requerido
    def post(self):
        """Cria um novo aluno"""
        dados = request.json
        with BancoDados.SessionLocal() as session:
            return AlunoService.criar_aluno(session, dados), 201

@alunos_namespace.route('/<int:id>')
@alunos_namespace.param('id', 'ID do aluno')
class AlunoResource(Resource):
    @alunos_namespace.marshal_with(aluno_model)
    @login_requerido
    def get(self, id):
        """Busca um aluno pelo ID"""
        with BancoDados.SessionLocal() as session:
            return AlunoService.buscar_aluno_por_id(session, id)

    @alunos_namespace.expect(aluno_model, validate=True)
    @alunos_namespace.marshal_with(aluno_model)
    @login_requerido
    def put(self, id):
        """Atualiza um aluno existente"""
        dados = request.json
        with BancoDados.SessionLocal() as session:
            return AlunoService.atualizar_aluno(session, id, dados)

    @login_requerido
    def delete(self, id):
        """Exclui um aluno pelo ID"""
        with BancoDados.SessionLocal() as session:
            AlunoService.excluir_aluno(session, id)
            return {'mensagem': 'Aluno excluído com sucesso'}, 200