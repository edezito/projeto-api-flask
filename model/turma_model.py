from flask import jsonify
from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import BancoDados

Base = BancoDados.Base
class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento com os alunos
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": self.ativo
        }

'''
dicie = {
    "turmas": [
        {"id": 3, "descricao": "Português", "professor_id": 2, "ativo": True}
    ]
}
'''
class TurmaNaoEncontrada(Exception):
    pass

# Listar turmas
def listar_turmas():
    return dicie["turmas"]

# Buscar turma por ID
def turma_por_id(id_turma):
    for turma in dicie["turmas"]:
        if turma["id"] == id_turma:
            return turma
    raise TurmaNaoEncontrada

# Criar turma
def criar_turma(dados):
    if "id" not in dados or "descricao" not in dados or "professor_id" not in dados:
        return jsonify({"error": "Faltam campos obrigatórios"}), 400
    
    if any(t["id"] == dados["id"] for t in dicie["turmas"]):
        return jsonify({"error": "ID já existente"}), 400
    
    nova_turma = {
        "id": dados["id"],
        "descricao": dados["descricao"],
        "professor_id": dados["professor_id"],
        "ativo": dados.get("ativo", True)
    }
    dicie["turmas"].append(nova_turma)
    return jsonify(nova_turma), 201

# Atualizar turma
def atualizar_turma(id_turma, dados):
    turma = next((t for t in dicie["turmas"] if t["id"] == id_turma), None)
    if turma is None:
        raise TurmaNaoEncontrada
    
    turma.update({
        "descricao": dados.get("descricao", turma["descricao"]),
        "professor_id": dados.get("professor_id", turma["professor_id"]),
        "ativo": dados.get("ativo", turma["ativo"])
    })
    
    return jsonify({"mensagem": "Turma atualizada", "turma": turma}), 200

# Excluir turma
def excluir_turma(id_turma):
    for turma in dicie["turmas"]:
        if turma["id"] == id_turma:
            dicie["turmas"].remove(turma)
            return jsonify({"mensagem": "Turma removida com sucesso"}), 200
    raise TurmaNaoEncontrada
