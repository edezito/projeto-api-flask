import jwt
import datetime
from config import BancoDados, Config
from model.usuario_model import Usuario
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Session = sessionmaker(bind=BancoDados.engine)

class AuthService:
    @staticmethod
    def autenticar_usuario(nickname, senha):
        session = Session()
        try:
            usuario_obj = session.query(Usuario).filter_by(nickname=nickname).one()
            if usuario_obj.senha != senha:
                raise ValueError("Senha inválida")

            token = jwt.encode({
                "usuario": usuario_obj.nickname,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, Config.SECRET_KEY, algorithm="HS256")

            return {"mensagem": f"Login bem-sucedido, {usuario_obj.nome}!", "token": token}, 200
        except NoResultFound:
            return {"erro": "Usuário não encontrado"}, 404
        except ValueError as e:
            return {"erro": str(e)}, 403
        except Exception as e:
            return {"erro": "Erro inesperado: " + str(e)}, 500
        finally:
            session.close()

    @staticmethod
    def verificar_token(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")