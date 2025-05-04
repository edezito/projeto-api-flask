from flask import request, current_app
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta
from functools import wraps
from model.usuario_model import Usuario, db

class LoginController:
    
    @staticmethod
    def handle_errors(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
                return {'message': 'Internal server error'}, 500
        return wrapper

    @staticmethod
    @handle_errors
    def autenticar_usuario():
        data = request.get_json(silent=True)
        if not data:
            return {'message': 'Dados não fornecidos'}, 400
            
        usuario = data.get('usuario')
        senha = data.get('senha')
        
        if not usuario or not senha:
            return {'message': 'Credenciais faltando'}, 400
        
        user = Usuario.query.filter_by(nickname=usuario).first()
        
        if not user or not check_password_hash(user.senha, senha):
            return {'message': 'Usuário ou senha incorretos'}, 401
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'nickname': user.nickname,
                'nome': user.nome
            }
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_info': user.to_dict()
        }, 200

    @staticmethod
    @jwt_required(refresh=True)
    @handle_errors
    def refresh_token():
        user_id = get_jwt_identity()
        user = Usuario.query.get(user_id)

        if not user:
            return {'message': 'Usuário não encontrado'}, 404

        new_token = create_access_token(
            identity=user.id,
            additional_claims={
                'nickname': user.nickname,
                'nome': user.nome
            }
        )

        return {
            'access_token': new_token
        }, 200

    @staticmethod
    @jwt_required()
    @handle_errors
    def obter_dados_usuario():
        user_id = get_jwt_identity()
        user = Usuario.query.get(user_id)

        if not user:
            return {'message': 'Usuário não encontrado'}, 404

        return user.to_dict(), 200

    @staticmethod
    @jwt_required()
    @handle_errors
    def realizar_logout():
        data = request.get_json(silent=True)
        
        if not data:
            return {'message': 'Corpo da requisição vazio'}, 400

        usuario = data.get('usuario')
        senha = data.get('senha')

        if not usuario or not senha:
            return {
                'message': 'Campos obrigatórios faltando',
                'required_fields': ['usuario', 'senha']
            }, 400

        user = Usuario.query.filter_by(nickname=usuario).first()

        if not user or not check_password_hash(user.senha, senha):
            return {'message': 'Credenciais inválidas'}, 401

        return {'message': 'Logout realizado com sucesso'}, 200