from functools import wraps
from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.turma_model import TurmaService, TurmaNaoEncontrada

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/turmas', methods=['GET'])
@login_requerido
def get_turmas():
    try:
        lista = TurmaService.listar_turmas()
        return jsonify({"turmas": lista}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
@login_requerido
def get_turma(id_turma):
    try:
        turma = TurmaService.turma_por_id(id_turma)
        return jsonify({"turma": turma}), 200
    except TurmaNaoEncontrada:
        return jsonify({"error": "Turma não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@turmas_blueprint.route('/turmas', methods=['POST'])
@login_requerido
def create_turma():
    data = request.json
    result, code = TurmaService.criar_turma(data)
    return jsonify(result), code

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT'])
@login_requerido
def update_turma(id_turma):
    data = request.json
    try:
        result, code = TurmaService.atualizar_turma(id_turma, data)
        return jsonify(result), code
    except TurmaNaoEncontrada:
        return jsonify({"error": "Turma não encontrada"}), 404

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['DELETE'])
@login_requerido
def delete_turma(id_turma):
    try:
        result, code = TurmaService.excluir_turma(id_turma)
        return jsonify(result), code
    except TurmaNaoEncontrada:
        return jsonify({"error": "Turma não encontrada"}), 404
