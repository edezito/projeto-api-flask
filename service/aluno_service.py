from sqlalchemy.exc import SQLAlchemyError

from model.aluno_model import Aluno

class AlunoService:

    @staticmethod
    def validar_dados(dados):
        if not all(key in dados for key in ["nome", "idade", "turma_id"]):
            raise ValueError("Faltam campos obrigatórios")
        
        if not isinstance(dados["idade"], int) or not 0 <= dados["idade"] <= 120:
            raise ValueError("Idade inválida")

    @staticmethod
    def calcular_media(dados):
        nota_primeiro = dados.get("nota_primeiro_semestre", 0.0)
        nota_segundo = dados.get("nota_segundo_semestre", 0.0)
        return (nota_primeiro + nota_segundo) / 2