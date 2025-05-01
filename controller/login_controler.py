from flask import request, jsonify
from service.autenticacao_services import AuthService

class LoginController:
    
    @staticmethod
    def autenticar_usuario():
        dados = request.get_json()
        
        usuario_nickname = dados.get("usuario")
        senha = dados.get("senha")
        
        if not usuario_nickname or not senha:
            return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400
        
        # Chama o serviço de autenticação
        response, status_code = AuthService.autenticar_usuario(usuario_nickname, senha)
        return jsonify(response), status_code

    @staticmethod
    def realizar_logout():
        response, status_code = AuthService.realizar_logout()
        return jsonify(response), status_code