from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.aluno_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, criar_aluno, atualizar_aluno, excluir_aluno

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
@login_requerido
def get_alunos():
    return jsonify(listar_alunos())

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
@login_requerido
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    
@alunos_blueprint.route('/alunos', methods=['POST'])
@login_requerido
def create_aluno():
    data = request.json
    criar_aluno(data)
    return jsonify(data), 201

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
@login_requerido
def update_aluno(id_aluno):
    data = request.json
    try:
        atualizar_aluno(id_aluno, data)
        return jsonify(aluno_por_id(id_aluno))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
@login_requerido
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return '', 204
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404