"""Download repository for public research documents."""

import streamlit as st

from portal import ASSET_DIRECTORIES, ensure_asset_directories

DOCUMENT_GROUPS = {
    "Pôsteres e banners": "posters",
    "Artigos publicados": "articles",
    "Slides de apresentações": "slides",
}
DOCUMENT_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".ppt", ".pptx"}
DOCUMENT_MIME_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def _render_document_group(title: str, key: str) -> None:
    """Show downloads and safe image previews for one document category."""
    st.subheader(title)
    directory = ASSET_DIRECTORIES[key]
    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in DOCUMENT_EXTENSIONS
    )
    if not files:
        st.caption(
            f"Nenhum arquivo público disponível. Adicione materiais em "
            f"`{directory.relative_to(directory.parents[2])}`."
        )
        return

    for path in files:
        with st.container(border=True):
            st.markdown(f"**{path.stem.replace('_', ' ')}**")
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                st.image(str(path), width="stretch")
            st.download_button(
                "Baixar arquivo",
                data=path.read_bytes(),
                file_name=path.name,
                mime=DOCUMENT_MIME_TYPES[path.suffix.lower()],
                key=f"download-{key}-{path.name}",
            )


ensure_asset_directories()
st.title("Repositório de documentos")
st.write("Materiais públicos da pesquisa organizados por tipo de publicação.")
st.info(
    "Questionários, entrevistas, dados brutos e relatórios relacionados não são publicados aqui."
)

for group_title, folder_key in DOCUMENT_GROUPS.items():
    _render_document_group(group_title, folder_key)
