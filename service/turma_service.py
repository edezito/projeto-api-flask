from model.professor_model import Professor
from model.turma_model import Turma, TurmaNaoEncontrada
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

class TurmaService:
    """Serviço para operações relacionadas a turmas"""
    
    def __init__(self, session=None):
        from config import BancoDados
        self.session = session or BancoDados.SessionLocal()

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()

    def listar_turmas(self, filtros=None):
        """Lista turmas com filtros opcionais"""
        query = self.session.query(Turma).options(joinedload(Turma.professor))
        
        if filtros:
            if 'ativo' in filtros and filtros['ativo'] is not None:
                query = query.filter(Turma.ativo == filtros['ativo'])
            if 'professor_id' in filtros and filtros['professor_id'] is not None:
                query = query.filter(Turma.professor_id == filtros['professor_id'])

        total = query.count()
        turmas = query.all()
        return turmas, total

    def buscar_turma_por_id(self, id_turma):
        """Busca uma turma pelo ID com relacionamentos carregados"""
        turma = self.session.query(Turma)\
                .options(joinedload(Turma.professor))\
                .get(id_turma)
        if not turma:
            raise TurmaNaoEncontrada(id_turma)
        return turma
    
    def validar_dados(self, dados, criacao=True):
        """Valida os dados da turma"""
        campos_obrigatorios = ['descricao', 'professor_id'] if criacao else []

        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório faltando: {campo}")

        if 'descricao' in dados:
            descricao = dados['descricao'].strip()
            if not isinstance(descricao, str) or len(descricao) < 3:
                raise ValueError("Descrição deve ter pelo menos 3 caracteres")
            dados['descricao'] = descricao  # Atualiza com valor sanitizado

        if 'professor_id' in dados:
            if not isinstance(dados['professor_id'], int) or dados['professor_id'] <= 0:
                raise ValueError("ID do professor deve ser um número positivo")

        if 'ativo' in dados and not isinstance(dados['ativo'], bool):
            raise ValueError("Status 'ativo' deve ser True ou False")

    def criar_turma(self, dados_turma):
        """Cria uma nova turma"""
        self.validar_dados(dados_turma)
        
        # Remove campos não mapeados
        dados_turma = {
            k: v for k, v in dados_turma.items() 
            if k in ['descricao', 'professor_id', 'ativo']
        }
        
        # Verifica se o professor existe
        professor = self.session.get(Professor, dados_turma['professor_id'])
        if not professor:
            raise ValueError(f"Professor com ID {dados_turma['professor_id']} não encontrado")

        # Cria a turma
        turma = Turma(
            descricao=dados_turma['descricao'],
            professor_id=dados_turma['professor_id'],
            ativo=dados_turma.get('ativo', True)
        )

        self.session.add(turma)
        self.session.commit()
        self.session.refresh(turma)
        return turma
    
    def atualizar_turma(self, id_turma, dados):
        """Atualiza uma turma existente"""
        self.validar_dados(dados, criacao=False)

        turma = self.buscar_turma_por_id(id_turma)

        # Atualiza somente os campos fornecidos
        if 'descricao' in dados:
            turma.descricao = dados['descricao']
        if 'professor_id' in dados:
            # Verifica se o novo professor existe
            professor = self.session.get(Professor, dados['professor_id'])
            if not professor:
                raise ValueError(f"Professor com ID {dados['professor_id']} não encontrado")
            turma.professor_id = dados['professor_id']
        if 'ativo' in dados:
            turma.ativo = dados['ativo']

        self.session.add(turma)
        self.session.commit()
        return turma

    def atualizar_status_turma(self, id_turma, ativo):
        """Atualiza o status ativo/inativo da turma"""
        turma = self.buscar_turma_por_id(id_turma)
        turma.ativo = ativo
        self.session.add(turma)
        self.session.commit()
        return turma

    def excluir_turma(self, id_turma):
        """Exclui uma turma"""
        turma = self.buscar_turma_por_id(id_turma)

        # Verifica se há alunos vinculados
        if turma.alunos.count() > 0:
            raise ValueError("Não é possível excluir turma com alunos vinculados")

        self.session.delete(turma)
        self.session.commit()