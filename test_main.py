import pytest
from unittest.mock import patch, MagicMock
from controller.professor_controller import ProfessorController

# ----------------------------------
# TESTANDO CONTROLLER DE PROFESSORES
# ----------------------------------
@pytest.fixture
def mock_professor_service():
    with patch('controller.professor_controller.ProfessorService') as mock_service:
        yield mock_service

def test_listar_professores(mock_professor_service):
    # Cenário: Professores encontrados
    mock_professor_service.listar_professores.return_value = [{'id': 1, 'nome': 'Professor A'}]
    response = ProfessorController.listar_professores()
    assert response == [{'id': 1, 'nome': 'Professor A'}]

    # Cenário: Nenhum professor encontrado
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
    # Cenário: Professor encontrado
    mock_professor = {'id': 1, 'nome': 'Professor A'}
    mock_professor_service.buscar_professor_por_id.return_value = mock_professor

    with patch('controller.professor_controller.marshal', return_value=mock_professor):
        response = ProfessorController.buscar_professor_por_id(1)
        assert response == mock_professor

    # Cenário: Professor não encontrado
    mock_professor_service.buscar_professor_por_id.return_value = None
    response = ProfessorController.buscar_professor_por_id(1)
    assert response == ({'error': 'Professor não encontrado'}, 404)

def test_atualizar_professor(mock_professor_service):
    # Cenário: Atualização bem-sucedida
    mock_professor = {'id': 1, 'nome': 'Professor Atualizado'}
    mock_professor_service.atualizar_professor.return_value = mock_professor

    with patch('controller.professor_controller.marshal', return_value=mock_professor):
        response = ProfessorController.atualizar_professor(1, {'nome': 'Professor Atualizado'})
        assert response == ({'message': 'Professor atualizado com sucesso', 'data': mock_professor}, 200)

    # Cenário: Professor não encontrado
    mock_professor_service.atualizar_professor.return_value = None
    response = ProfessorController.atualizar_professor(1, {'nome': 'Professor Atualizado'})
    assert response == ({'error': 'Professor não encontrado'}, 404)

def test_excluir_professor(mock_professor_service):
    # Cenário: Exclusão bem-sucedida
    mock_professor_service.excluir_professor.return_value = True
    response = ProfessorController.excluir_professor(1)
    assert response == ({'message': 'Professor removido com sucesso'}, 200)

    # Cenário: Professor não encontrado
    mock_professor_service.excluir_professor.return_value = False
    response = ProfessorController.excluir_professor(1)
    assert response == ({'error': 'Professor não encontrado'}, 404)




