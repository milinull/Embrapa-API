# 🍇 Embrapa Wine Data Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/Django-REST%20Framework-success)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)
![Apache Spark](https://img.shields.io/badge/BigData-Apache%20Spark-orange)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![Docker](https://img.shields.io/badge/Container-Docker-blue)
![AWS S3](https://img.shields.io/badge/Storage-AWS_S3-FF9900)
![Django CI](https://github.com/milinull/Embrapa-API/workflows/Django%20CI%2FCD/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)

**Plataforma completa de análise de dados da indústria vinícola brasileira**

[Visão Geral](#-visão-geral) • [Arquitetura](#️-arquitetura) • [Instalação](#-instalação-rápida) • [Testes](#-testes-e-qualidade) • [CI/CD](#-cicd-e-automação) • [Documentação](#-documentação-da-api) • [Tecnologias](#-stack-tecnológico)

</div>

---

## 📋 Visão Geral

Pipeline end-to-end de engenharia de dados que coleta, processa e visualiza informações sobre a **produção, comercialização, exportação e importação de vinhos no Brasil**, utilizando dados públicos da **Embrapa Uva & Vinho**.

### ✨ Principais Funcionalidades

- 🔄 **ETL automatizado** com Apache Spark e armazenamento em camadas (Bronze/Silver)
- 📊 **Dashboard interativo** com visualizações dinâmicas e filtros avançados
- 🚀 **API RESTful** escalável com Django e MongoDB
- 🐳 **Infraestrutura containerizada** com Docker Compose
- ☁️ **Integração com AWS S3** para data lake
- 📈 **Análises comparativas** de produção vs exportação
- ✅ **96% de cobertura** de testes automatizados
- 🔄 **CI/CD automatizado** com GitHub Actions

---

## 🏗️ Arquitetura

```mermaid
graph TD
    subgraph Cloud["☁️ AWS S3 Data Lake"]
        A1[📦 Bronze Layer<br/>Raw Data]
        A2[✨ Silver Layer<br/>Cleaned Data]
    end

    subgraph Spark["⚙️ Apache Spark ETL"]
        B1[🕷️ Web Scraping<br/>Embrapa Source]
        B2[🔧 Data Transformation<br/>Cleaning & Typing]
        B3[💾 MongoDB Loader<br/>Batch Insert]
    end

    subgraph Backend["🔌 Django REST API"]
        C1[🎯 REST Endpoints<br/>MongoEngine ORM]
        C2[🔐 Authentication]
    end

    subgraph Frontend["💻 React Dashboard"]
        D1[📊 Recharts Visualizations]
        D2[🎨 Interactive Filters]
    end

    subgraph Database["🗄️ MongoDB Cluster"]
        E1[📚 Collections<br/>Wine Data]
        E2[🖥️ Mongo Express<br/>Admin UI]
    end

    B1 -->|Extract| A1
    A1 -->|Transform| B2
    B2 -->|Load| A2
    A2 -->|Read| B3
    B3 -->|Insert| E1
    E1 <-->|Query| C1
    C1 <-->|REST API| D1
    E2 -.->|Monitor| E1
```

---

## 🐳 Serviços Docker

| Serviço | Descrição | Portas | URL de Acesso |
|---------|-----------|--------|---------------|
| **web** | Django REST API | `8000` | http://localhost:8000/api |
| **mongo** | MongoDB Database | `27017` | - |
| **mongo-express** | MongoDB Admin UI | `8081` | http://localhost:8081 |
| **spark-master** | Spark + Jupyter Notebook | `8889`, `8083`, `8040`, `7077` | http://localhost:8889 |
| **wine-frontend** | React Dashboard | `3000` | http://localhost:3000 |

---

## 🚀 Instalação Rápida

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Conta AWS (para S3)

### 1. Clone o repositório

```bash
git clone https://github.com/milinull/Embrapa-API.git
cd Embrapa-API
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Django Settings
DEBUG=True

# MongoDB Configuration
MDB_HOST=mongo
MDB_PORT=27017
MDB_USER=admin
MDB_PASS=admin123
MDB_NAME=embrapa_wine

# AWS S3 Configuration
AWS_ACCESS_KEY=your-access-key
AWS_SECRET_KEY=your-secret-key
AWS_DESTINY=your-bucket-name
AWS_LOCAL=us-east-1
```

### 3. Execute a aplicação

```bash
docker compose up --build
```

Aguarde alguns minutos enquanto os containers são construídos e inicializados.

### 4. Acesse as aplicações

| Aplicação | URL | Credenciais |
|-----------|-----|-------------|
| **Dashboard** | http://localhost:3000 | - |
| **API Django**| http://localhost:8000/api | - |
| **Mongo Express** | http://localhost:8081 | admin / admin123 |
| **Jupyter Notebook** | http://localhost:8889 | Token exibido no log |
| **Swagger UI** | http://localhost:8000/swagger | JWT |
| **ReDoc** | http://localhost:8000/redoc | - |

---

## 🧪 Testes e Qualidade

O projeto possui **32 testes unitários automatizados** cobrindo **96% do código** da API.

### 📊 Cobertura de Testes

| Módulo | Cobertura | Status |
|--------|-----------|--------|
| **Views** | 98% | ✅ |
| **Serializers** | 100% | ✅ |
| **URLs** | 100% | ✅ |
| **Models** | 89% | ✅ |
| **Total** | **96%** | ✅ |

### Executar Testes

#### Rodar todos os testes

```bash
# Via Docker
docker compose exec web python manage.py test embrapa

# Localmente
python manage.py test embrapa
```

#### Executar com relatório de cobertura

```bash
# Via Docker
docker compose exec web coverage run --source='.' manage.py test embrapa
docker compose exec web coverage report

# Localmente
coverage run --source='.' manage.py test embrapa
coverage report
```

#### Visualizar cobertura detalhada (HTML)

```bash
coverage html
# Abra htmlcov/index.html no navegador
```

### 🎯 O que é testado?

✅ **Listagem de endpoints** - Verifica se todos os endpoints retornam dados corretamente  
✅ **Filtros e query params** - Testa filtros por ano, categoria, produto, país, tipo e cultivar  
✅ **Actions customizadas** - `total_por_ano`, `top_paises`  
✅ **Comparativo produção x exportação** - Validação de cálculos e percentuais  
✅ **Ordenação de resultados** - Verifica ordenação por ano decrescente  
✅ **Paginação** - Navegação entre páginas de resultados  
✅ **Tratamento de erros** - Casos de dados inválidos ou inexistentes  

### Exemplo de Saída

```bash
Found 32 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
................................
----------------------------------------------------------------------
Ran 32 tests in 0.337s
OK
Destroying test database for alias 'default'...

Name                     Stmts   Miss  Cover
--------------------------------------------
embrapa/views.py           111      2    98%
embrapa/serializers.py      22      0   100%
embrapa/models.py           44      5    89%
embrapa/urls.py             10      0   100%
--------------------------------------------
TOTAL                      501     21    96%
```

---

## 🔄 CI/CD e Automação

O projeto utiliza **GitHub Actions** para integração e entrega contínuas, garantindo qualidade do código a cada push.

### 🚀 Pipeline Automatizado

```mermaid
graph LR
    A[💻 Git Push] --> B[🔍 GitHub Actions]
    B --> C[🧪 Testes Unitários]
    B --> D[📝 Code Linting]
    C --> E{✅ Passou?}
    D --> E
    E -->|Sim| F[✨ Deploy Ready]
    E -->|Não| G[❌ Bloqueado]
```

### Workflow de CI/CD

A cada **push** ou **pull request** nas branches `main` ou `develop`, o GitHub Actions executa automaticamente:

#### 1️⃣ **Job: Test**
- ✅ Configura ambiente Python 3.12
- ✅ Sobe container MongoDB para testes
- ✅ Instala dependências
- ✅ Executa 32 testes unitários
- ✅ Gera relatório de cobertura (96%)
- ✅ Valida que nenhum teste falhou

#### 2️⃣ **Job: Lint**
- ✅ Executa **Flake8** para verificar erros de sintaxe
- ✅ Executa **Black** para validar formatação do código
- ✅ Garante padrão de código consistente

<p>


Você pode ver o status de todos os workflows em: [Actions](https://github.com/milinull/Embrapa-API/actions)

### Arquivo de Configuração

O pipeline está definido em `.github/workflows/django-tests.yml`:

```yaml
name: Django CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:latest
        ports:
          - 27017:27017
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Run tests with coverage
        run: |
          coverage run --source='.' manage.py test embrapa
          coverage report

  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Run flake8
        run: flake8 .
      - name: Check formatting with black
        run: black --check .
```
---

## 🔐 Autenticação JWT

A API utiliza **JSON Web Tokens (JWT)** para autenticação segura.

### Obtendo Token de Acesso

```bash
# Requisição
POST http://localhost:8000/api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}

# Resposta
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usando o Token

```bash
# Adicione o token no header Authorization
GET http://localhost:8000/api/Producao/?ano=2024
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Renovando o Token

```bash
POST http://localhost:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Testando no Swagger

1. Acesse http://localhost:8000/swagger/
2. Clique no botão **"Authorize"** 🔓
3. Digite: `Bearer seu_token_aqui`
4. Clique em **"Authorize"** e depois **"Close"**
5. Agora você pode testar os endpoints autenticados!

---

## 📊 Dashboard Interativo

O dashboard React oferece análises visuais completas com:

### Funcionalidades

- **📈 Múltiplas visualizações**: Gráficos de barras, pizza e linhas temporais
- **🔍 Filtros dinâmicos**: Por ano, categoria e país
- **📑 Sistema de abas**: Comercialização, Produção, Exportação, Importação e Processamento
- **💹 Comparativos**: Análise de produção vs exportação
- **📱 Responsivo**: Interface adaptável para mobile e desktop

Acesse em: http://localhost:3000

---

## 🔄 Pipeline ETL

### Fluxo de Dados

```
1. EXTRAÇÃO → Web scraping da Embrapa (BeautifulSoup)
                ↓
2. BRONZE LAYER → Dados brutos salvos no S3
                ↓
3. TRANSFORMAÇÃO → Limpeza e tipagem com Spark
                ↓
4. SILVER LAYER → Dados processados no S3
                ↓
5. CARGA → Inserção em batch no MongoDB
```

### Notebooks Spark

1. **`scrap_embrapa.ipynb`** - Extração de dados
   - Web scraping das páginas da Embrapa
   - Parsing de tabelas HTML
   - Upload para S3 (bronze layer)

2. **`spark_transform.ipynb`** - Transformação
   - Limpeza de caracteres especiais
   - Conversão de tipos de dados
   - Validação e normalização
   - Geração da silver layer

3. **`MongoDBLoaderFromS3.py`** - Carga
   - Leitura batch do S3
   - Inserção otimizada no MongoDB
   - Logging e tratamento de erros

---

## 📡 Documentação da API

### Endpoints Disponíveis

#### Comercialização
```http
GET /api/Comercio/?ano=2024
```
Retorna dados de comercialização de vinhos no mercado interno.

#### Produção
```http
GET /api/Producao/?ano=2024
```
Dados de produção de vinhos e derivados.

#### Exportação
```http
GET /api/Exportacao/?ano=2024&pais=Italia
```
Volume e valor de exportações por país de destino.

#### Importação
```http
GET /api/Importacao/?ano=2024&pais=Argentina
```
Volume e valor de importações por país de origem.

#### Processamento
```http
GET /api/Processamento/?ano=2024
```
Quantidade de uvas processadas por variedade.

#### Comparativo
```http
GET /api/comparativo/2024/
```
Análise comparativa entre produção e exportação.

### Exemplo de Resposta

```json
{
  "ano": 2024,
  "data": [
    {
      "produto": "Vinho de Mesa",
      "quantidade": 125000000,
      "valor": 450000000
    }
  ],
  "total_registros": 15
}
```

---

## 🛠️ Stack Tecnológico

### Backend
- **Django 5.2+** - Framework web
- **Django REST Framework** - API RESTful
- **MongoEngine** - ODM para MongoDB
- **python-decouple** - Gerenciamento de variáveis

### Big Data & ETL
- **Apache Spark 3.5** - Processamento distribuído
- **PySpark** - Interface Python para Spark
- **boto3** - SDK AWS para Python
- **BeautifulSoup4** - Web scraping

### Database
- **MongoDB 8.2** - Banco de dados NoSQL
- **PyMongo** - Driver Python para MongoDB

### Frontend
- **React** - Biblioteca UI
- **Recharts** - Biblioteca de gráficos
- **Lucide React** - Ícones

### Infraestrutura & DevOps
- **Docker & Docker Compose** - Containerização
- **AWS S3** - Object storage (Data Lake)
- **GitHub Actions** - CI/CD
- **Coverage.py** - Análise de cobertura de testes
- **Black** - Formatação de código
- **Flake8** - Linting

---

## 📁 Estrutura do Projeto

```
embrapa-wine-data/
├── 📂 .github/
│   └── workflows/
│       └── django-tests.yml       # Pipeline CI/CD
├── 📂 embrapa/                    # App Django principal
│   ├── models.py                  # Models MongoEngine
│   ├── views.py                   # ViewSets da API
│   ├── serializers.py             # Serializadores DRF
│   ├── tests.py                   # 32 testes unitários
│   └── urls.py                    # Rotas da API
├── 📂 mongo/                      # Configuração MongoDB
│   ├── connection.py              # Setup de conexão
│   └── MongoDBLoaderFromS3.py     # Carga
├── 📂 src/spark/spark-apps/       # Pipeline ETL
│   ├── scrap_embrapa.ipynb        # Extração
│   └── spark_transform.ipynb      # Transformação
├── 📂 wine-frontend/              # Aplicação React
│   ├── src/
│   │   ├── public/                # Componentes React
│   │   └── src/                   # Componente principal
├── 📂 setup/                      # Configurações Django
│   ├── settings.py
│   └── urls.py
├── 📄 docker-compose.yml          # Orquestração
├── 📄 Dockerfile                  # Build Django
├── 📄 requirements.txt            # Dependências Python
├── 📄 .env                        # Template de variáveis
└── 📄 README.md                   # Este arquivo
```

---

## 🧪 Desenvolvimento

### Executar Django localmente

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python manage.py runserver
```

### Executar Frontend localmente

```bash
cd wine-frontend
npm install
npm start
```

### Acessar Jupyter Notebooks

```bash
# O token está nos logs do container
docker compose logs spark-master | grep token

# Acesse http://localhost:8889 e insira o token
```

### Formatação de Código

```bash
# Formatar código automaticamente
black .

# Verificar formatação sem modificar
black --check .

# Executar linting
flake8 .
```

---

## 📈 Roadmap

- [x] ~~Implementar autenticação JWT na API~~
- [x] ~~Adicionar documentação Swagger/ReDoc~~
- [x] ~~Criar testes automatizados (96% cobertura)~~
- [x] ~~Pipeline CI/CD com GitHub Actions~~
- [x] ~~Implementar linting e formatação automática~~
- [ ] Adicionar cache com Redis
- [ ] Adicionar forecasting com ML
- [ ] Implementar notificações em tempo real
- [ ] Dashboard de monitoramento (Grafana)
- [ ] Deploy automatizado em produção

---