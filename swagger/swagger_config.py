from flask_restx import Api
from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_blueprint,
    title='API Gestão Escolar',
    version='1.0',
    description='Documentação completa da API',
    doc='/swagger-ui',
    security='Bearer Auth',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)