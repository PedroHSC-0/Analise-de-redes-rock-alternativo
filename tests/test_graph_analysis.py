"""
Suíte de testes unitários automatizados para validação dos algoritmos de grafos e métricas.
"""
import pytest
import networkx as nx
from src.analysis.hybrid_weight import compute_hybrid_weights
from src.analysis.graph_builder import build_graph
from src.analysis.backbone import disparity_filter, maximum_spanning_tree, edge_betweenness_bridges
from src.analysis.metrics import compute_global_metrics, compute_node_centralities, fit_power_law
from src.analysis.communities import detect_communities


@pytest.fixture
def sample_dataset():
    return {
        "nodes": [
            {"id": "A", "name": "Artist A", "type": "person", "genre": "Grunge"},
            {"id": "B", "name": "Artist B", "type": "person", "genre": "Grunge"},
            {"id": "C", "name": "Artist C", "type": "band", "genre": "Alternative Rock"},
            {"id": "D", "name": "Producer D", "type": "person", "genre": "Post-Punk", "type_role": "producer"}
        ],
        "edges": [
            {"source": "A", "target": "B", "weight_count": 5, "critic_score": 90},
            {"source": "A", "target": "C", "weight_count": 2, "critic_score": 70},
            {"source": "B", "target": "C", "weight_count": 1, "critic_score": 60},
            {"source": "C", "target": "D", "weight_count": 8, "critic_score": 95}
        ]
    }


def test_hybrid_weights(sample_dataset):
    edges = sample_dataset["edges"]
    # Testar com alpha = 1.0 (apenas frequência)
    res_alpha_1 = compute_hybrid_weights(edges, alpha=1.0)
    assert len(res_alpha_1) == 4
    assert res_alpha_1[0]["weight_hybrid"] == pytest.approx(0.5714, abs=0.01) or res_alpha_1[3]["weight_hybrid"] == 1.0

    # Testar com alpha = 0.0 (apenas aclamação crítica)
    res_alpha_0 = compute_hybrid_weights(edges, alpha=0.0)
    assert res_alpha_0[0]["weight_hybrid"] == 0.90  # 90 / 100
    assert res_alpha_0[3]["weight_hybrid"] == 0.95  # 95 / 100


def test_build_graph(sample_dataset):
    G = build_graph(sample_dataset, genre="All", alpha=0.5, k_min=1, lcc_only=True)
    assert len(G.nodes()) == 4
    assert len(G.edges()) == 4
    assert nx.is_connected(G)


def test_maximum_spanning_tree(sample_dataset):
    G = build_graph(sample_dataset, alpha=0.5)
    mst = maximum_spanning_tree(G)
    # A MST de um grafo de N nós deve conter N-1 arestas e nenhum ciclo
    assert len(mst.nodes()) == 4
    assert len(mst.edges()) == 3
    assert nx.is_tree(mst)


def test_disparity_filter(sample_dataset):
    G = build_graph(sample_dataset, alpha=0.5)
    disp = disparity_filter(G, p_cutoff=0.99)
    assert len(disp.nodes()) > 0


def test_global_metrics(sample_dataset):
    G = build_graph(sample_dataset, alpha=0.5)
    metrics = compute_global_metrics(G)
    assert metrics["num_nodes"] == 4
    assert metrics["num_edges"] == 4
    assert metrics["is_connected"] is True
    assert metrics["avg_clustering"] >= 0.0


def test_centralities_and_communities(sample_dataset):
    G = build_graph(sample_dataset, alpha=0.5)
    cents = compute_node_centralities(G)
    assert "A" in cents
    assert cents["A"]["degree"] == 2

    comm_map, mod_score = detect_communities(G)
    assert len(comm_map) == 4
    assert -0.5 <= mod_score <= 1.0


def test_database_integrity():
    import json
    with open("data/rock_collaborations_multi_genre.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    node_ids = set(n["id"] for n in nodes)
    assert len(node_ids) == len(nodes), "Existem IDs de nós duplicados no banco de dados!"

    for e in edges:
        assert e["source"] in node_ids, f"Aresta órfã encontrada: source '{e['source']}' não existe!"
        assert e["target"] in node_ids, f"Aresta órfã encontrada: target '{e['target']}' não existe!"
        assert e["source"] != e["target"], f"Auto-loop inválido encontrado: '{e['source']}'"

