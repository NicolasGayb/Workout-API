# 🏋️‍♀️ Workout API

API construída com **FastAPI** para gerenciar atletas, categorias e centros de treinamento de forma simples, rápida e totalmente assíncrona. O projeto serve como base para estudos de FastAPI, SQLAlchemy 2.0 (ORM assíncrono), validação de dados com Pydantic v2 e versionamento de banco via Alembic.

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.119.0-009485?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-CE262C?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white" alt="PostgreSQL" />
</p>

---

## 📚 Sumário
- [Visão geral](#-visão-geral)
- [Arquitetura e tecnologias](#-arquitetura-e-tecnologias)
- [Preparando o ambiente](#-preparando-o-ambiente)
- [Executando a API](#-executando-a-api)
- [Migrações de banco](#-migrações-de-banco)
- [Coleção de endpoints](#-coleção-de-endpoints)
  - [Atletas](#atletas)
  - [Categorias](#categorias)
  - [Centros de treinamento](#centros-de-treinamento)
- [Modelagem dos dados](#-modelagem-dos-dados)
- [Documentação interativa](#-documentação-interativa)
- [Próximos passos](#-próximos-passos)

---

## 🌟 Visão geral
A Workout API expõe recursos REST para cadastros relacionados a rotinas de treino:

- **Atletas** com dados pessoais, categoria esportiva e centro de treinamento associado.
- **Categorias** que agrupam atletas por modalidade, intensidade ou objetivo.
- **Centros de treinamento** responsáveis pelos treinamentos dos atletas.

Toda a comunicação é feita em JSON e segue boas práticas HTTP (códigos de status semânticos, validação de entrada e saídas tipadas).

## 🧱 Arquitetura e tecnologias
| Camada | Tecnologias | Descrição |
| --- | --- | --- |
| API | [FastAPI](https://fastapi.tiangolo.com/) | Framework assíncrono, documentação automática com OpenAPI e validações com Pydantic.
| Banco de dados | PostgreSQL + [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) | ORM no modo assíncrono, models herdando de `BaseModel` com chaves UUID e PKs inteiras.
| Configuração | Pydantic Settings | Gerencia variáveis de ambiente e URL do banco (`settings.DB_URL`).
| Migrações | Alembic | Criação e versionamento de esquema do banco.
| Infra opcional | Docker Compose | Serviço PostgreSQL pronto para desenvolvimento local.

A organização do código fica em `workout_api/`:

```
workout_api/
├── main.py                # Criação da aplicação FastAPI
├── routers.py             # Registro das rotas principais
├── atleta/                # Domínio de atletas (models, schemas e controller)
├── categorias/            # Domínio de categorias
├── centro_treinamento/    # Domínio de centros de treinamento
└── contrib/               # Helpers compartilhados (DB, schemas base, repositórios)
```

## 🛠️ Preparando o ambiente
1. **Clone o projeto**
   ```bash
   git clone https://github.com/seu-usuario/Workout-API.git
   cd Workout-API
   ```
2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows
   ```
3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure o banco de dados**
   - Ajuste a variável `DB_URL` caso necessário (arquivo `workout_api/configs/settings.py` ou variável de ambiente).
   - Opcional: suba um PostgreSQL local com Docker Compose:
     ```bash
     docker-compose up -d db
     ```

## 🚀 Executando a API
Você pode iniciar o servidor diretamente com o Uvicorn ou usar os atalhos do `Makefile`.

```bash
make run
# ou
uvicorn workout_api.main:app --reload
```

A aplicação ficará disponível em `http://127.0.0.1:8000`.

## 🗃️ Migrações de banco
O projeto utiliza Alembic para controlar o schema.

```bash
make create-migrations d="nome_da_migracao"  # gera uma nova revisão
make run-migrations                          # aplica as migrações pendentes
```

Certifique-se de que o banco está acessível antes de rodar as migrações.

## 🔌 Coleção de endpoints
As rotas estão agrupadas por domínio e expostas no arquivo [`workout_api/routers.py`](workout_api/routers.py). Todas respondem e recebem JSON e utilizam UUID v4 como identificador público.

### Atletas
`/atletas`

| Método | Rota | Descrição | Observações |
| --- | --- | --- | --- |
| `POST` | `/` | Cria um novo atleta. | Requer objeto com dados pessoais, categoria e centro de treinamento já existentes.
| `GET` | `/` | Lista atletas cadastrados. | Suporta filtros `nome`, `cpf` e paginação `limit`/`offset`.
| `GET` | `/{id}` | Detalha um atleta pelo UUID. | Retorna dados completos, incluindo categoria e centro.
| `PATCH` | `/{id}` | Atualiza parcialmente os dados. | Permite alterar campos informados no corpo.
| `DELETE` | `/{id}` | Remove um atleta do sistema. | Retorna `204 No Content` em caso de sucesso.

**Exemplo de criação**
```json
POST /atletas
{
  "nome": "João Silva",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 70.5,
  "altura": 1.75,
  "genero": "M",
  "categoria": { "nome": "Força" },
  "centro_treinamento": { "nome": "Academia XYZ" }
}
```

### Categorias
`/categorias`

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/` | Cria uma categoria.
| `GET` | `/` | Lista todas as categorias.
| `GET` | `/{categoria_id}` | Busca detalhes por UUID.
| `PATCH` | `/{categoria_id}` | Atualiza o nome da categoria.
| `DELETE` | `/{categoria_id}` | Remove a categoria.

### Centros de treinamento
`/centros_treinamento`

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/` | Cadastra um novo centro de treinamento.
| `GET` | `/` | Lista centros cadastrados.
| `GET` | `/{ct_id}` | Busca detalhes por UUID.
| `PATCH` | `/{ct_id}` | Atualiza dados do centro.
| `DELETE` | `/{ct_id}` | Remove o registro.

## 🗂️ Modelagem dos dados
- **UUID público**: todos os recursos expõem um campo `id` (UUID v4) herdado de `BaseModel` (`workout_api/contrib/models.py`).
- **Chaves internas**: cada tabela possui um `pk_id` inteiro para relacionamentos e otimização.
- **Relacionamentos**:
  - `AtletaModel` referencia `CategoriaModel` e `CentroTreinamentoModel` via chaves estrangeiras (`categoria_id`, `centro_treinamento_id`).
  - As relações são carregadas com `selectinload`, garantindo eficiência nas consultas assíncronas.
- **Campos de auditoria**: o atleta registra `created_at` automaticamente ao ser inserido.

## 📖 Documentação interativa
Acesse os endpoints de documentação gerados automaticamente pelo FastAPI:

- Swagger UI: [`/docs`](http://127.0.0.1:8000/docs)
- ReDoc: [`/redoc`](http://127.0.0.1:8000/redoc)

## 🚀 Próximos passos
Sugestões para evoluir o projeto:

- Cobertura de testes automatizados.
- Autenticação e autorização para proteger os recursos.
- Versionamento da API e registros de auditoria mais completos.
- Cache e monitoramento de performance para cargas maiores.

---

Feito com 💪 e FastAPI!
