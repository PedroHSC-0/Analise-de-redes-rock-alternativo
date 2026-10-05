# Análise Topológica de Redes no Rock Alternativo

Trabalho acadêmico de análise topológica de grafos e estrutura de colaborações musicais no **Rock Alternativo** e gêneros correlatos (**Grunge, Post-Punk, Shoegaze, Britpop, Industrial/Experimental**).

![Dashboard Preview](web/index.html)

---

## 🎯 Teses Científicas Investigadas

1. **Tese 1: Topologia de Mundo Pequeno (*Small-World*) e Escala Livre (*Scale-Free*)**
   - Investigação do Coeficiente de Agrupamento ($C$), Caminho Médio ($L$) e ajuste da distribuição de graus em Lei de Potência ($P(k) \sim k^{-\gamma}$).
2. **Tese 2: Arestas Predominantes e Pontes Trans-Gênero (*Structural Bridges*)**
   - Poda topológica e extração do *Backbone* via **Filtro de Disparidade (Serrano et al., 2009)**, **Árvore Geradora Máxima (MST)** e **Centralidade de Intermediação de Arestas (*Edge Betweenness*)**.
3. **Tese 3: Divergência entre Volume Bruto vs. Impacto Crítico (Modelo Híbrido)**
   - Ponderação parametrizada de arestas: $W_{\text{híbrido}} = \alpha \cdot \bar{W}_{\text{bruto}} + (1-\alpha) \cdot \bar{Q}_{\text{crítica}}$.

---

## 🚀 Como Executar o Projeto

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar a Suíte de Testes Automatizados
```bash
pytest tests/
```

### 3. Iniciar o Dashboard Web Interativo
```bash
python3 -m http.server 8000 --directory web
```
Abra o navegador em `http://localhost:8000` para explorar o grafo de forças interativo!

### 4. Executar o Coletor/Crawler MusicBrainz (Opcional)
Para buscar qualquer novo gênero musical diretamente da API da MusicBrainz:
```python
from src.data.musicbrainz_crawler import crawl_genre_network
data = crawl_genre_network(genre_tag="shoegaze", max_seed_artists=15)
```

### 5. Executar a Análise Formal no Jupyter Notebook
```bash
jupyter notebook notebooks/analise_topologica_rock_alternativo.ipynb
```

---

## 📁 Estrutura de Arquivos

- `data/rock_collaborations_multi_genre.json`: Dataset inicial cobrindo 6 gêneros e dezenas de bandas/produtores.
- `src/analysis/`: Algoritmos de grafos (Filtro de Disparidade, MST, Edge Betweenness, Métrica Híbrida, Louvain).
- `src/data/musicbrainz_crawler.py`: Coletor via API REST da MusicBrainz.
- `src/exporters/export_json.py`: Exportador de bundles JSON para a Web UI.
- `web/`: Aplicação Web interativa em HTML5/CSS3/Vis.js.
- `notebooks/`: Relatório científico formal em Jupyter Notebook.
- `tests/`: Suíte de testes unitários automatizados com Pytest.
