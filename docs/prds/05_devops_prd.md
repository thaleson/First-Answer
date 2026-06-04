# PRD — DevOps, Qualidade e Ambiente de Desenvolvimento

## Objetivo

Garantir que o projeto possua ambiente reproduzível, padronização de código, automação de qualidade e facilidade de execução por qualquer avaliador.

O projeto deve ser executável localmente e via Docker sem configurações complexas.

---

# Ambiente

## Linguagem

```text
Python 3.11+
```

---

# Gerenciamento de Dependências

Utilizar:

```text
pip
requirements.txt
```

O arquivo requirements.txt deve conter apenas dependências realmente utilizadas.

Evitar bibliotecas desnecessárias.

---

# Variáveis de Ambiente

Utilizar:

```text
.env
.env.example
```

Nunca commitar:

```text
.env
```

---

## Variáveis Obrigatórias

```env
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
LOG_LEVEL=INFO
```

---

# Docker

## Objetivo

Permitir execução completa da aplicação sem necessidade de instalação manual de dependências.

---

## Dockerfile

Responsabilidades:

* utilizar imagem oficial Python
* instalar dependências
* copiar código
* definir diretório de trabalho
* executar aplicação

Imagem recomendada:

```text
python:3.11-slim
```

---

## Requisitos

A imagem deve:

* ser pequena
* ser reproduzível
* possuir build rápido

---

# Docker Compose

Criar:

```text
docker-compose.yml
```

Responsável por:

* serviço principal da aplicação
* serviço Streamlit

---

## Serviços

### app

Responsável por:

```text
CLI
Use Cases
Execução principal
```

---

### streamlit

Responsável por:

```text
Interface visual
```

Porta:

```text
8501
```

---

# Logs

Criar logger centralizado.

Arquivo:

```text
app/shared/logger.py
```

---

## Objetivos

Registrar:

* inicialização da aplicação
* execução do use case
* chamadas da Groq
* erros

---

## Proibições

Nunca registrar:

```text
API Keys
Tokens
Secrets
```

---

# Qualidade de Código

## Formatter

Utilizar:

```text
black
```

---

## Import Sorter

Utilizar:

```text
isort
```

---

## Linter

Utilizar:

```text
ruff
```

---

# Pre-Commit

Criar:

```text
.pre-commit-config.yaml
```

Objetivo:

Executar verificações antes de cada commit.

---

## Hooks Obrigatórios

### Black

Formatar código automaticamente.

---

### Isort

Organizar imports.

---

### Ruff

Validar qualidade.

---

### End Of File Fixer

Corrigir quebra de linha final.

---

### Trailing Whitespace

Remover espaços desnecessários.

---

# Git Ignore

Ignorar:

```text
__pycache__/
.pytest_cache/
.ruff_cache/
.venv/
.env
.coverage
htmlcov/
.streamlit/secrets.toml
```

---

# Estrutura de Branches

Padrão:

```text
main
```

Para futuras evoluções:

```text
feature/*
fix/*
hotfix/*
```

---

# Convenções de Commit

Seguir padrão Conventional Commits.

Exemplos:

```text
feat: add groq extractor
feat: add streamlit interface
fix: handle invalid llm response
test: add use case tests
docs: update architecture prd
chore: configure pre-commit
```

---

# Segurança

## API Keys

Nunca hardcodar credenciais.

Sempre utilizar:

```python
os.getenv()
```

ou

```python
BaseSettings
```

---

# Health Check

Criar mecanismo simples para validar:

* ambiente carregado
* configuração válida
* chave presente

Objetivo:

Facilitar diagnóstico.

---

# README

Deve conter:

## Instalação

### Local

```bash
pip install -r requirements.txt
```

---

### Docker

```bash
docker compose up --build
```

---

### Streamlit

```bash
streamlit run app/presentation/streamlit_app.py
```

---

# Critérios de Aceite

* Docker funcional.
* Docker Compose funcional.
* Pre-commit configurado.
* Black configurado.
* Ruff configurado.
* Isort configurado.
* Variáveis de ambiente isoladas.
* Logs implementados.
* README completo.
* Projeto executável em ambiente limpo.
