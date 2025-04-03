from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.aluno_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, criar_aluno, atualizar_aluno, excluir_aluno

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
@login_requerido
def get_alunos():
    return jsonify({"alunos": listar_alunos()}), 200

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
@login_requerido
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify({"aluno": aluno}), 200
    except AlunoNaoEncontrado:
        return jsonify({"error": "Aluno não encontrado"}), 404
    
@alunos_blueprint.route('/alunos', methods=['POST'])
@login_requerido
def create_aluno():
    data = request.json
    resultado, status_code = criar_aluno(data)
    return jsonify(resultado), status_code

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
@login_requerido
def update_aluno(id_aluno):
    data = request.json
    try:
        atualizar_aluno(id_aluno, data)
        return jsonify({"mensagem": "Aluno atualizado com sucesso", "aluno": aluno_por_id(id_aluno)}), 200
    except AlunoNaoEncontrado:
        return jsonify({"error": "Aluno não encontrado"}), 404
    
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
@login_requerido
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
    except AlunoNaoEncontrado:
        return jsonify({"error": "Aluno não encontrado"}), 404