# ADR 001 — Estratégia de Extração de Marcas Utilizando LLM

## Status

Aceito

---

# Contexto

O desafio consiste em identificar:

1. Se uma marca monitorada foi mencionada em um texto.
2. Quais outras marcas aparecem no mesmo conteúdo.

O enunciado permite múltiplas abordagens, incluindo:

* Regex
* Matching de strings
* NER
* Embeddings
* APIs de LLM
* Soluções híbridas

A escolha da estratégia impacta diretamente a flexibilidade, manutenção e capacidade de generalização da solução.

---

# Decisão

Foi decidido utilizar uma Large Language Model (LLM) através da API da Groq como mecanismo principal de extração de marcas.

A integração será realizada por meio de um componente dedicado chamado:

```text
GroqBrandExtractor
```

A aplicação utilizará prompts estruturados e validação de saída com Pydantic para garantir consistência no retorno.

---

# Motivação

A identificação de marcas em texto livre é um problema de reconhecimento de entidades.

Uma abordagem baseada apenas em listas estáticas apresenta limitações:

* Necessidade de manutenção constante.
* Incapacidade de reconhecer marcas novas.
* Dificuldade em lidar com variações linguísticas.
* Dependência de dicionários previamente cadastrados.

A utilização de uma LLM oferece:

* Melhor generalização.
* Reconhecimento de marcas não previamente cadastradas.
* Menor dependência de listas estáticas.
* Maior flexibilidade para textos variados.

Além disso, o próprio enunciado do teste sugere explicitamente o uso de APIs de LLM como alternativa válida.

---

# Consequências Positivas

## Flexibilidade

A solução consegue identificar marcas que não foram previamente cadastradas.

---

## Escalabilidade

Novas categorias de entidades podem ser adicionadas futuramente sem alterações significativas na arquitetura.

---

## Simplicidade de Regras

Evita grande quantidade de regras manuais baseadas em regex ou listas fixas.

---

## Evolução Futura

A arquitetura permite substituir ou adicionar novos provedores:

```text
Groq
Gemini
Claude
OpenAI
```

sem alterações no caso de uso principal.

---

# Consequências Negativas

## Dependência Externa

A solução depende de um serviço externo para execução.

---

## Custos

Em cenários futuros de alto volume pode existir custo operacional associado ao uso de LLMs.

---

## Não Determinismo

Modelos de linguagem podem gerar pequenas variações de resposta.

Para reduzir esse risco serão utilizados:

* prompts estruturados
* contratos de saída
* validação com Pydantic
* tratamento de exceções

---

# Alternativas Consideradas

## Regex e Matching de Strings

Vantagens:

* Simples
* Determinístico
* Sem dependências externas

Desvantagens:

* Pouca flexibilidade
* Dependência de listas de marcas

---

## NER Tradicional

Vantagens:

* Sem dependência de APIs externas

Desvantagens:

* Necessidade de modelos específicos
* Menor capacidade de generalização para o contexto do teste

---

## Embeddings

Vantagens:

* Boa capacidade semântica

Desvantagens:

* Complexidade desnecessária para o escopo do desafio

---

# Justificativa Final

A utilização de LLM via Groq oferece o melhor equilíbrio entre:

* simplicidade de implementação
* qualidade dos resultados
* flexibilidade
* aderência ao problema proposto

A arquitetura foi projetada para minimizar os riscos inerentes ao uso de LLMs através de validação estruturada e separação adequada de responsabilidades.

---

# Revisão Futura

Caso seja necessário reduzir dependências externas, a arquitetura permite implementar estratégias alternativas sem modificar o caso de uso principal.

Possíveis evoluções:

* Regex + LLM (abordagem híbrida)
* NER especializado
* Embeddings
* Múltiplos provedores de LLM
