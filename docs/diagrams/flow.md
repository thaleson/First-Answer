# Execution Flow

```mermaid
sequenceDiagram

    participant User
    participant Streamlit
    participant UseCase
    participant GroqExtractor
    participant Groq

    User->>Streamlit: Informa texto e marca

    Streamlit->>UseCase: Executa análise

    UseCase->>GroqExtractor: Solicita extração

    GroqExtractor->>Groq: Envia prompt

    Groq-->>GroqExtractor: Retorna JSON

    GroqExtractor-->>UseCase: Resultado validado

    UseCase-->>Streamlit: Output final

    Streamlit-->>User: Exibe resultado
```

## Fluxo

1. Usuário informa texto.
2. Usuário informa marca monitorada.
3. Streamlit envia dados para o Use Case.
4. O Use Case chama a interface de extração.
5. A implementação Groq realiza a chamada para a LLM.
6. O retorno é validado com Pydantic.
7. O resultado é devolvido para a interface.
8. O usuário visualiza o JSON final.

```
```
