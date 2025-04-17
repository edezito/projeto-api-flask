from flask import Blueprint, Flask, jsonify
from config import Config
from autenticacao import login_requerido
from model import aluno_model, professor_model, turma_model

from routes.aluno_routes import alunos_blueprint
from routes.professor_routes import professores_blueprint
from routes.turma_routes import turmas_blueprint
from autenticacao import login_blueprint

app = Flask(__name__)
app.config.from_object(Config)

admin_blueprint = Blueprint('admin', __name__)

# ROTA PRA RESETAR TD
@admin_blueprint.route("/reseta", methods=['POST'])
@login_requerido
def resetar_dados():
    aluno_model.dicie["alunos"] = []
    professor_model.dicie["professores"] = []
    turma_model.dicie["turma"] = []
    return jsonify({"mensagem": "Dados resetados com sucesso!"}), 200

# ---------------- BLUEPRINTS ----------------
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)
app.register_blueprint(turmas_blueprint)
app.register_blueprint(admin_blueprint) 
app.register_blueprint(login_blueprint)

# RODA A API
if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)


#from model.database import db

#db.init_app(app)

#with app.app_context():
#    db.create_all()
