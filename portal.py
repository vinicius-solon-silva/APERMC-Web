"""Shared visual components and public-portal asset configuration."""

import os
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
ASSET_ROOT = PROJECT_ROOT / "assets"
FAPESP_ACKNOWLEDGEMENT = (
    "O presente trabalho foi realizado com apoio da Fundação de Amparo à Pesquisa do Estado de "
    "São Paulo (FAPESP), Brasil. Processo nº 2026/11603-8. As opiniões, hipóteses e conclusões "
    "ou recomendações expressas neste material são de responsabilidade do(s) autor(es) e não "
    "necessariamente refletem a visão da FAPESP."
)

ASSET_DIRECTORIES = {
    "logos": ASSET_ROOT / "logos",
    "posters": ASSET_ROOT / "documents" / "posters",
    "articles": ASSET_ROOT / "documents" / "articles",
    "slides": ASSET_ROOT / "documents" / "slides",
    "events": ASSET_ROOT / "events",
}


def get_setting(name: str) -> str:
    """Read a public profile setting from environment variables or Streamlit secrets."""
    environment_value = os.getenv(name.upper(), "").strip()
    if environment_value:
        return environment_value

    try:
        return str(st.secrets.get(name, "")).strip()
    except (FileNotFoundError, RuntimeError):
        return ""


def ensure_asset_directories() -> None:
    """Create the documented asset folders when the portal first runs."""
    for directory in ASSET_DIRECTORIES.values():
        directory.mkdir(parents=True, exist_ok=True)


def render_header() -> None:
    """Render the shared region, research scope, and institutional identification."""
    ensure_asset_directories()
    st.markdown(
        """
        <style>
        :root {
            --portal-ink: #17324d;
            --portal-blue: #176b87;
            --portal-green: #28745a;
            --portal-muted: #536574;
            --portal-paper: #f5f7f6;
        }
        .stApp { background: var(--portal-paper); }
        h1, h2, h3 { color: var(--portal-ink); }
        .region-banner {
            border-bottom: 2px solid var(--portal-blue);
            margin: 0 0 1.1rem;
            padding: .2rem 0 .85rem;
        }
        .region-banner p {
            color: var(--portal-muted);
            font-size: .9rem;
            margin: .2rem 0 0;
        }
        .energy-label {
            color: var(--portal-green);
            font-size: .78rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .institution-wordmark {
            border-left: 3px solid var(--portal-blue);
            color: var(--portal-ink);
            font-size: .9rem;
            font-weight: 700;
            padding: .25rem .55rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <header class="region-banner">
          <div class="energy-label">Pesquisa de iniciação científica · setor de energia</div>
          <h1>Região Metropolitana de Campinas</h1>
          <p>Governança energética, emissões e mudanças climáticas</p>
        </header>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### APERMC-Web")
        st.caption("Ana Paula Marsarioli · pesquisadora")
        st.caption("Prof. Dr. André Luiz da Conceição · orientador")
        st.divider()
        st.caption("Instituições parceiras")
        logo_columns = st.columns(3)
        for column, (name, label) in zip(
            logo_columns,
            (("fapesp", "FAPESP"), ("cps", "CPS"), ("fatec_campinas", "FATEC Campinas")),
            strict=True,
        ):
            logo = next(
                (
                    path
                    for extension in ("png", "jpg", "jpeg", "webp")
                    if (path := ASSET_DIRECTORIES["logos"] / f"{name}.{extension}").is_file()
                ),
                None,
            )
            with column:
                if logo:
                    st.image(str(logo), width="stretch")
                else:
                    st.markdown(
                        f'<div class="institution-wordmark">{label}</div>', unsafe_allow_html=True
                    )


def render_footer() -> None:
    """Render the mandatory FAPESP acknowledgement on every page."""
    st.divider()
    st.caption(FAPESP_ACKNOWLEDGEMENT)
