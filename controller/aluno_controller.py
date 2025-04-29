from flask import request
from model.aluno_model import AlunoService
from model.turma_model import Turma

def listar_alunos(session):
    return AlunoService.listar_alunos(session), 200

def criar_aluno(session):
    data = request.get_json()
    if not data:
        raise ValueError("Dados não fornecidos")
    if 'id' in data:
        raise ValueError("O ID não deve ser fornecido manualmente")

    aluno = AlunoService.criar_aluno(session, data)
    turma = session.query(Turma).get(data['turma_id'])

    return {
        "mensagem": "Aluno criado com sucesso",
        "aluno": aluno,
        "turma": turma.to_dict() if turma else None
    }, 201

def buscar_aluno_por_id(session, id_aluno):
    aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
    turma = session.query(Turma).get(aluno['turma_id'])
    aluno['turma'] = turma.to_dict() if turma else None
    return aluno, 200

def atualizar_aluno(session, id_aluno):
    data = request.get_json()
    if not data:
        raise ValueError("Dados não fornecidos")
    aluno = AlunoService.atualizar_aluno(session, id_aluno, data)
    turma = session.query(Turma).get(aluno['turma_id'])

    return {
        "mensagem": "Aluno atualizado com sucesso",
        "aluno": aluno,
        "turma": turma.to_dict() if turma else None
    }, 200

def excluir_aluno(session, id_aluno):
    aluno = AlunoService.excluir_aluno(session, id_aluno)
    return {
        "mensagem": "Aluno removido com sucesso",
        "aluno_removido": aluno
    }, 200
