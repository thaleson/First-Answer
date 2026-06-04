# PRD — First Answer Brand Mention Extractor

## Visão Geral

Desenvolver uma aplicação em Python capaz de identificar se uma marca específica foi mencionada em um texto gerado por IA e listar outras marcas encontradas no mesmo conteúdo.

A solução será construída utilizando LLM via Groq como mecanismo principal de extração, seguindo princípios SOLID, Clean Architecture, Dockerização, testes automatizados e interface de validação via Streamlit.

---

# Problema

A First Answer monitora como modelos de IA mencionam marcas em suas respostas.

Dado um texto gerado por IA, precisamos identificar:

1. Se uma marca específica foi mencionada.
2. Quais outras marcas aparecem no mesmo texto.

---

# Objetivo

Receber:

```json
{
  "texto": "conteúdo gerado por IA",
  "marca_monitorada": "Nubank"
}
```

Retornar:

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": [
    "Banco Inter",
    "C6 Bank",
    "BTG Pactual"
  ]
}
```

---

# Requisitos Funcionais

## RF001

O sistema deve receber um texto em formato string.

## RF002

O sistema deve receber uma marca monitorada.

## RF003

O sistema deve identificar se a marca monitorada aparece no texto.

## RF004

O sistema deve identificar outras marcas mencionadas.

## RF005

O sistema deve retornar um JSON estruturado.

## RF006

O sistema deve impedir duplicidades na lista de marcas.

## RF007

A marca monitorada não deve aparecer dentro de outras_marcas.

## RF008

O sistema deve validar o retorno da LLM antes de responder ao usuário.

## RF009

O sistema deve disponibilizar interface visual via Streamlit.

## RF010

O sistema deve disponibilizar execução via terminal.

---

# Requisitos Não Funcionais

## RNF001

Utilizar Python 3.11 ou superior.

## RNF002

Utilizar Groq API como mecanismo principal.

## RNF003

Utilizar Docker.

## RNF004

Utilizar Docker Compose.

## RNF005

Utilizar princípios SOLID.

## RNF006

Utilizar Clean Architecture simplificada.

## RNF007

Possuir testes automatizados.

## RNF008

Possuir pre-commit configurado.

## RNF009

Possuir README detalhado.

## RNF010

Possuir código organizado e legível.

---

# Entradas

## Campo texto

Tipo:

```python
str
```

Descrição:

Texto completo gerado por IA.

---

## Campo marca_monitorada

Tipo:

```python
str
```

Descrição:

Marca que será monitorada.

---

# Saída

Estrutura:

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": []
}
```

---

# Critérios de Aceite

* Receber texto e marca monitorada.
* Consultar a LLM.
* Validar o retorno.
* Retornar JSON válido.
* Não possuir duplicidades.
* Executar localmente.
* Executar via Docker.
* Executar via Streamlit.
* Passar nos testes automatizados.

---

# Fora de Escopo

* Banco de dados.
* Autenticação.
* Histórico de consultas.
* Painel administrativo.
* Persistência de dados.
* Deploy em cloud.
* RAG.
* Vetorização.
* Multiusuário.
