from flask import Flask, session
from flask_jwt_extended import create_access_token
import pytest
from unittest.mock import patch, MagicMock
from controller.admin_controler import SistemaController
from controller.aluno_controller import AlunoController
from controller.professor_controller import ProfessorController
from model import aluno_model, professor_model, turma_model
from config import BancoDados, Config
from model.usuario_model import Usuario

# ----------------------------------
# TESTANDO CONTROLLER DE ADMIN
# ----------------------------------
@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    return app

@pytest.fixture
def db_session(app):
    db = BancoDados.SessionLocal()
    yield db
    db.rollback()
    db.close()

@pytest.fixture
def auth_token(client, db_session):
    usuario = Usuario(nome="Usuário Teste", nickname="testuser", senha="testpass")
    db_session.add(usuario)
    db_session.flush()
    with client.application.app_context():
        token = create_access_token(identity=usuario.id)
    db_session.commit()
    yield token
    db_session.query(Usuario).filter(Usuario.id == usuario.id).delete()
    db_session.commit()

def test_resetar_dados_sucesso(db_session, app):
    # Criação dos registros de teste
    professor = professor_model.Professor(nome="Teste Professor", idade=30, materia="inglês")
    db_session.add(professor)
    db_session.commit()
    
    turma = turma_model.Turma(descricao="Turma 1", professor_id=professor.id)
    db_session.add(turma)
    db_session.commit()

    aluno = aluno_model.Aluno(nome="Teste Aluno", idade=20, turma_id=turma.id)
    db_session.add(aluno)
    db_session.commit()

    # Verifique se o aluno foi adicionado corretamente
    assert db_session.query(aluno_model.Aluno).count() == 1

    with app.app_context():
        SistemaController.resetar_dados()

    # Verifique se os dados foram excluídos corretamente após resetar
    assert db_session.query(aluno_model.Aluno).count() == 0

def test_resetar_dados_erro(app):
    with app.app_context():
        with patch('config.BancoDados.SessionLocal') as mock_session:
            mock_session.side_effect = Exception("Erro simulado")
            response, status_code = SistemaController.resetar_dados()
            data = response.get_json()
            assert status_code == 500
            assert data["success"] is False
            assert "Erro ao resetar dados" in data["message"]

