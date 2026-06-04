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

O carregamento do `.env` é automático tanto na CLI quanto no Streamlit.
Se as variáveis já estiverem exportadas no ambiente, elas continuam tendo prioridade sobre o conteúdo do `.env`.

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

## Decisões Arquiteturais

As decisões principais deste projeto estão alinhadas com [docs/decisions/adr_001_llm_strategy.md](docs/decisions/adr_001_llm_strategy.md).

Resumo das decisões:

- o mecanismo principal de extração é uma LLM via Groq
- a resposta da LLM é validada estruturalmente com Pydantic
- a organização do código segue uma Clean Architecture simplificada
- o provider pode ser trocado no futuro sem alterar o `ExtractBrandsUseCase`, desde que implemente o contrato `BrandExtractor`

## Como usou ferramentas de IA

Ferramentas utilizadas:

- LLM para leitura e consolidação dos PRDs
- LLM para apoio na estruturação arquitetural
- LLM para apoio na implementação incremental

Onde ajudaram:

- na interpretação dos requisitos espalhados em múltiplos documentos
- na decomposição do trabalho em etapas pequenas e verificáveis
- na aceleração da implementação de boilerplate estrutural, testes e documentação
- na revisão de consistência entre camadas, imports e responsabilidades

Onde atrapalharam:

- em alguns momentos sugeriram estruturas genéricas demais para o contexto do desafio
- houve necessidade de corrigir detalhes específicos de execução, como integração com Streamlit, carregamento de `.env` e request HTTP para a Groq
- também houve necessidade de ajustar propostas para aderir exatamente ao que os PRDs pediam, sem extrapolar escopo

Como os problemas foram identificados:

- por execução real da CLI e do Streamlit
- por leitura crítica dos PRDs e ADRs
- por validação com `pytest`
- por validação com `pre-commit`
- por testes reais contra a API da Groq e, ao final, contra Docker

A implementação foi guiada pelos documentos do projeto e revisada passo a passo antes de avançar para cada etapa.

## Testes

Os testes automatizados cobrem:

- execução do caso de uso
- validações de entrada
- validação do schema de saída
- remoção da marca monitorada de `other_brands`
- deduplicação de marcas
- propagação de erros do extrator

Resultado atual:

- 13 testes passando

## Onde isso quebra

Limitações atuais da solução:

- depende de um serviço externo, então falhas de rede ou de API impactam a execução
- o comportamento da LLM não é totalmente determinístico
- mesmo com prompt restrito e validação, a resposta da LLM ainda pode vir vazia, inválida ou fora do esquema esperado
- nomes de marcas podem ter ambiguidades contextuais
- não há fallback local com regex, NER ou lista estática
- o ambiente Docker foi validado localmente, mas não foi testado em múltiplos sistemas operacionais ou ambientes de cloud

## Resultados Obtidos

Execução real dos três casos oficiais com integração ativa na Groq:

- Caso 1: a marca monitorada `Nubank` foi encontrada, e o retorno incluiu `Banco Inter`, `C6 Bank` e `BTG Pactual`.
- Caso 2: a marca monitorada `Nike` não foi encontrada no texto oficial, e o retorno incluiu `Olympikus`, `Asics`, `Mizuno` e `New Balance`.
- Caso 3: a marca monitorada `First Answer` foi encontrada, e o retorno incluiu `Profound`, `Brandlight`, `Peec AI`, `AthenaHQ`, `Gemini`, `Claude`, `Perplexity`, `Copilot` e `ChatGPT`.

## Observações

- A solução utiliza Groq + LLM como mecanismo principal de extração de marcas.
- A saída é validada estruturalmente com Pydantic antes de ser devolvida à interface.
- A arquitetura segue princípios SOLID e uma Clean Architecture simplificada.
- Foram implementados testes automatizados offline, sem dependência da Groq real.

## Execução com Docker

Build da imagem e dos serviços:

```bash
docker compose build
```

O serviço `app` é uma CLI. Ele executa os 3 casos oficiais, imprime os resultados em JSON e finaliza o processo.

Executar apenas a CLI no container:

```bash
docker compose run --rm app
```

O serviço `streamlit` é a interface visual. Ele permanece em execução até ser interrompido.

Subir apenas a interface Streamlit:

```bash
docker compose up streamlit
```

Após subir o serviço, a interface fica disponível em:

```text
http://localhost:8502
```

Se quiser subir os serviços definidos no compose de uma vez:

```bash
docker compose up
```

Nesse cenário, o serviço `app` executa a CLI e termina após processar os 3 casos oficiais, enquanto o serviço `streamlit` continua rodando.

Para encerrar os containers:

```bash
docker compose down
```

## Outputs

Outputs reais obtidos na execução final dos três casos oficiais.

### Caso 1

```json
{
  "case_id": "case-1",
  "title": "Caso 1 - Nubank",
  "output": {
    "monitored_brand_found": true,
    "other_brands": [
      "Banco Inter",
      "C6 Bank",
      "BTG Pactual"
    ]
  }
}
```

### Caso 2

```json
{
  "case_id": "case-2",
  "title": "Caso 2 - Nike",
  "output": {
    "monitored_brand_found": false,
    "other_brands": [
      "Olympikus",
      "Asics",
      "Mizuno",
      "New Balance"
    ]
  }
}
```

### Caso 3

```json
{
  "case_id": "case-3",
  "title": "Caso 3 - First Answer",
  "output": {
    "monitored_brand_found": true,
    "other_brands": [
      "Profound",
      "Brandlight",
      "Peec AI",
      "AthenaHQ",
      "Gemini",
      "Claude",
      "Perplexity",
      "Copilot",
      "ChatGPT"
    ]
  }
}
```
