# PRD — Interface Streamlit

## Objetivo

Criar uma interface moderna, intuitiva, profissional e responsiva para permitir que usuários testem a extração de marcas utilizando a aplicação.

A interface deve ser simples para uso, porém visualmente agradável e organizada.

A experiência do usuário deve transmitir qualidade, organização e clareza.

---

# Objetivos de UX

O usuário deve conseguir:

* Entender rapidamente o propósito da aplicação.
* Inserir um texto grande sem dificuldades.
* Informar a marca monitorada.
* Executar a análise com apenas um clique.
* Visualizar claramente o resultado.
* Testar rapidamente os casos do desafio.
* Entender possíveis erros de forma amigável.

---

# Design

## Tema

Utilizar Dark Mode moderno.

Inspirado em:

* OpenAI
* Claude
* Notion Dark
* Vercel

Visual:

* Minimalista
* Profissional
* Limpo
* Sem excesso de elementos

---

# Layout

## Estrutura

```text
┌────────────────────────────────────┐
│ Header                             │
├────────────────────────────────────┤
│ Descrição                          │
├────────────────────────────────────┤
│ Casos de teste                     │
├────────────────────────────────────┤
│ Marca monitorada                   │
├────────────────────────────────────┤
│ Texto                              │
├────────────────────────────────────┤
│ Botão Executar                     │
├────────────────────────────────────┤
│ Resultado                          │
├────────────────────────────────────┤
│ JSON                               │
└────────────────────────────────────┘
```

---

# Header

Exibir:

```text
First Answer Brand Mention Extractor
```

Subtítulo:

```text
Identifique marcas mencionadas em respostas geradas por IA.
```

Adicionar breve descrição explicando o objetivo.

---

# Casos de Teste

Criar seletor contendo:

```text
Caso 1 — Nubank
Caso 2 — Nike
Caso 3 — First Answer
```

Ao selecionar um caso:

* preencher automaticamente texto
* preencher automaticamente marca monitorada

Objetivo:

Permitir demonstração rápida.

---

# Campo Marca Monitorada

Componente:

```python
st.text_input()
```

Características:

* obrigatório
* placeholder amigável

Exemplo:

```text
Digite a marca monitorada
```

---

# Campo Texto

Componente:

```python
st.text_area()
```

Características:

* grande
* confortável para leitura
* múltiplas linhas

Altura mínima:

```python
300px
```

Placeholder:

```text
Cole aqui uma resposta gerada por IA...
```

---

# Botão Principal

Texto:

```text
Extrair Marcas
```

Características:

* destaque visual
* largura adequada
* feedback visual ao clicar

---

# Loading

Ao executar análise:

Exibir:

```python
st.spinner()
```

Mensagem:

```text
Analisando marcas...
```

---

# Resultado

Criar card principal contendo:

## Marca Monitorada Encontrada

Exibir:

```text
SIM
```

ou

```text
NÃO
```

Com ícones visuais.

---

## Outras Marcas

Exibir em formato:

```text
Banco Inter
C6 Bank
BTG Pactual
```

ou

```text
Nenhuma marca encontrada
```

---

# JSON Viewer

Exibir JSON completo.

Utilizar:

```python
st.json()
```

Objetivo:

Permitir inspeção técnica do retorno.

---

# Mensagens de Erro

Utilizar:

```python
st.error()
```

Exemplos:

* texto vazio
* marca vazia
* erro de conexão com Groq
* resposta inválida da LLM

Mensagens devem ser amigáveis.

---

# Mensagens de Sucesso

Utilizar:

```python
st.success()
```

Exemplo:

```text
Análise concluída com sucesso.
```

---

# CSS

Criar função:

```python
load_custom_css()
```

Responsável por:

* bordas arredondadas
* containers organizados
* melhor espaçamento
* tipografia agradável

Evitar aparência padrão do Streamlit.

---

# Organização do Código

Criar funções separadas.

Obrigatório:

```python
load_custom_css()

render_header()

render_examples()

render_input_form()

render_result()

render_json_result()

main()
```

---

# Responsividade

A interface deve funcionar em:

* notebook
* desktop
* monitor ultrawide

Evitar:

* larguras fixas
* elementos quebrando layout

Utilizar containers flexíveis.

---

# Separação de Responsabilidades

A interface NÃO pode conter:

* chamadas diretas para Groq
* regras de negócio
* validações complexas

A UI deve apenas chamar o Use Case.

Fluxo:

```text
UI
 ↓
Use Case
 ↓
Groq Extractor
```

---

# Acessibilidade

Utilizar:

* labels claros
* textos legíveis
* contraste adequado

---

# Critérios de Aceite

* Interface moderna.
* Dark Mode.
* CSS customizado.
* Responsiva.
* Casos de teste carregáveis.
* Exibição amigável dos resultados.
* JSON visível.
* Código organizado em funções.
* Sem regra de negócio na camada de apresentação.
* Compatível com Streamlit.
