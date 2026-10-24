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

- Logos institucionais: arquivos `fapesp.png`, `cps.png` e `fatec_campinas.png` em `assets/logos/` (formatos PNG, JPG, JPEG ou WebP).
- Pôsteres e banners: `assets/documents/posters/`.
- Artigos: `assets/documents/articles/`.
- Slides: `assets/documents/slides/`.
- Fotos de eventos: `assets/events/` (PNG, JPG, JPEG ou WebP).
- Configure `LATTES_URL`, `ORCID_URL`, `LINKEDIN_URL` e `ACADEMIC_EMAIL` como variáveis de ambiente ou chaves equivalentes em `.streamlit/secrets.toml`.

O portal exibe os nomes institucionais como fallback até que as logos oficiais sejam adicionadas. Links acadêmicos e e-mail não são inventados e permanecem ocultos enquanto não forem configurados.

## Citação

No Brasil, utilize as normas ABNT. Para publicações externas/internacionais, verifique as regras da revista. O rodapé do portal contém a nota de agradecimento exigida pela FAPESP.

Fonte de dados: [planilha APERMC](https://docs.google.com/spreadsheets/d/1vVuBkpo29YjDjNR5Pn_xFLwS52yiGri46ZPOCSTkRTA/edit?usp=sharing).
