from model.professor_model import Professor

class ProfessorService:
    
    @staticmethod
    def listar_professores():
        """Lista todos os professores cadastrados"""
        return Professor.query.all()

    @staticmethod
    def criar_professor(data):
        """Cria um novo professor"""
        professor = Professor(**data)
        professor.save()  # Assumindo que você tem um método `save()` no modelo
        return professor

    @staticmethod
    def buscar_professor_por_id(id_professor):
        """Busca um professor pelo ID"""
        return Professor.query.get(id_professor)

    @staticmethod
    def atualizar_professor(id_professor, data):
        """Atualiza os dados de um professor"""
        professor = Professor.query.get(id_professor)
        if professor:
            professor.update(data)  # Assumindo que você tem um método `update()` no modelo
            return professor
        return None

    @staticmethod
    def excluir_professor(id_professor):
        """Exclui um professor do sistema"""
        professor = Professor.query.get(id_professor)
        if professor:
            professor.delete()  # Assumindo que você tem um método `delete()` no modelo
            return True
        return False