# First Answer Brand Mention Extractor

## Visão geral

Este projeto resolve o desafio técnico da First Answer: receber um texto e uma marca monitorada, identificar se a marca aparece no conteúdo e listar outras marcas mencionadas no mesmo texto.

A solução foi construída em Python com arquitetura em camadas, integração com LLM via Groq, validação estruturada com Pydantic, execução por terminal e interface visual em Streamlit.

Entrada esperada:

```json
{
  "texto": "conteúdo gerado por IA",
  "marca_monitorada": "Nubank"
}
```

Saída esperada:

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": [
    "Banco Inter",
    "C6 Bank"
  ]
}
```

## Configuração do `.env`

Crie um arquivo `.env` local a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis:

```env
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=llama-3.3-70b-versatile
LOG_LEVEL=INFO
```

Descrição:

- `GROQ_API_KEY`: chave de acesso da API da Groq.
- `GROQ_MODEL`: modelo usado na extração.
- `LOG_LEVEL`: nível de logging da aplicação.

## Instalação local

Recomendado usar ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como rodar a CLI

Rodar todos os casos oficiais:

```bash
python main.py
```

Rodar apenas um caso:

```bash
python main.py --case case-1
python main.py --case case-2
python main.py --case case-3
```

A CLI usa os 3 textos oficiais do desafio e imprime o resultado em JSON formatado.

## Como rodar o Streamlit

```bash
streamlit run app/presentation/streamlit_app.py
```

A interface permite:

- selecionar os 3 casos oficiais
- editar marca monitorada e texto manualmente
- executar a análise com o mesmo use case da CLI
- visualizar resultado resumido e JSON técnico

## Arquitetura

### Domain

Contém o núcleo puro da regra de negócio.

Responsabilidades:

- entidades
- contratos abstratos

Arquivos principais:

- `app/domain/entities.py`
- `app/domain/interfaces.py`

O domínio não depende de Groq, Streamlit, Pydantic nem variáveis de ambiente.

### Application

Contém o caso de uso e os contratos de entrada e saída da aplicação.

Responsabilidades:

- receber entrada validada
- chamar a abstração do extrator
- normalizar o resultado
- remover duplicatas
- remover a marca monitorada da lista de outras marcas

Arquivos principais:

- `app/application/schemas.py`
- `app/application/extract_brands_use_case.py`

### Infrastructure

Contém implementações concretas e dependências externas.

Responsabilidades:

- leitura de ambiente
- construção de prompt
- chamada da API da Groq
- parsing da resposta da LLM

Arquivos principais:

- `app/infrastructure/settings.py`
- `app/infrastructure/prompts.py`
- `app/infrastructure/groq_brand_extractor.py`

### Presentation

Contém as interfaces de entrada do sistema.

Responsabilidades:

- CLI
- Streamlit
- captura de input
- renderização de output

Arquivos principais:

- `app/presentation/cli.py`
- `app/presentation/streamlit_app.py`

Importante: a camada de apresentação não implementa regra de negócio.

### Bootstrap

Contém o composition root da aplicação.

Responsabilidades:

- montar o use case
- conectar a abstração `BrandExtractor` com a implementação concreta `GroqBrandExtractor`

Arquivo principal:

- `app/bootstrap/container.py`

### Shared

Contém utilidades compartilhadas entre camadas.

Responsabilidades:

- exceções
- configuração de logging

Arquivos principais:

- `app/shared/exceptions.py`
- `app/shared/logger.py`

## Abordagem escolhida

A estratégia adotada foi:

- LLM via Groq como mecanismo principal de extração
- validação estruturada com Pydantic

Motivação:

- reconhecimento de marcas em texto livre é mais flexível com LLM do que com listas estáticas
- a arquitetura permite trocar o provider depois sem alterar o caso de uso
- Pydantic reduz risco de retorno malformado

Fluxo resumido:

1. Presentation recebe `texto` e `marca_monitorada`
2. Application executa o use case
3. Infrastructure chama a Groq
4. A resposta é validada
5. O resultado final é devolvido em JSON

## Como usei IA no desenvolvimento

A IA foi usada como apoio de engenharia para:

- consolidar e interpretar os PRDs
- propor a arquitetura inicial
- estruturar as camadas
- implementar os módulos de forma incremental
- revisar consistência de imports e dependências entre camadas
- montar a interface Streamlit sem colocar regra de negócio na UI

A implementação foi guiada pelos documentos do projeto e revisada passo a passo antes de avançar para cada etapa.

## Onde isso quebra

Limitações atuais da solução:

- depende de um serviço externo, então falhas de rede ou de API impactam a execução
- o comportamento da LLM não é totalmente determinístico
- mesmo com prompt restrito e validação, a resposta da LLM ainda pode vir vazia, inválida ou fora do esquema esperado
- nomes de marcas podem ter ambiguidades contextuais
- não há fallback local com regex, NER ou lista estática
- Docker e testes automatizados ainda não foram implementados nesta etapa do projeto

## Outputs

Seção reservada para colar os outputs finais dos 3 casos oficiais depois da execução real.

### Caso 1

```json
{}
```

### Caso 2

```json
{}
```

### Caso 3

```json
{}
```
