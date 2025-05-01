from flask_restx import Namespace, Resource, fields
from datetime import datetime
from controller.admin_controler import SistemaController  # ajuste o import conforme seu projeto

# Cria o namespace
admin_namespace = Namespace(
    'admin', 
    description='Operações administrativas do sistema',
    path='/admin'  # Define o path base para todas as rotas
)

# Modelo para respostas
reset_response_model = admin_namespace.model('ResetResponse', {
    'success': fields.Boolean(
        required=True,
        description='Indica se a operação foi bem-sucedida',
        example=True
    ),
    'message': fields.String(
        required=True,
        description='Mensagem da operação',
        example='Dados resetados com sucesso!'
    ),
    'data': fields.Raw(
        description='Dados adicionais retornados pela operação (se houver)'
    )
})

@admin_namespace.route('/resetar-dados')
class ResetarDadosResource(Resource):
    @admin_namespace.response(200, 'Sucesso', reset_response_model)
    @admin_namespace.response(500, 'Erro interno')
    def post(self):
        """Reseta todos os dados do sistema (alunos, professores e turmas)"""
        response, status_code = SistemaController.resetar_dados()
        
        # Adiciona timestamp à resposta
        response_json = response.get_json()
        response_json['timestamp'] = datetime.utcnow().isoformat()

        return response_json, status_code