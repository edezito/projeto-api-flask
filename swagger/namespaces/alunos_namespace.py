from flask_restx import Namespace, fields

# Configuração do Namespace
alunos_namespace = Namespace('alunos', description='Operações com alunos')

# Modelo de Turma (para inclusão no aluno)
turma_model = alunos_namespace.model('Turma', {
    'id': fields.Integer(description='ID da turma', example=1),
    'nome': fields.String(description='Nome da turma', example='Turma A')
})

# Modelo de Aluno
aluno_model = alunos_namespace.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID único do aluno', example=1),
    'nome': fields.String(required=True, description='Nome completo', example='João Silva', min_length=3),
    'idade': fields.Integer(required=True, description='Idade do aluno', example=15),
    'nota_primeiro_semestre': fields.Float(description='Nota do primeiro semestre', example=7.5),
    'nota_segundo_semestre': fields.Float(description='Nota do segundo semestre', example=8.0),
    'media': fields.Float(readOnly=True, description='Média calculada automaticamente'),
    'turma': fields.Nested(turma_model, description='Dados da turma associada ao aluno')
})

# Modelo de resposta de sucesso
success_model = alunos_namespace.model('SuccessResponse', {
    'mensagem': fields.String(description='Mensagem de sucesso', example='Operação realizada com sucesso')
})