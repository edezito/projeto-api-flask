import unittest
from unittest.mock import patch, MagicMock
import requests
from config import Config

BASE_URL = f"http://{Config.HOST}:{Config.PORT}"

class TestGerenciamentoAcademico(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        credenciais = {"usuario": "edezito", "senha": "1234"}
        response = self.session.post(f"{BASE_URL}/login", json=credenciais)
        
        try:
            response_data = response.json()
        except ValueError:
            self.fail(f"Resposta inválida da API: {response.text}")
            return

        if response.status_code == 200 and "token" in response_data:
            self.token = response_data["token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.fail(f"Falha na autenticação: {response.text}")

    def tearDown(self):
        self.session.close()

    def test_cadastrar_aluno(self):
        # Arrange: Configura o que precisa pro teste
        dados_aluno = {
            "id": 9,
            "nome": "Otavio",
            "idade": 18,
            "turma_id": 2,
            "data_nascimento": "2005-12-28",
            "nota_primeiro_semestre": 5.6,
            "nota_segundo_semestre": 5.6
        }

        # Act: Executa a ação 
        response = self.session.post(f"{BASE_URL}/alunos", json=dados_aluno, headers=self.headers)

         # Assert: Valida 
        self.assertEqual(response.status_code, 201, f"Falha ao cadastrar aluno: {response.text}")

    @patch('requests.Session.post')
    def test_cadastrar_professor_mock(self, mock_post):
        # Arrange
        dados_professor = {
            "id": 7,
            "nome": "Bruno",
            "idade": 33,
            "materia": "Filosofia",
            "observacoes": "professor-substituto"
        }
        mock_post.return_value = MagicMock(status_code=201, json=lambda: {"mensagem": "Professor cadastrado com sucesso"})

        # Act
        response = self.session.post(f"{BASE_URL}/professores", json=dados_professor, headers=self.headers)

        # Assert
        self.assertEqual(response.status_code, 201, "Mock: Falha ao cadastrar professor")
        self.assertIn("mensagem", response.json())

    def test_cadastrar_turma(self):
        # Arrange
        dados_turma = {
            "id": 12,
            "descricao": "Física",
            "professor_id": 4,
            "ativo": True
        }

        # Act
        response = self.session.post(f"{BASE_URL}/turmas", json=dados_turma, headers=self.headers)

        # Assert
        self.assertEqual(response.status_code, 201, f"Falha ao cadastrar turma: {response.text}")

    def test_resetar_dados(self):
        # Arrange
        endpoint = f"{BASE_URL}/reseta"

        # Act
        response = self.session.post(endpoint, headers=self.headers)

        # Assert 
        self.assertEqual(response.status_code, 200, f"Falha ao resetar dados: {response.text}")
        self.assertIn("mensagem", response.json())

if __name__ == "__main__":
    unittest.main()
