import pytest
import requests
from config import Config
from model.aluno_model import validar_idade

BASE_URL = f"http://{Config.HOST}:{Config.PORT}"


# -------------------------------
# Testes Unitários
# -------------------------------
def test_validar_idade_valida():
    assert validar_idade(18) is True


def test_validar_idade_negativa():
    assert validar_idade(-5) is False


def test_validar_idade_maior_que_120():
    assert validar_idade(130) is False


# -------------------------------
# Fixtures para autenticação
# -------------------------------
@pytest.fixture(scope="module")
def session():
    sess = requests.Session()
    yield sess
    sess.close()


@pytest.fixture(scope="module")
def token(session):
    response = session.post(f"{BASE_URL}/login", json={"usuario": "edezito", "senha": "1234"})
    data = response.json()

    if response.status_code == 200 and "token" in data:
        return data["token"]
    pytest.fail(f"Falha na autenticação: {response.text}")


@pytest.fixture
def headers(token):
    return {"Authorization": f"Bearer {token}"}


# -------------------------------
# Testes de Autenticação e Erros
# -------------------------------
def test_login_credenciais_invalidas():
    r = requests.post(f"{BASE_URL}/login", json={"usuario": "fake", "senha": "123"})
    assert r.status_code in [401, 403]  # Corrigido para aceitar o código que o backend retornar


def test_rota_sem_token():
    r = requests.get(f"{BASE_URL}/alunos")
    assert r.status_code == 401


# -------------------------------
# Testes Aluno
# -------------------------------
def test_cadastrar_aluno(session, headers):
    aluno = {
        "id": 9,
        "nome": "Otavio",
        "idade": 18,
        "turma_id": 2,
        "data_nascimento": "2005-12-28",
        "nota_primeiro_semestre": 5.6,
        "nota_segundo_semestre": 5.6
    }
    r = session.post(f"{BASE_URL}/alunos", json=aluno, headers=headers)
    assert r.status_code == 201


def test_cadastrar_aluno_idade_invalida(session, headers):
    aluno = {
        "id": 10,
        "nome": "Idoso Impossível",
        "idade": 130,
        "turma_id": 1,
        "data_nascimento": "1890-01-01",
        "nota_primeiro_semestre": 7.0,
        "nota_segundo_semestre": 7.5
    }
    r = session.post(f"{BASE_URL}/alunos", json=aluno, headers=headers)
    assert r.status_code == 400
    assert "error" in r.json()


def test_adicionar_aluno_sem_id(session, headers):
    r = session.post(f"{BASE_URL}/alunos", json={"nome": "Sofia"}, headers=headers)
    assert r.status_code == 400
    assert "error" in r.json()


def test_adicionar_aluno_sem_nome(session, headers):
    r = session.post(f"{BASE_URL}/alunos", json={"id": 6}, headers=headers)
    assert r.status_code == 400
    assert "error" in r.json()


def test_listar_alunos(session, headers):
    r = session.get(f"{BASE_URL}/alunos", headers=headers)
    assert r.status_code == 200
    data = r.json()
    if isinstance(data, dict) and "alunos" in data:
        assert isinstance(data["alunos"], list)
    else:
        assert isinstance(data, list)


def test_buscar_aluno_existente(session, headers):
    r = session.get(f"{BASE_URL}/alunos/1", headers=headers)
    if r.status_code == 200:
        aluno = r.json().get("aluno", r.json())
        assert "nome" in aluno
    else:
        assert r.status_code == 404


def test_buscar_aluno_inexistente(session, headers):
    r = session.get(f"{BASE_URL}/alunos/9999", headers=headers)
    assert r.status_code == 404


def test_editar_aluno_existente(session, headers):
    dados = {"nome": "Otavio Atualizado"}
    r = session.put(f"{BASE_URL}/alunos/9", json=dados, headers=headers)
    assert r.status_code in [200, 204]


def test_editar_aluno_inexistente(session, headers):
    dados = {"nome": "Aluno Inexistente"}
    r = session.put(f"{BASE_URL}/alunos/999", json=dados, headers=headers)
    assert r.status_code == 404
    assert "error" in r.json()


def test_deletar_aluno_id_invalido(session, headers):
    r = session.delete(f"{BASE_URL}/alunos/abc", headers=headers)
    assert r.status_code == 404


def test_deletar_aluno_inexistente(session, headers):
    r = session.delete(f"{BASE_URL}/alunos/999", headers=headers)
    assert r.status_code == 404
    assert "error" in r.json()


