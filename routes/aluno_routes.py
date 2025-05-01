from flask_restx import Resource
from autenticacao import login_requerido
from swagger.namespaces.alunos_namespace import alunos_namespace, aluno_model, success_model
from controller.aluno_controller import AlunoController

@alunos_namespace.route('/')
class ListaAlunos(Resource):
    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.marshal_list_with(aluno_model)
    @login_requerido
    def get(self):
        return AlunoController.listar()

    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.expect(aluno_model)
    @alunos_namespace.marshal_with(success_model, code=201)
    @login_requerido
    def post(self):
        return AlunoController.criar()

@alunos_namespace.route('/<int:id_aluno>')
@alunos_namespace.param('id_aluno', 'ID do aluno')
class AlunoResource(Resource):
    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.marshal_with(aluno_model)
    @login_requerido
    def get(self, id_aluno):
        return AlunoController.buscar_por_id(id_aluno)

    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.expect(aluno_model)
    @alunos_namespace.marshal_with(success_model)
    @login_requerido
    def put(self, id_aluno):
        return AlunoController.atualizar(id_aluno)

    @alunos_namespace.doc(security='Bearer Auth')
    @alunos_namespace.response(200, 'Aluno removido com sucesso')
    @login_requerido
    def delete(self, id_aluno):
        return AlunoController.excluir(id_aluno)