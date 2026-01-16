# StockFlow API

API desenvolvida para processamento automatizado de relatórios de estoque em PDF, realizando extração, tratamento e persistência dos dados via endpoints REST.

---

## ⚙️ Setup

### Pré-requisitos
- Docker
- Docker Compose

### Clonar o repositório
```bash
git clone <repo-url>
cd stockflow
```

## Subir os containers

```bash
docker-compose up --build
```

## Execução da Automação

A automação é responsável por:

- Ler arquivos PDF de relatórios de estoque
- Extrair e validar os dados
- Enviar os registros para a API em lote

### Execução da API
`POST /automation/run`

## Testes via Swagger
http://localhost:8000/docs