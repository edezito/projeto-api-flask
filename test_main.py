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
         r_joao = requests.post('http://localhost:5000/alunos',json={'nome':'João','id':2})
         r_luis = requests.post('http://localhost:5000/alunos',json={'nome':'Luis','id':3})

         r_lista = requests.get('http://localhost:5000/alunos')
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
        r = requests.post('http://localhost:5000/alunos', json={'nome': 'Julio', 'id': 4})

        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()

        self.assertEqual(type(lista_retornada), list)
        nome_aluno = [aluno['nome'] for aluno in lista_retornada]
        self.assertIn("Julio", nome_aluno)

    def teste_004_deletar_aluno(self):
        requests.post('http://localhost:5000/alunos',json={'nome':'Cicero','id':29})
        requests.post('http://localhost:5000/alunos',json={'nome':'Lucas','id':28})
        requests.post('http://localhost:5000/alunos',json={'nome':'Marta','id':27})

        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()

        nomes = [aluno['nome'] for aluno in lista_retornada]
        self.assertIn('Cicero', nomes)
        self.assertIn('Lucas', nomes)
        self.assertIn('Marta', nomes)

        requests.delete('http://localhost:5000/alunos/28')
        r_lista2 = requests.get('http://localhost:5000/alunos')
        lista_retornada2 = r_lista2.json()

        nomes2 = [aluno['nome'] for aluno in lista_retornada2]
        self.assertNotIn('Lucas', nomes2)
        
        self.assertEqual(type(lista_retornada2), list)

    def teste_005_editar_aluno(self):
        requests.post('http://localhost:5000/alunos', json={'nome': 'lucas', 'id': 28})

        r_antes = requests.get('http://localhost:5000/alunos/28')
        self.assertEqual(r_antes.json()['nome'], 'lucas')

        requests.put('http://localhost:5000/alunos/28', json={'nome': 'lucas mendes'})

        r_depois = requests.get('http://localhost:5000/alunos/28')
        self.assertEqual(r_depois.json()['nome'], 'lucas mendes')
        self.assertEqual(r_depois.json()['id'],28)


    #alunos erro
    def teste_006_adicionar_aluno_com_id_duplicado(self):
        r1 = requests.post('http://localhost:5000/alunos', json={'nome': 'Pedro', 'id': 5})
        r2 = requests.post('http://localhost:5000/alunos', json={'nome': 'Carlos', 'id': 5})

        self.assertEqual(r1.status_code, 201, "Aluno adicionado com sucesso")
        self.assertEqual(r2.status_code, 400, "Erro: ID Duplicado")
        self.assertIn('error', r2.json(), "Erro: ID Duplicado")

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

    def teste_015_editar_aluno_com_id_invalido(self):
        r = requests.put('http://localhost:5000/alunos/abc', json={'nome': 'Aluno Invalido'})
        print(r.text)
        self.assertEqual(r.status_code, 404, "ID inválido deve retornar 404")
        
        self.assertEqual(r.status_code, 404, "Erro: ID Incorreto")
        self.assertIn('error', r.json(), "Erro: ID Incorreto")

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
        r_paulo = requests.post('http://localhost:5000/professores', json={'nome':'Paulo', 'id':2})
        r_jorge = requests.post('http://localhost:5000/professores', json={'nome': 'Jorge', 'id':3})

        r_lista_professores = requests.get('http://localhost:5000/professores')
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
        r_caio = requests.post('http://localhost:5000/professores', json={'nome': 'Caio', "id": 4})

        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()

        self.assertEqual(type(lista_retornada),list)
        nome_professor = [professores['nome'] for professores in lista_retornada]
        self.assertIn('Caio', nome_professor)

    def teste_004_deletar_professor(self):
        requests.post('http://localhost:5000/professores', json={'nome': "Pablo", 'id':31})
        requests.post('http://localhost:5000/professores', json={'nome': "Juliana", 'id':32})
        requests.post('http://localhost:5000/professores', json={'nome': "Andre", 'id':33})

        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()

        requests.delete('http://localhost:5000/professores/33')

        r_lista2 = requests.get('http://localhost:5000/professores')
        lista_retornada2 = r_lista2.json()

        nomes2 = [professores['nome'] for professores in lista_retornada2]
        self.assertNotIn('Andre', nomes2)

        self.assertEqual(type(lista_retornada2), list)

    def teste_005_editar_professor(self):
        requests.post('http://localhost:5000/professores', json={'nome': "Monica", 'id':77})

        r_antes = requests.get('http://localhost:5000/professores/77')
        self.assertEqual(r_antes.json()['nome'],'Monica')

        requests.put('http://localhost:5000/professores/77', json={'nome': 'Monica Ribeiro'})
        r_depois = requests.get('http://localhost:5000/professores/77')

        self.assertEqual(r_depois.json()['nome'],'Monica Ribeiro')
        self.assertEqual(r_depois.json()['id'],77)

    #professores erros

    



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
        r_matematica = requests.post('http://localhost:5000/turmas', json={'nome': 'Matemática', 'id': 2})
        r_geografia = requests.post('http://localhost:5000/turmas', json={'nome': 'Geografia', 'id': 3})

        r_lista_turmas = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista_turmas.json()

        achei_matematica = False
        achei_geografia = False

        for turma in lista_retornada:
            if turma['nome'] == 'Matemática':
                achei_matematica = True
            if turma['nome'] == 'Geografia':
                achei_geografia = True

        if not achei_geografia:
            self.fail("Turma Geografia não apareceu na lista de turmas")
        if not achei_matematica:
            self.fail("Turma Matemática não apareceu na lista de turmas")

    def teste_003_exibir_turma_por_id(self):
        r_historia = requests.post('http://localhost:5000/turmas', json={'nome': 'História', 'id': 4})

        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()

        self.assertEqual(type(lista_retornada), list)
        nome_turma = [turma['nome'] for turma in lista_retornada]
        self.assertIn('História', nome_turma)

    def teste_004_deletar_professor(self):
        requests.post('http://localhost:5000/turmas', json={'nome': 'Inglês', 'id': 12})
        requests.post('http://localhost:5000/turmas', json={'nome': 'Biologia', 'id': 13})

        r_lista = requests.get('http://localhost:5000/turmas')
        lista_ordenada = r_lista.json()

        requests.delete('http://localhost:5000/turmas/13')

        r_lista2 = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista2.json()

        nomes2 = [turmas['nome'] for turmas in lista_retornada]
        self.assertNotIn('Biologia', nomes2)

        self.assertEqual(type(lista_retornada), list)

    def teste_005_editar_professor(self):
        requests.post('http://localhost:5000/turmas', json={'nome': 'Filosofia', 'id': 8})

        r_antes = requests.get('http://localhost:5000/turmas/8')
        self.assertEqual(r_antes.json()['nome'], 'Filosofia')

        requests.put('http://localhost:5000/turmas/8', json={'nome': 'Filosofia Moderna'})
        
        r_depois = requests.get('http://localhost:5000/turmas/8')
        self.assertEqual(r_depois.json()['nome'], 'Filosofia Moderna')
        self.assertEqual(r_depois.json()['id'], 8)

    #turmas erros



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TesteAPI)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()