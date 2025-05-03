from flask_restx import Namespace, fields

# Configuração do namespace
login_namespace = Namespace(
    'autenticação',
    description='Operações de autenticação e gerenciamento de tokens JWT',
    path='/autenticacao'
)

# --- Modelos de Dados ---
login_model = login_namespace.model('Credenciais', {
    'usuario': fields.String(
        required=True,
        example='admin',
        min_length=4,
        max_length=20,
        description='Nome de usuário'
    ),
    'senha': fields.String(
        required=True,
        example='1234',
        min_length=4,
        description='Senha do usuário'
    )
})

user_info_model = login_namespace.model('UserInfo', {
    'id': fields.Integer(
        required=False,  # Alterado para opcional
        description='ID do usuário'
    ),
    'nome': fields.String(
        required=False,  # Alterado para opcional
        description='Nome completo'
    ),
    'email': fields.String(
        required=False,  # Alterado para opcional
        description='E-mail do usuário'
    ),
    'roles': fields.List(
        fields.String,
        required=False,  # Alterado para opcional
        description='Perfis de acesso'
    )
})

login_response_model = login_namespace.model('RespostaLogin', {
    'access_token': fields.String(
        required=True,
        description='Token JWT para autenticação'
    ),
    'refresh_token': fields.String(
        required=True,
        description='Token para renovação'
    ),
    'token_type': fields.String(
        required=True,
        default='Bearer',
        description='Tipo do token'
    ),
    'expires_in': fields.Integer(
        required=True,
        default=3600,
        description='Tempo de expiração em segundos'
    ),
    'user_info': fields.Nested(
        user_info_model,
        required=True,
        description='Informações do usuário'
    )
})

error_model = login_namespace.model('Erro', {
    'status': fields.String(
        required=False,  # Alterado para True para alinhar com os testes
        default='error'
    ),
    'message': fields.String(
        required=True,
        description='Mensagem de erro'
    ),
    'code': fields.Integer(
        required=False,  # Alterado para True para alinhar com os testes
        example=401,
        description='Código HTTP do erro'
    )
})