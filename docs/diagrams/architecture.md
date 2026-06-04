# Architecture Diagram

```mermaid
flowchart TB

    UI[Streamlit UI]
    CLI[CLI]

    UI --> UC
    CLI --> UC

    UC[ExtractBrandsUseCase]

    UC --> IBrandExtractor

    IBrandExtractor --> GroqExtractor

    GroqExtractor --> GroqAPI[Groq API]

    UC --> OutputSchema[Pydantic Output Schema]

    OutputSchema --> Result[JSON Result]

    Settings[Settings]
    Logger[Logger]

    GroqExtractor --> Settings
    GroqExtractor --> Logger

```

## Camadas

### Presentation

* Streamlit UI
* CLI

### Application

* ExtractBrandsUseCase

### Domain

* Interfaces
* Schemas
* Entities

### Infrastructure

* GroqBrandExtractor
* Settings

### Shared

* Logger
* Exceptions

```
```