# ----------------------------------
# TESTES DE ALUNOS
# ----------------------------------

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
    aluno_mock = Aluno(nome="Aluno Original", idade=20, turma_id=4)
    session.add(aluno_mock)
    session.commit()

    # Configura o mock para retornar o aluno atualizado
    aluno_atualizado = Aluno(nome="Aluno Atualizado", idade=23, turma_id=1)
    aluno_atualizado.id = aluno_mock.id
    mock_aluno_service.atualizar_aluno.return_value = aluno_atualizado

    # Dados de atualização
    dados_update = {'nome': 'Aluno Atualizado', 'idade': 23}

    # Simula a requisição PUT com o caminho correto da API
    response = client.put(
        f"/api/alunos/{aluno_mock.id}",  # Corrigido aqui
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

# ----------------------------------
# TESTANDO CONTROLLER DE PROFESSORES
# ----------------------------------

from unittest.mock import patch
import pytest

from controller.professor_controller import ProfessorController


@pytest.fixture
def mock_professor_service():
    with patch('controller.professor_controller.ProfessorService') as mock_service:
        yield mock_service

def test_listar_professores(mock_professor_service):
    mock_professor_service.listar_professores.return_value = [{'id': 1, 'nome': 'Professor A'}]
    response = ProfessorController.listar_professores()
    assert response == [{'id': 1, 'nome': 'Professor A'}]

    mock_professor_service.listar_professores.return_value = []
    response = ProfessorController.listar_professores()
    assert response == ({'message': 'Nenhum professor encontrado'}, 404)

def test_criar_professor(mock_professor_service):
    mock_professor = {'id': 1, 'nome': 'Professor A'}
    mock_professor_service.criar_professor.return_value = mock_professor
    with patch('controller.professor_controller.marshal', return_value=mock_professor):
        response = ProfessorController.criar_professor({'nome': 'Professor A'})
        assert response == ({'message': 'Professor criado com sucesso', 'data': mock_professor}, 201)

def test_buscar_professor_por_id(mock_professor_service):
    mock_professor = {'id': 1, 'nome': 'Professor A'}
    mock_professor_service.buscar_professor_por_id.return_value = mock_professor
    with patch('controller.professor_controller.marshal', return_value=mock_professor):
        response = ProfessorController.buscar_professor_por_id(1)
        assert response == mock_professor

    mock_professor_service.buscar_professor_por_id.return_value = None
    response = ProfessorController.buscar_professor_por_id(1)
    assert response == ({'error': 'Professor não encontrado'}, 404)

def test_atualizar_professor(mock_professor_service):
    mock_professor = {'id': 1, 'nome': 'Professor Atualizado'}
    mock_professor_service.atualizar_professor.return_value = mock_professor
    with patch('controller.professor_controller.marshal', return_value=mock_professor):
        response = ProfessorController.atualizar_professor(1, {'nome': 'Professor Atualizado'})
        assert response == ({'message': 'Professor atualizado com sucesso', 'data': mock_professor}, 200)

    mock_professor_service.atualizar_professor.return_value = None
    response = ProfessorController.atualizar_professor(1, {'nome': 'Professor Atualizado'})
    assert response == ({'error': 'Professor não encontrado'}, 404)

def test_excluir_professor(mock_professor_service):
    mock_professor_service.excluir_professor.return_value = True
    response = ProfessorController.excluir_professor(1)
    assert response == ({'message': 'Professor removido com sucesso'}, 200)

    mock_professor_service.excluir_professor.return_value = False
    response = ProfessorController.excluir_professor(1)
    assert response == ({'error': 'Professor não encontrado'}, 404)

# ----------------------------------
# TESTANDO CONTROLLER DE TURMAS
# ----------------------------------

import pytest
from flask import Flask
from http import HTTPStatus
from unittest.mock import patch, MagicMock
from controller.turma_controller import TurmaController
from service.turma_service import TurmaNaoEncontrada

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def turma_mock():
    turma = MagicMock()
    turma.id = 1
    turma.nome = "Turma A"
    turma.ativo = True
    turma.professor_id = 1
    turma.to_dict.return_value = {
        'id': 1,
        'nome': 'Turma A',
        'ativo': True,
        'professor_id': 1
    }
    return turma

def test_listar_turmas_sucesso(app, turma_mock):
    with app.test_request_context('/turmas?ativo=true&professor_id=1'):
        with patch('controller.turma_controller.TurmaService.listar_turmas') as mock_service:
            mock_service.return_value = [turma_mock]
            
            response, status_code = TurmaController.listar_turmas()
            
            assert status_code == HTTPStatus.OK
            assert isinstance(response, list)
            assert len(response) == 1
            assert response[0]['id'] == 1

def test_listar_turmas_erro(app):
    with app.test_request_context('/turmas'):
        with patch('controller.turma_controller.TurmaService.listar_turmas') as mock_service:
            mock_service.side_effect = Exception("Erro no banco de dados")
            
            response, status_code = TurmaController.listar_turmas()
            assert status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response['message'] == 'Erro no banco de dados'

def test_criar_turma_sucesso(app, turma_mock):
    with app.test_request_context('/turmas', json={'nome': 'Turma A', 'professor_id': 1}):
        with patch('controller.turma_controller.TurmaService.criar_turma') as mock_service:
            mock_service.return_value = turma_mock
            
            response, status_code = TurmaController.criar_turma()
            
            assert status_code == HTTPStatus.CREATED
            assert response['id'] == 1

def test_criar_turma_dados_invalidos(app):
    with app.test_request_context('/turmas', json={'id': 1}):
        response, status_code = TurmaController.criar_turma()
        assert status_code == HTTPStatus.BAD_REQUEST
        assert response['message'] == "O ID não deve ser fornecido manualmente"

def test_buscar_por_id_sucesso(app, turma_mock):
    with app.test_request_context('/turmas/1'):
        with patch('controller.turma_controller.TurmaService.buscar_turma_por_id') as mock_service:
            mock_service.return_value = turma_mock
            
            response, status_code = TurmaController.buscar_por_id_turma(1)
            
            assert status_code == HTTPStatus.OK
            assert response['id'] == 1

def test_buscar_por_id_nao_encontrado(app):
    with app.test_request_context('/turmas/999'):
        with patch('controller.turma_controller.TurmaService.buscar_turma_por_id') as mock_service:
            mock_service.side_effect = TurmaNaoEncontrada("Turma não encontrada")
            
            response, status_code = TurmaController.buscar_por_id_turma(999)
            assert status_code == HTTPStatus.NOT_FOUND
            assert response['message'] == 'Turma não encontrada'

def test_atualizar_turma_sucesso(app, turma_mock):
    with app.test_request_context('/turmas/1', json={'nome': 'Turma Atualizada'}):
        with patch('controller.turma_controller.TurmaService.atualizar_turma') as mock_service:
            mock_service.return_value = turma_mock
            
            response, status_code = TurmaController.atualizar_turma(1)
            
            assert status_code == HTTPStatus.OK
            assert response['id'] == 1

def test_atualizar_turma_nao_encontrada(app):
    with app.test_request_context('/turmas/999', json={'nome': 'Turma Atualizada'}):
        with patch('controller.turma_controller.TurmaService.atualizar_turma') as mock_service:
            mock_service.side_effect = TurmaNaoEncontrada("Turma não encontrada")
            
            response, status_code = TurmaController.atualizar_turma(999)
            assert status_code == HTTPStatus.NOT_FOUND
            assert response['message'] == 'Turma não encontrada'

def test_desativar_turma_sucesso(app, turma_mock):
    with app.test_request_context('/turmas/1/desativar'):
        with patch('controller.turma_controller.TurmaService.desativar_turma') as mock_service:
            mock_service.return_value = turma_mock
            
            response, status_code = TurmaController.desativar_turma(1)
            
            assert status_code == HTTPStatus.OK
            assert response['mensagem'] == 'Turma desativada com sucesso'
            assert response['turma_id'] == 1

def test_excluir_turma_sucesso(app):
    with app.test_request_context('/turmas/1'):
        with patch('controller.turma_controller.TurmaService.excluir_turma') as mock_service:
            mock_service.return_value = None
            
            response, status_code = TurmaController.excluir_turma(1)
            
            assert status_code == HTTPStatus.OK
            assert response['mensagem'] == 'Turma excluída permanentemente'