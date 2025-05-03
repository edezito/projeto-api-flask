from flask_restx import Resource
from flask import request
from config import BancoDados
from service.aluno_service import AlunoService
from service.login_requerido import login_requerido
from swagger.namespaces.alunos_namespace import alunos_namespace, aluno_model

@alunos_namespace.route('/')
class AlunoListResource(Resource):
    @alunos_namespace.doc(security='Bearer Auth')
    @login_requerido
    def get(self):
        """Lista todos os alunos"""
        filters = {
            'page': request.args.get('page', 1, type=int),
            'per_page': request.args.get('per_page', 20, type=int),
            'order_by': request.args.get('order_by', 'nome')
        }
        with BancoDados.SessionLocal() as session:
            alunos, total = AlunoService.listar_alunos(session, **filters)
            return {
                "success": True,
                "message": "Lista de alunos recuperada com sucesso",
                "data": {
                    "alunos": [a.to_dict() for a in alunos],
                    "total": total
                }
            }, 200

    @alunos_namespace.expect(aluno_model, validate=True)
    @login_requerido
    def post(self):
        """Cria um novo aluno"""
        dados = request.json
        try:
            with BancoDados.SessionLocal() as session:
                aluno = AlunoService.criar_aluno(session, dados)
                return {
                    "success": True,
                    "message": "Aluno criado com sucesso",
                    "data": {"aluno": aluno.to_dict()}
                }, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500


@alunos_namespace.route('/<int:id>')
@alunos_namespace.param('id', 'ID do aluno')
class AlunoResource(Resource):
    @login_requerido
    def get(self, id):
        """Busca um aluno pelo ID"""
        try:
            with BancoDados.SessionLocal() as session:
                aluno = AlunoService.buscar_aluno_por_id(session, id)
                return {
                    "success": True,
                    "message": "Aluno encontrado com sucesso",
                    "data": aluno.to_dict()
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @alunos_namespace.expect(aluno_model, validate=True)
    @login_requerido
    def put(self, id):
        """Atualiza um aluno existente"""
        dados = request.json
        try:
            with BancoDados.SessionLocal() as session:
                aluno_atualizado = AlunoService.atualizar_aluno(session, id, dados)
                return {
                    "success": True,
                    "message": "Aluno atualizado com sucesso",
                    "data": {"aluno": aluno_atualizado.to_dict()}
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @login_requerido
    def delete(self, id):
        """Exclui um aluno pelo ID"""
        try:
            with BancoDados.SessionLocal() as session:
                AlunoService.excluir_aluno(session, id)
                return {
                    "success": True,
                    "message": "Aluno removido com sucesso",
                    "data": {"id": id}
                }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500