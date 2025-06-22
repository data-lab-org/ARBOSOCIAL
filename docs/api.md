# API Documentation - ARBOSOCIAL

## Visão Geral

A API do ARBOSOCIAL fornece endpoints RESTful para acesso aos dados epidemiológicos, indicadores sociais, predições de machine learning e sistema de alertas.

**Base URL**: `https://arbosocial.data-lab.org/api`

## Autenticação

A API utiliza autenticação JWT (JSON Web Tokens). Inclua o token no header Authorization:

```
Authorization: Bearer <seu_token_jwt>
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "name": "Nome do Usuário",
    "role": "user"
  }
}
```

## Endpoints Principais

### 1. Municípios

#### Listar Municípios
```http
GET /data/municipalities
```

**Parâmetros de Query:**
- `state` (string): Filtrar por estado (ex: SP, RJ)
- `region` (string): Filtrar por região (Norte, Nordeste, etc.)
- `search` (string): Buscar por nome

**Resposta:**
```json
[
  {
    "id": 1,
    "ibge_code": "3550308",
    "name": "São Paulo",
    "state": "SP",
    "region": "Sudeste",
    "population": 12325232,
    "area_km2": 1521.11
  }
]
```

#### Obter Município Específico
```http
GET /data/municipalities/{id}
```

### 2. Casos de Arboviroses

#### Listar Casos
```http
GET /data/cases
```

**Parâmetros de Query:**
- `municipality_id` (int): ID do município
- `disease` (string): dengue, zika, chikungunya
- `year` (int): Ano
- `start_week` (int): Semana epidemiológica inicial
- `end_week` (int): Semana epidemiológica final

**Resposta:**
```json
[
  {
    "id": 1,
    "municipality_id": 1,
    "disease": "dengue",
    "epidemiological_week": 10,
    "year": 2024,
    "confirmed_cases": 150,
    "probable_cases": 200,
    "deaths": 2,
    "incidence_rate": 12.5,
    "notification_date": "2024-03-10"
  }
]
```

#### Resumo de Casos
```http
GET /data/cases/summary
```

**Parâmetros de Query:**
- `disease` (string): Doença específica
- `year` (int): Ano
- `state` (string): Estado
- `region` (string): Região

### 3. Indicadores Sociais

#### Listar Indicadores
```http
GET /data/social-indicators
```

**Parâmetros de Query:**
- `municipality_id` (int): ID do município
- `year` (int): Ano

**Resposta:**
```json
[
  {
    "id": 1,
    "municipality_id": 1,
    "year": 2023,
    "population_density": 7398.26,
    "urban_population_pct": 99.1,
    "gdp_per_capita": 65629.0,
    "gini_index": 0.62,
    "poverty_rate": 8.5,
    "water_supply_pct": 99.8,
    "sewage_treatment_pct": 87.3
  }
]
```

#### Análise de Correlações
```http
GET /data/correlations
```

**Parâmetros de Query:**
- `disease` (string): Doença para análise
- `year` (int): Ano
- `indicators` (array): Lista de indicadores

### 4. Predições

#### Listar Predições
```http
GET /predictions
```

**Parâmetros de Query:**
- `municipality_id` (int): ID do município
- `disease` (string): Doença
- `model_name` (string): arima, lstm, prophet, ensemble
- `weeks_ahead` (int): Semanas à frente

**Resposta:**
```json
[
  {
    "id": 1,
    "municipality_id": 1,
    "disease": "dengue",
    "model_name": "ensemble",
    "prediction_date": "2024-03-15",
    "target_week": 15,
    "target_year": 2024,
    "predicted_cases": 180.5,
    "confidence_interval_lower": 150.2,
    "confidence_interval_upper": 210.8,
    "model_accuracy": 0.87
  }
]
```

#### Gerar Predições
```http
POST /predictions/generate
Content-Type: application/json

{
  "municipality_ids": [1, 2, 3],
  "disease": "dengue",
  "weeks_ahead": 4,
  "models": ["arima", "lstm", "prophet"]
}
```

#### Performance dos Modelos
```http
GET /predictions/performance
```

### 5. Alertas

#### Listar Alertas
```http
GET /alerts
```

**Parâmetros de Query:**
- `municipality_id` (int): ID do município
- `disease` (string): Doença
- `alert_level` (string): low, medium, high, critical
- `is_active` (boolean): Alertas ativos

**Resposta:**
```json
[
  {
    "id": 1,
    "municipality_id": 1,
    "disease": "dengue",
    "alert_level": "high",
    "alert_type": "outbreak_prediction",
    "message": "Predição de surto de dengue nas próximas 3 semanas",
    "predicted_cases": 250.0,
    "confidence_score": 0.89,
    "is_active": true,
    "created_at": "2024-03-15T10:30:00Z"
  }
]
```

#### Criar Alerta
```http
POST /alerts
Content-Type: application/json

{
  "municipality_id": 1,
  "disease": "dengue",
  "alert_level": "high",
  "alert_type": "threshold_exceeded",
  "message": "Número de casos excedeu o limiar esperado",
  "predicted_cases": 200.0,
  "confidence_score": 0.92
}
```

#### Resolver Alerta
```http
PATCH /alerts/{id}/resolve
```

### 6. Relatórios

#### Gerar Relatório
```http
POST /reports/generate
Content-Type: application/json

{
  "type": "cases",
  "format": "pdf",
  "filters": {
    "disease": "dengue",
    "year": 2024,
    "state": "SP"
  }
}
```

**Tipos de Relatório:**
- `cases`: Relatório de casos
- `predictions`: Relatório de predições
- `alerts`: Relatório de alertas
- `correlations`: Relatório de correlações

**Formatos:**
- `pdf`: Arquivo PDF
- `excel`: Planilha Excel
- `csv`: Arquivo CSV

### 7. Dados Geoespaciais

#### Obter Dados Geográficos
```http
GET /data/geo
```

**Parâmetros de Query:**
- `type` (string): municipalities, states, regions
- `level` (string): Nível de detalhe

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos na requisição
- `401 Unauthorized`: Token de autenticação inválido ou ausente
- `403 Forbidden`: Acesso negado
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Dados válidos mas não processáveis
- `500 Internal Server Error`: Erro interno do servidor

## Limitações de Taxa

- **Usuários autenticados**: 1000 requisições por hora
- **Usuários não autenticados**: 100 requisições por hora

## Exemplos de Uso

### Python
```python
import requests

# Login
response = requests.post('https://arbosocial.data-lab.org/api/auth/login', 
                        json={'email': 'user@example.com', 'password': 'password'})
token = response.json()['access_token']

# Obter casos de dengue em São Paulo
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://arbosocial.data-lab.org/api/data/cases',
                       params={'municipality_id': 1, 'disease': 'dengue'},
                       headers=headers)
cases = response.json()
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('https://arbosocial.data-lab.org/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'user@example.com', password: 'password'})
});
const {access_token} = await loginResponse.json();

// Obter predições
const predictionsResponse = await fetch('https://arbosocial.data-lab.org/api/predictions', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
const predictions = await predictionsResponse.json();
```

## Suporte

Para dúvidas sobre a API, entre em contato:
- **Email**: api-support@data-lab.org
- **Documentação**: https://docs.arbosocial.data-lab.org
- **GitHub**: https://github.com/castrokelly/ARBOSOCIAL

