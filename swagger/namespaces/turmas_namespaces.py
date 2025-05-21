from flask_restx import Namespace, fields

turmas_namespace = Namespace('turmas', 
                     description='Operações de gerenciamento de turmas',
                     path='/turmas')

# Modelo básico de professor
professor_model = turmas_namespace.model('Professor', {
    'id': fields.Integer,
    'nome': fields.String
})

# Modelo completo de turma
turma_model = turmas_namespace.model('Turma', {
    'id': fields.Integer(readOnly=True),
    'descricao': fields.String(required=True),
    'professor_id': fields.Integer(required=True),
    'ativo': fields.Boolean(default=True),
    'quantidade_alunos': fields.Integer(readonly=True),
    'professor': fields.Nested(professor_model)
})

success_model = turmas_namespace.model('SuccessResponse', {
    'message': fields.String(description='Mensagem de sucesso'),
    'data': fields.Nested(turma_model, description='Dados da turma')
})

error_model = turmas_namespace.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro'),
    'details': fields.String(description='Detalhes do erro')
})