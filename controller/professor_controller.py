from service.professor_service import ProfessorService
from flask_restx import marshal
from swagger.namespaces.professor_namespace import professor_model

class ProfessorController:

    @staticmethod
    def listar_professores():
        """Lista todos os professores cadastrados"""
        professores = ProfessorService.listar_professores()
        if not professores:
            return {'message': 'Nenhum professor encontrado'}, 404
        return professores

    @staticmethod
    def criar_professor(data):
        """Cria um novo professor"""
        professor = ProfessorService.criar_professor(data)
        return {'message': 'Professor criado com sucesso', 'data': marshal(professor, professor_model)}, 201

    @staticmethod
    def buscar_professor_por_id(id_professor):
        """Busca um professor pelo ID"""
        professor = ProfessorService.buscar_professor_por_id(id_professor)
        if not professor:
            return {'error': 'Professor não encontrado'}, 404
        return marshal(professor, professor_model)

    @staticmethod
    def atualizar_professor(id_professor, data):
        """Atualiza os dados de um professor"""
        professor = ProfessorService.atualizar_professor(id_professor, data)
        if not professor:
            return {'error': 'Professor não encontrado'}, 404
        return {'message': 'Professor atualizado com sucesso', 'data': marshal(professor, professor_model)}, 200

    @staticmethod
    def excluir_professor(id_professor):
        """Exclui um professor do sistema"""
        success = ProfessorService.excluir_professor(id_professor)
        if not success:
            return {'error': 'Professor não encontrado'}, 404
        return {'message': 'Professor removido com sucesso'}, 200