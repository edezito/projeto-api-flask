from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta
from service.autenticacao_services import AuthService
from model.usuario_model import Usuario

class LoginController:
    
    @staticmethod
    def autenticar_usuario():
        """Autenticação do usuário com base no nickname e senha fornecidos"""
        try:
            dados = request.get_json()

            # Verifica se os dados de login estão completos
            if not dados or 'usuario' not in dados or 'senha' not in dados:
                return jsonify({'message': 'Dados de login incompletos'}), 400

            usuario = Usuario.query.filter_by(usuario=dados['usuario']).first()

            if not usuario or not check_password_hash(usuario.senha, dados['senha']):
                return jsonify({
                    'status': 'error',
                    'message': 'Usuário ou senha incorretos',
                    'code': 401
                }), 401

            # Criação do access token e refresh token
            access_token = create_access_token(
                identity=usuario.id,
                expires_delta=timedelta(hours=1),
                additional_claims={
                    'roles': [role.nome for role in usuario.roles],
                    'email': usuario.email
                }
            )

            refresh_token = create_refresh_token(identity=usuario.id)

            user_data = {
                'id': usuario.id,
                'usuario': usuario.nickname,
                'nome': usuario.nome
            }

            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': 3600,
                'user_info': user_data
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Erro interno no servidor',
                'code': 500,
                'details': str(e)
            }), 500

    @staticmethod
    @jwt_required(refresh=True)
    def refresh_token():
        """Renova o access token usando o refresh token"""
        try:
            identity = get_jwt_identity()
            usuario = Usuario.query.get(identity)

            if not usuario:
                return jsonify({'message': 'Usuário não encontrado'}), 401

            new_token = create_access_token(
                identity=usuario.id,
                expires_delta=timedelta(hours=1),
                additional_claims={
                    'roles': [role.nome for role in usuario.roles],
                    'email': usuario.email
                }
            )

            return jsonify({
                'access_token': new_token,
                'token_type': 'Bearer',
                'expires_in': 3600
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Falha ao renovar token',
                'code': 500
            }), 500

    @staticmethod
    @jwt_required()
    def obter_dados_usuario():
        """Obtém os dados do usuário autenticado"""
        try:
            current_user = get_jwt_identity()
            usuario = Usuario.query.get(current_user)

            if not usuario:
                return jsonify({'message': 'Usuário não encontrado'}), 404

            # Retorna dados do usuário em uma lista (conforme necessário pelo erro)
            return jsonify([{
                'id': usuario.id,
                'usuario': usuario.nickname,
                'nome': usuario.nome
            }]), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Erro ao recuperar dados do usuário',
                'code': 500
            }), 500

    @staticmethod
    @jwt_required()
    def realizar_logout():
        """Logout com validação de credenciais"""
        try:
            dados = request.get_json()

            # Verifica se os dados de entrada não estão vazios
            if not dados:
                return jsonify({'message': 'Corpo da requisição vazio'}), 400

            # Verifica se os campos "usuario" e "senha" estão presentes
            if 'usuario' not in dados or 'senha' not in dados:
                return jsonify({'message': 'Campos "usuario" e "senha" são obrigatórios'}), 400

            usuario = dados['usuario']
            senha = dados['senha']

            # Verifica se os campos têm o tipo correto
            if not isinstance(usuario, str) or not isinstance(senha, str):
                return jsonify({'message': 'Campos "usuario" e "senha" devem ser do tipo string'}), 400

            # Verifica os comprimentos mínimos e máximos
            if len(usuario) < 4 or len(usuario) > 20:
                return jsonify({'message': 'Usuário deve ter entre 4 e 20 caracteres'}), 400

            if len(senha) < 4 or len(senha) > 100:
                return jsonify({'message': 'Senha deve ter entre 4 e 100 caracteres'}), 400

            # Verifica se o usuário existe e a senha está correta
            usuario_obj = Usuario.query.filter_by(usuario=usuario).first()

            if not usuario_obj or not check_password_hash(usuario_obj.senha, senha):
                return jsonify({
                    'status': 'error',
                    'message': 'Usuário ou senha incorretos',
                    'code': 401
                }), 401

            # Implementação de logout, pode ser feito via blacklist ou outra técnica
            response = {
                'message': 'Logout bem-sucedido'
            }

            return jsonify(response), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Erro interno no servidor',
                'code': 500,
                'details': str(e)
            }), 500