"""CLI entrypoint for running the official brand extraction cases."""

import argparse
import json
from dataclasses import dataclass

from app.application.schemas import BrandExtractionInput
from app.bootstrap.container import build_extract_brands_use_case_with_groq
from app.infrastructure.settings import GroqSettings
from app.shared.logger import configure_logging


@dataclass(frozen=True, slots=True)
class OfficialCase:
    """Represent one official challenge case used by the CLI and Streamlit UI."""

    case_id: str
    title: str
    monitored_brand: str
    text: str


OFFICIAL_CASES: tuple[OfficialCase, ...] = (
    OfficialCase(
        case_id="case-1",
        title="Caso 1 - Nubank",
        monitored_brand="Nubank",
        text="""
Não existe um único “melhor” cartão de crédito para todo mundo. O melhor depende do que você valoriza: cashback, milhas, ausência de anuidade ou benefícios de viagem.

Com base nas opções mais populares do mercado brasileiro, estas são algumas boas alternativas:

- Nubank: ideal para quem busca simplicidade, aplicativo fácil de usar e geralmente sem anuidade.
- Banco Inter: boa opção para quem quer cashback sem pagar anuidade.
- Nubank Ultravioleta: indicado para quem tem gastos mais elevados e deseja cashback em todas as compras.
- C6 Bank: interessante para quem quer acumular pontos e milhas.
- BTG Pactual Black: recomendado para quem viaja com frequência e valoriza benefícios premium, como acesso a salas VIP.

Sugestões por perfil:

- Se você está começando a usar cartão de crédito: Nubank.
- Se quer cashback sem anuidade: Banco Inter.
- Se gasta mais de R$ 5.000 por mês e busca maior retorno: Nubank Ultravioleta.
- Se o foco é acumular milhas para viajar: C6 Bank ou cartões Black de bancos tradicionais.

Se você informar sua idade, quanto costuma gastar por mês no cartão e se prefere cashback ou milhas, posso indicar a opção mais adequada para o seu perfil.
""",
    ),
    OfficialCase(
        case_id="case-2",
        title="Caso 2 - Nike",
        monitored_brand="Nike",
        text="""
Para a maioria das pessoas que está começando a correr, a melhor escolha é um tênis de treino diário, com bom amortecimento e conforto, sem necessidade de investir em modelos de competição.

**Melhor custo-benefício: Olympikus Corre 4**

- Marca brasileira muito bem avaliada.
- Leve, confortável e versátil.
- Excelente para quem pretende evoluir dos 5 km para distâncias maiores.

**Melhor para quem busca conforto: Olympikus Corre Max**

- Mais amortecido.
- Ótimo para iniciantes, pessoas mais pesadas ou quem sente mais o impacto da corrida.

**Melhor opção de entrada: Asics Gel-Excite 10**

- Geralmente encontrado por menos de R$ 400.
- Muito confortável para os primeiros meses de corrida.

**Melhor compra sem erro: Mizuno Wave Rider 29**

- Durável, confortável e confiável.
- Frequentemente recomendado por corredores experientes.
- Funciona bem para diferentes tipos de corredores.

**Melhor conforto premium: New Balance Fresh Foam X 1080 v14**

- Um dos tênis mais confortáveis do mercado.
- Excelente para treinos leves e corridas mais longas.
- Custa mais caro, mas entrega uma experiência superior.

Se eu tivesse que indicar apenas um modelo para a maioria dos iniciantes hoje, seria o **Olympikus Corre 4**, por oferecer uma combinação difícil de superar entre conforto, desempenho e preço.

Minha ordem de recomendação para quem está começando seria:

1. Olympikus Corre 4
2. Mizuno Wave Rider 29
3. Asics Gel-Excite 10
4. Olympikus Corre Max
5. New Balance Fresh Foam X 1080 v14

Se você me informar seu peso, orçamento e se pretende correr principalmente na rua ou na esteira, consigo indicar o modelo mais adequado para o seu caso.
""",
    ),
    OfficialCase(
        case_id="case-3",
        title="Caso 3 - First Answer",
        monitored_brand="First Answer",
        text="""
Se o objetivo é monitorar a visibilidade de uma marca em plataformas como ChatGPT, Gemini, Claude, Perplexity e Copilot, algumas soluções se destacam no mercado em 2026.

A Profound é atualmente considerada por muitos a referência do setor. A plataforma oferece monitoramento de presença em diferentes mecanismos de IA, análise de share of voice, inteligência competitiva e identificação dos prompts que geram menções à marca. É uma solução voltada principalmente para empresas de médio e grande porte que desejam estruturar uma estratégia robusta de visibilidade em IA.

A Brandlight tem um foco diferente. Além de medir presença, ela busca entender como a marca está sendo representada pelas IAs. A plataforma analisa narrativa, sentimento, precisão das respostas e possíveis distorções de posicionamento, sendo especialmente interessante para empresas preocupadas com reputação e branding.

A Peec AI vem ganhando espaço como uma alternativa com excelente custo-benefício. Oferece recursos de share of voice, benchmarking de concorrentes, análise das fontes utilizadas pelas IAs e suporte multilíngue, sendo bastante utilizada por startups, scale-ups e agências.

A AthenaHQ é uma solução mais voltada para grandes organizações que precisam segmentar análises por região, público ou unidade de negócio, oferecendo recursos avançados de governança e relatórios executivos.

Já a First Answer possui uma proposta focada na qualidade das respostas geradas pelas IAs. Em vez de apenas medir menções, a plataforma avalia se a marca está sendo apresentada corretamente, se seus diferenciais estão sendo compreendidos pelos modelos e se o posicionamento desejado está sendo refletido nas respostas.

De forma geral, cada plataforma atende a uma necessidade diferente. A Profound se destaca para monitoramento de presença e share of voice. A Brandlight é forte em reputação e narrativa. A Peec AI oferece uma excelente relação custo-benefício. A AthenaHQ atende demandas corporativas mais complexas. E a First Answer se diferencia por analisar a qualidade e a fidelidade da representação da marca pelas IAs.

Para empresas que estão investindo em GEO (Generative Engine Optimization), otimização para LLMs e gestão de percepção de marca em IA, a combinação entre monitoramento de presença, análise de narrativa e avaliação da qualidade das respostas tende a gerar a visão mais completa do mercado.
""",
    ),
)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for official case execution.

    Returns:
        argparse.ArgumentParser: Configured parser for selecting challenge cases.
    """

    parser = argparse.ArgumentParser(
        description="Run official brand extraction cases through Groq.",
    )
    parser.add_argument(
        "--case",
        choices=[official_case.case_id for official_case in OFFICIAL_CASES] + ["all"],
        default="all",
        help="Official case to run.",
    )
    return parser


def run_case(case: OfficialCase) -> dict[str, object]:
    """Execute the use case for a single official challenge input.

    Args:
        case (OfficialCase): Official challenge case to execute.

    Returns:
        dict[str, object]: Serializable execution payload with input and output data.
    """

    settings = GroqSettings.from_env()
    configure_logging(settings.log_level)
    use_case = build_extract_brands_use_case_with_groq()
    result = use_case.execute(
        BrandExtractionInput(
            text=case.text,
            monitored_brand=case.monitored_brand,
        )
    )
    return {
        "case_id": case.case_id,
        "title": case.title,
        "input": {
            "monitored_brand": case.monitored_brand,
            "text": case.text,
        },
        "output": result.model_dump(),
    }


def run_selected_cases(selected_case_id: str) -> list[dict[str, object]]:
    """Execute one or all official cases based on the selected identifier.

    Args:
        selected_case_id (str): Case identifier or the `all` sentinel.

    Returns:
        list[dict[str, object]]: List of serializable results for the executed cases.
    """

    if selected_case_id == "all":
        return [run_case(case) for case in OFFICIAL_CASES]

    selected_case = next(
        case for case in OFFICIAL_CASES if case.case_id == selected_case_id
    )
    return [run_case(selected_case)]


def main() -> int:
    """Run the CLI workflow and print JSON results to stdout.

    Returns:
        int: Process exit code for the CLI execution.
    """

    parser = build_parser()
    args = parser.parse_args()
    results = run_selected_cases(args.case)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0
