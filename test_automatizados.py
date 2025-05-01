import pytest
import requests
from config import Config
from service.aluno_service import AlunoService
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
    assert r.status_code in [401, 403]

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
    }
    media = AlunoService.calcular_media(dados)
    assert media == 4.0

def test_calcular_media_com_notas_zero():
    dados = {
        "nota_primeiro_semestre": 0.0,
        "nota_segundo_semestre": 0.0
    }
    media = AlunoService.calcular_media(dados)
    assert media == 0.0

def test_calcular_media_com_notas_default_ausentes():
    dados = {}
    media = AlunoService.calcular_media(dados)
    assert media == 0.0

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
    # Verifica se a resposta contém dados do aluno cadastrado
    data = r.json()
    assert "nome" in data
    assert data["nome"] == aluno["nome"]

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
    aluno = {
        "nome": "Sofia",
        "turma_id": 2,
        "data_nascimento": "2005-12-28",
        "nota_primeiro_semestre": 5.6,
        "nota_segundo_semestre": 5.6
    }
    r = session.post(f"{BASE_URL}/alunos", json=aluno, headers=headers)
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
    assert r.status_code == 200

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
    data = r.json()
    if isinstance(data, dict) and "professores" in data:
        assert isinstance(data["professores"], list)
    else:
        assert isinstance(data, list)

# -------------------------------
# ROTA - LOGIN
# -------------------------------

# Teste de login com dados válidos
def test_login_valido(session):
    usuario = {
        "email": "usuario@example.com",
        "senha": "senha123"
    }
    r = session.post(f"{BASE_URL}/login", json=usuario)
    assert r.status_code == 200
    assert "token" in r.json()

# Teste de login com dados inválidos
def test_login_invalido(session):
    usuario = {
        "email": "usuario@example.com",
        "senha": "senhaerrada"
    }
    r = session.post(f"{BASE_URL}/login", json=usuario)
    assert r.status_code == 401
    assert "erro" in r.json()

# Teste de login sem senha
def test_login_sem_senha(session):
    usuario = {
        "email": "usuario@example.com"
    }
    r = session.post(f"{BASE_URL}/login", json=usuario)
    assert r.status_code == 400
    assert "erro" in r.json()

# Teste de login sem email
def test_login_sem_email(session):
    usuario = {
        "senha": "senha123"
    }
    r = session.post(f"{BASE_URL}/login", json=usuario)
    assert r.status_code == 400
    assert "erro" in r.json()

# Teste de token de acesso inválido (para acesso a rotas protegidas)
def test_acesso_com_token_invalido(session):
    headers = {"Authorization": "Bearer tokeninvalido"}
    r = session.get(f"{BASE_URL}/perfil", headers=headers)
    assert r.status_code == 401
    assert "erro" in r.json()

# -------------------------------
# ROTA - ADMIN
# -------------------------------

# Teste de criação de novo admin
def test_criar_admin(session, headers):
    admin = {
        "nome": "Administrador",
        "email": "admin@example.com",
        "senha": "admin123"
    }
    r = session.post(f"{BASE_URL}/admin", json=admin, headers=headers)
    assert r.status_code == 201
    assert "id" in r.json()

# Teste de listar todos os admins
def test_listar_admins(session, headers):
    r = session.get(f"{BASE_URL}/admin", headers=headers)
    assert r.status_code == 200
    admins = r.json()
    assert isinstance(admins, list)

# Teste de editar dados de um admin
def test_editar_admin(session, headers):
    dados = {"nome": "Administrador Atualizado"}
    r = session.put(f"{BASE_URL}/admin/1", json=dados, headers=headers)
    assert r.status_code == 200
    admin = r.json()
    assert admin["nome"] == "Administrador Atualizado"

# Teste de deletar admin
def test_deletar_admin(session, headers):
    r = session.delete(f"{BASE_URL}/admin/1", headers=headers)
    assert r.status_code == 200
    r = session.get(f"{BASE_URL}/admin/1", headers=headers)
    assert r.status_code == 404

# -------------------------------
# ROTA - TURMA
# -------------------------------

# Teste de criação de turma
def test_criar_turma(session, headers):
    turma = {
        "nome": "Turma 1A",
        "curso_id": 1,
        "ano": 2025
    }
    r = session.post(f"{BASE_URL}/turmas", json=turma, headers=headers)
    assert r.status_code == 201
    turma_criada = r.json()
    assert turma_criada["nome"] == "Turma 1A"

# Teste de listar turmas
def test_listar_turmas(session, headers):
    r = session.get(f"{BASE_URL}/turmas", headers=headers)
    assert r.status_code == 200
    turmas = r.json()
    assert isinstance(turmas, list)

# Teste de editar dados de uma turma
def test_editar_turma(session, headers):
    dados = {"nome": "Turma 2A"}
    r = session.put(f"{BASE_URL}/turmas/1", json=dados, headers=headers)
    assert r.status_code == 200
    turma = r.json()
    assert turma["nome"] == "Turma 2A"

# Teste de deletar turma
def test_deletar_turma(session, headers):
    r = session.delete(f"{BASE_URL}/turmas/1", headers=headers)
    assert r.status_code == 200
    r = session.get(f"{BASE_URL}/turmas/1", headers=headers)
    assert r.status_code == 404

# Teste de associar alunos à turma
def test_associar_aluno_turma(session, headers):
    aluno_turma = {
        "aluno_id": 1,
        "turma_id": 1
    }
    r = session.post(f"{BASE_URL}/turmas/1/alunos", json=aluno_turma, headers=headers)
    assert r.status_code == 200
    turma = r.json()
    assert "alunos" in turma

# Teste de listar alunos de uma turma
def test_listar_alunos_turma(session, headers):
    r = session.get(f"{BASE_URL}/turmas/1/alunos", headers=headers)
    assert r.status_code == 200
    alunos = r.json()
    assert isinstance(alunos, list)
