from flask_restx import Namespace, fields

# Namespace com path e descrição personalizados
professores_namespace = Namespace(
    name='professores',
    description='Operações de gerenciamento de professores',
    path='/api/professores'
)

# Modelo do professor
professor_model = professores_namespace.model('Professor', {
    'id': fields.Integer(readOnly=True, description='ID do professor'),
    'nome': fields.String(required=True, description='Nome do professor'),
    'idade': fields.Integer(required=True, description='Idade do professor'),
    'disciplina': fields.String(required=True, description='Disciplina que o professor ministra'),
    'observacoes': fields.String(description='Observações adicionais')
})

# Modelo para mensagens de sucesso
success_model = professores_namespace.model('Success', {
    'message': fields.String,
    'data': fields.Raw
})

# Modelo para mensagens de erro
error_model = professores_namespace.model('Error', {
    'error': fields.String,
    'details': fields.String
})