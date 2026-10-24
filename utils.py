"""
Pure utility functions for the APERMC-Web app.

These functions are side-effect-free and do not depend on Streamlit,
making them easy to unit-test.
"""

from urllib.parse import urlencode

import pandas as pd

SHEET_ID = "1vVuBkpo29YjDjNR5Pn_xFLwS52yiGri46ZPOCSTkRTA"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"
ANNUAL_SHEET = "Emissões Anuais e Totais"
IBGE_SHEET = "Dados IBGE 2022"
YEARS = list(range(2010, 2025))

PALETTE = ["#0b6e69", "#e07a5f", "#3d5a80", "#f2cc8f", "#6a994e", "#bc4749"]

MUNICIPAL_COORDINATES = {
    "Americana": (-22.7392463, -47.3306032),
    "Artur Nogueira": (-22.572737, -47.172679),
    "Campinas": (-22.9056391, -47.059564),
    "Cosmópolis": (-22.6437398, -47.1972086),
    "Engenheiro Coelho": (-22.4896659, -47.2119005),
    "Holambra": (-22.6332028, -47.0545305),
    "Hortolândia": (-22.8620175, -47.2164219),
    "Indaiatuba": (-23.0908356, -47.2180677),
    "Itatiba": (-23.0055542, -46.8397726),
    "Jaguariúna": (-22.70374, -46.985062),
    "Monte Mor": (-22.945043, -47.312182),
    "Morungaba": (-22.88, -46.79167),
    "Nova Odessa": (-22.7805746, -47.2993805),
    "Paulínia": (-22.7630391, -47.1532213),
    "Pedreira": (-22.741347, -46.894846),
    "Santa Bárbara d'Oeste": (-22.7542539, -47.4137884),
    "Santo Antônio de Posse": (-22.6053304, -46.9197291),
    "Sumaré": (-22.8217964, -47.267105),
    "Valinhos": (-22.97056, -46.99583),
    "Vinhedo": (-23.0298535, -46.9749847),
}


def sheet_url(sheet_name: str) -> str:
    """Build a Google Sheets CSV export URL for a given sheet name."""
    query = urlencode({"tqx": "out:csv", "sheet": sheet_name})
    return f"{BASE_URL}?{query}"


def parse_brazilian_number(value: object) -> float:
    """Parse a Brazilian-formatted number (e.g. '1.234,56' → 1234.56)."""
    if pd.isna(value):
        return float("nan")
    text = str(value).strip().replace("\u00a0", "")
    if not text:
        return float("nan")
    text = text.replace(".", "").replace(",", ".") if "," in text else text.replace(".", "")
    return pd.to_numeric(text, errors="coerce")


def tidy_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop unnamed columns and rows/columns that are entirely NaN."""
    frame = frame.loc[:, ~frame.columns.astype(str).str.match(r"^Unnamed")]
    return frame.dropna(axis=1, how="all").dropna(axis=0, how="all")


def format_tonnes(value: float) -> str:
    """Format a value as a Brazilian-style tonnes string (e.g. 1.234,5)."""
    return f"{value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: float) -> str:
    """Format a value as a Brazilian-style percentage string (e.g. '5,3%')."""
    return f"{value:.1f}%".replace(".", ",")
