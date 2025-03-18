API SCHOOL SYSTEM

Projeto Flask Inicial

GRUPO: Éder Duarte, Felipe Lima Nogueira e Victor Henrique Souza Oliveira.

OBJETIVO:

O objetivo deste projeto é desenvolver uma API utilizando Flask para gerenciar Professores, Turmas e Alunos. A API permite a realização das operações CRUD (Create, Read, Update e Delete) para cada uma dessas entidades, fornecendo respostas em formato JSON. Além disso, utiliza um sistema de controle de versão para gerenciamento do código-fonte.

INTRODUÇÃO:

A implementação de APIs RESTful tornou-se uma prática essencial no desenvolvimento de sistemas modernos, permitindo integração eficiente entre diferentes aplicações e plataformas. O Flask, um micro framework em Python, é uma escolha popular para o desenvolvimento de APIs devido à sua simplicidade e flexibilidade.

Este projeto visa criar uma API básica para o gerenciamento de informações relacionadas a Professores, Turmas e Alunos, facilitando sua administração e manipulação de dados.

IMPLEMENTAÇÃO:

O projeto propõe a criação de uma API para gestão educacional, permitindo o cadastramento, consulta, edição e remoção de dados das seguintes entidades:

Entidades e Campos

Professores: Nome, área de atuação, identificação.

Turmas: Nome, professor responsável, lista de alunos.

Alunos: Nome, idade, turma associada.

A API retorna os dados em formato JSON, permitindo integração com outras aplicações e sistemas.

ENDPOINTS CRUD:

Professores

GET /professores - Listar todos os professores.

POST /professores - Adicionar um novo professor.

PUT /professores/<id> - Atualizar dados de um professor.

DELETE /professores/<id> - Remover um professor.

Turmas

GET /turmas - Listar todas as turmas.

POST /turmas - Criar uma nova turma.

PUT /turmas/<id> - Atualizar dados de uma turma.

DELETE /turmas/<id> - Remover uma turma.

Alunos

GET /alunos - Listar todos os alunos.

POST /alunos - Adicionar um novo aluno.

PUT /alunos/<id> - Atualizar dados de um aluno.

DELETE /alunos/<id> - Remover um aluno.

FORMATO DAS RESPOSTAS:

Todas as respostas da API seguem o formato JSON para garantir padronização e compatibilidade.

TESTES:

Os testes da API foram realizados utilizando o Postman, validando o funcionamento de todas as requisições.

CONTROLE DE VERSÃO:

A API utiliza um repositório Git para controle de versão e histórico do código.

CONCLUSÃO:

A API foi implementada com sucesso, permitindo a interação eficiente com as entidades do sistema. Os testes realizados demonstraram que os endpoints funcionam corretamente, possibilitando a manipulação de dados conforme esperado. O uso de JSON garantiu compatibilidade e facilidade de integração com outras aplicações.

MELHORIAS FUTURAS: 

Para aprimorar o projeto, algumas melhorias futuras podem ser implementadas:

Integração com Banco de Dados: Substituir armazenamento temporário por um banco de dados relacional ou NoSQL.

Autenticação e Autorização: Implementar um sistema de login para restringir acesso a usuários autenticados.

Melhoria nos Testes: Criar testes automatizados para garantir estabilidade do sistema.

Documentação Completa: Utilizar Swagger ou outra ferramenta para documentar a API de forma mais clara.

Essas melhorias garantirão maior segurança, escalabilidade e usabilidade para a API.
