from flask_restx import Namespace, fields

alunos_namespace = Namespace('alunos', description='Operações de gerenciamento de alunos')

aluno_model = alunos_namespace.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID único do aluno'),
    'nome': fields.String(required=True, description='Nome completo do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno'),
    'nota_primeiro_semestre': fields.Integer(required=True, description='Nota do Primeiro semestre do Aluno'),
    'nota_segundo_semestre': fields.Integer(required=True, description='Nota do Segundo semestre do Aluno'),
    'media': fields.Integer(required=True, description='Media final do Aluno'),
    'turma_id': fields.Integer(required=True, description='Turma do Aluno')
})

success_model = alunos_namespace.model('SuccessResponse', {
    'mensagem': fields.String(description='Mensagem de sucesso'),
    'aluno': fields.Nested(aluno_model),
    'turma': fields.Raw(description='Dados da turma do aluno')
})