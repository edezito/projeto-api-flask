from flask import jsonify, request

dicie = { 
    "alunos": [
        {"id": 1, "nome": "Caio", "idade": 18, "turma_id": 2, "data_nascimento": "28/12/2005", 'nota_primeiro_semestre': 5.6, 'nota_segundo_semestre': 5.6, 'media': 6}
    ]
}

class AlunoNaoEncontrado(Exception):
    pass

#listar alunos
def listar_alunos():
    return jsonify(dicie["alunos"])

#aluno por id
def aluno_por_id(id_aluno):
    lista_alunos = dicie['alunos']
    for dicionario in lista_alunos:
        if dicionario['id'] == id_aluno:
            return dicionario
    raise AlunoNaoEncontrado

#listar aluno
def listar_alunos():
    return jsonify(dicie["alunos"])

#criar aluno
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
    aluno["media_final"] = dados.get("media_final", aluno.get("media_final", 0))

    return jsonify({"mensagem": "Aluno atualizado com sucesso", "aluno": aluno}), 200

#excluir alunos
def excluir_aluno(id_aluno):
    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            dicie["alunos"].remove(aluno)
            return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
    return jsonify({'error': 'Aluno não encontrado'}), 404