from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api

import routes.login_routes
import routes.professor_routes
import routes.turma_routes

from swagger.swagger_config import api, api_blueprint
from swagger.namespaces.alunos_namespace import alunos_namespace
from swagger.namespaces.login_namespace import login_namespace
from swagger.namespaces.admin_namespaces import admin_namespace
from swagger.namespaces.professor_namespace import professores_namespace
from swagger.namespaces.turmas_namespaces import turmas_namespace

from config import BancoDados, Config

app = Flask(__name__)
app.config.from_object(Config)

# Configuração JWT mais robusta
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

# Configuração de CORS mais específica
CORS(app, resources={
    r"/autenticacao/*": {"origins": "*"},
    r"/api/*": {"origins": "*"},
    r"/health": {"origins": "*"}
})

# Inicializa JWT
jwt = JWTManager(app)

# Banco de dados
with app.app_context():
    BancoDados.Base.metadata.create_all(BancoDados.engine)

# Registra o blueprint do Swagger
app.register_blueprint(api_blueprint)

# Adiciona namespaces
api.add_namespace(admin_namespace)
api.add_namespace(login_namespace)
api.add_namespace(alunos_namespace)
api.add_namespace(professores_namespace)
api.add_namespace(turmas_namespace)

# Rota de Health Check
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

# Rota para servir o swagger.json
@app.route('/api/swagger.json')
def swagger_json():
    return jsonify(api.__schema__)

# Configuração de erro para rotas não encontradas
@app.errorhandler(404)
def handle_404(e):
    return {'message': 'Endpoint não encontrado'}, 404

# Configuração de erro para erros internos
@app.errorhandler(500)
def handle_500(e):
    return {'message': 'Erro interno no servidor'}, 500

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)