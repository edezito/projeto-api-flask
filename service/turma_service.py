from model.professor_model import Professor
from model.turma_model import Turma, TurmaNaoEncontrada
from sqlalchemy.exc import SQLAlchemyError
from config import BancoDados

Session = BancoDados.SessionLocal

class TurmaService:
    """Serviço para operações relacionadas a turmas"""

    @staticmethod
    def listar_turmas(session, filtros=None):
        from sqlalchemy.orm import joinedload
        
        query = session.query(Turma).options(joinedload(Turma.professor))
        try:
            if filtros:
                if 'ativo' in filtros and filtros['ativo'] is not None:
                    query = query.filter(Turma.ativo == filtros['ativo'])
                if 'professor_id' in filtros and filtros['professor_id'] is not None:
                    query = query.filter(Turma.professor_id == filtros['professor_id'])

            total = query.count()
            turmas = query.all()
            return turmas, total
        except Exception as e:
            session.rollback()
            raise e
        # Remover o session.close() aqui para evitar problemas com objetos desconectados

    @staticmethod
    def buscar_turma_por_id(session, id_turma):
        turma = session.query(Turma).get(id_turma)
        if not turma:
            raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada")
        return turma

    @staticmethod
    def validar_dados(dados, criacao=True):
        campos_obrigatorios = ['descricao', 'professor_id'] if criacao else []

        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório faltando: {campo}")

        if 'descricao' in dados and (not isinstance(dados['descricao'], str) or len(dados['descricao'].strip()) < 3):
            raise ValueError("Descrição deve ter pelo menos 3 caracteres")

        if 'professor_id' in dados and (not isinstance(dados['professor_id'], int) or dados['professor_id'] <= 0):
            raise ValueError("ID do professor deve ser um número positivo")

        if 'ativo' in dados and not isinstance(dados['ativo'], bool):
            raise ValueError("Status 'ativo' deve ser True ou False")

    @staticmethod
    def criar_turma(session, dados_turma):
        try:
            # Remove campos não mapeados
            dados_turma = {k: v for k, v in dados_turma.items() 
                        if k in ['descricao', 'professor_id', 'ativo']}
            
            # Verifica se o professor existe
            professor = session.get(Professor, dados_turma['professor_id'])
            if not professor:
                raise ValueError(f"Professor com ID {dados_turma['professor_id']} não encontrado")

            # Cria a turma
            turma = Turma(
                descricao=dados_turma['descricao'].strip(),
                professor_id=dados_turma['professor_id'],
                ativo=dados_turma.get('ativo', True)
            )

            session.add(turma)
            session.commit()
            
            # Recarrega a turma com relacionamentos
            session.refresh(turma)
            return turma
            
        except Exception as e:
            session.rollback()
            raise ValueError(f"Erro ao criar turma: {str(e)}")

    @staticmethod
    def atualizar_turma(session, id_turma, dados):
        TurmaService.validar_dados(dados, criacao=False)  # validação parcial para atualização

        turma = session.query(Turma).get(id_turma)
        if not turma:
            raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada")

        # Atualizar somente os campos que vieram no request
        if 'descricao' in dados:
            turma.descricao = dados['descricao']
        if 'professor_id' in dados:
            turma.professor_id = dados['professor_id']
        if 'ativo' in dados:
            turma.ativo = dados['ativo']

        session.add(turma)
        # Commit é feito no decorator do controller
        return turma

    @staticmethod
    def desativar_turma(id_turma):
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada")

            turma.ativo = False
            session.commit()
            return turma
        except TurmaNaoEncontrada as e:
            session.rollback()
            raise e
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao desativar turma: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def excluir_turma(id_turma):
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada")

            session.delete(turma)
            session.commit()
            return True
        except TurmaNaoEncontrada as e:
            session.rollback()
            raise e
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao excluir turma: {str(e)}")
        finally:
            session.close()
