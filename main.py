from flask import Flask, jsonify, request
from autenticacao import login_requerido
from routes.aluno_routes import alunos_blueprint
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

#ROTAS
#resetar
@app.route("/reseta", methods=['POST'])
@login_requerido
def resetar_professor():
    dicie["alunos"] = []
    dicie["professores"] = []
    dicie["turma"] = []
    return jsonify({"mensagem": "Dados resetados com sucesso!"}), 200
#PROFESSOR
# exibir professor
@app.route('/professores', methods=['GET'])
@login_requerido
def listar_professores():
    return jsonify({
        "mensagem": "Bem-vindo à página de professores!",
        "turma": dicie["turma"]
    }), 200
    

#exibir professor pelo id
@app.route('/professores/<int:id_professor>', methods=['GET'])
def obter_professor(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            return jsonify(professor)
    return jsonify({"error": "Professor não encontrado"}), 404

#criar um professor
@app.route('/professores', methods=['POST'])
def criar_professor():
    dados = request.json
    novo_professor = {"id": dados["id"], "nome": dados["nome"]}
    dicie["professores"].append(novo_professor)
    return jsonify(novo_professor), 201

#atualizar um professor
@app.route('/professores/<int:id_professor>', methods=['PUT'])
def atualizar_professor(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            dados = request.json
            nome_atualizado = dados.get("nome")
            if nome_atualizado:
                professor["nome"] = nome_atualizado
            return jsonify({"message": "Professor atualizado com sucesso", "professor": professor})
    return jsonify({"error": "Professor não encontrado"}), 404

#deletar um professor
@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def excluir_professor(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            dicie["professores"].remove(professor)
            return jsonify({"mensagem": "Professor removido com sucesso"})
    return jsonify({"error": "Professor não encontrado"}), 404


#TURMAS
#exibir turmas
@app.route('/turmas', methods=['GET'])
def listar_turmas():
    return jsonify(dicie["turma"])

#exibir turmas pelo id
@app.route('/turmas/<int:id_turma>', methods=['GET'])
def obter_turma(id_turma):
    for turma in dicie["turma"]:
        if turma["id"] == id_turma:
            return jsonify(turma)

#criar turmas
@app.route('/turmas', methods=['POST'])
def criar_turma():
    dados = request.json
    nova_turma = {"id": dados["id"], "nome": dados["nome"]}
    dicie["turma"].append(nova_turma)
    return jsonify(nova_turma), 201

#atualizar turmas
@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def atualizar_turma(id_turma):
    for turma in dicie["turma"]:
        if turma["id"] ==  id_turma:
            dados = request.json
            turma["nome"] = dados.get("nome", turma["nome"])
            return jsonify(turma)
    return jsonify({"error": "Turma não encontrado"}), 404

#deletar turma
@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def excluir_turma(id_turma):
    for turma in dicie["turma"]:
        if turma["id"] == id_turma:
            dicie["turma"].remove(turma)
            return jsonify({"mensagem": "Turma removida com sucesso"})
    return jsonify({"error": "Turma não encontrada"}), 404


# ---------------- ALUNOS ----------------
app.register_blueprint(alunos_blueprint)

# ---------------- LOGIN ----------------
app.register_blueprint(login_blueprint)

#roda essa api logo
if __name__ == '__main__':
    app.run(debug=True)


