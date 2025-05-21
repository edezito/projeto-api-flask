from flask_restx import Resource, fields, inputs
from controller.turma_controller import TurmaController
from service.turma_service import TurmaService
from swagger.namespaces.turmas_namespaces import turmas_namespace

# Instanciando serviço e controller
turma_service = TurmaService()
turma_controller = TurmaController(turma_service)

# Modelo de Professor para aninhamento
professor_model = turmas_namespace.model('Professor', {
    'id': fields.Integer,
    'nome': fields.String
})

# Modelo completo de Turma para resposta
turma_model = turmas_namespace.model('Turma', {
    'id': fields.Integer(readOnly=True, description='ID único da turma'),
    'descricao': fields.String(required=True, description='Nome/descrição da turma'),
    'professor_id': fields.Integer(required=True, description='ID do professor responsável'),
    'ativo': fields.Boolean(default=True, description='Status da turma (ativo/inativo)'),
    'quantidade_alunos': fields.Integer(
        readonly=True,
        description='Número de alunos na turma (calculado automaticamente)'
    ),
    'professor': fields.Nested(professor_model, description='Professor responsável')
})

# Modelo para criação/atualização (sem campos calculados)
turma_input_model = turmas_namespace.model('TurmaInput', {
    'descricao': fields.String(
        required=True,
        description='Nome/descrição da turma',
        min_length=3,
        max_length=100
    ),
    'professor_id': fields.Integer(
        required=True,
        description='ID do professor responsável',
        min=1
    ),
    'ativo': fields.Boolean(
        default=True,
        description='Status da turma'
    )
})

# Modelos de resposta
success_model = turmas_namespace.model('SuccessResponse', {
    'success': fields.Boolean(default=True),
    'message': fields.String,
    'data': fields.Raw
})

error_model = turmas_namespace.model('ErrorResponse', {
    'success': fields.Boolean(default=False),
    'message': fields.String,
    'error': fields.String(description='Tipo do erro'),
    'details': fields.String(description='Detalhes técnicos (opcional)')
})

# Filtros de consulta
filtros_model = turmas_namespace.parser()
filtros_model.add_argument(
    'ativo',
    type=inputs.boolean,
    required=False,
    help='Filtrar por status ativo/inativo',
    location='args'
)
filtros_model.add_argument(
    'professor_id',
    type=int,
    required=False,
    help='Filtrar por ID do professor',
    location='args'
)

@turmas_namespace.route('/')
class ListaTurmas(Resource):
    @turmas_namespace.expect(turma_input_model)
    @turmas_namespace.response(201, 'Success', success_model)
    @turmas_namespace.response(400, 'Bad Request', error_model)
    @turmas_namespace.response(500, 'Internal Error', error_model)
    def post(self):
        """Cria uma nova turma"""
        return turma_controller.criar_turma()


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

@turmas_namespace.route('/<int:id_turma>/status')
@turmas_namespace.param('id_turma', 'ID da turma', _in='path', required=True)
class StatusTurma(Resource):
    @turmas_namespace.response(200, 'Sucesso', success_model)
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def patch(self, id_turma):
        """Atualiza o status da turma (ativo/inativo)"""
        return turma_controller.atualizar_status_turma(id_turma)

@turmas_namespace.route('/<int:id_turma>')
@turmas_namespace.param('id_turma', 'ID da turma', _in='path', required=True)
class ExcluirTurma(Resource):
    @turmas_namespace.response(204, 'Turma excluída')
    @turmas_namespace.response(404, 'Turma não encontrada', error_model)
    @turmas_namespace.response(500, 'Erro interno', error_model)
    def delete(self, id_turma):
        """Exclui permanentemente uma turma"""
        return turma_controller.excluir_turma(id_turma)