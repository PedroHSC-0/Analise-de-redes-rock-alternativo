"""
Módulo para construção e pré-processamento (poda de limpeza) de Grafos NetworkX.
"""
import json
import networkx as nx
from src.analysis.hybrid_weight import compute_hybrid_weights


def load_dataset(json_path):
    """
    Carrega o dataset JSON contendo nós e arestas.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_graph(data, genre=None, alpha=0.5, k_min=1, min_edge_weight=0.0, lcc_only=False):
    """
    Constrói um grafo NetworkX ponderado a partir dos dados em dicionário/JSON.

    Parâmetros:
    -----------
    data : dict
        Dicionário contendo chaves 'nodes' e 'edges'.
    genre : str ou None
        Se especificado (ex: 'Grunge', 'Post-Punk'), filtra nós desse gênero ou conectados a ele.
        Se None ou 'All', inclui todos os gêneros.
    alpha : float (0.0 a 1.0)
        Parâmetro do modelo de peso híbrido (Frequência vs. Aclamação Crítica).
    k_min : int
        Grau mínimo de nó para a poda prévia de limpeza (k-core filtering).
    min_edge_weight : float
        Peso mínimo híbrido da aresta para mantê-la no grafo.
    lcc_only : bool
        Se True, extrai apenas o Maior Componente Conexo (Largest Connected Component).
        Default é False para preservar o supergrafo completo com todos os gêneros.

    Retorna:
    --------
    nx.Graph
        Grafo NetworkX ponderado e limpo.
    """
    nodes = data.get("nodes", [])
    raw_edges = data.get("edges", [])

    # Recomputar pesos híbridos com o alpha especificado
    edges = compute_hybrid_weights(raw_edges, alpha=alpha)

    # Dicionário de nós válidos
    node_dict = {n["id"]: n for n in nodes}

    # Filtrar por gênero se especificado
    if genre and genre != "All":
        target_node_ids = {n["id"] for n in nodes if n.get("genre") == genre}
        # Incluir também nós vizinhos diretos para manter conexões inter-gênero
        neighbor_ids = set()
        for e in edges:
            src, tgt = e["source"], e["target"]
            if src in target_node_ids:
                neighbor_ids.add(tgt)
            if tgt in target_node_ids:
                neighbor_ids.add(src)
        valid_node_ids = target_node_ids.union(neighbor_ids)
    else:
        valid_node_ids = set(node_dict.keys())

    G = nx.Graph()

    # Adicionar nós com atributos
    for node_id in valid_node_ids:
        if node_id in node_dict:
            n_data = node_dict[node_id]
            G.add_node(
                node_id,
                name=n_data.get("name", node_id),
                type=n_data.get("type", "person"),
                genre=n_data.get("genre", "Unknown"),
                type_role=n_data.get("type_role", "artist"),
                country=n_data.get("country", "")
            )

    # Adicionar arestas com atributos
    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in G and tgt in G:
            w = e.get("weight_hybrid", 1.0)
            if w >= min_edge_weight:
                G.add_edge(
                    src,
                    tgt,
                    weight=w,
                    weight_raw=e.get("weight_count", 1),
                    critic_score=e.get("critic_score", 50),
                    relation_type=e.get("relation_type", "collaboration"),
                    works=e.get("works", [])
                )

    # Poda Prévia 1: Grau Mínimo (k-core pruning)
    if k_min > 1:
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < k_min]
        G.remove_nodes_from(nodes_to_remove)

    # Poda Prévia 2: Maior Componente Conexo (LCC - apenas se lcc_only=True)
    if lcc_only and len(G) > 0 and not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    return G
