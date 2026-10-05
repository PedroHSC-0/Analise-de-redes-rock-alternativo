"""
Módulo para detecção de comunidades via Algoritmo de Louvain e cálculo de Modularidade Q.
"""
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity


def detect_communities(G):
    """
    Executa a detecção de comunidades no grafo usando o algoritmo guloso de otimização de modularidade (Louvain-like).

    Retorna:
    --------
    community_map : dict[node_id, int]
        Mapeamento de cada nó para o ID numérico da sua comunidade.
    mod_score : float
        Score de Modularidade Q da partição encontrada (-0.5 a 1.0).
    """
    if len(G) == 0 or G.number_of_edges() == 0:
        return {}, 0.0

    try:
        communities = list(greedy_modularity_communities(G, weight="weight"))
        mod_score = float(modularity(G, communities, weight="weight"))
    except Exception:
        communities = [set(G.nodes())]
        mod_score = 0.0

    community_map = {}
    for comm_idx, comm_nodes in enumerate(communities):
        for node in comm_nodes:
            community_map[node] = comm_idx

    return community_map, round(mod_score, 4)
