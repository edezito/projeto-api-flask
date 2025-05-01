from flask_restx import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)

from swagger.namespaces.login_namespace import (
    login_namespace, login_model, login_response_model, error_model
)

@login_namespace.route('/login')
class LoginResource(Resource):
    @login_namespace.expect(login_model)
    @login_namespace.response(200, 'Login realizado com sucesso', login_response_model)
    @login_namespace.response(401, 'Credenciais inválidas', error_model)
    def post(self):
        data = request.get_json()
        usuario = data.get('usuario')
        senha = data.get('senha')

        if usuario == 'admin' and senha == '1234':
            access_token = create_access_token(identity=usuario)
            refresh_token = create_refresh_token(identity=usuario)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': 3600
            }, 200
        else:
            return {'message': 'Credenciais inválidas'}, 401


@login_namespace.route('/logout')
class LogoutResource(Resource):
    @jwt_required()
    @login_namespace.response(200, 'Logout realizado com sucesso')
    def post(self):
        usuario = get_jwt_identity()
        return {'message': f'Logout realizado para o usuário {usuario}'}, 200