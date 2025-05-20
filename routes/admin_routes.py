import datetime
from flask_restx import Namespace, Resource, fields
from controller.admin_controler import SistemaController

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
        responses={
            200: ('Sucesso', reset_response_model),
            403: 'Forbidden',
            500: 'Erro interno'
        }
    )
    @admin_ns.marshal_with(reset_response_model)
    def post(self):
        # Chama a função de reset
        response, status_code = SistemaController.resetar_dados()
        
        # Prepara a resposta e adiciona o timestamp
        response['timestamp'] = datetime.utcnow().isoformat()

        return response, status_code