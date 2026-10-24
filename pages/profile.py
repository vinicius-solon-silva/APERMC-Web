"""Researcher profile and direct academic contact information."""

import streamlit as st

from portal import get_setting

PROFILE_LINKS = {
    "Currículo Lattes": "lattes_url",
    "ORCID": "orcid_url",
    "LinkedIn": "linkedin_url",
}

st.title("Perfil e contato")
st.subheader("Ana Paula Marsarioli")
st.write("Pesquisadora de Iniciação Científica · Projeto APERMC-Web")
st.write("Orientador: Prof. Dr. André Luiz da Conceição")

configured_links = [(label, get_setting(setting)) for label, setting in PROFILE_LINKS.items()]
for label, url in configured_links:
    if url:
        st.link_button(label, url)

if not any(url for _, url in configured_links):
    st.caption("Links acadêmicos serão exibidos após o cadastro dos endereços oficiais.")

st.subheader("Contato acadêmico")
academic_email = get_setting("academic_email")
if academic_email:
    st.markdown(f"E-mail: [{academic_email}](mailto:{academic_email})")
else:
    st.caption("O e-mail acadêmico será exibido após sua configuração.")
