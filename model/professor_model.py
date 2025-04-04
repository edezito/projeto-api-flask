from flask import jsonify, request

dicie = {
    "professores": [
        {"id": 2, "nome": "João"}
    ]
}

class ProfessorNaoEncontrado(Exception):
    pass

# Listar professores
def listar_professores():
    return dicie["professores"]

# Buscar professor por ID
def professor_por_id(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            return professor
    raise ProfessorNaoEncontrado

# Criar professor
def criar_professor(dados):
    if "id" not in dados or "nome" not in dados:
        return jsonify({"error": "Faltam campos obrigatórios"}), 400
    
    if any(prof["id"] == dados["id"] for prof in dicie["professores"]):
        return jsonify({"error": "ID já existente"}), 400
    
    novo_professor = {"id": dados["id"], "nome": dados["nome"]}
    dicie["professores"].append(novo_professor)
    return jsonify(novo_professor), 201

# Atualizar professor
def atualizar_professor(id_professor, dados):
    professor = next((p for p in dicie["professores"] if p["id"] == id_professor), None)
    if professor is None:
        raise ProfessorNaoEncontrado
    
    professor["nome"] = dados.get("nome", professor["nome"])
    return jsonify({"mensagem": "Professor atualizado", "professor": professor}), 200

# Excluir professor
def excluir_professor(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            dicie["professores"].remove(professor)
            return jsonify({"mensagem": "Professor removido com sucesso"}), 200
    raise ProfessorNaoEncontrado

