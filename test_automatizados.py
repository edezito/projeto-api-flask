import pytest
from flask_restx import fields
from swagger.namespaces.login_namespace import login_namespace

# Fixture para carregar os modelos
@pytest.fixture(scope="module")
def modelos():
    models = {
        'credenciais': login_namespace.models['Credenciais'],  # Usando acesso direto pois já validamos a existência
        'resposta_login': login_namespace.models['RespostaLogin'],
        'user_info': login_namespace.models['UserInfo'],
        'erro': login_namespace.models['Erro']
    }
    return models

## TESTES PARA O MODELO DE CREDENCIAIS ##
@pytest.mark.parametrize("campo,requerido,tipo,min_len,max_len,descricao,exemplo", [
    ('usuario', True, fields.String, 4, 20, "Nome de usuário", 'admin'),
    ('senha', True, fields.String, 4, None, "Senha do usuário", '1234'),
])
def test_campos_credenciais(modelos, campo, requerido, tipo, min_len, max_len, descricao, exemplo):
    """Testa os campos do modelo Credenciais"""
    credenciais = modelos['credenciais']
    campo_modelo = credenciais[campo]
    
    assert campo_modelo.required == requerido, f"Campo '{campo}' deve ser {'obrigatório' if requerido else 'opcional'}"
    assert isinstance(campo_modelo, tipo), f"Tipo do campo '{campo}' deve ser {tipo.__name__}"
    assert campo_modelo.min_length == min_len, f"Tamanho mínimo do campo '{campo}' deve ser {min_len}"
    if max_len:
        assert campo_modelo.max_length == max_len, f"Tamanho máximo do campo '{campo}' deve ser {max_len}"
    assert campo_modelo.description == descricao, f"Descrição do campo '{campo}' incorreta"
    assert campo_modelo.example == exemplo, f"Exemplo do campo '{campo}' incorreto"

## TESTES PARA O MODELO DE RESPOSTA DE LOGIN ##
@pytest.mark.parametrize("campo,requerido,tipo,descricao,default", [
    ('access_token', True, fields.String, "Token JWT para autenticação", None),
    ('refresh_token', True, fields.String, "Token para renovação", None),
    ('token_type', True, fields.String, "Tipo do token", 'Bearer'),
    ('expires_in', True, fields.Integer, "Tempo de expiração em segundos", 3600),
    ('user_info', True, fields.Nested, "Informações do usuário", None),
])
def test_campos_resposta_login(modelos, campo, requerido, tipo, descricao, default):
    """Testa os campos do modelo RespostaLogin"""
    resposta = modelos['resposta_login']
    campo_modelo = resposta[campo]
    
    assert campo_modelo.required == requerido, f"Campo '{campo}' deve ser {'obrigatório' if requerido else 'opcional'}"
    assert isinstance(campo_modelo, tipo), f"Tipo do campo '{campo}' deve ser {tipo.__name__}"
    assert campo_modelo.description == descricao, f"Descrição do campo '{campo}' incorreta"
    if default is not None:
        assert campo_modelo.default == default, f"Valor padrão do campo '{campo}' deve ser {default}"

## TESTES PARA O MODELO DE USER INFO ##
def test_estrutura_user_info(modelos):
    """Testa a estrutura aninhada de user_info"""
    user_info = modelos['user_info']
    
    campos_esperados = {
        'id': (fields.Integer, False, "ID do usuário"),
        'nome': (fields.String, False, "Nome completo"),
        'email': (fields.String, False, "E-mail do usuário"),
        'roles': (fields.List, False, "Perfis de acesso")
    }
    
    for campo, (tipo, requerido, descricao) in campos_esperados.items():
        campo_modelo = user_info[campo]
        assert campo_modelo.required == requerido, (
            f"Campo '{campo}' deveria ser {'obrigatório' if requerido else 'opcional'} "
            f"mas está marcado como {'obrigatório' if campo_modelo.required else 'opcional'}"
        )
        assert isinstance(campo_modelo, tipo), f"Tipo incorreto para {campo}"
        assert campo_modelo.description == descricao, f"Descrição incorreta para {campo}"
    
    # Verificação adicional para o campo roles
    assert isinstance(user_info['roles'].container, fields.String), "Itens da lista roles devem ser strings"

## TESTES PARA O MODELO DE ERRO ##
@pytest.mark.parametrize("campo,requerido,tipo,descricao,exemplo,default", [
    ('status', False, fields.String, None, None, 'error'),
    ('message', True, fields.String, None, None, None),
    ('code', False, fields.Integer, None, 401, None),
])
def test_campos_erro(modelos, campo, requerido, tipo, descricao, exemplo, default):
    """Testa os campos do modelo Erro"""
    erro = modelos['erro']
    campo_modelo = erro[campo]
    
    assert campo_modelo.required == requerido, f"Campo '{campo}' deve ser {'obrigatório' if requerido else 'opcional'}"
    assert isinstance(campo_modelo, tipo), f"Tipo do campo '{campo}' deve ser {tipo.__name__}"
    if descricao:
        assert campo_modelo.description == descricao, f"Descrição do campo '{campo}' incorreta"
    if exemplo:
        assert campo_modelo.example == exemplo, f"Exemplo do campo '{campo}' incorreto"
    if default:
        assert campo_modelo.default == default, f"Valor padrão do campo '{campo}' deve ser {default}"