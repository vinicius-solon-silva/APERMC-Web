"""Streamlit entry point for the public APERMC-Web research portal."""

import streamlit as st

from portal import render_footer, render_header

st.set_page_config(
    page_title="APERMC-Web | Energia e clima",
    page_icon="◒",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = [
    st.Page("pages/about.py", title="Sobre a pesquisa", icon=":material/article:"),
    st.Page("pages/dashboard.py", title="Dados e dashboards", icon=":material/monitoring:"),
    st.Page("pages/documents.py", title="Documentos", icon=":material/folder_open:"),
    st.Page("pages/gallery.py", title="Galeria de eventos", icon=":material/photo_library:"),
    st.Page("pages/profile.py", title="Perfil e contato", icon=":material/person:"),
]

page = st.navigation({"APERMC-Web": pages}, position="sidebar")
render_header()
page.run()
render_footer()
