from functools import wraps
from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.professor_model import ProfessorService, ProfessorNaoEncontrado

professores_blueprint = Blueprint('professores', __name__)

@professores_blueprint.route('/professores', methods=['GET'])
@login_requerido
def get_professores():
    try:
        lista = ProfessorService.listar_professores()
        return jsonify({"professores": lista}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
@login_requerido
def get_professor(id_professor):
    try:
        prof = ProfessorService.professor_por_id(id_professor)
        return jsonify({"professor": prof}), 200
    except ProfessorNaoEncontrado:
        return jsonify({"error": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@professores_blueprint.route('/professores', methods=['POST'])
@login_requerido
def create_professor():
    data = request.json
    result, code = ProfessorService.criar_professor(data)
    return jsonify(result), code

@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT'])
@login_requerido
def update_professor(id_professor):
    data = request.json
    try:
        result, code = ProfessorService.atualizar_professor(id_professor, data)
        return jsonify(result), code
    except ProfessorNaoEncontrado:
        return jsonify({"error": "Professor não encontrado"}), 404

@professores_blueprint.route('/professores/<int:id_professor>', methods=['DELETE'])
@login_requerido
def delete_professor(id_professor):
    try:
        result, code = ProfessorService.excluir_professor(id_professor)
        return jsonify(result), code
    except ProfessorNaoEncontrado:
        return jsonify({"error": "Professor não encontrado"}), 404
