import unittest
from main import app

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        """Reinicia os dados antes de cada teste (se a API permitir)."""  
        #criar professores
        response1 = self.app.post('/professores', json={"nome": "João", "disciplina": "Matemática"})
        response2 = self.app.post('/professores', json={"nome": "Maria", "disciplina": "História"})
        self.professor_id1 = response1.json.get("id")
        self.professor_id2 = response2.json.get("id")

        #criar turmas
        response3 = self.app.post('/turmas', json={"nome": "Turma_B", "turno": "Noite"})
        response4 = self.app.post('/turmas', json={"nome": "Turma_C", "turno": "Tarde"})
        self.turma_id1 = response3.json.get("id")
        self.turma_id2 = response4.json.get("id")

        #criar alunos
        response5 = self.app.post('/alunos', json={"nome": "José", "turma_id": self.turma_id1})
        response6 = self.app.post('/alunos', json={"nome": "Júlia", "turma_id": self.turma_id2})
        self.aluno_id1 = response5.json.get("id")
        self.aluno_id2 = response6.json.get("id")

#teste de prof
    def test_listar_professores(self):
        response = self.app.get('/professores')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_obter_professor(self):
        response = self.app.get(f'/professores/{self.professor_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.professor_id1, "nome": "João", "disciplina": "Matemática"})

    def test_criar_professor(self):
        response = self.app.post('/professores', json={"nome": "Carlos", "disciplina": "Geografia"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_atualizar_professor(self):
        response = self.app.put(f'/professores/{self.professor_id1}', json={"nome": "João Silva", "disciplina": "Matemática"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.professor_id1, "nome": "João Silva", "disciplina": "Matemática"})

    def test_excluir_professor(self):
        response = self.app.delete(f'/professores/{self.professor_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.json)

#teste de turma
    def test_listar_turmas(self):
        response = self.app.get('/turmas')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_obter_turma(self):
        response = self.app.get(f'/turmas/{self.turma_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.turma_id1, "nome": "Turma_B", "turno": "Noite"})

    def test_criar_turma(self):
        response = self.app.post('/turmas', json={"nome": "Matemática", "turno": "Noite"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_atualizar_turma(self):
        response = self.app.put(f'/turmas/{self.turma_id2}', json={"nome": "Matemática Avançada", "turno": "Noite"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.turma_id2, "nome": "Matemática Avançada", "turno": "Noite"})

    def test_excluir_turma(self):
        response = self.app.delete(f'/turmas/{self.turma_id2}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.json)

#teste alunop
    def test_listar_alunos(self):
        response = self.app.get('/alunos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_obter_aluno(self):
        response = self.app.get(f'/alunos/{self.aluno_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.aluno_id1, "nome": "José", "turma_id": self.turma_id1})

    def test_criar_aluno(self):
        response = self.app.post('/alunos', json={"nome": "Pedro", "turma_id": self.turma_id1})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_atualizar_aluno(self):
        response = self.app.put(f'/alunos/{self.aluno_id1}', json={"nome": "José Silva", "turma_id": self.turma_id1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.aluno_id1, "nome": "José Silva", "turma_id": self.turma_id1})

    def test_excluir_aluno(self):
        response = self.app.delete(f'/alunos/{self.aluno_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.json)

if __name__ == '__main__':
    unittest.main()
