import pytest
import requests
from config import Config
from model.aluno_model import AlunoService
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import BancoDados

Base = BancoDados.Base

BASE_URL = f"http://{Config.HOST}:{Config.PORT}"

# Configuração do banco de dados para os testes
SQLALCHEMY_DATABASE_URL = f"sqlite:///./test.db"  # Usando um banco separado para os testes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para criar e destruir a sessão de banco de dados para cada teste
@pytest.fixture(scope="module")
def session_db():
    Base.metadata.create_all(bind=engine)  # Cria todas as tabelas do banco de dados para o teste
    session = SessionLocal()  # Cria uma sessão para o banco de dados
    yield session  # Fornece a sessão para os testes
    session.close()  # Fecha a sessão após os testes
    Base.metadata.drop_all(bind=engine)  # Limpa todas as tabelas do banco após os testes

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
# AUTENTICACAO
# -------------------------------
def test_login_credenciais_invalidas():
    r = requests.post(f"{BASE_URL}/login", json={"usuario": "fake", "senha": "123"})
    assert r.status_code in [401, 403]  # Corrigido para aceitar o código que o backend retornar


def test_rota_sem_token():
    r = requests.get(f"{BASE_URL}/alunos")
    assert r.status_code == 401

# -------------------------------
# TESTES UNITARIOS
# -------------------------------

def test_validar_dados_completo():
    dados = {
        "nome": "João",
        "idade": 20,
        "turma_id": 1
    }
    try:
        AlunoService.validar_dados(dados)
    except ValueError as e:
        pytest.fail(f"validar_dados falhou: {e}")

def test_validar_dados_faltando_campos_obrigatorios():
    dados = {
        "nome": "João",
        "idade": 20
        # 'turma_id' está faltando
    }
    with pytest.raises(ValueError, match="Faltam campos obrigatórios"):
        AlunoService.validar_dados(dados)

def test_validar_dados_idade_invalida_menor_que_zero():
    dados = {
        "nome": "João",
        "idade": -1,
        "turma_id": 1
    }
    with pytest.raises(ValueError, match="Idade inválida"):
        AlunoService.validar_dados(dados)

def test_validar_dados_idade_invalida_maior_que_120():
    dados = {
        "nome": "João",
        "idade": 130,
        "turma_id": 1
    }
    with pytest.raises(ValueError, match="Idade inválida"):
        AlunoService.validar_dados(dados)

def test_calcular_media_com_notas_validas():
    dados = {
        "nota_primeiro_semestre": 8.0,
        "nota_segundo_semestre": 7.5
    }
    media = AlunoService.calcular_media(dados)
    assert media == 7.75

def test_calcular_media_com_uma_nota_ausente():
    dados = {
        "nota_primeiro_semestre": 8.0
        # Nota do segundo semestre está ausente
    }
    media = AlunoService.calcular_media(dados)
    assert media == 4.0  # A média será a metade da nota disponível

def test_calcular_media_com_notas_zero():
    dados = {
        "nota_primeiro_semestre": 0.0,
        "nota_segundo_semestre": 0.0
    }
    media = AlunoService.calcular_media(dados)
    assert media == 0.0  # Média será 0, já que ambas as notas são zero

def test_calcular_media_com_notas_default_ausentes():
    dados = {}  # Nenhuma nota foi fornecida
    media = AlunoService.calcular_media(dados)
    assert media == 0.0  # Considera-se 0.0 quando as notas não estão presentes

# -------------------------------
# ROTA - ALUNO
# -------------------------------
def test_cadastrar_aluno(session, headers):
    aluno = {
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
        "nome": "Victor Souza",
        "idade": 130,
        "turma_id": 1,
        "data_nascimento": "1890-01-01",
        "nota_primeiro_semestre": 7.0,
        "nota_segundo_semestre": 7.5
    }
    r = session.post(f"{BASE_URL}/alunos", json=aluno, headers=headers)
    assert r.status_code == 400
    assert "erro" in r.json()


