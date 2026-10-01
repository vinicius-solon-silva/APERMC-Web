from io import BytesIO
from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="APERMC | Energia e clima",
    page_icon="◒",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    query = urlencode({"tqx": "out:csv", "sheet": sheet_name})
    return f"{BASE_URL}?{query}"


def parse_brazilian_number(value: object) -> float:
    if pd.isna(value):
        return float("nan")
    text = str(value).strip().replace("\u00a0", "")
    if not text:
        return float("nan")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    else:
        text = text.replace(".", "")
    return pd.to_numeric(text, errors="coerce")


def tidy_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.loc[:, ~frame.columns.astype(str).str.match(r"^Unnamed")]
    return frame.dropna(axis=1, how="all").dropna(axis=0, how="all")


@st.cache_data(ttl=3600, show_spinner=False)
def load_annual_data() -> pd.DataFrame:
    frame = tidy_columns(pd.read_csv(sheet_url(ANNUAL_SHEET)))
    frame = frame.rename(columns={frame.columns[0]: "Município"})
    frame = frame[frame["Município"].notna()].copy()
    for year in YEARS:
        frame[str(year)] = frame[str(year)].map(parse_brazilian_number)
    long = frame.melt(id_vars="Município", var_name="Ano", value_name="Emissões")
    long["Ano"] = pd.to_numeric(long["Ano"], errors="coerce")
    return long.dropna(subset=["Ano", "Emissões"])


@st.cache_data(ttl=3600, show_spinner=False)
def load_ibge_data() -> pd.DataFrame:
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
    return pd.DataFrame(
        [
            {"Município": municipality, "Latitude": latitude, "Longitude": longitude}
            for municipality, (latitude, longitude) in MUNICIPAL_COORDINATES.items()
        ]
    )


def format_tonnes(value: float) -> str:
    return f"{value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: float) -> str:
    return f"{value:.1f}%".replace(".", ",")


try:
    annual = load_annual_data()
    ibge = load_ibge_data()
    coordinates = load_coordinates()
except Exception as error:
    st.error("Não foi possível carregar os dados públicos da planilha.")
    st.exception(error)
    st.stop()

municipalities = sorted(annual["Município"].unique())
municipalities = [name for name in municipalities if name not in {"Acumulado do Período", "Outras cidades da RMC"}]
annual = annual[annual["Município"].isin(municipalities)].copy()

