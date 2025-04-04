from flask import jsonify, request

dicie = { 
    "alunos": [
        {"id": 1, "nome": "Caio", "idade": 18, "turma_id": 2, "data_nascimento": "28/12/2005", 
         "nota_primeiro_semestre": 5.6, "nota_segundo_semestre": 5.6, "media": 6}
    ]
}

class AlunoNaoEncontrado(Exception):
    pass

# Listar alunos
def listar_alunos():
    return dicie["alunos"]

# Buscar aluno por ID
def aluno_por_id(id_aluno):
    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado

# Criar aluno
def criar_aluno(dados):
    # Verifica se o ID foi fornecido
    if 'id' not in dados:
        return ({"error": "Falta ID"}), 400
    
    # Verifica se o ID já existe
    if any(aluno["id"] == dados["id"] for aluno in dicie["alunos"]):
        return ({"error": "ID duplicado"}), 400

    # Verifica se todos os campos obrigatórios estão presentes
    if not all(key in dados for key in ["nome", "idade", "turma_id", "data_nascimento"]):
        return ({"error": "Faltam campos obrigatórios"}), 400

    # Calcula a média das notas
    nota_primeiro = dados.get("nota_primeiro_semestre", 0)
    nota_segundo = dados.get("nota_segundo_semestre", 0)
    media = (nota_primeiro + nota_segundo) / 2

    # Cria o novo aluno
    novo_aluno = {
        "id": dados["id"],
        "nome": dados["nome"],
        "idade": dados["idade"],
        "turma_id": dados["turma_id"],
        "data_nascimento": dados["data_nascimento"],
        "nota_primeiro_semestre": nota_primeiro,
        "nota_segundo_semestre": nota_segundo,
        "media": media
    }

    dicie["alunos"].append(novo_aluno)
    return ({"mensagem": "Aluno criado com sucesso", "aluno": novo_aluno}), 201

# Atualizar aluno
def atualizar_aluno(id_aluno, dados):
    aluno = next((a for a in dicie["alunos"] if a["id"] == id_aluno), None)
    if aluno is None:
        raise AlunoNaoEncontrado

    # Atualiza os dados fornecidos
    aluno.update({
        "nome": dados.get("nome", aluno["nome"]),
        "idade": dados.get("idade", aluno["idade"]),
        "turma_id": dados.get("turma_id", aluno["turma_id"]),
        "data_nascimento": dados.get("data_nascimento", aluno["data_nascimento"]),
        "nota_primeiro_semestre": dados.get("nota_primeiro_semestre", aluno["nota_primeiro_semestre"]),
        "nota_segundo_semestre": dados.get("nota_segundo_semestre", aluno["nota_segundo_semestre"])
    })

    aluno["media"] = (aluno["nota_primeiro_semestre"] + aluno["nota_segundo_semestre"]) / 2

    return ({"mensagem": "Aluno atualizado com sucesso", "aluno": aluno}), 200

# Excluir aluno
def excluir_aluno(id_aluno):
    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            dicie["alunos"].remove(aluno)
            return ({"mensagem": "Aluno removido com sucesso"}), 200
    raise AlunoNaoEncontrado