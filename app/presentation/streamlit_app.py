# ruff: noqa: E402
"""Streamlit interface for interactive brand extraction."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from app.application.schemas import BrandExtractionInput, BrandExtractionOutput
from app.bootstrap.container import build_extract_brands_use_case_with_groq
from app.infrastructure.settings import GroqSettings
from app.presentation.cli import OFFICIAL_CASES
from app.presentation.ui.styles_loader import load_css
from app.shared.logger import configure_logging, get_logger

CASE_OPTIONS = {case.title: case for case in OFFICIAL_CASES}
DEFAULT_CASE_TITLE = OFFICIAL_CASES[0].title
LOGGER = get_logger("streamlit_app")


def initialize_state() -> None:
    """Initialize Streamlit session state with the default official case.

    The default case is applied only when the corresponding session keys have not been set yet.
    """

    if "selected_case_title" not in st.session_state:
        st.session_state.selected_case_title = DEFAULT_CASE_TITLE
    if "monitored_brand" not in st.session_state:
        default_case = CASE_OPTIONS[st.session_state.selected_case_title]
        st.session_state.monitored_brand = default_case.monitored_brand
    if "text" not in st.session_state:
        default_case = CASE_OPTIONS[st.session_state.selected_case_title]
        st.session_state.text = default_case.text.strip()


def render_header() -> None:
    """Render the application header section."""

    st.markdown(
        """
        <div class="fa-header">
            <span class="fa-kicker">First Answer Challenge</span>
            <h1 class="fa-title">First Answer Brand Mention Extractor</h1>
            <p class="fa-subtitle">Identifique marcas mencionadas em respostas geradas por IA.</p>
            <p class="fa-description">
                Use os casos oficiais do desafio ou cole um texto próprio para verificar se a marca
                monitorada foi citada e quais outras marcas aparecem no conteúdo analisado.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def handle_case_selection() -> None:
    """Synchronize form state when the user selects an official case."""

    selected_case = CASE_OPTIONS[st.session_state.selected_case_title]
    st.session_state.monitored_brand = selected_case.monitored_brand
    st.session_state.text = selected_case.text.strip()


def render_examples() -> None:
    """Render the official case selector."""

    st.markdown(
        '<div class="fa-section-title">Casos de teste</div>', unsafe_allow_html=True
    )
    st.selectbox(
        "Selecione um caso oficial",
        options=list(CASE_OPTIONS.keys()),
        key="selected_case_title",
        on_change=handle_case_selection,
    )


def render_monitored_brand_input() -> str:
    """Render the monitored brand field.

    Returns:
        str: Current monitored brand value from Streamlit state.
    """

    st.markdown(
        '<div class="fa-section-title">Marca monitorada</div>', unsafe_allow_html=True
    )
    return st.text_input(
        "Marca monitorada",
        key="monitored_brand",
        placeholder="Digite a marca monitorada",
    )


def render_input_form() -> tuple[str, bool]:
    """Render the main text input form and submit action.

    Returns:
        tuple[str, bool]: Current text value and button submission state.
    """

    st.markdown('<div class="fa-section-title">Texto</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="fa-form-note">
            Você pode carregar um caso oficial acima ou editar manualmente o texto antes de executar a análise.
        </p>
        """,
        unsafe_allow_html=True,
    )
    text = st.text_area(
        "Texto",
        key="text",
        placeholder="Cole aqui uma resposta gerada por IA...",
        height=360,
    )
    submitted = st.button("Extrair Marcas", type="primary")
    return text, submitted


def execute_analysis(monitored_brand: str, text: str) -> BrandExtractionOutput:
    """Execute the analysis flow for the current Streamlit form state.

    Args:
        monitored_brand (str): Brand entered by the user.
        text (str): Text entered by the user.

    Returns:
        BrandExtractionOutput: Validated result returned by the application layer.
    """

    settings = GroqSettings.from_env()
    configure_logging(settings.log_level)
    use_case = build_extract_brands_use_case_with_groq()
    return use_case.execute(
        BrandExtractionInput(
            text=text,
            monitored_brand=monitored_brand,
        )
    )


def validate_form_input(monitored_brand: str, text: str) -> str | None:
    """Validate user-provided form input before execution.

    Args:
        monitored_brand (str): Brand entered by the user.
        text (str): Text entered by the user.

    Returns:
        str | None: Friendly validation message, or `None` when the input is valid.
    """

    has_brand = bool(monitored_brand.strip())
    has_text = bool(text.strip())

    if not has_brand and not has_text:
        return "Informe a marca monitorada e o texto antes de executar a análise."
    if not has_brand:
        return "Informe a marca monitorada antes de executar a análise."
    if not has_text:
        return "Informe o texto que será analisado antes de executar a análise."

    return None


def render_result(result: BrandExtractionOutput) -> None:
    """Render the human-readable result summary.

    Args:
        result (BrandExtractionOutput): Validated extraction result to display.
    """

    status_text = "SIM" if result.monitored_brand_found else "NÃO"
    status_icon = "●"
    status_class = "success" if result.monitored_brand_found else "danger"

    if result.other_brands:
        brands_markup = "".join(f"<li>{brand}</li>" for brand in result.other_brands)
        brands_content = f'<ul class="fa-brand-list">{brands_markup}</ul>'
    else:
        brands_content = '<p class="fa-empty">Nenhuma marca encontrada</p>'

    st.markdown(
        f"""
        <div class="fa-section">
            <div class="fa-section-title">Resultado</div>
            <div class="fa-result-grid">
                <div class="fa-card">
                    <div class="fa-card-label">Marca monitorada encontrada</div>
                    <div class="fa-status {status_class}">{status_icon} {status_text}</div>
                </div>
                <div class="fa-card">
                    <div class="fa-card-label">Outras marcas</div>
                    {brands_content}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_json_result(result: BrandExtractionOutput) -> None:
    """Render the raw JSON view for the current result.

    Args:
        result (BrandExtractionOutput): Validated extraction result to display.
    """

    st.markdown('<div class="fa-section-title">JSON</div>', unsafe_allow_html=True)
    st.json(result.model_dump())


def main() -> None:
    """Run the Streamlit application lifecycle."""

    st.set_page_config(
        page_title="First Answer Brand Mention Extractor",
        page_icon=":mag:",
        layout="wide",
    )
    load_css()
    initialize_state()

    render_header()
    st.markdown('<div class="fa-section">', unsafe_allow_html=True)
    top_left, top_right = st.columns([1.25, 0.75], gap="large")
    with top_left:
        render_examples()
    with top_right:
        monitored_brand = render_monitored_brand_input()
    text, submitted = render_input_form()
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        validation_message = validate_form_input(
            monitored_brand=monitored_brand,
            text=text,
        )
        if validation_message:
            st.error(validation_message)
            return

        try:
            with st.spinner("Analisando marcas..."):
                result = execute_analysis(
                    monitored_brand=monitored_brand,
                    text=text,
                )
        except Exception:
            LOGGER.exception("Unexpected error while executing Streamlit analysis.")
            st.error(
                "Não foi possível concluir a análise agora. Verifique sua conexão ou tente novamente em instantes."
            )
        else:
            st.success("Análise concluída com sucesso.")
            render_result(result)
            render_json_result(result)


if __name__ == "__main__":
    main()
