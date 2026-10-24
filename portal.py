"""Shared visual components and public-portal asset configuration."""

import base64
import html
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
        .institution-link {
            align-items: center;
            background: #fff;
            border: 1px solid #d6dfdf;
            border-radius: 4px;
            box-sizing: border-box;
            color: var(--portal-ink) !important;
            display: grid;
            gap: 12px;
            grid-template-columns: 58px minmax(0, 1fr);
            margin: 0 0 8px;
            min-height: 58px;
            padding: 6px 10px;
            text-decoration: none !important;
            width: 100%;
        }
        .institution-link:hover {
            border-color: var(--portal-blue);
            color: var(--portal-blue) !important;
        }
        .institution-link img {
            height: 42px;
            object-fit: contain;
            width: 58px;
        }
        .institution-link span {
            font-size: .85rem;
            font-weight: 700;
            text-align: left;
            white-space: nowrap;
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
        institutions = (
            ("FAPESP", "fapesp_logo.png", "https://fapesp.br/"),
            ("CPS", "cps_logo.png", "https://www.cps.sp.gov.br/"),
            (
                "FATEC Campinas",
                "fatec-campinas_logo.png",
                "https://fateccampinas.com.br/",
            ),
        )
        for institution_name, logo_filename, institution_url in institutions:
            logo_path = ASSET_DIRECTORIES["logos"] / logo_filename
            image_markup = ""
            if logo_path.is_file():
                encoded_logo = base64.b64encode(logo_path.read_bytes()).decode("ascii")
                image_markup = (
                    f'<img src="data:image/png;base64,{encoded_logo}" '
                    f'alt="Logo {html.escape(institution_name)}">'
                )
            st.markdown(
                f'<a class="institution-link" href="{html.escape(institution_url)}" '
                f'target="_blank" rel="noopener noreferrer">{image_markup}'
                f"<span>{html.escape(institution_name)}</span></a>",
                unsafe_allow_html=True,
            )


def render_footer() -> None:
    """Render the mandatory FAPESP acknowledgement on every page."""
    st.divider()
    st.caption(FAPESP_ACKNOWLEDGEMENT)
