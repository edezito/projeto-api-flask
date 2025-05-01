from flask import request
from flask import jsonify
from functools import wraps
from model import aluno_model, professor_model, turma_model

class SistemaController:

    @staticmethod
    def _handle_response(success, message, data=None, status_code=200):
        """Padroniza respostas da API"""
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return jsonify(response), status_code

    @staticmethod
    def handle_errors(func):
        """Tratamento centralizado de erros"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return SistemaController._handle_response(False, f"Erro ao resetar dados: {str(e)}", None, 500)
        return wrapper

    @staticmethod
    @handle_errors
    def resetar_dados():
        """Reseta os dados dos alunos, professores e turmas"""
        aluno_model.BancoDados["alunos"] = []
        professor_model.BancoDados["professores"] = []
        turma_model.BancoDados["turma"] = []

        return SistemaController._handle_response(True, "Dados resetados com sucesso!")