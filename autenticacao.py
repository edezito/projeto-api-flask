from flask import Blueprint, jsonify, request, session
from functools import wraps

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

# AUTENTICAÇÃO
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado'):
            return jsonify({
                "erro": "Usuário não autenticado",
                "redirecionar": "/login"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

@login_blueprint.route("/login", methods=["POST"])
def autenticar():
    dados = request.get_json() or {}
    usuario_nickname = dados.get("usuario")
    senha = dados.get("senha")

    usuario_obj = usuarios.get(usuario_nickname)  # Acessando corretamente o dicionário global

    if usuario_obj and usuario_obj.senha == senha:
        session['usuario_logado'] = usuario_obj.nickname
        session.permanent = True  # Mantém a sessão ativa
        return jsonify({"mensagem": "Login bem-sucedido", "usuario": usuario_obj.nickname}), 200

    return jsonify({"erro": "Usuário ou senha inválidos"}), 403

@login_blueprint.route('/logout', methods=["POST"])
def logout():
    if 'usuario_logado' in session:
        session.pop('usuario_logado')
        return jsonify({"mensagem": "Logout realizado com sucesso"}), 200
    else:
        return jsonify({"erro": "Nenhum usuário estava logado"}), 400