# PRD Técnico — Arquitetura e Estrutura do Projeto

## Objetivo

Definir a arquitetura técnica do projeto, responsabilidades de cada camada, padrões de desenvolvimento, fluxo de execução e organização de código.

O objetivo é garantir uma aplicação desacoplada, testável, escalável e aderente aos princípios SOLID.

---

# Arquitetura Escolhida

## Clean Architecture Simplificada

A aplicação deverá ser organizada em camadas independentes.

Fluxo:

```text
Presentation
      ↓
Application
      ↓
Domain
      ↑
Infrastructure
```

Regra principal:

As regras de negócio não podem depender de bibliotecas externas.

A camada Domain não deve conhecer:

* Groq
* Streamlit
* Docker
* Variáveis de ambiente
* Frameworks

---

# Estrutura de Pastas

```text
app/
│
├── domain/
│   ├── entities.py
│   ├── schemas.py
│   └── interfaces.py
│
├── application/
│   └── extract_brands_use_case.py
│
├── infrastructure/
│   ├── groq_brand_extractor.py
│   ├── prompts.py
│   └── settings.py
│
├── presentation/
│   ├── cli.py
│   └── streamlit_app.py
│
└── shared/
    ├── exceptions.py
    └── logger.py
```

---

# Responsabilidades

## Domain

Contém apenas regras de negócio.

Não deve possuir dependências externas.

Responsável por:

* contratos
* entidades
* schemas
* interfaces

---

## Application

Contém casos de uso.

Responsável por:

* orquestrar o fluxo
* validar entradas
* chamar interfaces
* retornar resultado final

Não deve conhecer Groq diretamente.

---

## Infrastructure

Contém implementações externas.

Responsável por:

* integração com Groq
* leitura de variáveis de ambiente
* prompts
* clientes externos

---

## Presentation

Responsável por interação com usuário.

Contém:

* CLI
* Streamlit

Não deve conter regra de negócio.

---

## Shared

Responsável por:

* logs
* exceções
* utilidades compartilhadas

---

# SOLID

## Single Responsibility Principle

Cada classe deve possuir apenas uma responsabilidade.

Exemplos:

```text
ExtractBrandsUseCase
↓
Executa o caso de uso

GroqBrandExtractor
↓
Realiza chamadas para Groq

StreamlitUI
↓
Renderiza interface
```

---

## Open Closed Principle

Novos extratores devem ser adicionados sem alterar o caso de uso.

Exemplo:

```text
GroqBrandExtractor
GeminiBrandExtractor
ClaudeBrandExtractor
```

Todos implementando a mesma interface.

---

## Liskov Substitution Principle

Qualquer implementação de extrator deve poder substituir outra sem quebrar a aplicação.

---

## Interface Segregation Principle

Interfaces devem ser pequenas e específicas.

Exemplo:

```python
class BrandExtractorInterface:
    def extract(...)
```

---

## Dependency Inversion Principle

O caso de uso depende da abstração.

Nunca da implementação.

Exemplo:

```python
use_case = ExtractBrandsUseCase(
    extractor=GroqBrandExtractor()
)
```

---

# Injeção de Dependência

Todas as dependências externas devem ser injetadas.

Não criar instâncias diretamente dentro do caso de uso.

Errado:

```python
extractor = GroqBrandExtractor()
```

Dentro do Use Case.

Correto:

```python
use_case = ExtractBrandsUseCase(
    extractor
)
```

---

# Modelos de Dados

## Input

```json
{
  "texto": "string",
  "marca_monitorada": "string"
}
```

---

## Output

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": [
    "Banco Inter",
    "C6 Bank"
  ]
}
```

---

# Pydantic

Utilizar Pydantic para:

* validação de entrada
* validação de saída
* serialização JSON

Criar:

```python
BrandExtractionInput
BrandExtractionOutput
```

---

# Integração com Groq

Implementação:

```text
GroqBrandExtractor
```

Responsabilidades:

* montar prompt
* chamar Groq
* validar resposta
* converter resposta para schema

Não deve conter regra de negócio.

---

# Prompt Strategy

A LLM deverá receber:

* texto
* marca monitorada

E responder apenas JSON.

Exemplo:

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": [
    "Banco Inter",
    "C6 Bank"
  ]
}
```

Proibido retornar:

* markdown
* explicações
* comentários

Apenas JSON.

---

# Tratamento de Erros

Criar exceções específicas.

Exemplo:

```python
GroqConnectionError
InvalidLLMResponseError
ValidationError
```

Todos os erros devem ser tratados.

---

# Logging

Implementar logging estruturado.

Logs obrigatórios:

* início da extração
* chamada para Groq
* resposta recebida
* erros

Nunca registrar:

* API keys
* segredos

---

# Testabilidade

O projeto deve permitir mocks.

Os testes não devem depender da Groq real.

Criar fake extractor para testes.

Exemplo:

```python
FakeBrandExtractor
```

---

# Escalabilidade

A arquitetura deve permitir adicionar futuramente:

* Gemini
* Claude
* OpenAI

Sem alterar o caso de uso principal.

---

# Critérios de Aceite

* Seguir SOLID.
* Seguir Clean Architecture.
* Utilizar injeção de dependência.
* Utilizar Pydantic.
* Permitir mocks.
* Não misturar camadas.
* Não colocar regra de negócio na interface.
* Não colocar lógica de negócio dentro da integração Groq.
