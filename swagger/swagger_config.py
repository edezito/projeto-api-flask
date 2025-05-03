from flask_restx import Api
from flask import Blueprint, jsonify

api_blueprint = Blueprint('api', __name__, url_prefix='/')

api = Api(
    api_blueprint,
    title='API Gestão Escolar',
    version='1.0',
    description='Documentação completa da API',
    doc='/swagger',  # Swagger será acessível em /swagger
    security='Bearer Auth',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Use: Bearer <JWT>'
        }
    }
)

@api_blueprint.route('/swagger.json')
def swagger_json():
    return jsonify(api.__schema__)