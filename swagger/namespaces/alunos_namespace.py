from flask_restx import Namespace, fields, Resource
from flask import request
from service.aluno_service import AlunoService
from config import BancoDados

# Configuração do Namespace
alunos_namespace = Namespace('alunos', description='Operações com alunos')

# Modelos Swagger
aluno_model = alunos_namespace.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID único do aluno', example=1),
    'nome': fields.String(required=True, description='Nome completo', example='João Silva', min_length=3),
    'idade': fields.Integer(required=True, description='Idade do aluno', example=15),
    'nota_primeiro_semestre': fields.Float(description='Nota do primeiro semestre', example=7.5),
    'nota_segundo_semestre': fields.Float(description='Nota do segundo semestre', example=8.0),
    'media': fields.Float(readOnly=True, description='Média calculada automaticamente'),
    'turma_id': fields.Integer(required=True, description='ID da turma', example=5)
})

# Recursos da API
@alunos_namespace.route('/')
class AlunoListResource(Resource):
    @alunos_namespace.marshal_list_with(aluno_model)
    def get(self):
        """Lista todos os alunos"""
        with BancoDados.SessionLocal() as session:
            return AlunoService.listar_alunos(session)

    @alunos_namespace.expect(aluno_model, validate=True)
    @alunos_namespace.marshal_with(aluno_model, code=201)
    def post(self):
        """Cria um novo aluno"""
        dados = request.json
        with BancoDados.SessionLocal() as session:
            return AlunoService.criar_aluno(session, dados), 201

@alunos_namespace.route('/<int:id>')
@alunos_namespace.param('id', 'ID do aluno')
class AlunoResource(Resource):
    @alunos_namespace.marshal_with(aluno_model)
    def get(self, id):
        """Busca um aluno pelo ID"""
        with BancoDados.SessionLocal() as session:
            return AlunoService.buscar_aluno_por_id(session, id)

    @alunos_namespace.expect(aluno_model, validate=True)
    @alunos_namespace.marshal_with(aluno_model)
    def put(self, id):
        """Atualiza um aluno existente"""
        dados = request.json
        with BancoDados.SessionLocal() as session:
            return AlunoService.atualizar_aluno(session, id, dados)

    def delete(self, id):
        """Exclui um aluno pelo ID"""
        with BancoDados.SessionLocal() as session:
            AlunoService.excluir_aluno(session, id)
            return {'mensagem': 'Aluno excluído com sucesso'}, 200

success_model = alunos_namespace.model('SuccessResponse', {
    'mensagem': fields.String(description='Mensagem de sucesso', example='Operação realizada com sucesso')
})

pagination_params = {
    'page': fields.Integer(description='Número da página', example=1, default=1),
    'per_page': fields.Integer(description='Número de itens por página', example=20, default=20),
    'order_by': fields.String(description='Campo para ordenação', example='nome', default='nome')
}
