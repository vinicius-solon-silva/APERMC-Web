"""Interactive, energy-sector-only emissions dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from data import load_annual_data, load_coordinates, load_ibge_data
from utils import PALETTE, YEARS, format_tonnes


def _load_dashboard_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] | None:
    """Load only public emissions, IBGE indicators, and maintained coordinates."""
    try:
        return load_annual_data(), load_ibge_data(), load_coordinates()
    except Exception as error:
        st.error("Não foi possível carregar os dados públicos do dashboard.")
        st.exception(error)
        return None


loaded_data = _load_dashboard_data()
if loaded_data is None:
    st.stop()

annual, ibge, coordinates = loaded_data
municipalities = sorted(annual["Município"].unique())
municipalities = [
    name for name in municipalities if name not in {"Acumulado do Período", "Outras cidades da RMC"}
]
annual = annual[annual["Município"].isin(municipalities)].copy()

summary = annual.groupby("Município", as_index=False).agg(
    Acumulado=("Emissões", "sum"),
    **{"Média anual": ("Emissões", "mean")},
    Pico=("Emissões", "max"),
)
first_year = annual[annual["Ano"] == min(YEARS)].set_index("Município")["Emissões"]
last_year = annual[annual["Ano"] == max(YEARS)].set_index("Município")["Emissões"]
summary["Variação no período"] = (
    summary["Município"].map(last_year).div(summary["Município"].map(first_year)).sub(1).mul(100)
)
summary = summary.merge(ibge, on="Município", how="left").merge(
    coordinates, on="Município", how="left"
)

st.title("Emissões do setor de energia")
st.caption(
    "Dados públicos municipais da Região Metropolitana de Campinas. Este painel contém somente "
    "séries do setor energético e indicadores públicos; não incorpora questionários ou entrevistas."
)

with st.sidebar:
    st.markdown("**Filtros do dashboard energético**")
    selected_municipalities = st.multiselect(
        "Municípios",
        municipalities,
        default=municipalities[:3],
        help="Selecione municípios para comparar as séries públicas de emissões do setor de energia.",
    )
    show_map_detail = st.checkbox("Detalhar mapa", value=True)
    selected_years = st.slider("Período", min(YEARS), max(YEARS), (min(YEARS), max(YEARS)))
    if st.button("Atualizar dados públicos", width="stretch", type="secondary"):
        load_annual_data.clear()
        load_ibge_data.clear()
        load_coordinates.clear()
        st.rerun()
    st.caption("Fonte: planilha pública APERMC · cache de 1 hora")

view_years = list(range(selected_years[0], selected_years[1] + 1))
filtered = annual[annual["Ano"].isin(view_years)].copy()
period_summary = (
    filtered.groupby("Município", as_index=False)["Emissões"]
    .sum()
    .rename(columns={"Emissões": "Emissões no período"})
)
period_totals = filtered.groupby("Ano")["Emissões"].sum()
selected_total = period_summary[period_summary["Município"].isin(selected_municipalities)][
    "Emissões no período"
].sum()

metric_columns = st.columns(4)
metric_columns[0].metric(
    "Emissões no recorte", f"{format_tonnes(filtered['Emissões'].sum())} tCO₂e"
)
metric_columns[1].metric("Municípios observados", str(len(municipalities)))
metric_columns[2].metric("Ano de maior emissão", str(int(period_totals.idxmax())))
metric_columns[3].metric("Municípios destacados", f"{format_tonnes(selected_total)} tCO₂e")

st.subheader("Leitura do período selecionado")
left, right = st.columns([1.55, 1])
with left:
    yearly = filtered.groupby("Ano", as_index=False)["Emissões"].sum()
    figure = px.area(
        yearly,
        x="Ano",
        y="Emissões",
        markers=True,
        color_discrete_sequence=[PALETTE[0]],
    )
    figure.update_traces(
        line_width=3,
        fillcolor="rgba(11,110,105,.14)",
        hovertemplate="%{x}: %{y:,.0f} tCO₂e<extra></extra>",
    )
    figure.update_layout(
        height=370,
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
        yaxis_title="tCO₂e",
        xaxis_title=None,
        hovermode="x unified",
    )
    st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
with right:
    ranking = period_summary.sort_values("Emissões no período", ascending=True).tail(10)
    figure = px.bar(
        ranking,
        x="Emissões no período",
        y="Município",
        orientation="h",
        color="Emissões no período",
        color_continuous_scale=["#cfe3da", PALETTE[0]],
    )
    figure.update_layout(
        height=370,
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
        xaxis_title="tCO₂e",
        yaxis_title=None,
        coloraxis_showscale=False,
    )
    st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})

comparison_tab, map_tab, data_tab = st.tabs(
    ["Séries municipais", "Mapa territorial", "Dados e indicadores"],
)

with comparison_tab:
    selected_data = filtered[filtered["Município"].isin(selected_municipalities)]
    if selected_data.empty:
        st.info("Selecione pelo menos um município na barra lateral para visualizar as séries.")
    else:
        figure = px.line(
            selected_data,
            x="Ano",
            y="Emissões",
            color="Município",
            markers=True,
            color_discrete_sequence=PALETTE,
        )
        figure.update_layout(
            height=430,
            margin={"l": 0, "r": 0, "t": 20, "b": 0},
            yaxis_title="tCO₂e",
            xaxis_title=None,
            legend_title=None,
            hovermode="x unified",
        )
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
        st.caption(
            f"Recorte selecionado: {format_tonnes(selected_total)} tCO₂e entre "
            f"{selected_years[0]} e {selected_years[1]}."
        )

with map_tab:
    map_data = summary[summary["Município"].isin(selected_municipalities)].copy()
    map_data = map_data.dropna(subset=["Latitude", "Longitude"])
    map_data = map_data.merge(period_summary, on="Município", how="left")
    if map_data.empty:
        st.info("Selecione municípios com coordenadas para visualizar o mapa.")
    else:
        map_options = {
            "lat": "Latitude",
            "lon": "Longitude",
            "hover_name": "Município",
            "hover_data": {"Emissões no período": ":,.0f", "Latitude": False, "Longitude": False},
            "opacity": 1,
            "zoom": 8.6,
            "center": {"lat": -22.8, "lon": -47.1},
            "height": 510,
        }
        if show_map_detail:
            map_options.update(
                size="Emissões no período",
                color="Emissões no período",
                color_continuous_scale=["#fff3b0", "#ffd166", "#f8961e", "#f94144", "#c1126b"],
                size_max=34,
            )
        else:
            map_options["color_discrete_sequence"] = [PALETTE[0]]
        figure = px.scatter_map(map_data, **map_options)
        figure.update_layout(
            margin={"l": 0, "r": 0, "t": 0, "b": 0}, coloraxis_colorbar_title="tCO₂e"
        )
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})

with data_tab:
    view = summary[
        [
            "Município",
            "Acumulado",
            "Variação no período",
            "População 2022",
            "IDHM 2010",
            "PIB per capita 2023",
        ]
    ].copy()
    view = view.sort_values("Acumulado", ascending=False)
    view.columns = [
        "Município",
        "Acumulado (tCO₂e)",
        "Variação 2010-2024 (%)",
        "População 2022",
        "IDHM 2010",
        "PIB per capita 2023 (R$)",
    ]
    st.dataframe(
        view.style.format(
            {
                "Acumulado (tCO₂e)": "{:,.0f}",
                "Variação 2010-2024 (%)": "{:.1f}",
                "População 2022": "{:,.0f}",
                "IDHM 2010": "{:.3f}",
                "PIB per capita 2023 (R$)": "R$ {:,.2f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )
    csv = view.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Baixar tabela CSV", csv, "apermc-indicadores.csv", "text/csv")
