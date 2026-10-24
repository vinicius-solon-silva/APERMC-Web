"""Researcher profile and direct academic contact information."""

import streamlit as st

from portal import get_setting

PROFILE_LINKS = {
    "Currículo Lattes": "http://lattes.cnpq.br/8699461135793030",
    "LinkedIn": "https://www.linkedin.com/in/ana-paula-marsarioli-2aa6a8131/",
    "ORCID": "orcid_url",
}

st.title("Perfil e contato")
st.subheader("Ana Paula Marsarioli")
st.write("Pesquisadora de Iniciação Científica · Projeto APERMC-Web")
st.write("Orientador: Prof. Dr. André Luiz da Conceição")

for label, setting in PROFILE_LINKS.items():
    url = get_setting(setting) if label == "ORCID" else setting
    if url:
        st.link_button(label, url)

if not get_setting("orcid_url"):
    st.caption("ORCID não informado.")

st.subheader("Contato acadêmico")
academic_email = "apmarsarioli@gmail.com"
st.markdown(f"E-mail: [{academic_email}](mailto:{academic_email})")
