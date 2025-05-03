import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, json, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controller.aluno_controller import AlunoController
from model.aluno_model import Aluno
from model.turma_model import Turma
from service.aluno_service import AlunoService
from config import BancoDados

@pytest.fixture
def app(mock_aluno_service):
    """Configuração do aplicativo Flask para testes."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Cria o controller e registra as rotas
    aluno_controller = AlunoController(mock_aluno_service)
    app.route('/alunos', methods=['GET'])(aluno_controller.listar)
    app.route('/alunos', methods=['POST'])(aluno_controller.criar)
    app.route('/alunos/<int:id>', methods=['GET'])(aluno_controller.buscar_por_id)
    app.route('/alunos/<int:id>', methods=['PUT'])(aluno_controller.atualizar)
    app.route('/alunos/<int:id>', methods=['DELETE'])(aluno_controller.excluir)
    
    return app


@pytest.fixture
def session(app):
    """Configuração do banco de dados para os testes, usando SQLAlchemy."""
    # Cria a engine e session para o banco de dados em memória
    engine = create_engine('sqlite:///:memory:')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Criação das tabelas no banco de dados em memória
    Aluno.metadata.create_all(bind=engine)
    Turma.metadata.create_all(bind=engine)

    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def mock_aluno_service():
    """Mock do serviço AlunoService."""
    mock = MagicMock(AlunoService)
    return mock


@pytest.fixture
def mock_aluno_controller(mock_aluno_service):
    """Mock do controlador AlunoController, injetando o serviço mockado."""
    mock = AlunoController(mock_aluno_service)
    return mock


@pytest.fixture
def client(app):
    """Fixture para o cliente de testes Flask."""
    with app.test_client() as client:
        yield client


def test_listar_alunos(mock_aluno_controller, session):
    """Testa a função listar alunos"""
    # Criar dados mockados para alunos diretamente no banco em memória
    aluno1 = Aluno(nome='Nome do Aluno', idade=20, turma_id=1)
    aluno2 = Aluno(nome='Nome do Aluno', idade=20, turma_id=1)
    session.add_all([aluno1, aluno2])
    session.commit()

    # Mock para a função de listagem do serviço
    mock_aluno_controller.aluno_service.listar_alunos.return_value = ([aluno1, aluno2], 2)

    response, status_code = mock_aluno_controller.listar(session, page=1, per_page=2)
    assert status_code == 200
    assert response['success'] is True
    assert response['message'] == "Lista de alunos recuperada com sucesso"
    assert len(response['data']['alunos']) == 2


def test_criar_aluno(mock_aluno_controller, session, app):
    """Testa a criação de um aluno"""
    mock_dados = {
        'nome': 'Novo Aluno',
        'idade': 19,
        'turma_id': 1,
        'nota_primeiro_semestre': 8.5,
        'nota_segundo_semestre': 9.0
    }

    aluno_mock = Aluno(**mock_dados)
    session.add(aluno_mock)
    session.commit()

    mock_aluno_controller.aluno_service.criar_aluno.return_value = aluno_mock

    # Use the app fixture's test_request_context
    with app.test_request_context(json=mock_dados):
        response, status_code = mock_aluno_controller.criar(session)
    
    assert status_code == 201
    assert response['success'] is True
    assert response['message'] == "Aluno criado com sucesso"
    assert response['data']['aluno']['nome'] == 'Novo Aluno'


def test_buscar_aluno_por_id(mock_aluno_controller, session):
    """Testa a busca de aluno por ID"""
    aluno_mock = Aluno(nome="Aluno 1", idade=20, turma_id=1)
    session.add(aluno_mock)
    session.commit()

    mock_aluno_controller.aluno_service.buscar_aluno_por_id.return_value = aluno_mock
    response, status_code = mock_aluno_controller.buscar_por_id(session, aluno_mock.id)

    assert status_code == 200
    assert response['success'] is True
    assert response['message'] == "Aluno encontrado com sucesso"
    assert response['data']['id'] == aluno_mock.id


def test_atualizar_aluno(mock_aluno_controller, session, client, mock_aluno_service):
    """Testa a atualização de um aluno"""
    # Cria um aluno no banco de dados
    aluno_mock = Aluno(nome="Aluno Original", idade=20, turma_id=1)
    session.add(aluno_mock)
    session.commit()

    # Configura o mock para retornar o aluno atualizado
    aluno_atualizado = Aluno(nome="Aluno Atualizado", idade=20, turma_id=1)
    aluno_atualizado.id = aluno_mock.id
    mock_aluno_service.atualizar_aluno.return_value = aluno_atualizado

    # Dados de atualização
    dados_update = {'nome': 'Aluno Atualizado', 'matricula': '54321'}

    # Simula a requisição PUT
    response = client.put(
        f"/alunos/{aluno_mock.id}",
        data=json.dumps(dados_update),
        content_type='application/json'
    )

    # Verificações
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['success'] is True
    assert response_data['message'] == "Aluno atualizado com sucesso"
    assert response_data['data']['aluno']['nome'] == "Aluno Atualizado"


def test_excluir_aluno(mock_aluno_controller, session):
    """Testa a exclusão de um aluno"""
    aluno_mock = Aluno(nome="Aluno Para Excluir", idade=20, turma_id=1)
    session.add(aluno_mock)
    session.commit()

    session.delete(aluno_mock)
    session.commit()

    mock_aluno_controller.aluno_service.excluir_aluno.return_value = aluno_mock

    response, status_code = mock_aluno_controller.excluir(session, aluno_mock.id)

    assert status_code == 200
    assert response['success'] is True
    assert response['message'] == "Aluno removido com sucesso"
    assert response['data']['id'] == aluno_mock.id