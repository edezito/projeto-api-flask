from flask import Flask, jsonify, request, redirect, render_template_string, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "projeto-escola"

#BANCO DE DADOS
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

dicie = { 
    "alunos": [
        {"id": 1, "nome": "Caio"}
    ],
    "professores": [
        {"id": 2, "nome": "João"}
    ],
    "turma": [
        {"id": 3, "nome": "Português"}
    ],
   "usuarios": {
        "edezito": Usuario("Eder", "edezito", "1234"),
        "felipe": Usuario("Felipe", "felipe", "senha"),
        "vitor": Usuario("Victor", "vitor", "abcd")
    }
}

#AUTENTICAÇÃO
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado'):
            return jsonify({
                "erro": "Usuário não autenticado",
                "redirecionar": "/login"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["POST"])
def autenticar():
    dados = request.get_json() or {}
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    usuario_obj = dicie["usuarios"].get(usuario)

    if usuario_obj and usuario_obj.senha == senha:
        session['usuario_logado'] = usuario_obj.nickname
        return jsonify({"mensagem": "Login bem-sucedido", "usuario": usuario_obj.nickname}), 200

    return jsonify({"erro": "Usuário ou senha inválidos"}), 403

@app.route('/logout', methods=["POST"])
def logout():
    if 'usuario_logado' in session:
        session.pop('usuario_logado')
        return jsonify({"mensagem": "Logout realizado com sucesso"}), 200
    else:
        return jsonify({"erro": "Nenhum usuário estava logado"}), 400


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

#ALUNOS
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
            return jsonify({"error": "ID duplicado"}), 400  # Retorna erro 400 se o ID for duplicado

    # Verificando se o nome foi fornecido
    if 'nome' not in dados:
        return jsonify({'error': 'Falta nome'}), 400
    
    # Se o ID não for duplicado, adiciona o novo aluno
    novo_aluno = {"id": dados['id'], "nome": dados["nome"]}
    dicie["alunos"].append(novo_aluno)
    
    return jsonify(novo_aluno), 201

#atualizar aluno
@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    dados = request.json 

    # Verifica se o campo "nome" foi enviado
    if "nome" not in dados:
        return jsonify({"error": "O campo 'nome' é obrigatório"}), 400

    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            aluno["nome"] = dados.get("nome", aluno["nome"])  # Atualiza o nome
            return jsonify({"mensagem": "Aluno atualizado com sucesso", "aluno": aluno}), 200


    return jsonify({"error": "Aluno não encontrado"}), 404

#deletar um aluno
@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def excluir_aluno(id_aluno):
    for aluno in dicie["alunos"]:
        if aluno["id"] == id_aluno:
            dicie["alunos"].remove(aluno)
            return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
    return jsonify({'error': 'Aluno não encontrado'}), 404


#roda essa api logo
if __name__ == '__main__':
    app.run(debug=True)


