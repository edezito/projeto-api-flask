from flask import jsonify
from functools import wraps
import logging

def handle_response(success, message, data=None, status_code=200):
    response = {
        'success': success,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Erro: {str(e)}")
            return handle_response(False, f"Erro: {str(e)}", None, 500)
    return wrapper