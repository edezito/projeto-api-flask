# API School System – Entrega 3: Projeto Flask com BD

Grupo 1: Éder Duarte, Felipe Lima Nogueira, Victor Henrique Souza Oliveira

Data da atividade: 04/05/2025

## Melhorias Implementadas na Entrega 3

A entrega 3 do projeto API School System focou em aprimorar a API Flask, abordando vários desafios e melhorias propostas na entrega 2.

# 📚 Sistema de Gestão Escolar - API REST

Este é um sistema de gestão escolar desenvolvido com *Python* e *Flask, estruturado em múltiplas camadas (controller, service, model e routes) e documentado com **Swagger. A aplicação permite o gerenciamento de alunos, professores, turmas e usuários administrativos com autenticação via **JWT*.

---

## ✅ Melhorias desde a Entrega 2 (detalhadas)

### 🔄 Refatoração completa da estrutura do projeto

A estrutura do projeto foi reorganizada seguindo o padrão MVC (Model-View-Controller), porém com a adição de camadas modernas como service e routes, proporcionando:

- Melhor *separação de responsabilidades*
- Maior *legibilidade e manutenibilidade*
- Facilidade na *testabilidade* e *escalabilidade* do código

A nova estrutura agrupa funcionalidades relacionadas por domínio (aluno, professor, etc.), deixando o código mais modular e limpo.

---

### 🔐 Implementação de autenticação JWT

Foi implementado um sistema de autenticação baseado em *JSON Web Tokens (JWT)*:

- Usuários autenticados recebem um token JWT ao fazer login
- Rotas protegidas só podem ser acessadas com um token válido
- Um middleware (login_requerido.py) foi criado para validar o token e restringir o acesso

Isso garante maior segurança e controle de acesso à API.

---

### 📁 Criação da camada de serviços (service/)

Foi introduzida uma nova camada chamada *service*, responsável por:

- Encapsular a lógica de negócio
- Reduzir o acoplamento entre controllers e modelos
- Reutilizar funcionalidades comuns (ex: autenticação)

Exemplo: aluno_service.py centraliza operações relacionadas a alunos, como validações, consultas e regras de negócio.

---

### 🌐 Separação das rotas por entidade (routes/)

As rotas foram organizadas por domínio (aluno, professor, turma, etc.), permitindo:

- Maior clareza e organização
- Manutenção facilitada, já que cada arquivo lida com apenas um contexto
- Possibilidade de expandir o sistema sem gerar conflito entre endpoints

---

### 📘 Documentação modular com Swagger

A documentação da API foi completamente reformulada usando *Swagger* com namespaces:

- Cada domínio possui um arquivo de namespace (alunos_namespace.py, turmas_namespace.py etc.)
- Os endpoints são automaticamente documentados
- A interface gerada facilita testes manuais e integração com frontend

Isso melhora a *usabilidade* e a *transparência* da API para outros desenvolvedores.

---

### 🐳 Containerização com Docker e Docker Compose

Foi adicionada containerização para facilitar a execução e distribuição:

- Dockerfile: empacota o app em uma imagem leve
- docker-compose.yml: define o ambiente com o banco de dados e app juntos

Com isso, o sistema pode ser executado com um simples comando:

```bash
docker-compose up --build
