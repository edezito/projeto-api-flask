from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from model.aluno_model import Aluno
from model.turma_model import Turma

class AlunoService:

    @staticmethod
    def calcular_media(dados):
        """Calcula a média das notas do aluno."""
        nota_primeiro = dados.get("nota_primeiro_semestre", 0.0)
        nota_segundo = dados.get("nota_segundo_semestre", 0.0)
        
        # Calcula a média apenas se as duas notas forem fornecidas
        if nota_primeiro is None or nota_segundo is None:
            return None
            
        return (nota_primeiro + nota_segundo) / 2

    @staticmethod
    def listar_alunos(session, page=1, per_page=20, order_by='nome'):
        """Lista alunos com paginação e ordenação."""
        query = session.query(Aluno)
        
        # Ordenação
        if hasattr(Aluno, order_by):
            query = query.order_by(getattr(Aluno, order_by))
            
        # Paginação
        total = query.count()
        alunos = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return alunos, total

    @staticmethod
    def criar_aluno(session, nome, idade, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
        """Cria um novo aluno e salva no banco de dados."""
        aluno = Aluno(
            nome=nome,
            idade=idade,
            nota_primeiro_semestre=nota_primeiro_semestre,
            nota_segundo_semestre=nota_segundo_semestre,
            turma_id=turma_id
        )
        
        # Calcula a média após criar o aluno
        aluno.calcular_media()

        session.add(aluno)
        session.commit()  # Comita a transação

        return aluno.to_dict()

    @staticmethod
    def buscar_aluno_por_id(session, id_aluno):
        """Busca um aluno pelo ID. Levanta uma exceção caso não seja encontrado."""
        aluno = session.query(Aluno).get(id_aluno)
        if not aluno:
            raise NoResultFound("Aluno não encontrado")
        return aluno

    @staticmethod
    def atualizar_aluno(session, id_aluno, dados):
        """Atualiza os dados de um aluno existente no banco de dados."""
        AlunoService.validar_dados(dados, is_update=True)
        aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
        
        # Atualiza os atributos do aluno
        for key, value in dados.items():
            if hasattr(aluno, key) and key != 'id':
                setattr(aluno, key, value)
        
        # Recalcula a média após a atualização das notas
        aluno.calcular_media()

        session.flush()
        return aluno

    @staticmethod
    def excluir_aluno(session, id_aluno):
        """Remove um aluno do banco de dados."""
        aluno = AlunoService.buscar_aluno_por_id(session, id_aluno)
        session.delete(aluno)
        session.flush()
        return aluno

    @staticmethod
    def validar_dados(dados, is_update=False):
        """Valida os dados do aluno conforme as regras de negócio."""
        if not dados:
            raise ValueError("Dados não fornecidos")
        
        # Campos obrigatórios para criação de aluno
        required_fields = ['nome', 'turma_id']
        if not is_update:
            for field in required_fields:
                if field not in dados:
                    raise ValueError(f"Campo obrigatório faltando: {field}")
                    
        # Não é permitido fornecer o campo 'id' manualmente
        if 'id' in dados:
            raise ValueError("O ID não deve ser fornecido manualmente")
        
        # Validação de idade
        if 'idade' in dados and (not isinstance(dados['idade'], int) or not 0 <= dados['idade'] <= 120):
            raise ValueError("Idade inválida")
        
        # Validação de matrícula
        if 'matricula' in dados and not isinstance(dados['matricula'], str):
            raise ValueError("Matrícula deve ser uma string")