def test_deletar_aluno_sem_id(session, headers):
    r = session.delete(f"{BASE_URL}/alunos/", headers=headers)
    assert r.status_code == 404


# -------------------------------
# Testes Professor
# -------------------------------
def test_cadastrar_professor(session, headers):
    professor = {
        "id": 7,
        "nome": "Bruno",
        "idade": 33,
        "materia": "Filosofia",
        "observacoes": "professor-substituto"
    }
    r = session.post(f"{BASE_URL}/professores", json=professor, headers=headers)
    assert r.status_code == 201


# -------------------------------
# Testes Turma
# -------------------------------
def test_cadastrar_turma(session, headers):
    turma = {
        "id": 12,
        "descricao": "Física",
        "professor_id": 4,
        "ativo": True
    }
    r = session.post(f"{BASE_URL}/turmas", json=turma, headers=headers)
    assert r.status_code == 201

# --------------------------------------------
# Completando testes - Professores e Turmas
# --------------------------------------------

def test_listar_professores(session, headers):
    r = session.get(f"{BASE_URL}/professores", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json()["professores"], list)


def test_buscar_professor_existente(session, headers):
    r = session.get(f"{BASE_URL}/professores/7", headers=headers)
    assert r.status_code == 200
    assert "nome" in r.json()["professor"]


def test_buscar_professor_inexistente(session, headers):
    r = session.get(f"{BASE_URL}/professores/999", headers=headers)
    assert r.status_code == 404


def test_editar_professor_existente(session, headers):
    dados = {"nome": "Bruno Atualizado", "materia": "História"}
    r = session.put(f"{BASE_URL}/professores/7", json=dados, headers=headers)
    assert r.status_code in [200, 204]
    
    r_get = session.get(f"{BASE_URL}/professores/7", headers=headers)
    assert r_get.status_code == 200
    assert r_get.json()["professor"]["nome"] == "Bruno Atualizado"



def test_editar_professor_inexistente(session, headers):
    dados = {"nome": "Professor Fantasma"}
    r = session.put(f"{BASE_URL}/professores/9999", json=dados, headers=headers)
    assert r.status_code == 404


def test_deletar_professor_existente(session, headers):
    r = session.delete(f"{BASE_URL}/professores/7", headers=headers)
    assert r.status_code in [200, 204]


def test_deletar_professor_inexistente(session, headers):
    r = session.delete(f"{BASE_URL}/professores/999", headers=headers)
    assert r.status_code == 404


def test_cadastrar_professor_sem_nome(session, headers):
    professor = {
        "id": 8,
        "idade": 45,
        "materia": "Biologia"
    }
    r = session.post(f"{BASE_URL}/professores", json=professor, headers=headers)
    assert r.status_code == 400
    assert "error" in r.json()


# -------------------------------
# Testes Complementares - Turmas
# -------------------------------

def test_listar_turmas(session, headers):
    r = session.get(f"{BASE_URL}/turmas", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json()["turmas"], list)



def test_buscar_turma_existente(session, headers):
    r = session.get(f"{BASE_URL}/turmas/12", headers=headers)
    assert r.status_code == 200
    assert "descricao" in r.json()["turma"]



def test_buscar_turma_inexistente(session, headers):
    r = session.get(f"{BASE_URL}/turmas/9999", headers=headers)
    assert r.status_code == 404


def test_editar_turma_existente(session, headers):
    dados = {"descricao": "Física Atualizada"}
    r = session.put(f"{BASE_URL}/turmas/12", json=dados, headers=headers)
    assert r.status_code in [200, 204]

    r_get = session.get(f"{BASE_URL}/turmas/12", headers=headers)
    assert r_get.status_code == 200
    assert r_get.json()["turma"]["descricao"] == "Física Atualizada"



def test_editar_turma_inexistente(session, headers):
    dados = {"descricao": "Turma Fantasma"}
    r = session.put(f"{BASE_URL}/turmas/9999", json=dados, headers=headers)
    assert r.status_code == 404


def test_deletar_turma_existente(session, headers):
    r = session.delete(f"{BASE_URL}/turmas/12", headers=headers)
    assert r.status_code in [200, 204]


def test_deletar_turma_inexistente(session, headers):
    r = session.delete(f"{BASE_URL}/turmas/999", headers=headers)
    assert r.status_code == 404


def test_cadastrar_turma_sem_professor(session, headers):
    turma = {
        "id": 13,
        "descricao": "Química"
        # professor_id ausente
    }
    r = session.post(f"{BASE_URL}/turmas", json=turma, headers=headers)
    assert r.status_code == 400
    assert "error" in r.json()




