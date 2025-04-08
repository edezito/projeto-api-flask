import unittest
import requests
from config import Config
from model.aluno_model import validar_idade

BASE_URL = f"http://{Config.HOST}:{Config.PORT}"


# -------------------------------
# Testes Unitários
# -------------------------------
class TestValidarIdade(unittest.TestCase):
    def test_idade_valida(self):
        self.assertTrue(validar_idade(18))

    def test_idade_invalida_negativa(self):
        self.assertFalse(validar_idade(-5))

    def test_idade_invalida_maior_que_120(self):
        self.assertFalse(validar_idade(130))


# -------------------------------
# Testes E2E + Integração
# -------------------------------
class TestGerenciamentoAcademico(unittest.TestCase):

    def setUp(self):
        self.session = requests.Session()

        credenciais = {
            "usuario": "edezito",
            "senha": "1234"
        }

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
            self.token = None
            self.headers = {}
            self.fail(f"Falha na autenticação: {response.text}")

    def tearDown(self):
        self.session.close()

    # ---------- E2E ----------
    def test_cadastrar_aluno(self):
        dados_aluno = {
            "id": 9,
            "nome": "Otavio",
            "idade": 18,
            "turma_id": 2,
            "data_nascimento": "2005-12-28",
            "nota_primeiro_semestre": 5.6,
            "nota_segundo_semestre": 5.6
        }

        # Envia o POST para cadastrar o aluno
        response = self.session.post(f"{BASE_URL}/alunos", json=dados_aluno, headers=self.headers)
        self.assertEqual(response.status_code, 201, f"Falha ao cadastrar aluno: {response.text}")

        # Faz uma requisição GET para buscar os alunos e verificar o retorno
        response_get = self.session.get(f"{BASE_URL}/alunos", headers=self.headers)
        self.assertEqual(response_get.status_code, 200)

        obj_retornado = response_get.json()
        self.assertIn("alunos", obj_retornado)
        self.assertIsInstance(obj_retornado["alunos"], list)

    def test_cadastrar_professor(self):
        dados_professor = {
            "id": 7,
            "nome": "Bruno",
            "idade": 33,
            "materia": "Filosofia",
            "observacoes": "professor-substituto"
        }

        response = self.session.post(f"{BASE_URL}/professores", json=dados_professor, headers=self.headers)
        self.assertEqual(response.status_code, 201, f"Falha ao cadastrar professor: {response.text}")

    def test_cadastrar_turma(self):
        dados_turma = {
            "id": 12,
            "descricao": "Física",
            "professor_id": 4,
            "ativo": True
        }

        response = self.session.post(f"{BASE_URL}/turmas", json=dados_turma, headers=self.headers)
        self.assertEqual(response.status_code, 201, f"Falha ao cadastrar turma: {response.text}")

    # ---------- Integração ----------
    def test_cadastrar_aluno_dados_invalidos(self):
        dados_aluno = {
            "nome": "",
            "idade": -1,
        }

        response = self.session.post(f"{BASE_URL}/alunos", json=dados_aluno, headers=self.headers)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()