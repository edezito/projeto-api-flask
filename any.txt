from flask import Flask, jsonify, request

app = Flask(__name__)

#rotas prof

dicie = { 
    "alunos": [
        {"id": 1, "nome": "Caio", "idade": 18, "turma_id": 2, "data_nascimento": "28/12/2005", 'nota_primeiro_semestre': 5.6, 'nota_segundo_semestre': 5.6, 'media': 6}
    ],
    "professores": [
        {"id": 2, "nome": "João", "idade": 36, "materia": "Produção de Textos", "observacoes": "novo-professor"}
    ],
    "turma": [
        {"id": 3, "descricao": "Português", "professor_id": 2, "status": True}
    ]
}

#resetar
@app.route("/reseta", methods=['POST'])
def resetar_professor():
    dicie["alunos"] = []
    dicie["professores"] = []
    dicie["turma"] = []
    return jsonify({"mensagem": "Dados resetados com sucesso!"}), 200

# ---------------- PROFESSORES ----------------
# exibir professor
@app.route('/professores', methods=['GET'])
def listar_professores():
    return jsonify(dicie["professores"])

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

    if 'id' not in dados:
        return jsonify({'error': 'Falta ID'}), 400
    
    for professor in dicie["professores"]:
        if professor["id"] == dados["id"]:
            return jsonify({"error": "ID duplicado"}), 400
    
    if 'nome' not in dados or 'idade' not in dados or 'materia' not in dados or 'observacoes' not in dados:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400
    
    novo_professor = {
        "id": dados["id"],
        "nome": dados["nome"],
        "idade": dados["idade"],
        "materia": dados["materia"],
        "observacoes": dados["observacoes"]
    }
    
    dicie["professores"].append(novo_professor)
    return jsonify({"status": "success", "data": novo_professor}), 201

#atualizar um professor
@app.route('/professores/<int:id_professor>', methods=['PUT'])
def atualizar_professor(id_professor):
    dados = request.json

    if 'nome' not in dados:
        return jsonify({'error': 'Nome é obrigatório'}), 400

    professor = next((p for p in dicie["professores"] if p["id"] == id_professor), None)
    if professor is None:
        return jsonify({"error": "Professor não encontrado"}), 404

    professor["nome"] = dados.get("nome", professor["nome"])
    professor["idade"] = dados.get("idade", professor["idade"])
    professor["materia"] = dados.get("materia", professor["materia"])
    professor["observacoes"] = dados.get("observacoes", professor["observacoes"])

    return jsonify({"message": "Professor atualizado com sucesso", "professor": professor}), 200

#deletar um professor
@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def excluir_professor(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            dicie["professores"].remove(professor)
            return jsonify({"mensagem": "Professor removido com sucesso"})
    return jsonify({"error": "Professor não encontrado"}), 404


# ---------------- TURMAS ----------------
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
    return jsonify({"error": "Turma não encontrada"}), 404

#criar turmas
@app.route('/turmas', methods=['POST'])
def criar_turma():
    dados = request.json

    # Verificando se o ID foi fornecido
    if 'id' not in dados:
        return jsonify({'error': 'Falta ID'}), 400
    
    # Verificar se o ID da turma já existe
    for turma in dicie["turma"]:
        if turma["id"] == dados["id"]:
            return jsonify({"error": "ID duplicado"}), 400

    # Verificando se a descrição, professor_id e status foram fornecidos
    if 'descricao' not in dados or 'professor_id' not in dados or 'status' not in dados:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400
    
    nova_turma = {
        "id": dados["id"],
        "descricao": dados["descricao"],
        "professor_id": dados["professor_id"],
        "status": dados["status"]
    }
    dicie["turma"].append(nova_turma)
    return jsonify(nova_turma), 201

#atualizar turmas
@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def atualizar_turma(id_turma):
    for turma in dicie["turma"]:
        if turma["id"] == id_turma:
            dados = request.json
            turma["descricao"] = dados.get("descricao", turma["descricao"])
            turma["professor_id"] = dados.get("professor_id", turma["professor_id"])
            turma["status"] = dados.get("status", turma["status"])
            return jsonify({"message": "Turma atualizada com sucesso", "turma": turma})
    
    return jsonify({"error": "Turma não encontrada"}), 404

#deletar turma
@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def excluir_turma(id_turma):
    for turma in dicie["turma"]:
        if turma["id"] == id_turma:
            dicie["turma"].remove(turma)
            return jsonify({"mensagem": "Turma removida com sucesso"})
    return jsonify({"error": "Turma não encontrada"}), 404

# ---------------- ALUNOS ----------------
#exibir alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    return jsonify(dicie["alunos"])

#exibir alunos pelo id
@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def obter_aluno(id_aluno):
    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            return jsonify(aluno)
    return jsonify({'error': 'Aluno não encontrado'}), 404

#criar aluno
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    dados = request.json

    # Verificando se o ID foi fornecido
    if 'id' not in dados:
        return jsonify({'error': 'Falta ID'}), 400
    
    # Verificar se o ID do aluno já existe
    for aluno in dicie["alunos"]:
        if aluno["id"] == dados["id"]:
            return jsonify({"error": "ID duplicado"}), 400

    # Verificando se os campos obrigatórios foram fornecidos
    if 'nome' not in dados or 'idade' not in dados or 'turma_id' not in dados or 'data_nascimento' not in dados:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400
    
    novo_aluno = {
        "id": dados['id'],
        "nome": dados["nome"],
        "idade": dados.get("idade", None),
        "turma_id": dados.get("turma_id", None),
        "data_nascimento": dados.get("data_nascimento", None),
        "nota_primeiro_semestre": dados.get("nota_primeiro_semestre", 0),
        "nota_segundo_semestre": dados.get("nota_segundo_semestre", 0),
        "media": (dados.get("nota_primeiro_semestre", 0) + dados.get("nota_segundo_semestre", 0)) / 2

    }

    dicie["alunos"].append(novo_aluno)
    print("Alunos após adição:", dicie["alunos"]) 
    return jsonify(novo_aluno), 201

#atualizar aluno
@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    dados = request.json

    if 'nome' not in dados:
        return jsonify({'error': 'Nome é obrigatório'}), 400

    aluno = next((a for a in dicie["alunos"] if a["id"] == id_aluno), None)
    if aluno is None:
        return jsonify({'error': 'ID inválido'}), 404

    aluno["nome"] = dados.get("nome", aluno["nome"])
    aluno["idade"] = dados.get("idade", aluno["idade"])
    aluno["turma_id"] = dados.get("turma_id", aluno["turma_id"])
    aluno["data_nascimento"] = dados.get("data_nascimento", aluno["data_nascimento"])
    aluno["nota_primeiro_semestre"] = dados.get("nota_primeiro_semestre", aluno["nota_primeiro_semestre"])
    aluno["nota_segundo_semestre"] = dados.get("nota_segundo_semestre", aluno["nota_segundo_semestre"])
    aluno["media_final"] = dados.get("media_final", aluno["media_final"])

    return jsonify({"mensagem": "Aluno atualizado com sucesso", "aluno": aluno}), 200


#deletar um aluno
@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def excluir_aluno(id_aluno):
    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            dicie["alunos"].remove(aluno)
            return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
    return jsonify({'error': 'Aluno não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)


