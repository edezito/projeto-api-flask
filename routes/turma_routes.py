from flask_restx import Resource, fields, inputs
from controller.turma_controller import TurmaController
from service.turma_service import TurmaService
from swagger.namespaces.turmas_namespaces import turmas_namespace

# Instanciando serviço e controller
turma_service = TurmaService()
turma_controller = TurmaController(turma_service)

# Modelos
professor_model = turmas_namespace.model('Professor', {
    'id': fields.Integer,
    'nome': fields.String
})

turma_model = turmas_namespace.model('Turma', {
    'id': fields.Integer(readOnly=True),
    'descricao': fields.String(required=True),
    'professor_id': fields.Integer(required=True),
    'ativo': fields.Boolean(default=True),
    'quantidade_alunos': fields.Integer(readonly=True),
    'professor': fields.Nested(professor_model)
})

turma_input_model = turmas_namespace.model('TurmaInput', {
    'descricao': fields.String(required=True, min_length=3, max_length=100),
    'professor_id': fields.Integer(required=True, min=1),
    'ativo': fields.Boolean(default=True)
})

success_model = turmas_namespace.model('SuccessResponse', {
    'success': fields.Boolean(default=True),
    'message': fields.String,
    'data': fields.Raw
})

error_model = turmas_namespace.model('ErrorResponse', {
    'success': fields.Boolean(default=False),
    'message': fields.String,
    'error': fields.String,
    'details': fields.String
})

# Filtros
filtros_model = turmas_namespace.parser()
filtros_model.add_argument('ativo', type=inputs.boolean, location='args')
filtros_model.add_argument('professor_id', type=int, location='args')

# ===== Rota principal =====
@turmas_namespace.route('/')
class ListaTurmas(Resource):
    @turmas_namespace.expect(filtros_model)
    @turmas_namespace.response(200, 'Sucesso', success_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def get(self):
        """Lista todas as turmas com filtros opcionais"""
        return turma_controller.listar_turmas()

    @turmas_namespace.expect(turma_input_model)
    @turmas_namespace.response(201, 'Turma criada', success_model)
    @turmas_namespace.response(400, 'Dados inválidos', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def post(self):
        """Cria uma nova turma"""
        return turma_controller.criar_turma()

# ===== Rota individual para turmas =====
@turmas_namespace.route('/<int:id_turma>')
@turmas_namespace.param('id_turma', 'ID da turma', _in='path', required=True)
class TurmaResource(Resource):
    @turmas_namespace.response(200, 'Sucesso', turma_model)
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def get(self, id_turma):
        """Obtém detalhes de uma turma específica"""
        return turma_controller.buscar_turma_por_id(id_turma)

    @turmas_namespace.expect(turma_input_model)
    @turmas_namespace.response(200, 'Turma atualizada', turma_model)
    @turmas_namespace.response(400, 'Dados inválidos', error_model)
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def put(self, id_turma):
        """Atualiza uma turma existente"""
        return turma_controller.atualizar_turma(id_turma)

    @turmas_namespace.response(204, 'Turma excluída')
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def delete(self, id_turma):
        """Exclui permanentemente uma turma"""
        return turma_controller.excluir_turma(id_turma)

# ===== Rota para status da turma =====
@turmas_namespace.route('/<int:id_turma>/status')
@turmas_namespace.param('id_turma', 'ID da turma', _in='path', required=True)
class StatusTurma(Resource):
    @turmas_namespace.response(200, 'Sucesso', success_model)
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def patch(self, id_turma):
        """Atualiza o status da turma (ativo/inativo)"""
        return turma_controller.atualizar_status_turma(id_turma)