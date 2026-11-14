"""
Script de Purificação Histórica Escopo 80s/90s:
Remoção de Nós Contemporâneos do Século XXI (Phoebe Bridgers, boygenius, Julien Baker, Lucy Dacus, Big Thief, etc.)
e Limpeza de Vértices Isolados para Garantir 100% de Alinhamento com o Recorte Temporal do Trabalho Acadêmico.
"""
import json

def prune_21st_century_nodes():
    dataset_path = "data/rock_collaborations_multi_genre.json"
    print(f"[🔍] Lendo dataset {dataset_path} para purificação de escopo temporal...")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # Lista de IDs de nós do Século XXI fora do escopo do Rock 80s/90s
    nodes_to_remove = {
        "Phoebe_Bridgers",
        "Better_Oblivion_Community_Center",
        "boygenius",
        "Julien_Baker",
        "Lucy_Dacus",
        "Big_Thief",
        "Big_Red_Machine",
        "Bleachers",
        "DARK"
    }

    # Filtrar nós
    filtered_nodes = [n for n in nodes if n["id"] not in nodes_to_remove]
    removed_nodes_count = len(nodes) - len(filtered_nodes)

    # Filtrar arestas conectadas a nós removidos
    filtered_edges = [e for e in edges if e["source"] not in nodes_to_remove and e["target"] not in nodes_to_remove]
    removed_edges_count = len(edges) - len(filtered_edges)

    # Identificar e remover eventuais nós isolados (grau 0) resultantes da poda
    deg = {n["id"]: 0 for n in filtered_nodes}
    for e in filtered_edges:
        if e["source"] in deg: deg[e["source"]] += 1
        if e["target"] in deg: deg[e["target"]] += 1

    isolated_ids = {nid for nid, d in deg.items() if d == 0}
    if isolated_ids:
        print(f"[🗑️] Removendo {len(isolated_ids)} nós isolados de grau 0: {isolated_ids}")
        filtered_nodes = [n for n in filtered_nodes if n["id"] not in isolated_ids]
        filtered_edges = [e for e in filtered_edges if e["source"] not in isolated_ids and e["target"] not in isolated_ids]

    data["nodes"] = filtered_nodes
    data["edges"] = filtered_edges
    data["metadata"]["total_nodes"] = len(filtered_nodes)
    data["metadata"]["total_edges"] = len(filtered_edges)

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Purificação Temporal Concluída:")
    print(f"    - Nós do Século XXI removidos: {removed_nodes_count} (ex: Phoebe Bridgers, boygenius, Julien Baker)")
    print(f"    - Arestas obsoletas removidas: {removed_edges_count}")
    print(f"    - Vértices Isolados purificados: {len(isolated_ids)}")
    print(f"    - Grafo Sanitizado Final: {len(filtered_nodes)} nós e {len(filtered_edges)} arestas.")

if __name__ == "__main__":
    prune_21st_century_nodes()
