from flask import Blueprint
from flask_restx import Api
from .namespaces.alunos_namespace import alunos_namespace

aluno_bp = Blueprint('aluno', __name__, url_prefix='/api')

api = Api(
    aluno_bp,
    version='1.0',
    title='API Sistema Acadêmico',
    description='Documentação interativa da API',
    doc='/swagger',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Digite: Bearer <seu_token_jwt>'
        }
    },
    security='Bearer Auth'
)

api.add_namespace(alunos_namespace)