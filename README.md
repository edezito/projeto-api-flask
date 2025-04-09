# API School System – Entrega 2: Projeto Flask com MVC

Grupo 1: Éder Duarte, Felipe Lima Nogueira, Victor Henrique Souza Oliveira

Data da atividade: 09/04/2025

## Melhorias Implementadas na Entrega 2

A entrega 2 do projeto API School System focou em aprimorar a API Flask, abordando vários desafios e melhorias propostas na entrega 1.

## Autenticação e Autorização

Foi implementado um sistema de autenticação utilizando JWT (JSON Web Tokens) para proteger as rotas da API. Isso garante que apenas usuários autenticados possam acessar e manipular os dados de Professores, Turmas e Alunos. As rotas agora utilizam o decorador `@login_requerido` para verificar a validade do token.

## Validações

Para a entidade Aluno, foram adicionadas validações no momento da criação. Agora, a API verifica a presença de campos obrigatórios como "id", "nome", "idade", "turma_id" e "data_nascimento". Também foi implementada a função `validar_idade` para garantir que a idade fornecida seja um número inteiro entre 0 e 120. A criação de Professores e Turmas também foi aprimorada com a verificação da presença de campos obrigatórios e a não duplicação de IDs.

## Tratamento de Erros

A API agora retorna mensagens de erro mais informativas em formato JSON, com códigos de status HTTP apropriados (e.g., 400 para Bad Request, 404 para Not Found). Isso facilita o diagnóstico de problemas durante o uso da API.

## Testes Automatizados

Foram criados testes automatizados utilizando o framework `pytest`. Esses testes cobrem tanto a lógica de validação (testes unitários para `validar_idade`) quanto o funcionamento das rotas da API (testes de integração e E2E). Os testes verificam o comportamento esperado da API em diferentes cenários, incluindo casos de sucesso e casos de erro.

## Organização do Código

O código foi estruturado em blueprints para melhor organização das rotas (`aluno_routes.py`, `professor_routes.py`, `turma_routes.py`, `autenticacao.py`). Isso facilita a manutenção e escalabilidade do projeto. Os alunos Éder Bento Duarte e Victor Henrique Souza de Oliveira foram os principais responsáveis pela implementação dos arquivos de models, routes e autenticação, além da implementação dos testes automatizados, com apoio de Felipe Lima Nogueira.

## Configuração

Foi adicionado um arquivo `config.py` para centralizar as configurações da API (host, porta, debug, secret key). Isso permite uma configuração mais fácil do ambiente de execução. O aluno Felipe Lima Nogueira criou o arquivo `config.py`, elaborou este relatório e implementou outros testes automatizados, além de prestar apoio na criação dos outros arquivos.