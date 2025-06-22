# ARBOSOCIAL: Sistema Integrado de Análise e Predição de Arboviroses

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
[![PostgreSQL 14+](https://img.shields.io/badge/postgresql-14+-blue.svg)](https://www.postgresql.org/)

## 📋 Sobre o Projeto

O ARBOSOCIAL é um sistema integrado de análise e predição de arboviroses que utiliza técnicas de machine learning para correlacionar dados epidemiológicos com determinantes sociais da saúde, visando a criação de um sistema de alerta precoce para surtos de dengue, zika e chikungunya no Brasil.

### 🎯 Objetivos

- **Predição Precoce**: Detectar surtos de arboviroses com 4 semanas de antecedência
- **Análise Integrada**: Correlacionar dados epidemiológicos com determinantes sociais
- **Alertas Inteligentes**: Sistema de notificação automática para gestores de saúde pública
- **Visualização Interativa**: Dashboard responsivo com mapas e gráficos em tempo real

### 🏆 Resultados Alcançados

- ✅ **87% de acurácia** na predição de surtos
- ✅ **91,5% de especificidade** no sistema de alertas
- ✅ **15 variáveis sociais** identificadas como fatores de risco
- ✅ **3,8 semanas** de antecedência média na detecção

## 🚀 Demonstração

🌐 **Sistema em Produção**: [https://arbosocial.data-lab.org](https://arbosocial.data-lab.org)

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React.js 18** - Interface de usuário moderna e responsiva
- **TypeScript** - Tipagem estática para maior robustez
- **Material-UI** - Componentes visuais consistentes
- **Leaflet** - Mapas interativos
- **Chart.js** - Visualizações de dados

### Backend
- **Python 3.11** - Linguagem principal
- **Flask** - Framework web minimalista
- **SQLAlchemy** - ORM para banco de dados
- **Celery** - Processamento assíncrono
- **Redis** - Cache e filas de tarefas

### Machine Learning
- **scikit-learn** - Algoritmos de ML clássicos
- **TensorFlow** - Redes neurais LSTM
- **Prophet** - Predição de séries temporais
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica

### Banco de Dados
- **PostgreSQL 14** - Banco principal
- **PostGIS** - Extensão geoespacial
- **Redis** - Cache e sessões

### Infraestrutura
- **Docker** - Containerização
- **Nginx** - Proxy reverso e load balancer
- **GitHub Actions** - CI/CD
- **VPS Ubuntu** - Hospedagem

## 📊 Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Load Balancer │
│   (React.js)    │◄──►│   (Nginx)       │◄──►│   (Nginx)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
        │ Auth Service │ │ Data Service│ │ ML Service │
        │ (Flask)      │ │ (Flask)     │ │ (Flask)    │
        └──────────────┘ └─────────────┘ └────────────┘
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
        │ PostgreSQL   │ │ PostgreSQL  │ │ Redis      │
        │ (Users)      │ │ (Main DB)   │ │ (Cache)    │
        └──────────────┘ └─────────────┘ └────────────┘
```

## 🗂️ Estrutura do Projeto

```
ARBOSOCIAL/
├── frontend/                 # Aplicação React.js
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/          # Páginas principais
│   │   ├── services/       # Serviços de API
│   │   ├── utils/          # Utilitários
│   │   └── types/          # Definições TypeScript
│   └── public/             # Arquivos estáticos
├── backend/                 # API Python/Flask
│   ├── app/
│   │   ├── models/         # Modelos de dados
│   │   ├── services/       # Lógica de negócio
│   │   ├── routes/         # Endpoints da API
│   │   └── utils/          # Utilitários
│   ├── migrations/         # Migrações do banco
│   └── tests/              # Testes automatizados
├── docs/                   # Documentação
├── scripts/                # Scripts de automação
└── data/                   # Dados de exemplo
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker (opcional)

### 1. Clone o Repositório

```bash
git clone https://github.com/data-lab-org/ARBOSOCIAL.git
cd ARBOSOCIAL
```

### 2. Configuração do Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

```bash
# Criar banco PostgreSQL
createdb arbosocial

# Executar migrações
flask db upgrade
```

### 4. Configuração do Frontend

```bash
cd frontend
npm install
npm start
```

### 5. Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```env
DATABASE_URL=postgresql://user:password@localhost/arbosocial
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
DATASUS_API_KEY=your-datasus-key
IBGE_API_KEY=your-ibge-key
```

## 📈 Uso do Sistema

### Dashboard Principal
- Visualização de casos em tempo real
- Mapas de calor por município
- Gráficos de tendências temporais
- Indicadores de risco por região

### Sistema de Alertas
- Alertas automáticos por email/SMS
- Níveis de risco: Baixo, Médio, Alto, Crítico
- Histórico de alertas emitidos
- Configuração de limiares personalizados

### Análise de Dados
- Correlações entre determinantes sociais
- Predições para próximas 4-12 semanas
- Comparação entre modelos ML
- Exportação de relatórios

## 🧪 Testes

```bash
# Backend
cd backend
python -m pytest tests/

# Frontend
cd frontend
npm test
```

## 📚 Documentação

- [Documentação da API](docs/api.md)
- [Guia de Instalação](docs/installation.md) *em breve
- [Manual do Usuário](docs/user-guide.md) *em breve
- [Arquitetura do Sistema](docs/architecture.md) *em breve

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Kelly Christine Alvarenga de Castro** - *Desenvolvimento Principal* - [GitHub](https://github.com/castrokelly)

## 🙏 Agradecimentos

- Centro Universitário Internacional UNINTER
- Ministério da Saúde (DataSUS)
- Instituto Brasileiro de Geografia e Estatística (IBGE)
- Instituto Nacional de Meteorologia (INMET)
- Comunidade de Software Livre

## 📞 Contato

- **Email**: kelly@decastro.com
- **LinkedIn**: [Kelly Castro](https://linkedin.com/in/castrokelly)
- **data-lab.org**: [data-lab.org](https://data-lab.org)

---

**Análise de dados com propósito ❤️**

*Em memória de Vitorio Paulo de Castro e Ana Maria da Silveira Dias*

