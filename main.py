from flask import Flask, jsonify, request

app = Flask(__name__)

professores = []
turmas = []
alunos = []

#rotas prof
@app.route('/professores', methods=['GET'])
def listar_professores():
    return jsonify(professores)

@app.route('/professores/<int:id_professor>', methods=['GET'])
def obter_professor(id_professor):
    professor = next((p for p in professores if p["id"] == id_professor), None)
    return jsonify(professor) if professor else (jsonify({"erro": "Professor não encontrado"}), 404)

@app.route('/professores', methods=['POST'])
def criar_professor():
    dados = request.json
    novo_professor = {
        "id": len(professores) + 1,
        "nome": dados["nome"],
        "idade": dados["idade"],
        "materia": dados["materia"],
        "observacoes": dados.get("observacoes", "")
    }
    professores.append(novo_professor)
    return jsonify(novo_professor), 201

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def atualizar_professor(id_professor):
    professor = next((p for p in professores if p["id"] == id_professor), None)
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    dados = request.json
    professor.update({
        "nome": dados.get("nome", professor["nome"]),
        "idade": dados.get("idade", professor["idade"]),
        "materia": dados.get("materia", professor["materia"]),
        "observacoes": dados.get("observacoes", professor.get("observacoes", ""))
    })
    return jsonify(professor)


@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def excluir_professor(id_professor):
    global professores
    professores = [p for p in professores if p["id"] != id_professor]
    return jsonify({"mensagem": "Professor removido"}), 200

#rotas turma
@app.route('/turmas', methods=['GET'])
def listar_turmas():
    return jsonify(turmas)

@app.route('/turmas/<int:id_turma>', methods=['GET'])
def obter_turma(id_turma):
    turma = next((t for t in turmas if t["id"] == id_turma), None)
    return jsonify(turma) if turma else (jsonify({"erro": "Turma não encontrada"}), 404)

@app.route('/turmas', methods=['POST'])
def criar_turma():
    dados = request.json
    nova_turma = {
        "id": len(turmas) + 1,
        "descricao": dados["descricao"],
        "professor_id": dados["professor_id"],
        "ativo": dados["ativo"]
    }
    turmas.append(nova_turma)
    return jsonify(nova_turma), 201

@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def atualizar_turma(id_turma):
    turma = next((t for t in turmas if t["id"] == id_turma), None)
    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    dados = request.json
    turma.update({
        "descricao": dados.get("descricao", turma["descricao"]),
        "professor_id": dados.get("professor_id", turma["professor_id"]),
        "ativo": dados.get("ativo", turma["ativo"])
    })
    return jsonify(turma)

@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def excluir_turma(id_turma):
    global turmas
    turmas = [t for t in turmas if t["id"] != id_turma]
    return jsonify({"mensagem": "Turma removida"}), 200

#rotas alunso
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    return jsonify(alunos)

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def obter_aluno(id_aluno):
    aluno = next((a for a in alunos if a["id"] == id_aluno), None)
    return jsonify(aluno) if aluno else (jsonify({"erro": "Aluno não encontrado"}), 404)

@app.route('/alunos', methods=['POST'])
def criar_aluno():
    dados = request.json
    novo_aluno = {
        "id": len(alunos) + 1,
        "nome": dados["nome"],
        "idade": dados["idade"],
        "turma_id": dados["turma_id"],
        "data_nascimento": dados["data_nascimento"],
        "nota_primeiro_semestre": dados["nota_primeiro_semestre"],
        "nota_segundo_semestre": dados["nota_segundo_semestre"],
        "media_final": dados["media_final"]
    }
    alunos.append(novo_aluno)
    return jsonify(novo_aluno), 201

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    aluno = next((a for a in alunos if a["id"] == id_aluno), None)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.json
    aluno.update({
        "nome": dados.get("nome", aluno["nome"]),
        "idade": dados.get("idade", aluno["idade"]),
        "turma_id": dados.get("turma_id", aluno["turma_id"]),
        "data_nascimento": dados.get("data_nascimento", aluno["data_nascimento"]),
        "nota_primeiro_semestre": dados.get("nota_primeiro_semestre", aluno["nota_primeiro_semestre"]),
        "nota_segundo_semestre": dados.get("nota_segundo_semestre", aluno["nota_segundo_semestre"]),
        "media_final": dados.get("media_final", aluno["media_final"])
    })
    return jsonify(aluno)

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def excluir_aluno(id_aluno):
    global alunos
    alunos = [a for a in alunos if a["id"] != id_aluno]
    return jsonify({"mensagem": "Aluno removido"}), 200

if __name__ == '__main__':
    app.run(debug=True)
