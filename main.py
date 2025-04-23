from flask import Blueprint, Flask, jsonify
from flask_restx import Api, Namespace
from config import BancoDados, Config
from autenticacao import login_requerido
from model import aluno_model, professor_model, turma_model

from routes.aluno_routes import alunos_namespace
from routes.professor_routes import professores_ns
from routes.turma_routes import turmas_ns
from autenticacao import login_blueprint, login_ns  # Importar login_ns

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.config.from_object(Config)

# Configuração de autenticação para Swagger
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Digite: Bearer <seu_token_jwt>'
    }
}

# ---------------- FLASK-RESTX (Swagger) ----------------
api = Api(
    app,
    version='1.0',
    title='API Sistema Acadêmico',
    description='Documentação interativa da API',
    doc='/swagger/',  # Documentação Swagger acessível em /swagger/
    authorizations=authorizations,
    security='Bearer Auth'
)

# Registrando os Namespaces diretamente
api.add_namespace(alunos_namespace)
api.add_namespace(professores_ns)
api.add_namespace(turmas_ns)
api.add_namespace(login_ns)  # Registrar login_ns para o login

# ---------------- ENDPOINT ADMIN ----------------
admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route("/reseta", methods=['POST'])
@login_requerido
def resetar_dados():
    aluno_model.BancoDados["alunos"] = []
    professor_model.BancoDados["professores"] = []
    turma_model.BancoDados["turma"] = []
    return jsonify({"mensagem": "Dados resetados com sucesso!"}), 200

# ---------------- BLUEPRINTS REGISTRADOS ----------------
# Registrar o Blueprint admin (não faz parte da API REST)
app.register_blueprint(admin_blueprint)

# Registrar o Blueprint de login
app.register_blueprint(login_blueprint)

# ---------------- BANCO DE DADOS ----------------
def init_db():
    with app.app_context():
        BancoDados.Base.metadata.create_all(BancoDados.engine)

init_db()

# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(host=Config.HOST)