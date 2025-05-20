from flask_restx import Resource
from flask import request
from config import BancoDados
from service.professor_service import ProfessorService
from swagger.namespaces.professor_namespace import professores_namespace, professor_model, success_model, error_model

@professores_namespace.route('/')
class ListaProfessores(Resource):
    @professores_namespace.marshal_list_with(professor_model)
    def get(self):
        filters = {
            'page': request.args.get('page', 1, type=int),
            'per_page': request.args.get('per_page', 20, type=int),
            'order_by': request.args.get('order_by', 'nome')
        }
        try:
            with BancoDados.SessionLocal() as session:
                professores, total = ProfessorService.listar_professores(session, **filters)
                return {
                    "success": True,
                    "message": "Lista de professores recuperada com sucesso",
                    "data": {
                        "professores": [p.to_dict() for p in professores],
                        "total": total
                    }
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @professores_namespace.expect(professor_model, validate=True)
    @professores_namespace.marshal_with(success_model, code=201)
    def post(self):
        dados = request.json
        try:
            with BancoDados.SessionLocal() as session:
                professor = ProfessorService.criar_professor(session, dados)
                return {
                    "success": True,
                    "message": "Professor criado com sucesso",
                    "data": {"professor": professor.to_dict()}
                }, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500


@professores_namespace.route('/<int:id_professor>')
@professores_namespace.param('id_professor', 'ID do professor')
class ProfessorResource(Resource):
    @professores_namespace.marshal_with(professor_model)
    def get(self, id_professor):
        try:
            with BancoDados.SessionLocal() as session:
                professor = ProfessorService.buscar_professor_por_id(session, id_professor)
                return {
                    "success": True,
                    "message": "Professor encontrado com sucesso",
                    "data": professor.to_dict()
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @professores_namespace.expect(professor_model, validate=True)
    @professores_namespace.marshal_with(success_model)
    def put(self, id_professor):
        dados = request.json
        try:
            with BancoDados.SessionLocal() as session:
                professor_atualizado = ProfessorService.atualizar_professor(session, id_professor, dados)
                return {
                    "success": True,
                    "message": "Professor atualizado com sucesso",
                    "data": {"professor": professor_atualizado.to_dict()}
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @professores_namespace.response(200, 'Professor removido com sucesso', model=success_model)
    def delete(self, id_professor):
        try:
            with BancoDados.SessionLocal() as session:
                ProfessorService.excluir_professor(session, id_professor)
                return {
                    "success": True,
                    "message": "Professor removido com sucesso",
                    "data": {"id": id_professor}
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500