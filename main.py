from flask import Flask, jsonify, request
from autenticacao import login_requerido

from routes.aluno_routes import alunos_blueprint
from routes.professor_routes import professores_blueprint
from routes.turma_routes import turmas_blueprint
from autenticacao import login_blueprint

app = Flask(__name__)
app.secret_key = "projeto-escola"

dicie = { 
    "professores": [
        {"id": 2, "nome": "João"}
    ],
    "turma": [
        {"id": 3, "nome": "Português"}
    ],
}

# ROTA PRA RESETAR TD
@app.route("/reseta", methods=['POST'])
@login_requerido
def resetar_professor():
    dicie["alunos"] = []
    dicie["professores"] = []
    dicie["turma"] = []
    return jsonify({"mensagem": "Dados resetados com sucesso!"}), 200

# ---------------- BLUEPRINTS ----------------
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)
app.register_blueprint(turmas_blueprint)

# LOGIN
app.register_blueprint(login_blueprint)

# RODA A API
if __name__ == '__main__':
    app.run(debug=True)
