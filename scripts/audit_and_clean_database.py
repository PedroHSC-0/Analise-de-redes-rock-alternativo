"""
Script de Auditoria, Limpeza e Normalização Estrutural do Banco de Dados.
Garante integridade referencial 100%, remove arestas órfãs/duplicadas e prepara o banco para futuras expansões massivas.
"""
import json
import os

def audit_and_clean_database(dataset_path="data/rock_collaborations_multi_genre.json"):
    print(f"[🔍] Iniciando auditoria em {dataset_path}...")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # 1. Normalizar e indexar Nós
    node_map = {}
    cleaned_nodes = []
    
    for n in nodes:
        nid = n.get("id", "").strip()
        if not nid:
            continue
            
        name = n.get("name", nid.replace("_", " ")).strip()
        ntype = n.get("type", "person").strip().lower()
        if ntype not in ["person", "band"]:
            ntype = "person"
            
        genre = n.get("genre", "Alternative Rock").strip()
        type_role = n.get("type_role", "producer" if "producer" in n.get("type_role", "") or "Produtor" in name else "artist")
        country = n.get("country", "USA").strip()
        
        cleaned_node = {
            "id": nid,
            "name": name,
            "type": ntype,
            "genre": genre,
            "type_role": type_role,
            "country": country
        }
        if "formed_year" in n and n["formed_year"]:
            cleaned_node["formed_year"] = int(n["formed_year"])

        if nid not in node_map:
            node_map[nid] = cleaned_node
            cleaned_nodes.append(cleaned_node)

    # 2. Identificar nós faltantes referenciados em arestas
    referenced_node_ids = set()
    for e in edges:
        if "source" in e: referenced_node_ids.add(e["source"].strip())
        if "target" in e: referenced_node_ids.add(e["target"].strip())

    missing_node_ids = referenced_node_ids - set(node_map.keys())
    print(f"[!] Nós faltantes identificados em arestas: {len(missing_node_ids)} -> {missing_node_ids}")

    # Injetar definições para nós faltantes conhecidos
    for m_id in missing_node_ids:
        if m_id == "Beck":
            new_n = {"id": "Beck", "name": "Beck", "type": "person", "genre": "Indie Rock", "type_role": "artist", "country": "USA"}
        elif m_id == "Foals":
            new_n = {"id": "Foals", "name": "Foals", "type": "band", "genre": "Indie Rock", "type_role": "artist", "country": "UK", "formed_year": 2005}
        else:
            new_n = {"id": m_id, "name": m_id.replace("_", " "), "type": "person", "genre": "Alternative Rock", "type_role": "artist", "country": "USA"}
        
        node_map[m_id] = new_n
        cleaned_nodes.append(new_n)
        print(f"[+] Nó faltante auto-criado: {new_n['name']} ({m_id})")

    # 3. Normalizar e consolidar Arestas (Remover duplicatas não-direcionadas e órfãos)
    seen_edges = {}
    cleaned_edges = []
    
    valid_rel_types = {"member", "producer", "guest", "writer", "collaboration"}
    rel_labels = {
        "member": "integrante",
        "producer": "produtor",
        "guest": "participação",
        "writer": "co-autor",
        "collaboration": "colaboração"
    }

    for e in edges:
        src = e.get("source", "").strip()
        tgt = e.get("target", "").strip()
        
        # Validar integridade dos ponteiros
        if not src or not tgt or src not in node_map or tgt not in node_map:
            print(f"[⚠️] Aresta órfã descartada: {src} -> {tgt}")
            continue
            
        if src == tgt:
            print(f"[⚠️] Auto-loop descartado: {src}")
            continue
            
        pair_key = tuple(sorted([src, tgt]))
        
        rel_type = e.get("relation_type", "collaboration").strip().lower()
        if rel_type not in valid_rel_types:
            rel_type = "collaboration"
            
        weight_count = int(e.get("weight_count", 1))
        critic_score = int(e.get("critic_score", 75))
        relation_desc = e.get("relation_desc", f"Parceria do tipo {rel_type}").strip()
        works = list(dict.fromkeys(e.get("works", [])))
        
        edge_obj = {
            "source": src,
            "target": tgt,
            "weight_count": weight_count,
            "relation_type": rel_type,
            "relation_label": rel_labels.get(rel_type, rel_type),
            "relation_desc": relation_desc,
            "critic_score": critic_score,
            "works": works
        }

        if pair_key in seen_edges:
            # Consolidar metadados de arestas duplicadas
            prev_e = seen_edges[pair_key]
            prev_e["weight_count"] = max(prev_e["weight_count"], weight_count) + 1
            prev_e["critic_score"] = max(prev_e["critic_score"], critic_score)
            combined_works = list(dict.fromkeys(prev_e["works"] + works))
            prev_e["works"] = combined_works
            print(f"[🔄] Aresta duplicada consolidada: {src} <-> {tgt}")
        else:
            seen_edges[pair_key] = edge_obj
            cleaned_edges.append(edge_obj)

    # 4. Validar conectividade global (Detectar nós isolados)
    degree_count = {n["id"]: 0 for n in cleaned_nodes}
    for e in cleaned_edges:
        degree_count[e["source"]] += 1
        degree_count[e["target"]] += 1
        
    isolated_nodes = [nid for nid, deg in degree_count.items() if deg == 0]
    print(f"[📊] Diagnóstico de Conectividade: {len(isolated_nodes)} nós isolados identificados.")

    # 5. Salvar banco sanitizado
    sanitized_data = {
        "metadata": {
            "total_nodes": len(cleaned_nodes),
            "total_edges": len(cleaned_edges),
            "version": "2.0.0-validated"
        },
        "nodes": cleaned_nodes,
        "edges": cleaned_edges
    }

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(sanitized_data, f, ensure_ascii=False, indent=2)

    print(f"[✅] Banco de dados totalmente sanitizado e validado! Nós: {len(cleaned_nodes)}, Arestas: {len(cleaned_edges)}")
    return sanitized_data

if __name__ == "__main__":
    audit_and_clean_database()
