"""Helpers for loading presentation-layer styles."""

from pathlib import Path

import streamlit as st


def load_css() -> None:
    """Load the shared Streamlit stylesheet into the current page.

    The stylesheet is kept in the presentation layer so UI-specific styling remains
    isolated from application and infrastructure concerns.
    """

    css_path = Path(__file__).resolve().parents[1] / "styles" / "main.css"
    css_content = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
