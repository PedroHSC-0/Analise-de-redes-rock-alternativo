"""
Módulo para exportar grafos, métricas, comunidades e backbones para JSON consumível pela Web UI.
"""
import json
import networkx as nx
from src.analysis.graph_builder import build_graph, load_dataset
from src.analysis.backbone import disparity_filter, maximum_spanning_tree, edge_betweenness_bridges
from src.analysis.metrics import compute_global_metrics, compute_node_centralities, fit_power_law
from src.analysis.communities import detect_communities


def export_graph_data(G, backbone_type="full", p_cutoff=0.05, top_percentile=0.2):
    """
    Exporta um grafo NetworkX e suas métricas para o formato JSON do dashboard web.
    """
    if backbone_type == "disparity":
        graph_active = disparity_filter(G, p_cutoff=p_cutoff)
    elif backbone_type == "mst":
        graph_active = maximum_spanning_tree(G)
    elif backbone_type == "bridges":
        graph_active = edge_betweenness_bridges(G, top_percentile=top_percentile)
    else:
        graph_active = G.copy()

    global_metrics = compute_global_metrics(graph_active)
    centralities = compute_node_centralities(graph_active)
    comm_map, mod_score = detect_communities(graph_active)
    power_law_stats = fit_power_law(graph_active)
    global_metrics["modularity"] = mod_score

    nodes_out = []
    for n_id, attrs in graph_active.nodes(data=True):
        cents = centralities.get(n_id, {})
        nodes_out.append({
            "id": n_id,
            "label": attrs.get("name", n_id),
            "type": attrs.get("type", "person"),
            "genre": attrs.get("genre", "Unknown"),
            "type_role": attrs.get("type_role", "artist"),
            "country": attrs.get("country", ""),
            "community": comm_map.get(n_id, 0),
            "degree": cents.get("degree", 0),
            "strength": cents.get("strength", 0.0),
            "betweenness": cents.get("betweenness", 0.0),
            "closeness": cents.get("closeness", 0.0),
            "eigenvector": cents.get("eigenvector", 0.0),
            "pagerank": cents.get("pagerank", 0.0)
        })

    rel_labels = {
        "member": "integrante",
        "producer": "produtor",
        "guest": "participação",
        "writer": "co-autor",
        "collaboration": "colaboração"
    }

    edges_out = []
    for u, v, attrs in graph_active.edges(data=True):
        rel_type = attrs.get("relation_type", "collaboration")
        edges_out.append({
            "source": u,
            "target": v,
            "weight": round(float(attrs.get("weight", 1.0)), 4),
            "weight_raw": int(attrs.get("weight_raw", 1)),
            "critic_score": int(attrs.get("critic_score", 50)),
            "relation_type": rel_type,
            "relation_label": rel_labels.get(rel_type, rel_type),
            "relation_desc": attrs.get("relation_desc", f"Parceria do tipo {rel_type}"),
            "works": attrs.get("works", [])
        })

    return {
        "backbone_type": backbone_type,
        "global_metrics": global_metrics,
        "power_law": power_law_stats,
        "nodes": nodes_out,
        "edges": edges_out
    }


def generate_web_bundle(json_path, output_json_path, alpha=0.5, genre="All", k_min=1, backbone_type="full"):
    """
    Função helper para carregar dataset, construir grafo e salvar arquivo JSON para o dashboard.
    Garante que lcc_only=False para exportar a totalidade dos nós e gêneros do supergrafo.
    """
    raw_data = load_dataset(json_path)
    G = build_graph(raw_data, genre=genre, alpha=alpha, k_min=k_min, lcc_only=False)

    raw_edge_map = {(e["source"], e["target"]): e.get("relation_desc", "") for e in raw_data.get("edges", [])}
    raw_edge_map.update({(e["target"], e["source"]): e.get("relation_desc", "") for e in raw_data.get("edges", [])})

    for u, v in G.edges():
        G[u][v]["relation_desc"] = raw_edge_map.get((u, v), G[u][v].get("relation_desc", "Parceria de colaboração"))

    bundle = export_graph_data(G, backbone_type=backbone_type)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    print(f"[✓] Bundle JSON exportado com sucesso: {len(bundle['nodes'])} nós e {len(bundle['edges'])} arestas!")
    return bundle
