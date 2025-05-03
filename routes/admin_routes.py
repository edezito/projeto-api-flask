from datetime import datetime
from flask_restx import Namespace, Resource, fields
from controller.admin_controler import SistemaController
from service.login_requerido import login_requerido

# Criação do namespace
admin_ns = Namespace('admin', description='Operações administrativas', path='/admin')

# Modelo de resposta
reset_response_model = admin_ns.model('ResetResponse', {
    'success': fields.Boolean(required=True, description='Indica se a operação foi bem-sucedida'),
    'message': fields.String(required=True, description='Mensagem da operação'),
    'timestamp': fields.DateTime(dt_format='iso8601', description='Horário da operação')
})

@admin_ns.route('/reset')
class AdminReset(Resource):
    @admin_ns.doc(
        security='Bearer Auth',
        responses={
            200: ('Sucesso', reset_response_model),
            401: 'Unauthorized',
            403: 'Forbidden',
            500: 'Erro interno'
        }
    )
    @admin_ns.marshal_with(reset_response_model)
    @login_requerido
    def post(self):
        """
        Reset completo do sistema
        
        Remove todos os dados de:
        - Alunos
        - Professores
        - Turmas
        - Relacionamentos
        
        Requer privilégios de administrador.
        """
        # Chama a função de reset
        response, status_code = SistemaController.resetar_dados()
        
        # Prepara a resposta e adiciona o timestamp
        response['timestamp'] = datetime.utcnow().isoformat()

        return response, status_code