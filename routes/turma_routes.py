from flask_restx import Resource, fields
from controller.turma_controller import TurmaController
from service.turma_service import TurmaService
from swagger.namespaces.turmas_namespaces import turmas_namespace

# Instanciando serviço e controller
turma_service = TurmaService()
turma_controller = TurmaController(turma_service)

# Modelos atualizados
turma_model = turmas_namespace.model('Turma', {
    'id': fields.Integer(readOnly=True, description='ID único da turma'),
    'descricao': fields.String(required=True, description='Nome/descrição da turma'),
    'professor_id': fields.Integer(required=True, description='ID do professor responsável'),
    'ativo': fields.Boolean(default=True, description='Status da turma (ativo/inativo)'),
    'quantidade_alunos': fields.Integer(description='Número de alunos na turma'),
    'professor': fields.Nested(turmas_namespace.model('Professor', {
        'id': fields.Integer,
        'nome': fields.String
    }), description='Professor responsável')
})

turma_input_model = turmas_namespace.model('TurmaInput', {
    'descricao': fields.String(required=True, description='Nome/descrição da turma'),
    'professor_id': fields.Integer(required=True, description='ID do professor responsável'),
    'ativo': fields.Boolean(default=True, description='Status da turma')
})

success_model = turmas_namespace.model('SuccessResponse', {
    'mensagem': fields.String(description='Mensagem de sucesso'),
    'turma_id': fields.Integer(description='ID da turma afetada')
})

error_model = turmas_namespace.model('ErrorResponse', {
    'erro': fields.String(description='Mensagem de erro'),
    'detalhes': fields.String(description='Detalhes do erro')
})

# Filtros de consulta
filtros_model = turmas_namespace.parser()
filtros_model.add_argument('ativo', type=bool, required=False, help='Filtrar por status ativo/inativo')
filtros_model.add_argument('professor_id', type=int, required=False, help='Filtrar por ID do professor')

@turmas_namespace.route('/')
class ListaTurmas(Resource):
    @turmas_namespace.expect(filtros_model)
    @turmas_namespace.marshal_list_with(turma_model)
    @turmas_namespace.response(200, 'Lista de turmas obtida com sucesso')
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def get(self):
        return turma_controller.listar_turmas()

    @turmas_namespace.expect(turma_input_model)
    @turmas_namespace.marshal_with(turma_model, code=201)
    @turmas_namespace.response(201, 'Turma criada com sucesso')
    @turmas_namespace.response(400, 'Dados inválidos', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def post(self):
        return turma_controller.criar_turma()

@turmas_namespace.route('/<int:id_turma>')
@turmas_namespace.param('id_turma', 'ID da turma')
class TurmaResource(Resource):
    @turmas_namespace.marshal_with(turma_model)
    @turmas_namespace.response(200, 'Turma encontrada')
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def get(self, id_turma):
        return turma_controller.buscar_turma_por_id(id_turma)

    @turmas_namespace.expect(turma_input_model)
    @turmas_namespace.marshal_with(turma_model)
    @turmas_namespace.response(200, 'Turma atualizada com sucesso')
    @turmas_namespace.response(400, 'Dados inválidos', error_model)
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def put(self, id_turma):
        return turma_controller.atualizar_turma(id_turma)

@turmas_namespace.route('/<int:id_turma>/desativar')
@turmas_namespace.param('id_turma', 'ID da turma a ser desativada')
class DesativarTurma(Resource):
    @turmas_namespace.marshal_with(success_model)
    @turmas_namespace.response(200, 'Turma desativada com sucesso')
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def patch(self, id_turma):
        return turma_controller.desativar_turma(id_turma)

@turmas_namespace.route('/<int:id_turma>/excluir')
@turmas_namespace.param('id_turma', 'ID da turma a ser excluída permanentemente')
class ExcluirTurma(Resource):
    @turmas_namespace.marshal_with(success_model)
    @turmas_namespace.response(200, 'Turma excluída permanentemente')
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def delete(self, id_turma):
        return turma_controller.excluir_turma(id_turma)
