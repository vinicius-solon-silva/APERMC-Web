"""Public presentation of the APERMC-Web research project."""

import streamlit as st

st.title("Sobre a pesquisa")
st.write(
    "Análise das políticas de governança energética na mitigação e/ou adaptação às mudanças "
    "climáticas pelos municípios da Região Metropolitana de Campinas."
)

summary_tab, abstract_tab = st.tabs(["Resumo", "Abstract"])
with summary_tab:
    st.subheader("Resumo")
    st.write(
        "A pesquisa aborda a governança energética municipal e sua relação com a mitigação e a "
        "adaptação às mudanças climáticas na Região Metropolitana de Campinas. O portal apresenta "
        "uma visão pública das emissões associadas ao setor energético e indicadores municipais "
        "de fontes públicas."
    )

with abstract_tab:
    st.subheader("Abstract")
    st.write(
        "This research examines municipal energy governance and its relationship to climate "
        "change mitigation and adaptation in the Campinas Metropolitan Region. The portal presents "
        "a public view of energy-sector emissions and municipal indicators from public sources."
    )

st.subheader("Objetivos e justificativa")
st.write(
    "Investigar políticas de governança energética dos municípios da RMC e sua contribuição "
    "potencial para enfrentar as mudanças climáticas. A análise municipal permite contextualizar "
    "as emissões do setor de energia e apoiar a discussão sobre políticas públicas locais."
)

st.subheader("Metodologia de pesquisa")
st.write(
    "O dashboard organiza séries anuais de emissões do setor de energia e indicadores municipais "
    "públicos para comparação descritiva. A versão pública não apresenta dados brutos nem resultados "
    "de questionários ou entrevistas. A descrição metodológica detalhada deve seguir o texto final "
    "validado pela pesquisadora e as normas de citação da ABNT."
)

st.info(
    "Acesso público em formato de portfólio somente para leitura. Nenhum diário de bordo é publicado."
)
