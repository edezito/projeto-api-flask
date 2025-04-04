from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.professor_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, criar_professor, atualizar_professor, excluir_professor

professores_blueprint = Blueprint('professores', __name__)

@professores_blueprint.route('/professores', methods=['GET'])
@login_requerido
def get_professores():
    return jsonify({"professores": listar_professores()}), 200

@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
@login_requerido
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return jsonify({"professor": professor}), 200
    except ProfessorNaoEncontrado:
        return jsonify({"error": "Professor não encontrado"}), 404

@professores_blueprint.route('/professores', methods=['POST'])
@login_requerido
def create_professor():
    data = request.json
    return criar_professor(data)

@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT'])
@login_requerido
def update_professor(id_professor):
    data = request.json
    try:
        return atualizar_professor(id_professor, data)
    except ProfessorNaoEncontrado:
        return jsonify({"error": "Professor não encontrado"}), 404

@professores_blueprint.route('/professores/<int:id_professor>', methods=['DELETE'])
@login_requerido
def delete_professor(id_professor):
    try:
        return excluir_professor(id_professor)
    except ProfessorNaoEncontrado:
        return jsonify({"error": "Professor não encontrado"}), 404