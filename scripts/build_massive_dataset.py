"""
Script de Construção de Dataset Massivo de Grafos de Colaboração.
Percorre a lista de artistas do projeto e expande a rede via API REST da MusicBrainz,
capturando centenas de arestas de integrantes, feats, produção e co-autoria.
"""
import sys
import os
import time
import json
import musicbrainzngs

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.analysis.graph_builder import load_dataset

musicbrainzngs.set_useragent(
    "AnaliseRedesRockAcademico",
    "3.0",
    "contato@analise-redes-rock.org"
)


def expand_massive_dataset(dataset_path="data/rock_collaborations_multi_genre.json", max_artists_to_query=40):
    """
    Realiza a varredura em massa para multiplicar exponencialmente o número de arestas no dataset.
    """
    print("=================================================================")
    print("🚀 INICIANDO ENRIQUECIMENTO MASSIVO DE ARESTAS VIA MUSICBRAINZ")
    print("=================================================================")

    data = load_dataset(dataset_path)

    node_dict = {n["id"]: n for n in data["nodes"]}
    existing_edges = {(e["source"], e["target"]) for e in data["edges"]}
    existing_edges.update({(e["target"], e["source"]) for e in data["edges"]})

    artist_nodes = [n for n in data["nodes"] if n.get("type") == "person"]
    query_target_nodes = artist_nodes[:max_artists_to_query]

    added_edges_count = 0
    added_nodes_count = 0

    rel_type_map = {
        "member of band": ("member", "Integrante de Banda / Projeto Oficial"),
        "guest performer": ("guest", "Participação Especial em Gravação (Feat)"),
        "producer": ("producer", "Produtor Musical / Engenheiro de Som"),
        "writer": ("writer", "Co-autor de Letra / Composição Musical"),
        "collaboration": ("collaboration", "Colaboração Artística Oficial")
    }

    for idx, artist in enumerate(query_target_nodes):
        art_id = artist["id"]
        art_name = artist["name"]
        print(f"[{idx+1}/{len(query_target_nodes)}] Consultando MusicBrainz para: {art_name}...")

        try:
            search_res = musicbrainzngs.search_artists(artist=art_name, limit=1)
            artist_list = search_res.get("artist-list", [])
            if not artist_list:
                continue

            mbid = artist_list[0]["id"]
            time.sleep(0.8)

            details = musicbrainzngs.get_artist_by_id(mbid, includes=["artist-rels", "recording-rels"])
            rels = details.get("artist", {}).get("artist-relation-list", [])

            for r in rels:
                rel_type = r.get("type", "")
                target_art = r.get("artist", {})
                target_name = target_art.get("name", "")
                if not target_name:
                    continue

                target_node_id = target_name.replace(" ", "_")

                if target_node_id == art_id:
                    continue

                # Adicionar nó se não existir
                if target_node_id not in node_dict:
                    t_type = "band" if target_art.get("type", "").lower() == "group" else "person"
                    new_node = {
                        "id": target_node_id,
                        "name": target_name,
                        "type": t_type,
                        "genre": artist.get("genre", "Indie Rock"),
                        "country": target_art.get("country", "")
                    }
                    data["nodes"].append(new_node)
                    node_dict[target_node_id] = new_node
                    added_nodes_count += 1

                # Adicionar aresta se não existir
                if (art_id, target_node_id) not in existing_edges:
                    mapped_rel, mapped_desc = rel_type_map.get(rel_type, ("collaboration", f"Colaboração MusicBrainz ({rel_type})"))
                    
                    data["edges"].append({
                        "source": art_id,
                        "target": target_node_id,
                        "weight_count": 2,
                        "relation_type": mapped_rel,
                        "relation_label": mapped_rel,
                        "relation_desc": mapped_desc,
                        "critic_score": 88,
                        "works": [rel_type.title()]
                    })
                    existing_edges.add((art_id, target_node_id))
                    existing_edges.add((target_node_id, art_id))
                    added_edges_count += 1

        except Exception as err:
            print(f"[!] Erro ao processar {art_name}: {err}")
            continue

    # Salvar dataset massivo
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n================================================Scope=================")
    print(f"🎉 VARREDURA MASSIVA CONCLUÍDA!")
    print(f"➕ Novos Nós Adicionados: {added_nodes_count}")
    print(f"➕ Novas Arestas Adicionadas: {added_edges_count}")
    print(f"📊 Total Atual no Dataset: {len(data['nodes'])} Nós e {len(data['edges'])} Arestas!")
    print("=================================================================")


if __name__ == "__main__":
    expand_massive_dataset()
