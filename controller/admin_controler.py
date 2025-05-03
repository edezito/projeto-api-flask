from flask import request, jsonify
from functools import wraps
from model import aluno_model, professor_model, turma_model
from config import BancoDados
import logging 
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
                logging.error(f"Erro ao resetar dados: {str(e)}")  # Log correto usando o logger padrão
                return SistemaController._handle_response(False, f"Erro ao resetar dados: {str(e)}", None, 500)
        return wrapper

    @staticmethod
    @handle_errors
    def resetar_dados():
        db = BancoDados.SessionLocal()
        try:
            # Excluir dados de teste (exemplo)
            db.query(aluno_model.Aluno).delete()
            db.query(turma_model.Turma).delete()
            db.query(professor_model.Professor).delete()
            db.commit()
            print("Dados resetados com sucesso!")  # Log para garantir que o método está sendo chamado
        except Exception as e:
            db.rollback()
            print(f"Erro ao resetar dados: {e}")