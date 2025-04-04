from flask import jsonify, request

dicie = {
    "turmas": [
        {"id": 3, "nome": "Português"}
    ]
}

class TurmaNaoEncontrada(Exception):
    pass

# Listar turmas
def listar_turmas():
    return dicie["turmas"]

# Buscar turma por ID
def turma_por_id(id_turma):
    for turma in dicie["turmas"]:
        if turma["id"] == id_turma:
            return turma
    raise TurmaNaoEncontrada

# Criar turma
def criar_turma(dados):
    if "id" not in dados or "nome" not in dados:
        return jsonify({"error": "Faltam campos obrigatórios"}), 400
    
    nova_turma = {"id": dados["id"], "nome": dados["nome"]}
    dicie["turmas"].append(nova_turma)
    return jsonify(nova_turma), 201

# Atualizar turma
def atualizar_turma(id_turma, dados):
    turma = next((t for t in dicie["turmas"] if t["id"] == id_turma), None)
    if turma is None:
        raise TurmaNaoEncontrada
    
    turma["nome"] = dados.get("nome", turma["nome"])
    return jsonify({"mensagem": "Turma atualizada", "turma": turma}), 200

# Excluir turma
def excluir_turma(id_turma):
    for turma in dicie["turmas"]:
        if turma["id"] == id_turma:
            dicie["turmas"].remove(turma)
            return jsonify({"mensagem": "Turma removida com sucesso"}), 200
    raise TurmaNaoEncontrada
