# APERMC-Web

Portal público de iniciação científica de Ana Paula Marsarioli, orientada pelo Prof. Dr. André Luiz da Conceição. A pesquisa analisa políticas de governança energética na mitigação e/ou adaptação às mudanças climáticas nos municípios da Região Metropolitana de Campinas (RMC). O dashboard apresenta somente dados públicos relacionados ao setor de energia.

## Executar localmente

### Via streamlit cli
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Via docker cli
```bash
docker build -t apermc-web .
docker run --rm -p 8501:8501 apermc-web
```

Acesse a aplicação em <http://localhost:8501>.


O portal usa navegação multipágina: apresentação da pesquisa, dashboard, repositório de documentos, galeria de eventos e perfil/contato. Não publica questionários, entrevistas, dados brutos desses instrumentos nem diário de bordo.

O dashboard consulta as abas públicas de emissões e indicadores IBGE da planilha em tempo de execução. As coordenadas de referência dos municípios são mantidas na aplicação. Os dados consultados ficam em cache por uma hora; o botão de atualização limpa o cache e consulta a planilha novamente.

## Materiais e configuração

- Logos institucionais: `assets/logos/fapesp_logo.png`, `assets/logos/cps_logo.png` e `assets/logos/fatec-campinas_logo.png`.
- Pôsteres e banners: `assets/documents/posters/`.
- Artigos: `assets/documents/articles/`.
- Slides: `assets/documents/slides/`.
- Fotos de eventos: `assets/events/` (PNG, JPG, JPEG ou WebP).
- Os links do Currículo Lattes e LinkedIn e o e-mail profissional da pesquisadora estão cadastrados na página Perfil e contato. Configure `ORCID_URL` como variável de ambiente ou chave equivalente em `.streamlit/secrets.toml` caso queira exibir o ORCID.

Os nomes das instituições são exibidos em linhas próprias com links para seus sites oficiais.

## Citação

No Brasil, utilize as normas ABNT. Para publicações externas/internacionais, verifique as regras da revista. O rodapé do portal contém a nota de agradecimento exigida pela FAPESP.

Fonte de dados: [planilha APERMC](https://docs.google.com/spreadsheets/d/1vVuBkpo29YjDjNR5Pn_xFLwS52yiGri46ZPOCSTkRTA/edit?usp=sharing).
