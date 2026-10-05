"""
Módulo de Enriquecimento Automático de Grafo via API da MusicBrainz.
Permite consultar qualquer artista ou banda no banco global da MusicBrainz e injetar
automaticamente todas as suas colaborações e participações reais no dataset do projeto.
"""
import time
import musicbrainzngs
from src.analysis.graph_builder import load_dataset

musicbrainzngs.set_useragent(
    "AnaliseRedesRockAcademico",
    "2.0",
    "contato@analise-redes-rock.org"
)


def enrich_artist_connections(artist_name, dataset_path="data/rock_collaborations_multi_genre.json"):
    """
    Busca um artista na API da MusicBrainz e injeta seus relacionamentos no dataset local.

    Parâmetros:
    -----------
    artist_name : str
        Nome do artista ou banda a enriquecer (ex: 'Kim Deal', 'Robert Pollard', 'Guided by Voices').
    dataset_path : str
        Caminho do arquivo JSON do dataset local.

    Retorna:
    --------
    dict com contagem de novas arestas e nós adicionados.
    """
    print(f"[*] Buscando relacionamentos oficiais na MusicBrainz para: '{artist_name}'...")
    data = load_dataset(dataset_path)

    existing_node_ids = {n["id"]: n for n in data["nodes"]}
    existing_edges = {(e["source"], e["target"]) for e in data["edges"]}
    existing_edges.update({(e["target"], e["source"]) for e in data["edges"]})

    try:
        search_res = musicbrainzngs.search_artists(artist=artist_name, limit=1)
        artist_list = search_res.get("artist-list", [])
        if not artist_list:
            print(f"[!] Artista '{artist_name}' não encontrado na MusicBrainz.")
            return {"new_nodes": 0, "new_edges": 0}

        target_artist = artist_list[0]
        mbid = target_artist["id"]
        mb_name = target_artist["name"]

        time.sleep(1.0)
        details = musicbrainzngs.get_artist_by_id(mbid, includes=["artist-rels", "recording-rels", "release-group-rels"])
        rels = details.get("artist", {}).get("artist-relation-list", [])

        new_nodes_count = 0
        new_edges_count = 0

        # Garantir que o nó principal exista
        main_node_id = mb_name.replace(" ", "_")
        if main_node_id not in existing_node_ids:
            data["nodes"].append({
                "id": main_node_id,
                "name": mb_name,
                "type": "band" if target_artist.get("type", "").lower() == "group" else "person",
                "genre": "Indie Rock",
                "country": target_artist.get("country", "")
            })
            existing_node_ids[main_node_id] = data["nodes"][-1]
            new_nodes_count += 1

        for r in rels:
            rel_type = r.get("type", "")
            other_art = r.get("artist", {})
            other_id_raw = other_art.get("name", "")
            other_node_id = other_id_raw.replace(" ", "_")

            if not other_id_raw or other_node_id == main_node_id:
                continue

            # Injetar novo nó se não existir no dataset
            if other_node_id not in existing_node_ids:
                data["nodes"].append({
                    "id": other_node_id,
                    "name": other_id_raw,
                    "type": "band" if other_art.get("type", "").lower() == "group" else "person",
                    "genre": "Indie Rock",
                    "country": other_art.get("country", "")
                })
                existing_node_ids[other_node_id] = data["nodes"][-1]
                new_nodes_count += 1

            # Injetar nova aresta se não existir
            if (main_node_id, other_node_id) not in existing_edges:
                rel_map = {
                    "member of band": ("member", "Integrante de banda / Projeto"),
                    "guest performer": ("guest", "Participação especial / Feat em faixa"),
                    "producer": ("producer", "Produtor de álbum / Engenheiro"),
                    "collaboration": ("collaboration", "Parceria e composição conjunta")
                }
                mapped_type, mapped_desc = rel_map.get(rel_type, ("collaboration", f"Relacionamento oficial MusicBrainz ({rel_type})"))

                data["edges"].append({
                    "source": main_node_id,
                    "target": other_node_id,
                    "weight_count": 2,
                    "relation_type": mapped_type,
                    "relation_desc": mapped_desc,
                    "critic_score": 88,
                    "works": [rel_type.title()]
                })
                existing_edges.add((main_node_id, other_node_id))
                existing_edges.add((other_node_id, main_node_id))
                new_edges_count += 1

        # Salvar dataset enriquecido
        import json
        with open(dataset_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[✓] Enriquecimento concluído: +{new_nodes_count} nós e +{new_edges_count} arestas reais adicionadas!")
        return {"new_nodes": new_nodes_count, "new_edges": new_edges_count}

    except Exception as e:
        print(f"[!] Erro ao enriquecer via MusicBrainz: {e}")
        return {"new_nodes": 0, "new_edges": 0}
