from flask import Blueprint, Flask, jsonify
from config import BancoDados, Config
from autenticacao import login_requerido
from model import aluno_model, professor_model, turma_model
from swagger.namespaces.alunos_namespace import alunos_namespace

from routes.aluno_routes import alunos_namespace
from routes.professor_routes import professores_ns
from routes.turma_routes import turmas_ns

from autenticacao import login_blueprint, login_ns

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.config.from_object(Config)

# Registrando os Namespaces diretamente
app.register_blueprint(alunos_namespace)


#api.add_namespace(professores_ns)
#api.add_namespace(turmas_ns)
#api.add_namespace(login_ns)

# ---------------- ENDPOINT ADMIN ----------------
admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route("/reseta", methods=['POST'])
@login_requerido
def resetar_dados():
    aluno_model.BancoDados["alunos"] = []
    professor_model.BancoDados["professores"] = []
    turma_model.BancoDados["turma"] = []
    return jsonify({"mensagem": "Dados resetados com sucesso!"}), 200

app.register_blueprint(admin_blueprint)
app.register_blueprint(login_blueprint)

# ---------------- BANCO DE DADOS ----------------
def init_db():
    with app.app_context():
        BancoDados.Base.metadata.create_all(BancoDados.engine)

init_db()

# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(host=Config.HOST)

#atualizar controller
#atualizar testes
#atualizar docker
#atualizar render