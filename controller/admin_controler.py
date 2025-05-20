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
                logging.error(f"Erro: {str(e)}")
                return SistemaController._handle_response(False, f"Erro ao processar a requisição: {str(e)}", None, 500)
        return wrapper

    @staticmethod
    @handle_errors
    def resetar_dados():
        db = BancoDados.SessionLocal()
        try:
            # Exclui os dados das tabelas (ordem importa se há FK)
            db.query(aluno_model.Aluno).delete()
            db.query(turma_model.Turma).delete()
            db.query(professor_model.Professor).delete()
            db.commit()
            logging.info("Dados resetados com sucesso!")
            return SistemaController._handle_response(True, "Dados resetados com sucesso.")
        except Exception as e:
            db.rollback()
            logging.error(f"Erro ao resetar dados: {e}")
            return SistemaController._handle_response(False, f"Erro ao resetar dados: {str(e)}", None, 500)
        finally:
            db.close()