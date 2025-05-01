from flask_restx import Resource
from flask_jwt_extended import jwt_required
from flask import request
from controller.login_controler import (
    LoginController
)
from swagger.namespaces.login_namespace import login_namespace, login_model, login_response_model, error_model

@login_namespace.route('/login')
class LoginResource(Resource):
    @login_namespace.expect(login_model, validate=True)
    def post(self):
        return LoginController.autenticar_usuario()

@login_namespace.route('/refresh')
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        return LoginController.refresh_token()

@login_namespace.route('/me')
class UserInfoResource(Resource):
    @jwt_required()
    def get(self):
        return LoginController.obter_dados_usuario()

@login_namespace.route('/logout')
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        return LoginController.realizar_logout()