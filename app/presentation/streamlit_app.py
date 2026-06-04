import streamlit as st

from app.application.schemas import BrandExtractionInput, BrandExtractionOutput
from app.bootstrap.container import build_extract_brands_use_case_with_groq
from app.infrastructure.settings import GroqSettings
from app.presentation.cli import OFFICIAL_CASES
from app.shared.logger import configure_logging

CASE_OPTIONS = {case.title: case for case in OFFICIAL_CASES}
DEFAULT_CASE_TITLE = OFFICIAL_CASES[0].title


def load_custom_css() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg: #0c0f12;
                --panel: #12171d;
                --panel-soft: #171d24;
                --border: rgba(255, 255, 255, 0.08);
                --text: #f3f5f7;
                --muted: #9aa6b2;
                --accent: #7dd3fc;
                --accent-strong: #38bdf8;
                --success: #34d399;
                --danger: #fb7185;
                --shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 30%),
                    radial-gradient(circle at top right, rgba(125, 211, 252, 0.12), transparent 28%),
                    linear-gradient(180deg, #0b0e11 0%, #0f1318 100%);
                color: var(--text);
            }

            .block-container {
                max-width: 1040px;
                padding-top: 2.5rem;
                padding-bottom: 4rem;
            }

            .fa-shell {
                border: 1px solid var(--border);
                background: linear-gradient(180deg, rgba(18, 23, 29, 0.96), rgba(13, 18, 24, 0.96));
                border-radius: 28px;
                padding: 1.6rem;
                box-shadow: var(--shadow);
                backdrop-filter: blur(10px);
            }

            .fa-header {
                border: 1px solid var(--border);
                background:
                    linear-gradient(135deg, rgba(56, 189, 248, 0.16), rgba(18, 23, 29, 0.72)),
                    rgba(18, 23, 29, 0.92);
                border-radius: 24px;
                padding: 1.7rem 1.7rem 1.4rem 1.7rem;
                margin-bottom: 1.2rem;
            }

            .fa-kicker {
                display: inline-block;
                color: #d8f4ff;
                background: rgba(56, 189, 248, 0.16);
                border: 1px solid rgba(125, 211, 252, 0.32);
                border-radius: 999px;
                padding: 0.32rem 0.7rem;
                font-size: 0.78rem;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }

            .fa-title {
                margin: 0.9rem 0 0.3rem 0;
                font-size: 2.2rem;
                line-height: 1.05;
                color: var(--text);
                font-weight: 700;
            }

            .fa-subtitle {
                margin: 0;
                font-size: 1.02rem;
                color: #dbe5ef;
            }

            .fa-description {
                margin-top: 1rem;
                color: var(--muted);
                line-height: 1.6;
                max-width: 760px;
            }

            .fa-section {
                margin-top: 1rem;
                padding: 1.15rem 1.15rem 1rem 1.15rem;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid var(--border);
            }

            .fa-section-title {
                font-size: 0.92rem;
                color: #dfe7ef;
                margin-bottom: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }

            .fa-result-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 1rem;
                margin-top: 0.9rem;
            }

            .fa-card {
                border-radius: 20px;
                padding: 1.1rem;
                border: 1px solid var(--border);
                background: linear-gradient(180deg, rgba(22, 29, 37, 0.95), rgba(16, 22, 28, 0.95));
            }

            .fa-card-label {
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--muted);
                margin-bottom: 0.65rem;
            }

            .fa-status {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text);
            }

            .fa-status.success {
                color: var(--success);
            }

            .fa-status.danger {
                color: var(--danger);
            }

            .fa-brand-list {
                margin: 0;
                padding-left: 1.15rem;
                color: var(--text);
                line-height: 1.7;
            }

            .fa-empty {
                color: var(--muted);
                margin: 0;
            }

            div[data-baseweb="select"] > div,
            div[data-baseweb="input"] > div,
            div[data-baseweb="textarea"] > div {
                background: rgba(14, 19, 25, 0.95) !important;
                border-color: rgba(255, 255, 255, 0.08) !important;
                border-radius: 16px !important;
            }

            .stTextInput label,
            .stTextArea label,
            .stSelectbox label {
                color: #dfe7ef !important;
                font-weight: 600 !important;
            }

            .stTextArea textarea {
                min-height: 320px !important;
            }

            .stButton > button {
                width: 100%;
                border: 0;
                border-radius: 16px;
                padding: 0.85rem 1rem;
                background: linear-gradient(135deg, var(--accent-strong), var(--accent));
                color: #071018;
                font-weight: 700;
                box-shadow: 0 12px 30px rgba(56, 189, 248, 0.28);
            }

            .stButton > button:hover {
                filter: brightness(1.05);
            }

            [data-testid="stJson"] {
                border-radius: 18px;
                border: 1px solid var(--border);
                overflow: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    if "selected_case_title" not in st.session_state:
        st.session_state.selected_case_title = DEFAULT_CASE_TITLE
    if "monitored_brand" not in st.session_state:
        default_case = CASE_OPTIONS[st.session_state.selected_case_title]
        st.session_state.monitored_brand = default_case.monitored_brand
    if "text" not in st.session_state:
        default_case = CASE_OPTIONS[st.session_state.selected_case_title]
        st.session_state.text = default_case.text.strip()


def render_header() -> None:
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
    selected_case = CASE_OPTIONS[st.session_state.selected_case_title]
    st.session_state.monitored_brand = selected_case.monitored_brand
    st.session_state.text = selected_case.text.strip()


def render_examples() -> None:
    st.markdown(
        '<div class="fa-section-title">Casos de teste</div>', unsafe_allow_html=True
    )
    st.selectbox(
        "Selecione um caso oficial",
        options=list(CASE_OPTIONS.keys()),
        key="selected_case_title",
        on_change=handle_case_selection,
    )


def render_input_form() -> tuple[str, str, bool]:
    st.markdown('<div class="fa-section-title">Entrada</div>', unsafe_allow_html=True)
    monitored_brand = st.text_input(
        "Marca monitorada",
        key="monitored_brand",
        placeholder="Digite a marca monitorada",
    )
    text = st.text_area(
        "Texto",
        key="text",
        placeholder="Cole aqui uma resposta gerada por IA...",
        height=320,
    )
    submitted = st.button("Extrair Marcas", type="primary")
    return monitored_brand, text, submitted


def execute_analysis(monitored_brand: str, text: str) -> BrandExtractionOutput:
    settings = GroqSettings.from_env()
    configure_logging(settings.log_level)
    use_case = build_extract_brands_use_case_with_groq()
    return use_case.execute(
        BrandExtractionInput(
            text=text,
            monitored_brand=monitored_brand,
        )
    )


def render_result(result: BrandExtractionOutput) -> None:
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
    st.markdown('<div class="fa-section-title">JSON</div>', unsafe_allow_html=True)
    st.json(result.model_dump())


def main() -> None:
    st.set_page_config(
        page_title="First Answer Brand Mention Extractor",
        page_icon=":mag:",
        layout="wide",
    )
    load_custom_css()
    initialize_state()

    st.markdown('<div class="fa-shell">', unsafe_allow_html=True)
    render_header()

    st.markdown('<div class="fa-section">', unsafe_allow_html=True)
    render_examples()
    monitored_brand, text, submitted = render_input_form()
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        try:
            with st.spinner("Analisando marcas..."):
                result = execute_analysis(
                    monitored_brand=monitored_brand,
                    text=text,
                )
        except Exception as exc:
            st.error(f"Não foi possível concluir a análise: {exc}")
        else:
            st.success("Análise concluída com sucesso.")
            render_result(result)
            render_json_result(result)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
