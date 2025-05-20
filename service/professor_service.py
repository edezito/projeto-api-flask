from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from model.professor_model import Professor
from config import BancoDados

class ProfessorService:

    @staticmethod
    def listar_professores(page=1, per_page=20, order_by='nome'):
        """Lista professores com paginação e ordenação."""
        session = BancoDados.get_session()
        try:
            query = session.query(Professor)
            
            # Ordenação
            if hasattr(Professor, order_by):
                query = query.order_by(getattr(Professor, order_by))
                
            # Paginação
            total = query.count()
            professores = query.offset((page - 1) * per_page).limit(per_page).all()
            
            return [p.to_dict() for p in professores], total
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def criar_professor(data):
        """Cria um novo professor e salva no banco de dados."""
        session = BancoDados.get_session()
        try:
            professor = Professor(
                nome=data.get('nome'),
                idade=data.get('idade'),
                materia=data.get('materia'),
                observacoes=data.get('observacoes', None)
            )
            
            session.add(professor)
            session.commit()
            return professor
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def buscar_professor_por_id(id_professor):
        """Busca um professor pelo ID. Levanta uma exceção caso não seja encontrado."""
        session = BancoDados.get_session()
        try:
            professor = session.query(Professor).get(id_professor)
            if not professor:
                raise NoResultFound("Professor não encontrado")
            return professor
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def atualizar_professor(id_professor, data):
        """Atualiza os dados de um professor existente no banco de dados."""
        session = BancoDados.get_session()
        try:
            professor = session.query(Professor).get(id_professor)
            if not professor:
                raise NoResultFound("Professor não encontrado")
            
            # Atualiza os atributos do professor
            for key, value in data.items():
                if hasattr(professor, key) and key != 'id':
                    setattr(professor, key, value)
            
            session.commit()
            return professor
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def excluir_professor(id_professor):
        """Remove um professor do banco de dados."""
        session = BancoDados.get_session()
        try:
            professor = session.query(Professor).get(id_professor)
            if not professor:
                raise NoResultFound("Professor não encontrado")
            
            session.delete(professor)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()