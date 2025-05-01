from flask_restx import Namespace, fields

# Criar o namespace com caminho /autenticacao e nome mais amigável no Swagger
login_namespace = Namespace(
    'autenticação',
    description='Operações de autenticação de usuários',
    path='/autenticacao'  # Prefixo para as rotas
)

# Modelo de entrada para login
login_model = login_namespace.model('Login', {
    'usuario': fields.String(required=True, example='admin', min_length=4),
    'senha': fields.String(required=True, example='1234', min_length=4)
})

# Modelo de resposta para login
login_response_model = login_namespace.model('LoginResponse', {
    'access_token': fields.String(description='Token JWT para autenticação'),
    'refresh_token': fields.String(description='Token para renovação'),
    'expires_in': fields.Integer(description='Tempo de expiração em segundos')
})

# Modelo de erro
error_model = login_namespace.model('Error', {
    'message': fields.String(description='Mensagem de erro')
})