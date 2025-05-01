from flask import Flask
from flask_cors import CORS
from swagger.swagger_config import api, api_blueprint

from swagger.namespaces.alunos_namespace import alunos_namespace
from swagger.namespaces.login_namespace import login_namespace
from swagger.namespaces.admin_namespaces import admin_namespace
from swagger.namespaces.professor_namespace import professores_namespace
from swagger.namespaces.turmas_namespaces import turmas_namespace

from config import BancoDados

import routes.login_routes
import routes.professor_routes
import routes.turma_routes


app = Flask(__name__)
app.config['DEBUG'] = True

CORS(app)

# Banco de dados
with app.app_context():
    BancoDados.Base.metadata.create_all(BancoDados.engine)

# Swagger
api.add_namespace(admin_namespace)
api.add_namespace(login_namespace)
api.add_namespace(alunos_namespace)
api.add_namespace(professores_namespace)
api.add_namespace(turmas_namespace)

# Registra o blueprint do Swagger
app.register_blueprint(api_blueprint)

# Rota de Health Check
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200  # Explicitando o código de status

if __name__ == '__main__':
    app.run()