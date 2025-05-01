from flask_restx import Resource
from flask import request
from service.login_requerido import login_requerido
from controller.aluno_controller import AlunoController
from swagger.namespaces.alunos_namespace import alunos_namespace, aluno_model, success_model, pagination_params

@alunos_namespace.route('/')
class AlunoListResource(Resource):
    @alunos_namespace.doc(security='Bearer Auth', params=pagination_params)
    @alunos_namespace.marshal_list_with(aluno_model)
    @login_requerido
    def get(self):
        filters = {
            'page': request.args.get('page', 1, type=int),
            'per_page': request.args.get('per_page', 20, type=int),
            'order_by': request.args.get('order_by', 'nome')
        }
        return AlunoController.listar(**filters)

    @alunos_namespace.expect(aluno_model)
    @alunos_namespace.marshal_with(success_model, code=201)
    @login_requerido
    def post(self):
        return AlunoController.criar()

@alunos_namespace.route('/<int:aluno_id>')
@alunos_namespace.param('aluno_id', 'ID único do aluno')
class AlunoDetailResource(Resource):
    @alunos_namespace.marshal_with(aluno_model)
    @login_requerido
    def get(self, aluno_id):
        return AlunoController.buscar_por_id(aluno_id)

    @alunos_namespace.expect(aluno_model)
    @alunos_namespace.marshal_with(success_model)
    @login_requerido
    def put(self, aluno_id):
        return AlunoController.atualizar(aluno_id)

    @alunos_namespace.marshal_with(success_model)
    @login_requerido
    def delete(self, aluno_id):
        return AlunoController.excluir(aluno_id)