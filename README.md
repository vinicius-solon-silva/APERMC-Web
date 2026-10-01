# APERMC-Web

Painel Streamlit para explorar as emissões de gases de efeito estufa associadas ao setor energético dos municípios da Região Metropolitana de Campinas (RMC), no contexto da pesquisa **Análise das políticas de governança energética na mitigação e/ou adaptação às mudanças climáticas pelos municípios da RMC**.

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


A aplicação consulta as abas públicas de emissões e indicadores IBGE da planilha em tempo de execução. As coordenadas de referência dos municípios, consultadas via Photon com dados do OpenStreetMap, são mantidas na aplicação, independentemente das abas auxiliares da planilha. Os dados consultados ficam em cache por uma hora; o botão **Atualizar dados** limpa o cache e consulta a planilha novamente.

## Visões disponíveis

- evolução anual agregada e ranking do período;
- séries comparativas por município;
- mapa territorial com emissões no recorte;
- tabela com acumulado, variação, população, IDHM e PIB per capita;
- download da tabela filtrada em CSV.

Fonte de dados: [planilha APERMC](https://docs.google.com/spreadsheets/d/1vVuBkpo29YjDjNR5Pn_xFLwS52yiGri46ZPOCSTkRTA/edit?usp=sharing).
