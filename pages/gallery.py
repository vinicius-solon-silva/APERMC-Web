"""Public gallery of academic events."""

import streamlit as st

from portal import ASSET_DIRECTORIES, ensure_asset_directories

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

ensure_asset_directories()
st.title("Galeria de eventos")
st.write("Registros de participação em eventos acadêmicos, simpósios e congressos.")

photos = sorted(
    path
    for path in ASSET_DIRECTORIES["events"].iterdir()
    if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
)
if not photos:
    st.info("As fotos públicas de eventos serão exibidas aqui quando forem disponibilizadas.")
else:
    columns = st.columns(3)
    for index, photo in enumerate(photos):
        with columns[index % len(columns)]:
            st.image(str(photo), caption=photo.stem.replace("_", " "), width="stretch")
