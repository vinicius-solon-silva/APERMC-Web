"""Public presentation of the APERMC-Web research project."""

import streamlit as st

st.title("Sobre a pesquisa")
st.markdown(
    "**Análise das políticas de governança energética na mitigação e/ou adaptação às mudanças "
    "climáticas pelos municípios da Região Metropolitana de Campinas (RMC).**"
)
st.caption(
    "Projeto de Iniciação Científica · Ana Paula Marsarioli · Orientador: Prof. Dr. André Luiz da Conceição"
)

summary_tab, abstract_tab = st.tabs(["Resumo", "Abstract"])
with summary_tab:
    st.subheader("Resumo")
    st.write(
        "A pesquisa investiga as relações entre governança energética, ambiental e climática nos "
        "municípios da Região Metropolitana de Campinas. Seu objetivo é mapear e analisar políticas "
        "públicas de mitigação de gases de efeito estufa e de adaptação a eventos climáticos extremos, "
        "identificando diretrizes e avaliando sua efetividade socioambiental. O estudo combina revisão "
        "bibliográfica e documental, análise de políticas e dados de emissões do setor energético, "
        "além de pesquisa de campo prevista com gestores públicos municipais. A análise relaciona o "
        "inventário de emissões à capacidade institucional e aos instrumentos locais de planejamento, "
        "com vistas a contribuir para a transição energética e a resiliência climática regional."
    )

with abstract_tab:
    st.subheader("Abstract")
    st.write(
        "This study investigates the relationship between energy, environmental, and climate "
        "governance in the municipalities of the Campinas Metropolitan Region, Brazil. It aims to map "
        "and analyze public policies for greenhouse gas mitigation and adaptation to extreme climate "
        "events, identifying policy guidelines and assessing their socio-environmental effectiveness. "
        "The research combines bibliographic and documentary review, policy analysis, and energy-sector "
        "emissions data, with fieldwork involving municipal public managers planned in the research "
        "proposal. The analysis connects emissions inventories with institutional capacity and local "
        "planning instruments to inform regional energy transition and climate resilience."
    )

st.subheader("Problema e justificativa")
st.write(
    "A região reúne contextos distintos de emissões e infraestrutura: a atividade de refino em "
    "Paulínia e as emissões associadas à mobilidade e à expansão urbana em Campinas e em outros "
    "municípios. Essa diversidade torna relevante compreender como políticas e capacidades públicas "
    "locais se articulam para enfrentar as mudanças climáticas. O projeto parte da questão de como os "
    "municípios da RMC incorporam mitigação, adaptação e transição energética em suas políticas e "
    "instrumentos de planejamento."
)

st.subheader("Objetivos")
st.markdown(
    "- Mapear políticas públicas, marcos regulatórios, programas e instrumentos municipais de "
    "planejamento relacionados a energia, ambiente e clima.\n"
    "- Diagnosticar emissões de gases de efeito estufa vinculadas ao setor energético regional, "
    "com foco inicial em Paulínia, Campinas e Sumaré.\n"
    "- Relacionar o perfil de emissões à capacidade institucional e à infraestrutura municipal para "
    "descarbonização, adaptação e resiliência.\n"
    "- Avaliar a articulação entre políticas locais e governança regional, identificando caminhos "
    "para fortalecer a transição energética na RMC."
)

st.subheader("Metodologia de pesquisa")
st.write(
    "O projeto classifica a pesquisa como aplicada e explicativa, com abordagem quali-quantitativa "
    "(métodos mistos). A etapa bibliográfica e documental examina literatura, legislação, programas "
    "e instrumentos de planejamento. A vertente quantitativa prevê tabulação e tratamento estatístico "
    "de inventários públicos de emissões; a qualitativa busca contextualizar a implementação e os "
    "desafios institucionais das políticas. A integração das duas vertentes subsidia uma análise "
    "explicativa da relação entre emissões e governança."
)

with st.expander("Dimensões de governança consideradas"):
    st.markdown(
        "- Estrutura administrativa e responsabilidades por energia e clima.\n"
        "- Metas de descarbonização e marcos regulatórios climáticos.\n"
        "- Articulação intersetorial e participação na governança metropolitana.\n"
        "- Diretrizes de eficiência energética e fontes renováveis no planejamento urbano.\n"
        "- Previsão orçamentária, mecanismos financeiros e incentivos fiscais.\n"
        "- Mobilidade sustentável e transição de frotas públicas."
    )

st.subheader("Fontes e análise")
st.write(
    "O projeto prevê consulta a bases e publicações de órgãos como SEEG, EPE, SEADE, IBGE, "
    "Ministérios do Meio Ambiente e de Minas e Energia, ANEEL, IEMA, AdaptaBrasil MCTI e IEA. "
    "As emissões e os indicadores públicos são analisados em conjunto com os instrumentos de "
    "governança e planejamento identificados. Citações e referências bibliográficas seguem as normas "
    "ABNT, observadas as regras específicas de publicações internacionais."
)

st.warning(
    "O documento prevê pesquisa de campo com gestores e submissão do protocolo ao Comitê de Ética "
    "em Pesquisa. Em cumprimento às regras de divulgação do portal, respostas, transcrições, dados "
    "brutos e resultados de questionários ou entrevistas não são exibidos."
)
