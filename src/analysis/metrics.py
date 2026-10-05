"""
Módulo para cálculo de métricas topológicas de rede, centralidades de nós, teste de Mundo Pequeno (Small-Worldness Index S) e ajuste à Lei de Potência.
"""
import networkx as nx
import numpy as np
from scipy import stats


def compute_global_metrics(G):
    """
    Calcula as estatísticas topológicas globais do grafo, incluindo o Índice de Mundo Pequeno S (Watts-Strogatz).
    """
    if len(G) == 0:
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "density": 0.0,
            "avg_clustering": 0.0,
            "avg_shortest_path": 0.0,
            "diameter": 0,
            "is_connected": False,
            "small_world_index": 0.0,
            "is_small_world": False
        }

    n = G.number_of_nodes()
    m = G.number_of_edges()
    density = float(nx.density(G))
    avg_clustering = float(nx.average_clustering(G, weight="weight"))

    is_conn = nx.is_connected(G)
    
    if is_conn:
        sub_g = G
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        sub_g = G.subgraph(largest_cc)

    n_lcc = sub_g.number_of_nodes()
    if n_lcc > 1:
        avg_path = float(nx.average_shortest_path_length(sub_g))
        diam = int(nx.diameter(sub_g))
        
        # Cálculo do Índice de Mundo Pequeno (Watts-Strogatz S = (C / C_rand) / (L / L_rand))
        k_avg = (2.0 * sub_g.number_of_edges()) / float(n_lcc)
        c_rand = k_avg / float(n_lcc) if n_lcc > 0 else 0.001
        l_rand = np.log(n_lcc) / np.log(k_avg) if k_avg > 1 else 1.0
        
        c_ratio = avg_clustering / c_rand if c_rand > 0 else 1.0
        l_ratio = avg_path / l_rand if l_rand > 0 else 1.0
        small_world_s = c_ratio / l_ratio if l_ratio > 0 else 0.0
    else:
        avg_path = 0.0
        diam = 0
        small_world_s = 0.0

    return {
        "num_nodes": n,
        "num_edges": m,
        "num_lcc_nodes": n_lcc,
        "density": round(density, 4),
        "avg_clustering": round(avg_clustering, 4),
        "avg_shortest_path": round(avg_path, 4),
        "diameter": diam,
        "is_connected": is_conn,
        "small_world_index": round(float(small_world_s), 2),
        "is_small_world": bool(small_world_s > 1.0)
    }


def compute_node_centralities(G):
    if len(G) == 0:
        return {}

    deg = dict(G.degree())
    strength = {n: sum(G[n][nbr].get("weight", 1.0) for nbr in G.neighbors(n)) for n in G.nodes()}

    try:
        bet = nx.betweenness_centrality(G, weight="weight")
    except Exception:
        bet = {n: 0.0 for n in G.nodes()}

    try:
        close = nx.closeness_centrality(G)
    except Exception:
        close = {n: 0.0 for n in G.nodes()}

    try:
        eig = nx.eigenvector_centrality_numpy(G, weight="weight")
    except Exception:
        eig = {n: 0.0 for n in G.nodes()}

    try:
        page = nx.pagerank(G, weight="weight")
    except Exception:
        page = {n: 0.0 for n in G.nodes()}

    centralities = {}
    for n in G.nodes():
        centralities[n] = {
            "degree": int(deg[n]),
            "strength": round(float(strength[n]), 4),
            "betweenness": round(float(bet.get(n, 0.0)), 4),
            "closeness": round(float(close.get(n, 0.0)), 4),
            "eigenvector": round(float(eig.get(n, 0.0)), 4),
            "pagerank": round(float(page.get(n, 0.0)), 4)
        }

    return centralities


def fit_power_law(G):
    degrees = [d for n, d in G.degree() if d > 0]
    if len(degrees) < 3:
        return {"gamma": 0.0, "r_squared": 0.0, "status": "Dados insuficientes"}

    val, counts = np.unique(degrees, return_counts=True)
    probs = counts / float(sum(counts))

    log_k = np.log(val)
    log_p = np.log(probs)

    slope, intercept, r_value, p_value, std_err = stats.linregress(log_k, log_p)

    gamma = -slope
    r_squared = r_value ** 2

    return {
        "gamma": round(float(gamma), 3),
        "r_squared": round(float(r_squared), 4),
        "p_value": float(p_value),
        "is_scale_free": bool(r_squared > 0.6 and gamma > 0)
    }
