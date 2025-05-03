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

# ----------------------------------
# TESTES DE ADMIN
# ----------------------------------
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

'''
# ----------------------------------
# TESTANDO CONTROLLER DE ALUNOS
# ----------------------------------

@pytest.fixture
def mock_aluno_service():
    with patch('controller.aluno_controller.AlunoService') as mock_service:
        yield mock_service.return_value

def test_listar_alunos(mock_aluno_service):
    mock_aluno_service.listar_alunos.return_value = [{'id': 1, 'nome': 'Aluno A'}]
    response = AlunoController.listar(page=1, per_page=10, order_by='nome')
    assert response[0]['message'] == 'Lista de alunos recuperada com sucesso'
    assert response[1] == 200

    mock_aluno_service.listar_alunos.return_value = []
    response = AlunoController.listar(page=1, per_page=10, order_by='nome')
    assert response[0]['message'] == 'Nenhum aluno encontrado'
    assert response[1] == 404

def test_criar_aluno(mock_aluno_service):
    mock_aluno = {'id': 1, 'nome': 'Aluno A'}
    mock_aluno_service.criar_aluno.return_value = mock_aluno
    with patch('controller.aluno_controller.marshal', return_value=mock_aluno):
        response = AlunoController.criar()
        assert response[0]['message'] == 'Aluno criado com sucesso'
        assert response[1] == 201

def test_buscar_aluno_por_id(mock_aluno_service):
    mock_aluno = {'id': 1, 'nome': 'Aluno A'}
    mock_aluno_service.buscar_aluno_por_id.return_value = mock_aluno
    response = AlunoController.buscar_por_id(1)
    assert response[0]['message'] == 'Aluno encontrado com sucesso'
    assert response[1] == 200

    mock_aluno_service.buscar_aluno_por_id.return_value = None
    response = AlunoController.buscar_por_id(1)
    assert response[0]['message'] == 'Aluno não encontrado'
    assert response[1] == 404

def test_atualizar_aluno(mock_aluno_service):
    mock_aluno = {'id': 1, 'nome': 'Atualizado'}
    mock_aluno_service.atualizar_aluno.return_value = mock_aluno
    response = AlunoController.atualizar(1)
    assert response[0]['message'] == 'Aluno atualizado com sucesso'
    assert response[1] == 200

    mock_aluno_service.atualizar_aluno.return_value = None
    response = AlunoController.atualizar(1)
    assert response[0]['message'] == 'Aluno não encontrado'
    assert response[1] == 404

def test_excluir_aluno(mock_aluno_service):
    mock_aluno_service.excluir_aluno.return_value = True
    response = AlunoController.excluir(1)
    assert response[0]['message'] == 'Aluno removido com sucesso'
    assert response[1] == 200

    mock_aluno_service.excluir_aluno.return_value = False
    response = AlunoController.excluir(1)
    assert response[0]['message'] == 'Aluno não encontrado'
    assert response[1] == 404

'''

# ----------------------------------
# TESTANDO CONTROLLER DE PROFESSORES
# ----------------------------------
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