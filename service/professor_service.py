from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from model.professor_model import Professor
from config import BancoDados

class ProfessorService:

    @staticmethod
    def listar_professores(session, page=1, per_page=20, order_by='nome'):
        query = session.query(Professor)
        if hasattr(Professor, order_by):
            query = query.order_by(getattr(Professor, order_by))
        total = query.count()
        professores = query.offset((page - 1) * per_page).limit(per_page).all()
        return professores, total

    @staticmethod
    def criar_professor(session, data):
        try:
            professor = Professor(
                nome=data['nome'],  # Acessa como obrigatório
                idade=data['idade'],
                materia=data['materia'],
                observacoes=data.get('observacoes')  # Opcional
            )
            session.add(professor)
            session.commit()
            session.refresh(professor)  # Garante que temos o ID gerado
            return professor
        except KeyError as e:
            raise ValueError(f"Campo obrigatório faltando: {str(e)}")

    @staticmethod
    def buscar_professor_por_id(session, id_professor):
        professor = session.get(Professor, id_professor)
        if not professor:
            raise NoResultFound("Professor não encontrado")
        return professor

    @staticmethod
    def atualizar_professor(session, id_professor, data):
        professor = session.get(Professor, id_professor)
        if not professor:
            raise NoResultFound("Professor não encontrado")
        for key, value in data.items():
            if hasattr(professor, key) and key != 'id':
                setattr(professor, key, value)
        session.commit()
        return professor

    @staticmethod
    def excluir_professor(session, id_professor):
        professor = session.get(Professor, id_professor)
        if not professor:
            raise NoResultFound("Professor não encontrado")
        session.delete(professor)
        session.commit()
        return professor