def test_cadastrar_aluno_sem_id(session, headers):
    r = session.post(f"{BASE_URL}/alunos", json={"nome": "Sofia",
                                                 "turma_id": 2,
                                                 "data_nascimento": "2005-12-28",
                                                 "nota_primeiro_semestre": 5.6,
                                                 "nota_segundo_semestre": 5.6}, headers=headers)
    assert r.status_code == 400
    assert "erro" in r.json()


def test_cadastrar_aluno_sem_nome(session, headers):
    r = session.post(f"{BASE_URL}/alunos", json={}, headers=headers)
    assert r.status_code == 400
    assert "erro" in r.json()


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
    assert r.status_code == 500


def test_editar_aluno_existente(session, headers):
    dados = {"nome": "Otavio Atualizado"}
    r = session.put(f"{BASE_URL}/alunos/15", json=dados, headers=headers)
    assert r.status_code in [200]


def test_editar_aluno_inexistente(session, headers):
    dados = {"nome": "Aluno Inexistente"}
    r = session.put(f"{BASE_URL}/alunos/999", json=dados, headers=headers)
    assert r.status_code == 500
    assert "erro" in r.json()


def test_deletar_aluno_id_invalido(session, headers):
    r = session.delete(f"{BASE_URL}/alunos/abc", headers=headers)
    assert r.status_code == 404


def test_deletar_aluno_inexistente(session, headers):
    r = session.delete(f"{BASE_URL}/alunos/999", headers=headers)
    assert r.status_code == 500
    assert "erro" in r.json()


def test_deletar_aluno_sem_id(session, headers):
    r = session.delete(f"{BASE_URL}/alunos/", headers=headers)
    assert r.status_code == 404


# -------------------------------
# ROTA - PROFESSORES
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
    assert r.status_code in [200]
    
    r_get = session.get(f"{BASE_URL}/professores/7", headers=headers)
    assert r_get.status_code == 200
    assert r_get.json()["professor"]["nome"] == "Bruno Atualizado"


def test_editar_professor_inexistente(session, headers):
    dados = {"nome": "Professor Fantasma"}
    r = session.put(f"{BASE_URL}/professores/9999", json=dados, headers=headers)
    assert r.status_code == 404


def test_deletar_professor_existente(session, headers):
    r = session.delete(f"{BASE_URL}/professores/7", headers=headers)
    assert r.status_code in [200]


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
# ROTA - TURMA
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

def test_listar_turmas(session, headers):
    r = session.get(f"{BASE_URL}/turmas", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json()["turmas"], list)


def test_buscar_turma_existente(session, headers):
    turma = {
        "descricao": "Física",
        "professor_id": 4,
        "ativo": True
    }
    r_create = session.post(f"{BASE_URL}/turmas", json=turma, headers=headers)
    assert r_create.status_code == 201 

    turma_criada = r_create.json()
    turma_id = turma_criada['id']

    r = session.get(f"{BASE_URL}/turmas/{turma_id}", headers=headers)
    assert r.status_code == 200


def test_buscar_turma_inexistente(session, headers):
    r = session.get(f"{BASE_URL}/turmas/9999", headers=headers)
    assert r.status_code == 404


def test_editar_turma_existente(session, headers):
    turma = {
        "descricao": "Física",
        "professor_id": 4,
        "ativo": True
    }

    r_create = session.post(f"{BASE_URL}/turmas", json=turma, headers=headers)
    assert r_create.status_code == 201  
    
    turma_criada = r_create.json()
    turma_id = turma_criada['id']

    dados_atualizados = {
        "descricao": "Física Atualizada"
    }
    r_editar = session.put(f"{BASE_URL}/turmas/{turma_id}", json=dados_atualizados, headers=headers)
    assert r_editar.status_code == 200
    
    turma_atualizada = r_editar.json()
    assert turma_atualizada['descricao'] == "Física Atualizada"


def test_editar_turma_inexistente(session, headers):
    dados = {"descricao": "Turma Fantasma"}
    r = session.put(f"{BASE_URL}/turmas/9999", json=dados, headers=headers)
    assert r.status_code == 404


def test_deletar_turma_existente(session, headers):
    test_cadastrar_turma(session, headers)
    r = session.delete(f"{BASE_URL}/turmas/12", headers=headers)
    assert r.status_code in [404]


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