"""Cached public data loaders for the energy-emissions dashboard."""

import pandas as pd
import streamlit as st

from utils import (
    ANNUAL_SHEET,
    IBGE_SHEET,
    MUNICIPAL_COORDINATES,
    YEARS,
    parse_brazilian_number,
    sheet_url,
    tidy_columns,
)


@st.cache_data(ttl=3600, show_spinner=False)
def load_annual_data() -> pd.DataFrame:
    """Load annual energy-sector emissions from the public project spreadsheet."""
    frame = tidy_columns(pd.read_csv(sheet_url(ANNUAL_SHEET)))
    frame = frame.rename(columns={frame.columns[0]: "Município"})
    frame = frame[frame["Município"].notna()].copy()
    for year in YEARS:
        frame[str(year)] = frame[str(year)].map(parse_brazilian_number)
    annual = frame.melt(id_vars="Município", var_name="Ano", value_name="Emissões")
    annual["Ano"] = pd.to_numeric(annual["Ano"], errors="coerce")
    return annual.dropna(subset=["Ano", "Emissões"])


@st.cache_data(ttl=3600, show_spinner=False)
def load_ibge_data() -> pd.DataFrame:
    """Load public IBGE municipal indicators used for dashboard context."""
    frame = tidy_columns(pd.read_csv(sheet_url(IBGE_SHEET)))
    frame = frame.rename(columns={frame.columns[0]: "Município"})
    names = {
        frame.columns[1]: "Código IBGE",
        frame.columns[2]: "Área (km²)",
        frame.columns[3]: "População 2022",
        frame.columns[4]: "Densidade demográfica",
        frame.columns[5]: "População estimada 2025",
        frame.columns[6]: "IDHM 2010",
        frame.columns[7]: "Receitas brutas 2025",
        frame.columns[8]: "Despesas empenhadas 2025",
        frame.columns[9]: "PIB per capita 2023",
    }
    frame = frame.rename(columns=names)
    for column in frame.columns[1:]:
        frame[column] = frame[column].map(parse_brazilian_number)
    return frame


@st.cache_data(ttl=3600, show_spinner=False)
def load_coordinates() -> pd.DataFrame:
    """Return the maintained reference coordinates for RMC municipalities."""
    return pd.DataFrame(
        [
            {"Município": municipality, "Latitude": latitude, "Longitude": longitude}
            for municipality, (latitude, longitude) in MUNICIPAL_COORDINATES.items()
        ],
    )
