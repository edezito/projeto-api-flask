from flask_restx import Resource
from flask import request
from controller.professor_controller import ProfessorController
from service.login_requerido import login_requerido
from swagger.namespaces.professor_namespace import professores_namespace, professor_model, success_model, error_model

@professores_namespace.route('/')
class ListaProfessores(Resource):
    @professores_namespace.doc(security='Bearer Auth', description='Lista todos os professores cadastrados')
    @professores_namespace.marshal_list_with(professor_model)
    @professores_namespace.response(200, 'Professores listados com sucesso')
    @professores_namespace.response(404, 'Nenhum professor encontrado', model=error_model)
    @login_requerido
    def get(self):
        return ProfessorController.listar_professores()

    @professores_namespace.doc(security='Bearer Auth', description='Cria um novo professor')
    @professores_namespace.expect(professor_model)
    @professores_namespace.marshal_with(success_model, code=201)
    @professores_namespace.response(400, 'Dados inválidos', model=error_model)
    @login_requerido
    def post(self):
        data = request.get_json()
        return ProfessorController.criar_professor(data)

@professores_namespace.route('/<int:id_professor>')
@professores_namespace.param('id_professor', 'ID do professor')
class ProfessorResource(Resource):
    @professores_namespace.doc(security='Bearer Auth', description='Busca um professor pelo ID')
    @professores_namespace.marshal_with(professor_model)
    @professores_namespace.response(404, 'Professor não encontrado', model=error_model)
    @login_requerido
    def get(self, id_professor):
        return ProfessorController.buscar_professor_por_id(id_professor)

    @professores_namespace.doc(security='Bearer Auth', description='Atualiza os dados de um professor')
    @professores_namespace.expect(professor_model)
    @professores_namespace.marshal_with(success_model)
    @professores_namespace.response(404, 'Professor não encontrado', model=error_model)
    @professores_namespace.response(400, 'Dados inválidos', model=error_model)
    @login_requerido
    def put(self, id_professor):
        data = request.get_json()
        return ProfessorController.atualizar_professor(id_professor, data)

    @professores_namespace.doc(security='Bearer Auth', description='Exclui um professor')
    @professores_namespace.response(200, 'Professor removido com sucesso', model=success_model)
    @professores_namespace.response(404, 'Professor não encontrado', model=error_model)
    @login_requerido
    def delete(self, id_professor):
        return ProfessorController.excluir_professor(id_professor)