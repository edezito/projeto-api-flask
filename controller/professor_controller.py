from service.professor_service import ProfessorService
from flask_restx import marshal
from sqlalchemy.orm.exc import NoResultFound
from swagger.namespaces.professor_namespace import professor_model
from functools import wraps

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            return {'error': 'Professor não encontrado'}, 404
        except Exception as e:
            if func.__name__ in ('criar_professor', 'atualizar_professor'):
                return {'error': str(e)}, 400
            return {'error': str(e)}, 500
    return wrapper

class ProfessorController:

    @staticmethod
    @handle_exceptions
    def listar_professores():
        """Lista todos os professores cadastrados"""
        professores, total = ProfessorService.listar_professores()
        if not professores:
            return {'message': 'Nenhum professor encontrado'}, 404
        
        return {
            'message': 'Professores listados com sucesso',
            'data': [marshal(p, professor_model) for p in professores],
            'total': total
        }, 200

    @staticmethod
    @handle_exceptions
    def criar_professor(data):
        """Cria um novo professor"""
        professor = ProfessorService.criar_professor(data)
        return {
            'message': 'Professor criado com sucesso',
            'data': marshal(professor.to_dict(), professor_model)
        }, 201

    @staticmethod
    @handle_exceptions
    def buscar_professor_por_id(id_professor):
        """Busca um professor pelo ID"""
        professor = ProfessorService.buscar_professor_por_id(id_professor)
        return {
            'message': 'Professor encontrado com sucesso',
            'data': marshal(professor.to_dict(), professor_model)
        }, 200

    @staticmethod
    @handle_exceptions
    def atualizar_professor(id_professor, data):
        """Atualiza os dados de um professor"""
        professor = ProfessorService.atualizar_professor(id_professor, data)
        return {
            'message': 'Professor atualizado com sucesso',
            'data': marshal(professor.to_dict(), professor_model)
        }, 200

    @staticmethod
    @handle_exceptions
    def excluir_professor(id_professor):
        """Exclui um professor do sistema"""
        success = ProfessorService.excluir_professor(id_professor)
        if success:
            return {'message': 'Professor removido com sucesso'}, 200
        return {'error': 'Falha ao remover professor'}, 500