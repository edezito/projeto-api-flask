from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.turma_model import TurmaNaoEncontrada, listar_turmas, turma_por_id, criar_turma, atualizar_turma, excluir_turma

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/turmas', methods=['GET'])
@login_requerido
def get_turmas():
    return jsonify({"turmas": listar_turmas()}), 200

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
@login_requerido
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return jsonify({"turma": turma}), 200
    except TurmaNaoEncontrada:
        return jsonify({"error": "Turma não encontrada"}), 404

@turmas_blueprint.route('/turmas', methods=['POST'])
@login_requerido
def create_turma():
    data = request.json
    return criar_turma(data)

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT'])
@login_requerido
def update_turma(id_turma):
    data = request.json
    try:
        return atualizar_turma(id_turma, data)
    except TurmaNaoEncontrada:
        return jsonify({"error": "Turma não encontrada"}), 404

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['DELETE'])
@login_requerido
def delete_turma(id_turma):
    try:
        return excluir_turma(id_turma)
    except TurmaNaoEncontrada:
        return jsonify({"error": "Turma não encontrada"}), 404
