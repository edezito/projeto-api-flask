from model.turma_model import Turma, TurmaNaoEncontrada
from sqlalchemy.exc import SQLAlchemyError
from config import BancoDados

Session = BancoDados.Session

class TurmaService:
    """Serviço para operações relacionadas a turmas"""

    @staticmethod
    def listar_turmas(filtros=None):
        """
        Lista todas as turmas com possibilidade de filtros
        
        Args:
            filtros (dict): Dicionário com filtros (ex: {'ativo': True})
            
        Returns:
            list: Lista de objetos Turma
            
        Raises:
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            query = session.query(Turma)
            
            # Aplicar filtros se fornecidos
            if filtros:
                if 'ativo' in filtros:
                    query = query.filter(Turma.ativo == filtros['ativo'])
                if 'professor_id' in filtros:
                    query = query.filter(Turma.professor_id == filtros['professor_id'])
            
            return query.all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao listar turmas: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def buscar_turma_por_id(id_turma):
        """
        Busca uma turma específica pelo ID
        
        Args:
            id_turma (int): ID da turma
            
        Returns:
            Turma: Objeto Turma encontrado
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada")
            return turma
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar turma: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def validar_dados(dados, criacao=True):
        """
        Valida os dados da turma antes de criar ou atualizar
        
        Args:
            dados (dict): Dados da turma a validar
            criacao (bool): Se True, valida campos obrigatórios para criação
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        campos_obrigatorios = ['descricao', 'professor_id'] if criacao else []
        
        # Verifica campos obrigatórios
        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório faltando: {campo}")
        
        # Valida tipos dos campos
        if 'descricao' in dados and (not isinstance(dados['descricao'], str) or len(dados['descricao'].strip()) < 3):
            raise ValueError("Descrição deve ter pelo menos 3 caracteres")
            
        if 'professor_id' in dados and (not isinstance(dados['professor_id'], int) or dados['professor_id'] <= 0):
            raise ValueError("ID do professor deve ser um número positivo")
            
        if 'ativo' in dados and not isinstance(dados['ativo'], bool):
            raise ValueError("Status 'ativo' deve ser True ou False")

    @staticmethod
    def criar_turma(dados_turma):
        """
        Cria uma nova turma no sistema
        
        Args:
            dados_turma (dict): Dados da nova turma
            
        Returns:
            Turma: Objeto Turma criado
            
        Raises:
            ValueError: Se os dados forem inválidos
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            # Valida os dados
            TurmaService.validar_dados(dados_turma, criacao=True)
            
            # Cria a turma
            turma = Turma(
                descricao=dados_turma['descricao'].strip(),
                professor_id=dados_turma['professor_id'],
                ativo=dados_turma.get('ativo', True)
            )
            
            session.add(turma)
            session.commit()
            return turma
        except ValueError as ve:
            session.rollback()
            raise ve
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao criar turma: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def atualizar_turma(id_turma, dados_atualizacao):
        """
        Atualiza os dados de uma turma existente
        
        Args:
            id_turma (int): ID da turma a atualizar
            dados_atualizacao (dict): Dados a serem atualizados
            
        Returns:
            Turma: Objeto Turma atualizado
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            ValueError: Se os dados forem inválidos
            Exception: Em caso de erro no banco de dados
        """
        session = Session()
        try:
            # Busca a turma
            turma = session.query(Turma).get(id_turma)
            if not turma:
                raise TurmaNaoEncontrada(f"Turma com ID {id_turma} não encontrada")
            
            # Valida os dados
            TurmaService.validar_dados(dados_atualizacao, criacao=False)
            
            # Aplica as atualizações
            if 'descricao' in dados_atualizacao:
                turma.descricao = dados_atualizacao['descricao'].strip()
            if 'professor_id' in dados_atualizacao:
                turma.professor_id = dados_atualizacao['professor_id']
            if 'ativo' in dados_atualizacao:
                turma.ativo = dados_atualizacao['ativo']
            
            session.commit()
            return turma
        except (TurmaNaoEncontrada, ValueError) as e:
            session.rollback()
            raise e
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar turma: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def desativar_turma(id_turma):
        """
        Desativa uma turma (exclusão lógica)
        
        Args:
            id_turma (int): ID da turma a desativar
            
        Returns:
            Turma: Objeto Turma desativado
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            Exception: Em caso de erro no banco de dados
        """
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
        """
        Remove permanentemente uma turma do sistema (exclusão física)
        
        Args:
            id_turma (int): ID da turma a excluir
            
        Returns:
            bool: True se a exclusão foi bem-sucedida
            
        Raises:
            TurmaNaoEncontrada: Se a turma não existir
            Exception: Em caso de erro no banco de dados
        """
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