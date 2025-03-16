import unittest
from main import app

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        """Reinicia os dados antes de cada teste (se a API permitir)."""
        # Criar professores
        response1 = self.app.post('/professores', json={"nome": "João", "idade": 30, "materia": "Matemática"})
        response2 = self.app.post('/professores', json={"nome": "Maria", "idade": 40, "materia": "História"})
        self.professor_id1 = response1.json.get("id")
        self.professor_id2 = response2.json.get("id")

        # Criar turmas
        response3 = self.app.post('/turmas', json={"descricao": "Turma B", "professor_id": self.professor_id1, "ativo": True})
        response4 = self.app.post('/turmas', json={"descricao": "Turma C", "professor_id": self.professor_id2, "ativo": False})
        self.turma_id1 = response3.json.get("id")
        self.turma_id2 = response4.json.get("id")

        # Criar alunos
        response5 = self.app.post('/alunos', json={"nome": "José", "idade": 20, "turma_id": self.turma_id1,
                                                   "data_nascimento": "2003-04-15", "nota_primeiro_semestre": 7.5,
                                                   "nota_segundo_semestre": 8.0, "media_final": 7.75})
        response6 = self.app.post('/alunos', json={"nome": "Júlia", "idade": 22, "turma_id": self.turma_id2,
                                                   "data_nascimento": "2001-05-20", "nota_primeiro_semestre": 9.0,
                                                   "nota_segundo_semestre": 8.5, "media_final": 8.75})
        self.aluno_id1 = response5.json.get("id")
        self.aluno_id2 = response6.json.get("id")

    # Testes de professores
    def test_listar_professores(self):
        response = self.app.get('/professores')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_obter_professor(self):
        response = self.app.get(f'/professores/{self.professor_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.professor_id1, "nome": "João", "idade": 30, "materia": "Matemática", "observacoes": ''})


    def test_criar_professor(self):
        response = self.app.post('/professores', json={"nome": "Carlos", "idade": 35, "materia": "Geografia"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_atualizar_professor(self):
        response = self.app.put(f'/professores/{self.professor_id1}', json={"nome": "João Silva", "idade": 31, "materia": "Matemática"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.professor_id1, "nome": "João Silva", "idade": 31, "materia": "Matemática", "observacoes": ''})


    def test_excluir_professor(self):
        response = self.app.delete(f'/professores/{self.professor_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.json)

    # Testes de turmas
    def test_listar_turmas(self):
        response = self.app.get('/turmas')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_obter_turma(self):
        response = self.app.get(f'/turmas/{self.turma_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.turma_id1, "descricao": "Turma B", "professor_id": self.professor_id1, "ativo": True})

    def test_criar_turma(self):
        response = self.app.post('/turmas', json={"descricao": "Matemática", "professor_id": self.professor_id1, "ativo": True})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_atualizar_turma(self):
        response = self.app.put(f'/turmas/{self.turma_id2}', json={"descricao": "Matemática Avançada", "professor_id": self.professor_id2, "ativo": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.turma_id2, "descricao": "Matemática Avançada", "professor_id": self.professor_id2, "ativo": True})

    def test_excluir_turma(self):
        response = self.app.delete(f'/turmas/{self.turma_id2}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.json)

    # Testes de alunos
    def test_listar_alunos(self):
        response = self.app.get('/alunos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_obter_aluno(self):
        response = self.app.get(f'/alunos/{self.aluno_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.aluno_id1, "nome": "José", "idade": 20, "turma_id": self.turma_id1,
                                        "data_nascimento": "2003-04-15", "nota_primeiro_semestre": 7.5, "nota_segundo_semestre": 8.0, "media_final": 7.75})

    def test_criar_aluno(self):
        response = self.app.post('/alunos', json={"nome": "Pedro", "idade": 21, "turma_id": self.turma_id1,
                                                 "data_nascimento": "2002-09-10", "nota_primeiro_semestre": 7.0,
                                                 "nota_segundo_semestre": 7.5, "media_final": 7.25})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_atualizar_aluno(self):
        response = self.app.put(f'/alunos/{self.aluno_id1}', json={"nome": "José Silva", "idade": 21, "turma_id": self.turma_id1,
                                                                 "data_nascimento": "2003-04-15", "nota_primeiro_semestre": 8.0,
                                                                 "nota_segundo_semestre": 8.5, "media_final": 8.25})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": self.aluno_id1, "nome": "José Silva", "idade": 21, "turma_id": self.turma_id1,
                                        "data_nascimento": "2003-04-15", "nota_primeiro_semestre": 8.0, "nota_segundo_semestre": 8.5, "media_final": 8.25})

    def test_excluir_aluno(self):
        response = self.app.delete(f'/alunos/{self.aluno_id1}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.json)

if __name__ == '__main__':
    unittest.main()
