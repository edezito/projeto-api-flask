import unittest
import requests #consumir a API

class TesteAPI(unittest.TestCase):
    #alunos

    def teste_001_exibir_alunos(self):
        r = requests.get("http://localhost:5000/alunos")

        if r.status_code == 404:
                self.fail("voce nao definiu a página /alunos no seu server")

        try:
            obj_retornado = r.json()
            
        except:
            self.fail("Queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def teste_002_adicionar_alunos(self):
        r_joao = requests.post('http://localhost:5000/alunos', json={
            'nome': 'João',
            'id': 2,
            'idade': 20,
            'turma_id': 1,
            'data_nascimento': '2005-01-01'
        })
        self.assertEqual(r_joao.status_code, 201, "Aluno João não foi adicionado corretamente.")
        
        r_luis = requests.post('http://localhost:5000/alunos', json={
            'nome': 'Luis',
            'id': 3,
            'idade': 22,
            'turma_id': 2,
            'data_nascimento': '2003-05-01'
        })
        self.assertEqual(r_luis.status_code, 201, "Aluno Luis não foi adicionado corretamente.")
        
        r_lista = requests.get('http://localhost:5000/alunos')
        self.assertEqual(r_lista.status_code, 200, "Falha ao obter a lista de alunos.")
        lista_retornada = r_lista.json()
        
        achei_joao = False
        achei_luis = False
    
        for aluno in lista_retornada:
            if aluno['nome'] == 'João':
                achei_joao = True
            if aluno['nome'] == 'Luis':
                achei_luis = True

        if not achei_joao:
            self.fail('Aluno João não apareceu na lista de alunos')
        if not achei_luis:
            self.fail('Aluno Luis não apareceu na lista de alunos')


    def teste_003_exbir_aluno_por_id(self):
        r_carlos = requests.post('http://localhost:5000/alunos', json={
            'nome': 'Carlos',
            'id': 7,
            'idade': 20,
            'turma_id': 1,
            'data_nascimento': '2005-12-01'
        })

        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()

        self.assertEqual(type(lista_retornada), list)
        nome_aluno = [aluno['nome'] for aluno in lista_retornada]
        self.assertIn("Carlos", nome_aluno)

    def teste_004_deletar_aluno(self):
        requests.post('http://localhost:5000/alunos', json={
            'nome': 'Manoel',
            'id': 8,
            'idade': 20,
            'turma_id': 1,
            'data_nascimento': '2005-12-03'
        })
        requests.post('http://localhost:5000/alunos', json={
            'nome': 'Eduardo',
            'id': 9,
            'idade': 20,
            'turma_id': 2,
            'data_nascimento': '2006-04-03'
        })
        requests.post('http://localhost:5000/alunos', json={
            'nome': 'Thiago',
            'id': 10,
            'idade': 20,
            'turma_id': 3,
            'data_nascimento': '2006-10-03'
        })

        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()

        nomes = [aluno['nome'] for aluno in lista_retornada]
        self.assertIn('Manoel', nomes)
        self.assertIn('Eduardo', nomes)
        self.assertIn('Thiago', nomes)

        requests.delete('http://localhost:5000/alunos/9')
        r_lista2 = requests.get('http://localhost:5000/alunos')
        lista_retornada2 = r_lista2.json()

        nomes2 = [aluno['nome'] for aluno in lista_retornada2]
        self.assertNotIn('Eduardo', nomes2)
        
        self.assertEqual(type(lista_retornada2), list)

    def teste_005_editar_aluno(self):
        r_antes = requests.get('http://localhost:5000/alunos/1')
        self.assertEqual(r_antes.json()['nome'], 'Caio')

        requests.put('http://localhost:5000/alunos/1', json={'nome': 'Caio Chaves'})

        r_depois = requests.get('http://localhost:5000/alunos/1')
        self.assertEqual(r_depois.json()['nome'], 'Caio Chaves')
        self.assertEqual(r_depois.json()['id'],1)


    #alunos erro
    def teste_006_adicionar_aluno_com_id_duplicado(self):
        r_amanda = requests.post('http://localhost:5000/alunos', json={
            'nome': 'Amanda',
            'id': 62,
            'idade': 20,
            'turma_id': 1,
            'data_nascimento': '2005-01-01'
        })
        self.assertEqual(r_amanda.status_code, 201, "Aluno João não foi adicionado corretamente.")
        
        r_humberto = requests.post('http://localhost:5000/alunos', json={
            'nome': 'Humberto',
            'id': 62,
            'idade': 22,
            'turma_id': 2,
            'data_nascimento': '2003-05-01'
        })
        self.assertEqual(r_humberto.status_code, 400, "Erro: ID Duplicado")

        resposta = r_humberto.json()
        self.assertIn('error', resposta, "Erro: A chave 'error' não foi encontrada na resposta")
        self.assertEqual(resposta['error'], "ID duplicado", "Erro: Mensagem de erro não é 'ID duplicado'")


    def teste_007_adicionar_aluno_sem_nome(self):
        r = requests.post('http://localhost:5000/alunos', json={'id': 6})
        self.assertEqual(r.status_code, 400, "Erro: Falta nome")
        self.assertIn('error', r.json(), "Erro: Falta nome")

    def teste_008_adicionar_aluno_sem_id(self):
        r = requests.post('http://localhost:5000/alunos', json={'nome': 'Sofia'})
        self.assertEqual(r.status_code, 400, "Erro: Falta ID")
        self.assertIn('error', r.json(), "Erro: Falta ID")

    def teste_009_exibir_aluno_inexistente(self):
        r = requests.get('http://localhost:5000/alunos/999')
        self.assertEqual(r.status_code, 404, "Erro: Aluno Inexistente")
        self.assertIn('error', r.json(), "Erro: Aluno Inexistente")

    def teste_010_deletar_aluno_inexistente(self):
        r = requests.delete('http://localhost:5000/alunos/999')
        self.assertEqual(r.status_code, 404, "Erro: Aluno Inexistente")
        self.assertIn('error', r.json(), "Erro: Aluno Inexistente")

    def teste_011_deletar_aluno_sem_id(self):
        r = requests.delete('http://localhost:5000/alunos/')
        self.assertEqual(r.status_code, 404, "Erro: Rota não encontrada")

    def teste_012_deletar_aluno_com_id_invalido(self):
        r = requests.delete('http://localhost:5000/alunos/abc')
        self.assertEqual(r.status_code, 404, "Erro: ID Incorreto")

    def teste_013_editar_aluno_inexistente(self):
        r = requests.put('http://localhost:5000/alunos/999', json={'nome': 'Aluno Inexistente'})
        self.assertEqual(r.status_code, 404, "Erro: Aluno Inexistente")
        self.assertIn('error', r.json(), "Erro: Aluno Inexistente")

    def teste_014_editar_aluno_sem_nome(self):
        r = requests.put('http://localhost:5000/alunos/28', json={'id': 28})
        self.assertEqual(r.status_code, 400, "Erro: Falta nome")
        self.assertIn('error', r.json(), "Erro: Falta nome")

        resposta = r.json()
        self.assertEqual(resposta['error'], "Nome é obrigatório", "Erro: Mensagem de erro não é 'Nome é obrigatório'")
        
    #professores

    def teste_001_exibir_professores(self):
        r = requests.get('http://localhost:5000/professores')

        if r.status_code == 404:
            self.fail("Você não definiu a página /professores no seu servidos")
        
        try:
            professores_retornado = r.json()
            
        except:
            self.fail("Queria um json mas voce retornou outra coisa")

        self.assertEqual(type(professores_retornado),type([]))

    def teste_002_adicionar_professores(self):
        r_paulo = requests.post('http://localhost:5000/professores', json={
            'nome': 'Paulo',
            'id': 42,
            'idade': 40,
            'materia': 'Matemática',
            'observacoes': 'Professor com 10 anos de experiência'
        })
        self.assertEqual(r_paulo.status_code, 201, "Professor Paulo não foi adicionado corretamente.")
        
        r_jorge = requests.post('http://localhost:5000/professores', json={
            'nome': 'Jorge',
            'id': 43,
            'idade': 35,
            'materia': 'Física',
            'observacoes': 'Professor dedicado e atento aos alunos'
        })
        self.assertEqual(r_jorge.status_code, 201, "Professor Jorge não foi adicionado corretamente.")

        r_lista_professores = requests.get('http://localhost:5000/professores')
        self.assertEqual(r_lista_professores.status_code, 200, "Falha ao obter a lista de professores.")
        lista_retornada = r_lista_professores.json()

        achei_paulo = False
        achei_jorge = False

        for professor in lista_retornada:
            if professor['nome'] == 'Paulo':
                achei_paulo = True
            if professor['nome'] == 'Jorge':
                achei_jorge = True

        if not achei_paulo:
            self.fail("Professor Paulo não apareceu na lista de professores")
        if not achei_jorge:
            self.fail("Professor Jorge não apareceu na lista de professores")

    def teste_003_exibir_professor_por_id(self):

        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()

        self.assertEqual(type(lista_retornada), list)
        nome_professor = [professores['nome'] for professores in lista_retornada]
        self.assertIn('João', nome_professor)

    def teste_004_deletar_professor(self):
        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()

        nomes = [professor['nome'] for professor in lista_retornada]
        self.assertIn('João', nomes)

        r_deletar = requests.delete('http://localhost:5000/professores/2')
        self.assertEqual(r_deletar.status_code, 200, "Erro ao excluir professor")

        r_lista2 = requests.get('http://localhost:5000/professores')
        lista_retornada2 = r_lista2.json()

        nomes2 = [professor['nome'] for professor in lista_retornada2]
        self.assertNotIn('João', nomes2)

        self.assertEqual(type(lista_retornada2), list)

    def teste_005_editar_professor(self):

        r_antes = requests.get('http://localhost:5000/professores/42')
        self.assertEqual(r_antes.json()['nome'], 'Paulo')

        requests.put('http://localhost:5000/professores/42', json={'nome': 'Paulo Bacelar'})
        r_depois = requests.get('http://localhost:5000/professores/42')

        self.assertEqual(r_depois.json()['nome'], 'Paulo Bacelar')
        self.assertEqual(r_depois.json()['id'], 42)

    #professores erros

    def teste_006_adicionar_professor_com_id_duplicado(self):
        r_carla = requests.post('http://localhost:5000/professores', json={
            'nome': 'Carla',
            'id': 65,
            'idade': 40,
            'materia': 'Matemática',
            'observacoes': 'Professor com 10 anos de experiência'
        })
        self.assertEqual(r_carla.status_code, 201, "Professor Paulo não foi adicionado corretamente.")
        
        r_leandro = requests.post('http://localhost:5000/professores', json={
            'nome': 'Leandro',
            'id': 65,
            'idade': 35,
            'materia': 'Física',
            'observacoes': 'Professor dedicado e atento aos alunos'
        })
        
        self.assertEqual(r_leandro.status_code, 400, "Erro: ID Duplicado")

        resposta = r_leandro.json()
        self.assertIn('error', resposta, "Erro: A chave 'error' não foi encontrada na resposta")
        self.assertEqual(resposta['error'], "ID duplicado", "Erro: Mensagem de erro não é 'ID duplicado'")

    def teste_007_adicionar_professor_sem_nome(self):
        r = requests.post('http://localhost:5000/professores', json={'id': 51})
        self.assertEqual(r.status_code, 400, "Erro: Falta nome")
        self.assertIn('error', r.json(), "Erro: Falta nome")

    def teste_008_adicionar_professor_sem_id(self):
        r = requests.post('http://localhost:5000/professores', json={'nome': 'Marcos'})
        self.assertEqual(r.status_code, 400, "Erro: Falta ID")
        self.assertIn('error', r.json(), "Erro: Falta ID")

    def teste_009_exibir_professor_inexistente(self):
        r = requests.get('http://localhost:5000/professores/999')
        self.assertEqual(r.status_code, 404, "Erro: Professor Inexistente")
        self.assertIn('error', r.json(), "Erro: Professor Inexistente")

    def teste_010_deletar_professor_inexistente(self):
        r = requests.delete('http://localhost:5000/professores/999')
        self.assertEqual(r.status_code, 404, "Erro: Professor Inexistente")
        self.assertIn('error', r.json(), "Erro: Professor Inexistente")

    def teste_011_deletar_professor_sem_id(self):
        r = requests.delete('http://localhost:5000/professores/')
        self.assertEqual(r.status_code, 404, "Erro: Rota não encontrada")

    def teste_012_deletar_professor_com_id_invalido(self):
        r = requests.delete('http://localhost:5000/professores/abc')
        self.assertEqual(r.status_code, 404, "Erro: ID Incorreto")

    def teste_013_editar_professor_inexistente(self):
        r = requests.put('http://localhost:5000/professores/999', json={'nome': 'Professor Inexistente'})
        self.assertEqual(r.status_code, 404, "Erro: Professor Inexistente")
        self.assertIn('error', r.json(), "Erro: Professor Inexistente")

    def teste_014_editar_professor_sem_nome(self):
        r = requests.put('http://localhost:5000/alunos/28', json={'id': 28})
        self.assertEqual(r.status_code, 400, "Erro: Falta nome")
        self.assertIn('error', r.json(), "Erro: Falta nome")

        resposta = r.json()
        self.assertEqual(resposta['error'], "Nome é obrigatório", "Erro: Mensagem de erro não é 'Nome é obrigatório'")

    



    #turmas

    def teste_001_exibir_turmas(self):
        r = requests.get('http://localhost:5000/turmas')

        if r.status_code == 404:
            self.fail("Você não definiu a página /turmas no seu servidor")
        
        try:
            turma_retornada = r.json()
        except:
            self.fail("Queria um json mas voce retornou outra coisa")

        self.assertEqual(type(turma_retornada),type([]))

    def teste_002_adicionar_turmas(self):
        r_matematica = requests.post('http://localhost:5000/turmas', json={
            'id': 8,
            'descricao': 'Matemática',
            'professor_id': 66,
            'status': 'Ativa'
        })
        self.assertEqual(r_matematica.status_code, 201, "Turma Matemática não foi adicionada corretamente.")

        r_geografia = requests.post('http://localhost:5000/turmas', json={
            'id': 9,
            'descricao': 'Geografia',
            'professor_id': 65,
            'status': 'Ativa'
        })
        self.assertEqual(r_geografia.status_code, 201, "Turma Geografia não foi adicionada corretamente.")
        
        r_lista_turmas = requests.get('http://localhost:5000/turmas')
        self.assertEqual(r_lista_turmas.status_code, 200, "Falha ao obter a lista de turmas.")
        lista_retornada = r_lista_turmas.json()

        achei_matematica = False
        achei_geografia = False

        for turma in lista_retornada:
            if turma['descricao'] == 'Matemática':
                achei_matematica = True
            if turma['descricao'] == 'Geografia':
                achei_geografia = True

        if not achei_matematica:
            self.fail("Turma Matemática não apareceu na lista de turmas")
        if not achei_geografia:
            self.fail("Turma Geografia não apareceu na lista de turmas")

    def teste_003_exibir_turma_por_id(self):

        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()

        self.assertEqual(type(lista_retornada), list)
        nome_turma = [turma['descricao'] for turma in lista_retornada]
        self.assertIn('Geografia', nome_turma)

    def teste_004_deletar_turma(self):
        r_lista = requests.get('http://localhost:5000/turmas')
        lista_ordenada = r_lista.json()

        requests.delete('http://localhost:5000/turmas/3')

        r_lista2 = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista2.json()

        nomes2 = [turmas['descricao'] for turmas in lista_retornada]
        self.assertNotIn('Português', nomes2)

        self.assertEqual(type(lista_retornada), list)

    def teste_005_editar_turma(self):
        r_antes = requests.get('http://localhost:5000/turmas/9')
        self.assertEqual(r_antes.json()['descricao'], 'Geografia')

        requests.put('http://localhost:5000/turmas/9', json={'descricao': 'Geografia Política'})
        
        r_depois = requests.get('http://localhost:5000/turmas/9')
        self.assertEqual(r_depois.json()['descricao'], 'Geografia Política')
        self.assertEqual(r_depois.json()['id'], 9)

    #turmas erros

    def teste_006_adicionar_turma_com_id_duplicado(self):
        r_fisica = requests.post('http://localhost:5000/turmas', json={
            'id': 47,
            'descricao': 'Fisica',
            'professor_id': 66,
            'status': 'Ativa'
        })
        self.assertEqual(r_fisica.status_code, 201, "Professor Paulo não foi adicionado corretamente.")
        
        r_quimica = requests.post('http://localhost:5000/turmas', json={
            'id': 47,
            'descricao': 'Quimica',
            'professor_id': 78,
            'status': 'Ativa'
        })
        
        self.assertEqual(r_quimica.status_code, 400, "Erro: ID Duplicado")

        resposta = r_quimica.json()
        self.assertIn('error', resposta, "Erro: A chave 'error' não foi encontrada na resposta")
        self.assertEqual(resposta['error'], "ID duplicado", "Erro: Mensagem de erro não é 'ID duplicado'")

    def teste_007_adicionar_turma_sem_descricao(self):
        r = requests.post('http://localhost:5000/turmas', json={'id': 61})
        self.assertEqual(r.status_code, 400, "Erro: Falta descrição")
        self.assertIn('error', r.json(), "Erro: Falta descrição")

    def teste_008_adicionar_turma_sem_id(self):
        r = requests.post('http://localhost:5000/turmas', json={'descricao': 'Biologia'})
        self.assertEqual(r.status_code, 400, "Erro: Falta ID")
        self.assertIn('error', r.json(), "Erro: Falta ID")

    def teste_009_exibir_turma_inexistente(self):
        r = requests.get('http://localhost:5000/turmas/999')
        self.assertEqual(r.status_code, 404, "Erro: Turma Inexistente")
        self.assertIn('error', r.json(), "Erro: Turma Inexistente")

    def teste_010_deletar_turma_inexistente(self):
        r = requests.delete('http://localhost:5000/turmas/999')
        self.assertEqual(r.status_code, 404, "Erro: Turma Inexistente")
        self.assertIn('error', r.json(), "Erro: Turma Inexistente")

    def teste_011_editar_turma_inexistente(self):
        r = requests.put('http://localhost:5000/turmas/999', json={'descricao': 'Turma Inexistente'})
        self.assertEqual(r.status_code, 404, "Erro: Turma Inexistente")
        self.assertIn('error', r.json(), "Erro: Turma Inexistente")



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TesteAPI)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()