summary = annual.groupby("Município", as_index=False).agg(
    Acumulado=("Emissões", "sum"),
    **{"Média anual": ("Emissões", "mean")},
    Pico=("Emissões", "max"),
)
first_year = annual[annual["Ano"] == min(YEARS)].set_index("Município")["Emissões"]
last_year = annual[annual["Ano"] == max(YEARS)].set_index("Município")["Emissões"]
summary["Variação no período"] = summary["Município"].map(last_year).div(summary["Município"].map(first_year)).sub(1).mul(100)
summary = summary.merge(ibge, on="Município", how="left").merge(coordinates, on="Município", how="left")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink: #172b2a; --muted: #61706d; --teal: #0b6e69; --paper: #f6f3ec; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
    .stApp { background: var(--paper); }
    [data-testid="stSidebar"] { background: #e4eee9; border-right: 1px solid #c6d9d0; }
    [data-testid="stMetric"] { background: #fffdf8; border: 1px solid #dfded7; border-radius: 8px; padding: 1rem; }
    [data-testid="stMetricValue"] { color: var(--teal); }
    .eyebrow { color: var(--teal); font-size: .76rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    .hero { border-bottom: 1px solid #d9d9d0; padding: .4rem 0 1.4rem; margin-bottom: 1.4rem; }
    .hero h1 { font-size: clamp(2rem, 4vw, 3.6rem); line-height: 1.02; margin: .35rem 0 .7rem; }
    .hero p { color: var(--muted); max-width: 780px; font-size: 1.02rem; margin: 0; }
    .section-label { color: var(--muted); font-size: .8rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin: .8rem 0 .5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### APERMC-Web")
    st.caption("Painel de análise das emissões do setor energético na Região Metropolitana de Campinas")
    st.divider()
    st.markdown("**Filtros de análise**")
    selected_municipalities = st.multiselect(
        "Municípios",
        municipalities,
        default=municipalities[:3],
        help="Escolha um ou mais municípios para destacar nas séries e comparações.",
    )
    show_map_detail = st.checkbox(
        "Detalhar mapa",
        value=True,
        help="Use tamanho e cor dos pontos para comparar as emissões no período selecionado.",
    )
    selected_years = st.slider("Período", min(YEARS), max(YEARS), (min(YEARS), max(YEARS)))
    view_years = list(range(selected_years[0], selected_years[1] + 1))
    st.divider()
    if st.button("Atualizar dados", width="stretch", type="secondary"):
        load_annual_data.clear()
        load_ibge_data.clear()
        load_coordinates.clear()
        st.rerun()
    st.caption("Fonte: planilha pública APERMC · cache de 1 hora")

filtered = annual[annual["Ano"].isin(view_years)].copy()
period_summary = filtered.groupby("Município", as_index=False)["Emissões"].sum().rename(columns={"Emissões": "Emissões no período"})

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Energia · território · clima</div>
      <h1>Emissões na RMC</h1>
      <p>Explore a evolução das emissões de gases de efeito estufa associadas ao setor energético dos municípios da Região Metropolitana de Campinas.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

period_total = filtered["Emissões"].sum()
period_peak = filtered.groupby("Ano")["Emissões"].sum().idxmax()
period_low = filtered.groupby("Ano")["Emissões"].sum().idxmin()
selected_total = period_summary[period_summary["Município"].isin(selected_municipalities)]["Emissões no período"].sum()

metric_columns = st.columns(4)
metric_columns[0].metric("Emissões no recorte", f"{format_tonnes(period_total)} tCO₂e")
metric_columns[1].metric("Municípios observados", f"{len(municipalities)}")
metric_columns[2].metric("Ano de maior emissão", f"{int(period_peak)}")
metric_columns[3].metric("Municípios destacados", f"{format_tonnes(selected_total)} tCO₂e")

st.markdown('<div class="section-label">Leitura do período selecionado</div>', unsafe_allow_html=True)
left, right = st.columns([1.55, 1])
with left:
    yearly = filtered.groupby("Ano", as_index=False)["Emissões"].sum()
    figure = px.area(yearly, x="Ano", y="Emissões", markers=True, color_discrete_sequence=[PALETTE[0]])
    figure.update_traces(line_width=3, fillcolor="rgba(11,110,105,.14)", hovertemplate="%{x}: %{y:,.0f} tCO₂e<extra></extra>")
    figure.update_layout(height=370, margin=dict(l=0, r=0, t=20, b=0), yaxis_title="tCO₂e", xaxis_title=None, hovermode="x unified")
    st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
with right:
    ranking = period_summary.sort_values("Emissões no período", ascending=True).tail(10)
    figure = px.bar(ranking, x="Emissões no período", y="Município", orientation="h", color="Emissões no período", color_continuous_scale=["#cfe3da", PALETTE[0]])
    figure.update_layout(height=370, margin=dict(l=0, r=0, t=20, b=0), xaxis_title="tCO₂e", yaxis_title=None, coloraxis_showscale=False)
    st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})

st.markdown('<div class="section-label">Comparação municipal</div>', unsafe_allow_html=True)
comparison_tab, map_tab, data_tab = st.tabs(["Séries selecionadas", "Mapa territorial", "Dados e indicadores"])

with comparison_tab:
    selected_data = filtered[filtered["Município"].isin(selected_municipalities)]
    if selected_data.empty:
        st.info("Selecione pelo menos um município na barra lateral para visualizar as séries.")
    else:
        figure = px.line(selected_data, x="Ano", y="Emissões", color="Município", markers=True, color_discrete_sequence=PALETTE)
        figure.update_layout(height=430, margin=dict(l=0, r=0, t=20, b=0), yaxis_title="tCO₂e", xaxis_title=None, legend_title=None, hovermode="x unified")
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
        st.caption(f"O recorte selecionado soma {format_tonnes(selected_total)} tCO₂e entre {selected_years[0]} e {selected_years[1]}.")

with map_tab:
    map_data = summary[summary["Município"].isin(selected_municipalities)].copy()
    map_data = map_data.dropna(subset=["Latitude", "Longitude"])
    map_data = map_data.merge(period_summary, on="Município", how="left")
    if map_data.empty:
        st.info("Selecione pelo menos um município com coordenadas para visualizar o mapa.")
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
        figure.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_colorbar_title="tCO₂e")
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})

with data_tab:
    view = summary[["Município", "Acumulado", "Variação no período", "População 2022", "IDHM 2010", "PIB per capita 2023"]].copy()
    view = view.sort_values("Acumulado", ascending=False)
    view.columns = ["Município", "Acumulado (tCO₂e)", "Variação 2010–2024 (%)", "População 2022", "IDHM 2010", "PIB per capita 2023 (R$)"]
    st.dataframe(
        view.style.format({"Acumulado (tCO₂e)": "{:,.0f}", "Variação 2010–2024 (%)": "{:.1f}", "População 2022": "{:,.0f}", "IDHM 2010": "{:.3f}", "PIB per capita 2023 (R$)": "R$ {:,.2f}"}),
        width="stretch",
        hide_index=True,
    )
    csv = view.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Baixar tabela CSV", csv, "apermc-indicadores.csv", "text/csv")

st.divider()
st.caption(f"Dados exibidos: {min(YEARS)}–{max(YEARS)} · menor ano agregado no recorte: {int(period_low)} · atualização manual disponível na barra lateral")
