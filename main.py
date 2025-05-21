from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import BancoDados, Config
from swagger.swagger_config import api, api_blueprint

# Namespaces
from swagger.namespaces.alunos_namespace import alunos_namespace
from swagger.namespaces.admin_namespaces import admin_namespace
from swagger.namespaces.professor_namespace import professores_namespace
from swagger.namespaces.turmas_namespaces import turmas_namespace
from routes.turma_routes import turmas_namespace

# Importar rotas adicionais
import routes.aluno_routes
import routes.professor_routes
import routes.turma_routes

app = Flask(__name__)
app.config.from_object(Config)

# JWT
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
jwt = JWTManager(app)

# CORS
CORS(app, resources={
    r"/autenticacao/*": {"origins": "*"},
    r"/api/*": {"origins": "*"},
    r"/health": {"origins": "*"}
})

# Banco de dados
with app.app_context():
    BancoDados.Base.metadata.create_all(BancoDados.engine)

# Registra Swagger em "/swagger"
app.register_blueprint(api_blueprint)

# Namespaces da API
api.add_namespace(admin_namespace)
api.add_namespace(alunos_namespace)
api.add_namespace(professores_namespace)
api.add_namespace(turmas_namespace)

# Health check
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

# Erros
@app.errorhandler(404)
def not_found(e):
    return {'message': 'Endpoint não encontrado'}, 404

@app.errorhandler(500)
def internal_error(e):
    return {'message': 'Erro interno no servidor'}, 500

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)