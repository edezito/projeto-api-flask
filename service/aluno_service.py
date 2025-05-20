from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from model.aluno_model import Aluno
from model.turma_model import Turma

class AlunoService:

    @staticmethod
    def calcular_media(dados):
        """Calcula a média das notas do aluno."""
        nota_primeiro = dados.get("nota_primeiro_semestre")
        nota_segundo = dados.get("nota_segundo_semestre")
        
        if nota_primeiro is None or nota_segundo is None:
            return None
            
        return (nota_primeiro + nota_segundo) / 2

    @staticmethod
    def listar_alunos(session, page=1, per_page=20, order_by='nome'):
        """Lista alunos com paginação e ordenação."""
        query = session.query(Aluno)
        
        if hasattr(Aluno, order_by):
            query = query.order_by(getattr(Aluno, order_by))
        
        total = query.count()
        alunos = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return alunos, total

    @staticmethod
    def criar_aluno(session, dados):
        """Cria um novo aluno a partir de um dicionário de dados."""
        AlunoService.validar_dados(dados)

        aluno = Aluno(
            nome=dados["nome"],
            idade=dados["idade"],
            nota_primeiro_semestre=dados.get("nota_primeiro_semestre"),
            nota_segundo_semestre=dados.get("nota_segundo_semestre"),
            turma_id=dados["turma_id"]
        )

        aluno.calcular_media()

        try:
            session.add(aluno)
            session.commit()
            session.refresh(aluno)
            return aluno  # Retorna o objeto Aluno em vez do dicionário
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Erro ao criar aluno: {str(e)}")

    @staticmethod
    def buscar_aluno_por_id(session, id_aluno):
        if not isinstance(id_aluno, int) or id_aluno <= 0:
            raise ValueError("ID do aluno inválido")
        
        aluno = session.get(Aluno, id_aluno)
        if not aluno:
            raise NoResultFound(f"Aluno com ID {id_aluno} não encontrado")
        
        # Verificação adicional
        if not hasattr(aluno, 'nome') or not hasattr(aluno, 'idade'):
            raise ValueError("Objeto aluno corrompido")
        
        return aluno

    @staticmethod
    def atualizar_aluno(dados, aluno_obj):
        """Atualiza um aluno existente com os novos dados.
        
        Args:
            dados: Dicionário com os dados para atualização
            aluno_obj: Objeto Aluno a ser atualizado
        """
        # Verificação do objeto aluno
        if not hasattr(aluno_obj, 'id') or not isinstance(aluno_obj.id, int):
            raise ValueError("Objeto aluno inválido")

        # Atualização dos campos
        campos_permitidos = ['nome', 'idade', 'nota_primeiro_semestre', 
                            'nota_segundo_semestre', 'turma_id']
        
        for campo in campos_permitidos:
            if campo in dados:
                setattr(aluno_obj, campo, dados[campo])

        aluno_obj.calcular_media()
        return aluno_obj

    @staticmethod
    def excluir_aluno(session, id_aluno):
        """Remove um aluno do banco de dados."""
        aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
        try:
            session.delete(aluno)
            session.commit()  # Alterado de flush() para commit()
            return {"id": aluno.id}  # Retorna dict simples em vez de chamar to_dict()
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Erro ao excluir aluno: {str(e)}")

    @staticmethod
    def validar_dados(dados, is_update=False):
        """Valida os dados do aluno conforme as regras de negócio."""
        if not dados:
            raise ValueError("Dados não fornecidos")
        
        required_fields = ['nome', 'idade', 'turma_id']
        if not is_update:
            for field in required_fields:
                if field not in dados:
                    raise ValueError(f"Campo obrigatório faltando: {field}")
        
        if 'id' in dados:
            raise ValueError("O ID não deve ser fornecido manualmente")
        
        if 'idade' in dados and (not isinstance(dados['idade'], int) or not 0 <= dados['idade'] <= 120):
            raise ValueError("Idade inválida")
