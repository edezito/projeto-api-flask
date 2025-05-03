from flask_restx import Namespace, fields

# Criação do namespace
turmas_namespace = Namespace('turmas', 
                     description='Operações de gerenciamento de turmas',
                     path='/turmas')  # Path completo

# Modelos
turma_model = turmas_namespace.model('Turma', {
    'id': fields.Integer(readOnly=True, description='ID único da turma'),
    'descricao': fields.String(required=True, description='Nome da turma', example='Turma A'),
    'professor_id': fields.Integer(required=True, description='ID do professor responsável', example=1),
    'ativo': fields.Boolean(default=True, description='Status da turma')
})

success_model = turmas_namespace.model('SuccessResponse', {
    'message': fields.String(description='Mensagem de sucesso'),
    'data': fields.Nested(turma_model, description='Dados da turma')
})

error_model = turmas_namespace.model('ErrorResponse', {
    'error': fields.String(description='Mensagem de erro'),
    'details': fields.String(description='Detalhes do erro')
})