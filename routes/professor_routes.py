from flask_restx import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from config import BancoDados
from service.professor_service import ProfessorService
from swagger.namespaces.professor_namespace import professores_namespace, professor_model, success_model, error_model

@professores_namespace.route('/')
class ListaProfessores(Resource):
    @professores_namespace.doc('listar_professores')
    @professores_namespace.response(200, 'Sucesso', success_model)
    @professores_namespace.response(500, 'Erro interno', error_model)
    def get(self):
        """Lista todos os professores com paginação"""
        try:
            filters = {
                'page': request.args.get('page', 1, type=int),
                'per_page': request.args.get('per_page', 20, type=int),
                'order_by': request.args.get('order_by', 'nome')
            }
            
            with BancoDados.SessionLocal() as session:
                professores, total = ProfessorService.listar_professores(session, **filters)
                
                return {
                    "success": True,
                    "message": "Lista de professores recuperada com sucesso",
                    "data": {
                        "professores": [p.to_dict() for p in professores],
                        "total": total,
                        "pagina": filters['page'],
                        "por_pagina": filters['per_page']
                    }
                }, 200
                
        except ValueError as e:
            return {
                "success": False,
                "message": "Parâmetros inválidos",
                "error": str(e)
            }, 400
        except Exception as e:
            return {
                "success": False,
                "message": "Erro ao listar professores",
                "error": str(e)
            }, 500

    @professores_namespace.doc('criar_professor')
    @professores_namespace.expect(professor_model)
    @professores_namespace.response(201, 'Professor criado', success_model)
    @professores_namespace.response(400, 'Dados inválidos', error_model)
    @professores_namespace.response(500, 'Erro interno', error_model)
    def post(self):
        """Cria um novo professor"""
        dados = request.get_json()
        if not dados:
            return {
                "success": False,
                "message": "Nenhum dado fornecido",
                "error": "O corpo da requisição está vazio"
            }, 400

        try:
            with BancoDados.SessionLocal() as session:
                professor = ProfessorService.criar_professor(session, dados)
                return {
                    "success": True,
                    "message": "Professor criado com sucesso",
                    "data": professor.to_dict()
                }, 201
        except ValueError as e:
            return {
                "success": False,
                "message": "Dados inválidos",
                "error": str(e)
            }, 400
        except Exception as e:
            return {
                "success": False,
                "message": "Erro ao criar professor",
                "error": str(e)
            }, 500


@professores_namespace.route('/<int:id_professor>')
@professores_namespace.param('id_professor', 'ID do professor')
class ProfessorResource(Resource):
    @professores_namespace.doc('obter_professor')
    @professores_namespace.response(200, 'Sucesso', success_model)
    @professores_namespace.response(404, 'Não encontrado', error_model)
    @professores_namespace.response(500, 'Erro interno', error_model)
    def get(self, id_professor):
        """Obtém um professor pelo ID"""
        try:
            with BancoDados.SessionLocal() as session:
                professor = ProfessorService.buscar_professor_por_id(session, id_professor)
                return {
                    "success": True,
                    "message": "Professor encontrado com sucesso",
                    "data": professor.to_dict()
                }, 200
        except NoResultFound:
            return {
                "success": False,
                "message": "Professor não encontrado",
                "error": f"Professor com ID {id_professor} não existe"
            }, 404
        except Exception as e:
            return {
                "success": False,
                "message": "Erro ao buscar professor",
                "error": str(e)
            }, 500

    @professores_namespace.doc('atualizar_professor')
    @professores_namespace.expect(professor_model)
    @professores_namespace.response(200, 'Professor atualizado', success_model)
    @professores_namespace.response(400, 'Dados inválidos', error_model)
    @professores_namespace.response(404, 'Não encontrado', error_model)
    @professores_namespace.response(500, 'Erro interno', error_model)
    def put(self, id_professor):
        """Atualiza um professor existente"""
        dados = request.get_json()
        if not dados:
            return {
                "success": False,
                "message": "Nenhum dado fornecido",
                "error": "O corpo da requisição está vazio"
            }, 400

        try:
            with BancoDados.SessionLocal() as session:
                professor = ProfessorService.atualizar_professor(session, id_professor, dados)
                return {
                    "success": True,
                    "message": "Professor atualizado com sucesso",
                    "data": professor.to_dict()
                }, 200
        except NoResultFound:
            return {
                "success": False,
                "message": "Professor não encontrado",
                "error": f"Professor com ID {id_professor} não existe"
            }, 404
        except ValueError as e:
            return {
                "success": False,
                "message": "Dados inválidos",
                "error": str(e)
            }, 400
        except Exception as e:
            return {
                "success": False,
                "message": "Erro ao atualizar professor",
                "error": str(e)
            }, 500

    @professores_namespace.doc('remover_professor')
    @professores_namespace.response(204, 'Professor removido')
    @professores_namespace.response(404, 'Não encontrado', error_model)
    @professores_namespace.response(500, 'Erro interno', error_model)
    def delete(self, id_professor):
        """Remove um professor"""
        try:
            with BancoDados.SessionLocal() as session:
                ProfessorService.excluir_professor(session, id_professor)
                return '', 204
        except NoResultFound:
            return {
                "success": False,
                "message": "Professor não encontrado",
                "error": f"Professor com ID {id_professor} não existe"
            }, 404
        except Exception as e:
            return {
                "success": False,
                "message": "Erro ao remover professor",
                "error": str(e)
            }, 500