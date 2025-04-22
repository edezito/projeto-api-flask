from functools import wraps
from flask import Blueprint, jsonify, request
from autenticacao import login_requerido
from model.aluno_model import AlunoService
from model.turma_model import Turma  
from config import BancoDados
from sqlalchemy.orm.exc import NoResultFound

alunos_blueprint = Blueprint('alunos', __name__)

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = BancoDados.Session()
        try:
            return func(session, *args, **kwargs)
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        except NoResultFound as e:
            return jsonify({"erro": "Registro não encontrado"}), 404
        except Exception as e:
            session.rollback()
            return jsonify({"erro": str(e)}), 500
        finally:
            session.close()
    return wrapper

@alunos_blueprint.route('/alunos', methods=['GET'])
@login_requerido
@handle_db_errors
def get_alunos(session):
    alunos = AlunoService.listar_alunos(session)
    return jsonify({
        "quantidade": len(alunos),
        "alunos": alunos
    }), 200

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
@login_requerido
@handle_db_errors
def get_aluno(session, id_aluno):
    aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
    
    # Busca informações da turma associada
    turma = session.query(Turma).get(aluno['turma_id'])
    aluno_com_turma = aluno.copy()
    aluno_com_turma['turma'] = turma.to_dict() if turma else None
    
    return jsonify(aluno_com_turma), 200

@alunos_blueprint.route('/alunos', methods=['POST'])
@login_requerido
@handle_db_errors
def create_aluno(session):
    data = request.get_json()
    if not data:
        raise ValueError("Dados não fornecidos")
    
    # Verifica e remove ID se existir
    if 'id' in data:
        raise ValueError("O ID não deve ser fornecido manualmente")
    
    # Cria o aluno e obtém informações da turma
    aluno = AlunoService.criar_aluno(session, data)
    turma = session.query(Turma).get(data['turma_id'])
    
    return jsonify({
        "mensagem": "Aluno criado com sucesso",
        "aluno": aluno,
        "turma": turma.to_dict() if turma else None
    }), 201

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
@login_requerido
@handle_db_errors
def update_aluno(session, id_aluno):
    data = request.get_json()
    if not data:
        raise ValueError("Dados não fornecidos")
    
    # Remove ID se existir para evitar atualização do mesmo
    data.pop('id', None)
    
    aluno = AlunoService.atualizar_aluno(session, id_aluno, data)
    turma = session.query(Turma).get(aluno['turma_id'])
    
    return jsonify({
        "mensagem": "Aluno atualizado com sucesso",
        "aluno": aluno,
        "turma": turma.to_dict() if turma else None
    }), 200

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
@login_requerido
@handle_db_errors
def delete_aluno(session, id_aluno):
    # Primeiro obtém o aluno para retornar informações
    aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
    
    # Depois executa a exclusão
    AlunoService.excluir_aluno(session, id_aluno)
    
    return jsonify({
        "mensagem": "Aluno removido com sucesso",
        "aluno_removido": aluno
    }), 200