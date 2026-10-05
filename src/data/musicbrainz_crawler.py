"""
Módulo para amostragem Bola de Neve (Snowball Sampling) de colaborações via API da MusicBrainz.
Permite buscar por qualquer tag de gênero musical e extrair o grafo de relacionamentos.
"""
import time
import musicbrainzngs

# Configurar User-Agent exigido pela MusicBrainz
musicbrainzngs.set_useragent(
    "TopologicalRockAnalysis",
    "1.0",
    "contato@analise-redes-rock.org"
)


def crawl_genre_network(genre_tag="alternative rock", max_seed_artists=15, rate_limit_delay=1.0):
    """
    Realiza a varredura e amostragem na API da MusicBrainz para um determinado gênero musical.

    Parâmetros:
    -----------
    genre_tag : str
        Tag de gênero no MusicBrainz (ex: 'alternative rock', 'shoegaze', 'post-punk', 'grunge', 'metal', 'jazz').
    max_seed_artists : int
        Número máximo de artistas semente principais a buscar.
    rate_limit_delay : float
        Tempo de espera em segundos entre requisições (a API requer ~1s por solicitação).

    Retorna:
    --------
    dict com 'nodes' e 'edges' formatados no padrão do projeto.
    """
    print(f"[*] Iniciando varredura MusicBrainz para o gênero: '{genre_tag}'...")

    nodes = []
    edges = []
    visited_artists = set()

    try:
        # Buscar artistas semente associados à tag
        search_res = musicbrainzngs.search_artists(tag=genre_tag, limit=max_seed_artists)
        seed_artists = search_res.get("artist-list", [])
    except Exception as e:
        print(f"[!] Erro ao buscar artistas semente: {e}")
        return {"nodes": [], "edges": []}

    for seed in seed_artists:
        mbid = seed["id"]
        name = seed["name"]
        artist_type = seed.get("type", "Group")

        if mbid in visited_artists:
            continue
        visited_artists.add(mbid)

        node_type = "band" if artist_type.lower() == "group" else "person"
        nodes.append({
            "id": mbid,
            "name": name,
            "type": node_type,
            "genre": genre_tag.title(),
            "country": seed.get("country", "")
        })

        time.sleep(rate_limit_delay)

        # Buscar relacionamentos do artista
        try:
            art_details = musicbrainzngs.get_artist_by_id(
                mbid,
                includes=["artist-rels", "release-group-rels"]
            )
            rel_list = art_details.get("artist", {}).get("artist-relation-list", [])

            for rel in rel_list:
                rel_type = rel.get("type", "")
                target_art = rel.get("artist", {})
                target_id = target_art.get("id")
                target_name = target_art.get("name")

                if not target_id or not target_name:
                    continue

                if target_id not in visited_artists:
                    visited_artists.add(target_id)
                    t_type = "band" if target_art.get("type", "").lower() == "group" else "person"
                    nodes.append({
                        "id": target_id,
                        "name": target_name,
                        "type": t_type,
                        "genre": genre_tag.title(),
                        "country": target_art.get("country", "")
                    })

                # Mapear tipos de relação para o grafo
                rel_map = {
                    "member of band": "member",
                    "guest performer": "guest",
                    "producer": "producer",
                    "collaboration": "collaboration"
                }
                mapped_rel = rel_map.get(rel_type, "collaboration")

                edges.append({
                    "source": mbid,
                    "target": target_id,
                    "weight_count": 1,
                    "relation_type": mapped_rel,
                    "critic_score": 80,  # Score padrão caso não haja fonte de crítica externa vinculada
                    "works": [rel_type]
                })

        except Exception as err:
            print(f"[!] Erro ao obter detalhes do artista {name} ({mbid}): {err}")
            continue

    print(f"[✓] Varredura concluída: {len(nodes)} nós e {len(edges)} arestas capturadas.")
    return {
        "metadata": {
            "title": f"Rede MusicBrainz - {genre_tag.title()}",
            "genre": genre_tag.title()
        },
        "nodes": nodes,
        "edges": edges
    }
