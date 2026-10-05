"""
Módulo para extração de Backbone e Poda Topológica Estrutural:
- Filtro de Disparidade (Disparity Filter - Serrano et al. 2009)
- Árvore Geradora Máxima (Maximum Spanning Tree - MST)
- Arestas-Ponte por Centralidade de Intermediação de Aresta (Edge Betweenness Centrality)
"""
import networkx as nx
import numpy as np


def disparity_filter(G, p_cutoff=0.05):
    """
    Aplica o Filtro de Disparidade (Disparity Filter - Serrano et al. 2009)
    para extrair a espinha dorsal (backbone) estatisticamente significante de uma rede ponderada.

    Parâmetros:
    -----------
    G : nx.Graph
        Grafo ponderado de entrada.
    p_cutoff : float (0.0 a 1.0)
        Nível de significância (p-value threshold). Arestas com p-value < p_cutoff são mantidas.

    Retorna:
    --------
    nx.Graph
        Subgrafo mantendo apenas as arestas do backbone e os nós conectados.
    """
    if len(G) == 0:
        return nx.Graph()

    B = G.copy()
    edges_to_keep = set()

    for u in G.nodes():
        k = G.degree(u)
        if k <= 1:
            # Se o nó só tem 1 conexão, a aresta é sempre significante no nível local do nó
            for v in G.neighbors(u):
                edges_to_keep.add(tuple(sorted((u, v))))
            continue

        # Força (s_u) = soma dos pesos das arestas conectadas a u
        strength_u = sum(G[u][v].get("weight", 1.0) for v in G.neighbors(u))
        if strength_u == 0:
            continue

        for v in G.neighbors(u):
            w = G[u][v].get("weight", 1.0)
            p_ij = w / strength_u
            # Fórmula de Serrano et al.: alpha_ij = (1 - p_ij)^(k - 1)
            alpha_ij = (1.0 - p_ij) ** (k - 1)

            if alpha_ij < p_cutoff:
                edges_to_keep.add(tuple(sorted((u, v))))

    # Remover arestas que não atingiram a significância estatística em nenhuma das pontas
    all_edges = list(B.edges())
    for u, v in all_edges:
        if tuple(sorted((u, v))) not in edges_to_keep:
            B.remove_edge(u, v)

    # Remover nós isolados que ficaram sem arestas após a poda
    isolated = [n for n in B.nodes() if B.degree(n) == 0]
    B.remove_nodes_from(isolated)

    return B


def maximum_spanning_tree(G):
    """
    Calcula a Árvore Geradora Máxima (Maximum Spanning Tree - MST).
    Poda o grafo mantendo a árvore conectada de maior peso possível sem ciclos (contendo N-1 arestas).

    Retorna:
    --------
    nx.Graph
        Grafo em estrutura de árvore.
    """
    if len(G) == 0:
        return nx.Graph()

    # NetworkX fornece maximum_spanning_tree via algoritmo de Kruskal
    mst = nx.maximum_spanning_tree(G, weight="weight")
    return mst


def edge_betweenness_bridges(G, top_percentile=0.2):
    """
    Identifica e extrai o subgrafo formado pelas Arestas-Ponte (High Edge Betweenness Centrality),
    revelando quais conexões são gargalos críticos que unem diferentes partes do grafo.

    Parâmetros:
    -----------
    G : nx.Graph
    top_percentile : float (0.0 a 1.0)
        Fração das arestas de maior intermediação a manter (ex: top 20%).

    Retorna:
    --------
    nx.Graph
        Subgrafo com as arestas ponte mais importantes.
    """
    if len(G) == 0 or G.number_of_edges() == 0:
        return nx.Graph()

    # Calcular Edge Betweenness Centrality
    ebc = nx.edge_betweenness_centrality(G, weight="weight")
    sorted_edges = sorted(ebc.items(), key=lambda x: x[1], reverse=True)

    num_to_keep = max(1, int(len(sorted_edges) * top_percentile))
    top_edges = set(e[0] for e in sorted_edges[:num_to_keep])

    B = nx.Graph()
    for n, data in G.nodes(data=True):
        B.add_node(n, **data)

    for u, v in top_edges:
        B.add_edge(u, v, **G[u][v])

    # Inserir atributos de edge_betweenness em todas as arestas do grafo original para exportação
    for (u, v), val in ebc.items():
        G[u][v]["edge_betweenness"] = float(val)

    isolated = [n for n in B.nodes() if B.degree(n) == 0]
    B.remove_nodes_from(isolated)

    return B
