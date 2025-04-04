import datetime
from flask import Blueprint, jsonify, request
from config import Config
from functools import wraps
import jwt

login_blueprint = Blueprint('login', __name__)

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuarios = {
    "edezito": Usuario("Eder", "edezito", "1234"),
    "felipe": Usuario("Felipe", "felipe", "senha"),
    "vitor": Usuario("Victor", "vitor", "abcd")
}

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"erro": "Token não fornecido", "redirecionar": "/login"}), 401

        try:
            token = auth_header.split(" ")[1]  # "Bearer <token>"
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.usuario = payload['usuario']
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({"erro": "Token inválido ou expirado", "redirecionar": "/login"}), 401

        return f(*args, **kwargs)
    return decorated_function

@login_blueprint.route("/login", methods=["POST"])
def autenticar():
    dados = request.get_json() or {}
    usuario_nickname = dados.get("usuario")
    senha = dados.get("senha")

    usuario_obj = usuarios.get(usuario_nickname)

    if usuario_obj and usuario_obj.senha == senha:
        token = jwt.encode(
            {
                "usuario": usuario_obj.nickname,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"mensagem": "Login bem-sucedido", "token": token}), 200

    return jsonify({"erro": "Usuário ou senha inválidos"}), 403

@login_blueprint.route('/logout', methods=["POST"])
@login_requerido
def logout():
    return jsonify({"mensagem": "Logout realizado com sucesso (JWT descartado no cliente)"}), 200