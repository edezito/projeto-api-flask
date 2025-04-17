from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from config import BancoDados
from flask import jsonify

Base = BancoDados.Base

class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    disciplina = Column(String, nullable=False)
    salario = Column(Float, nullable=False)

    output = relationship("ProfessorOutput", back_populates="professor", 
                         uselist=False, cascade="all, delete-orphan")

class ProfessorOutput(Base):
    __tablename__ = 'professor_outputs'
    
    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('professores.id'))
    # Adicione outros campos específicos da saída do professor
    
    # Relacionamento de volta para Professor
    professor = relationship("Professor", back_populates="output")

'''
dicie = {
    "professores": [
        {"id": 2, "nome": "João", "idade": 33, "materia": "Historia", "observacoes": "professor-novo" }
    ]
}
'''

class ProfessorNaoEncontrado(Exception):
    pass

# Listar professores
def listar_professores():
    return dicie["professores"]

# Buscar professor por ID
def professor_por_id(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            return professor
    raise ProfessorNaoEncontrado

# Criar professor
def criar_professor(dados):
    if "id" not in dados or "nome" not in dados or "idade" not in dados or "materia" not in dados:
        return jsonify({"error": "Faltam campos obrigatórios"}), 400
    
    if any(prof["id"] == dados["id"] for prof in dicie["professores"]):
        return jsonify({"error": "ID já existente"}), 400
    
    novo_professor = {
        "id": dados["id"],
        "nome": dados["nome"],
        "idade": dados["idade"],
        "materia": dados["materia"],
        "observacoes": dados.get("observacoes", "")
    }
    dicie["professores"].append(novo_professor)
    return jsonify(novo_professor), 201

# Atualizar professor
def atualizar_professor(id_professor, dados):
    professor = next((p for p in dicie["professores"] if p["id"] == id_professor), None)
    if professor is None:
        raise ProfessorNaoEncontrado
    
    professor.update({
        "nome": dados.get("nome", professor["nome"]),
        "idade": dados.get("idade", professor["idade"]),
        "materia": dados.get("materia", professor["materia"]),
        "observacoes": dados.get("observacoes", professor.get("observacoes", ""))
    })
    
    return jsonify({"mensagem": "Professor atualizado", "professor": professor}), 200

# Excluir professor
def excluir_professor(id_professor):
    for professor in dicie["professores"]:
        if professor["id"] == id_professor:
            dicie["professores"].remove(professor)
            return jsonify({"mensagem": "Professor removido com sucesso"}), 200
    raise ProfessorNaoEncontrado

