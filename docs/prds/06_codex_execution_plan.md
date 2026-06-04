# PRD — Plano de Execução para Codex

## Objetivo

Implementar o projeto completo seguindo rigorosamente todos os PRDs presentes na pasta:

```text
docs/prds/
```

Antes de iniciar qualquer implementação, o agente deve ler:

```text
docs/prds/
docs/decisions/
docs/diagrams/
```

e compreender completamente os requisitos.

---

# Estratégia de Implementação

O projeto deve ser construído em etapas.

Não implementar tudo de uma vez.

Cada etapa deve ser validada antes de avançar para a próxima.

---

# Etapa 1 — Validação Inicial

Objetivo:

Verificar estrutura do projeto.

Validar:

```text
app/
tests/
docs/
```

Confirmar existência dos arquivos:

```text
README.md
requirements.txt
Dockerfile
docker-compose.yml
.env.example
.pre-commit-config.yaml
```

---

# Etapa 2 — Construção do Domínio

Criar:

```text
app/domain/
```

Implementar:

```text
entities.py
schemas.py
interfaces.py
```

Responsabilidades:

* entidades
* contratos
* schemas pydantic

Não utilizar Groq nesta etapa.

---

# Etapa 3 — Construção da Camada Application

Criar:

```text
app/application/
```

Implementar:

```text
extract_brands_use_case.py
```

Responsabilidades:

* receber entrada
* validar dados
* chamar interface de extração
* retornar resultado

Não conhecer Groq diretamente.

---

# Etapa 4 — Construção da Infraestrutura

Criar:

```text
app/infrastructure/
```

Implementar:

```text
settings.py
prompts.py
groq_brand_extractor.py
```

Responsabilidades:

* integração com Groq
* leitura de ambiente
* montagem de prompt

---

# Etapa 5 — Prompt Engineering

Implementar prompt robusto.

Objetivo:

Extrair:

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": []
}
```

Regras:

* retornar apenas JSON
* não gerar explicações
* não gerar markdown
* não incluir duplicatas

---

# Etapa 6 — Validação Estruturada

Utilizar Pydantic.

Validar:

* entrada
* saída

Criar tratamento para:

* JSON inválido
* campos ausentes
* tipos incorretos

---

# Etapa 7 — CLI

Criar:

```text
app/presentation/cli.py
```

Objetivos:

* executar manualmente
* rodar os 3 casos do teste
* imprimir JSON formatado

---

# Etapa 8 — Interface Streamlit

Criar:

```text
app/presentation/streamlit_app.py
```

Seguir integralmente:

```text
03_streamlit_ui_prd.md
```

Implementar:

* Dark Mode
* CSS customizado
* cards
* exemplos do desafio
* JSON viewer
* feedback visual

---

# Etapa 9 — Logging

Criar:

```text
app/shared/logger.py
```

Implementar logs estruturados.

Registrar:

* início
* execução
* erros
* resposta da LLM

Nunca registrar segredos.

---

# Etapa 10 — Tratamento de Exceções

Criar:

```text
app/shared/exceptions.py
```

Implementar:

```python
GroqConnectionError
InvalidLLMResponseError
ValidationError
```

---

# Etapa 11 — Testes

Criar:

```text
tests/
```

Implementar:

```text
test_use_case.py
test_output_schema.py
test_validations.py
test_error_handling.py
```

Criar:

```text
tests/fakes/fake_brand_extractor.py
```

Todos os testes devem rodar sem acesso à Groq.

---

# Etapa 12 — Docker

Implementar:

```text
Dockerfile
docker-compose.yml
```

Validar:

```bash
docker compose up --build
```

---

# Etapa 13 — Qualidade

Implementar:

```text
black
ruff
isort
pre-commit
```

Validar:

```bash
pre-commit run --all-files
```

---

# Etapa 14 — README

Gerar README completo contendo:

## Como executar

### Local

```bash
pip install -r requirements.txt
python main.py
```

### Docker

```bash
docker compose up --build
```

### Streamlit

```bash
streamlit run app/presentation/streamlit_app.py
```

---

## Arquitetura

Explicar:

* SOLID
* Clean Architecture
* Groq
* Streamlit

---

## Uso de IA

Documentar:

* ferramentas utilizadas
* pontos positivos
* dificuldades encontradas

---

## Onde isso quebra

Explicar limitações da solução.

---

# Etapa 15 — Casos Oficiais

Executar:

Caso 1

Caso 2

Caso 3

Salvar os outputs.

Inserir os outputs no README.

---

# Critérios Finais de Aceite

* Projeto executável.
* Docker funcional.
* Streamlit funcional.
* Testes passando.
* Arquitetura SOLID.
* Clean Architecture.
* Integração Groq funcional.
* README completo.
* Outputs gerados.
* Código organizado e legível.
