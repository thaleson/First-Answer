# PRD — Estratégia de Testes

## Objetivo

Garantir que a aplicação seja confiável, previsível e testável.

A estratégia de testes não deve depender da API real da Groq.

Todos os testes devem ser rápidos, determinísticos e executáveis localmente.

---

# Framework

Utilizar:

```text
pytest
pytest-mock
```

---

# Filosofia

Testar:

* regras de negócio
* contratos
* validações
* fluxo da aplicação

Não testar:

* comportamento interno da Groq
* disponibilidade da API externa

---

# Estrutura

```text
tests/
│
├── test_use_case.py
├── test_output_schema.py
├── test_validations.py
├── test_error_handling.py
└── fakes/
    └── fake_brand_extractor.py
```

---

# Fake Extractor

Criar:

```python
FakeBrandExtractor
```

Objetivo:

Simular respostas da LLM.

Exemplo:

```python
return {
    "marca_monitorada_encontrada": True,
    "outras_marcas": [
        "Banco Inter",
        "C6 Bank"
    ]
}
```

---

# Testes do Use Case

Validar:

* execução correta
* retorno esperado
* integração com interfaces

---

## Cenário 1

Marca encontrada.

Entrada:

```text
marca_monitorada = Nubank
```

Resultado esperado:

```python
True
```

---

## Cenário 2

Marca não encontrada.

Resultado esperado:

```python
False
```

---

## Cenário 3

Outras marcas identificadas.

Resultado esperado:

Lista preenchida.

---

# Testes de Contrato

Validar saída:

```json
{
  "marca_monitorada_encontrada": true,
  "outras_marcas": []
}
```

Campos obrigatórios:

* marca_monitorada_encontrada
* outras_marcas

---

# Testes de Duplicidade

Entrada:

```text
Nubank
Nubank
Nubank
Banco Inter
```

Resultado:

```json
{
  "outras_marcas": [
    "Banco Inter"
  ]
}
```

Sem duplicações.

---

# Testes de Exclusão

A marca monitorada nunca deve aparecer em:

```json
outras_marcas
```

Exemplo:

Monitorada:

```text
Nubank
```

Resposta da LLM:

```json
{
  "outras_marcas": [
    "Nubank",
    "Banco Inter"
  ]
}
```

Resultado final:

```json
{
  "outras_marcas": [
    "Banco Inter"
  ]
}
```

---

# Testes de Validação

Validar:

* texto vazio
* marca vazia
* campos nulos
* campos inválidos

---

# Testes de Erro

Simular:

* timeout
* erro Groq
* resposta inválida
* JSON malformado

Verificar tratamento correto.

---

# Cobertura

Meta mínima:

```text
80%
```

Meta ideal:

```text
90%
```

---

# CI Friendly

Os testes devem:

* rodar sem internet
* rodar sem Groq
* rodar em Docker
* rodar em GitHub Actions futuramente

---

# Critérios de Aceite

* Todos os testes passando.
* Nenhum teste dependente da Groq.
* Cobertura mínima de 80%.
* Fake extractor implementado.
* Casos de erro cobertos.
