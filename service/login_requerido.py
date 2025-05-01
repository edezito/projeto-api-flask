from functools import wraps
from flask import request, jsonify
from service.autenticacao_services import AuthService

def login_requerido(f):
    """Decorador para garantir que o usuário está autenticado (token válido)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtém o cabeçalho de autorização
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"erro": "Token não fornecido", "redirecionar": "/login"}), 401

        try:
            # O token é esperado após "Bearer " no cabeçalho
            token = auth_header.split(" ")[1]
            
            # Chama o serviço para verificar a validade do token
            payload = AuthService.verificar_token(token)
            request.usuario = payload['usuario']  # Atribui o usuário ao request
        except IndexError:
            # Caso o token não seja fornecido ou não siga o formato esperado
            return jsonify({
                "erro": "Token malformado. Certifique-se de usar 'Bearer <token>' no cabeçalho.",
                "redirecionar": "/login"
            }), 401
        except ValueError as e:
            # Caso o token não seja válido
            return jsonify({
                "erro": f"Token inválido: {str(e)}",
                "redirecionar": "/login"
            }), 401
        except Exception as e:
            # Erro inesperado durante a verificação do token
            return jsonify({
                "erro": "Erro inesperado ao verificar token",
                "detalhes": str(e),
                "redirecionar": "/login"
            }), 500

        return f(*args, **kwargs)
    return decorated_function