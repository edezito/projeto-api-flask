import datetime
from flask import Blueprint, jsonify, request
from config import Config
from functools import wraps
import jwt
from flask_restx import Namespace, Resource, fields

# Definindo o Blueprint
login_blueprint = Blueprint('login', __name__)

# Definindo a classe de Usuário para simular um banco de dados em memória
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

# Usuários simulados (substitua por banco de dados real)
usuarios = {
    "edezito": Usuario("Eder", "edezito", "1234"),
    "felipe": Usuario("Felipe", "felipe", "senha"),
    "vitor": Usuario("Victor", "vitor", "abcd")
}

# Decorator de verificação de token JWT
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"erro": "Token não fornecido", "redirecionar": "/login"}), 401

        try:
            # Pegando o token do cabeçalho
            token = auth_header.split(" ")[1]  # "Bearer <token>"
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.usuario = payload['usuario']  # Adicionando o usuário ao contexto da requisição
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            return jsonify({"erro": "Token inválido ou expirado", "detalhes": str(e), "redirecionar": "/login"}), 401

        return f(*args, **kwargs)
    return decorated_function

# Definindo o namespace do Swagger para o login
login_ns = Namespace('login', description='Operações de login e logout')

# Definindo o modelo de login no Swagger
login_model = login_ns.model('Login', {
    'usuario': fields.String(required=True, description='Nome de usuário', example='edezito'),
    'senha': fields.String(required=True, description='Senha do usuário', example='1234')
})

# Definindo o modelo de resposta do login
login_response_model = login_ns.model('LoginResponse', {
    'mensagem': fields.String(description='Mensagem de sucesso'),
    'token': fields.String(description='Token JWT gerado')
})

# Rota de login
@login_ns.route('/login')
class Login(Resource):
    @login_ns.doc('Autenticação', responses={200: 'Login bem-sucedido', 403: 'Credenciais inválidas'})
    @login_ns.expect(login_model)
    @login_ns.marshal_with(login_response_model)
    def post(self):
        """
        Endpoint para autenticação
        Recebe o username e senha, e retorna um token JWT.
        """
        dados = request.get_json() or {}
        usuario_nickname = dados.get("usuario")
        senha = dados.get("senha")

        usuario_obj = usuarios.get(usuario_nickname)

        if usuario_obj and usuario_obj.senha == senha:
            # Gerando o token JWT
            token = jwt.encode(
                {
                    "usuario": usuario_obj.nickname,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )
            
            # Retornando uma mensagem de sucesso com o token
            return {
                "mensagem": f"Login bem-sucedido, {usuario_obj.nome}!",
                "token": token
            }, 200

        return {'erro': 'Usuário ou senha inválidos'}, 403

# Rota de logout
@login_ns.route('/logout')
class Logout(Resource):
    @login_requerido
    @login_ns.doc('Logout', responses={200: 'Logout realizado com sucesso'})
    def post(self):
        """
        Endpoint de logout
        No JWT, o logout acontece no lado do cliente (o token é descartado pelo cliente).
        """
        return {'mensagem': 'Logout realizado com sucesso (JWT descartado no cliente)'}, 200