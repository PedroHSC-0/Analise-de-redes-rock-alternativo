"""
Script para Enriquecer e Classificar a Cena de The Strokes e o Revival dos Anos 2000 (Garage Rock Revival & Post-Punk Revival).

Organiza rigorosamente:
1. GARAGE ROCK REVIVAL:
   - The Strokes, Julian Casablancas, Albert Hammond Jr, Nick Valensi, Nikolai Fraiture, Fabrizio Moretti, Gordon Raphael.
   - The White Stripes, Jack White, Meg White.
   - The Hives, Howlin' Pelle Almqvist.
   - The Vines, Craig Nicholls.
   - The Libertines, Pete Doherty, Carl Barât, Mick Jones (The Clash / Produtor).
   - The Black Keys, Dan Auerbach, Patrick Carney.
   - Kings of Leon, Caleb Followill.
   - Precursores 80s/90s: The Cramps, The Fuzztones, The Gories, Dead Moon, Jon Spencer Blues Explosion, Thee Headcoats, Billy Childish.

2. POST-PUNK REVIVAL:
   - Interpol, Paul Banks, Daniel Kessler, Sam Fogarino, Carlos D, Peter Katis.
   - Yeah Yeah Yeahs, Karen O, Nick Zinner, Brian Chase.
   - TV on the Radio, Dave Sitek, Tunde Adebimpe.
   - Franz Ferdinand, Alex Kapranos, FFS.
   - Arctic Monkeys, Alex Turner, Matt Helders, James Ford.
   - The Killers, Brandon Flowers.
   - LCD Soundsystem, James Murphy.
   - Editors, Bloc Party, Maxïmo Park.
"""

import json

def run_revival_enrichment():
    dataset_path = "data/rock_collaborations_multi_genre.json"
    print(f"[*] Lendo dataset {dataset_path} para inclusão e classificação do movimento The Strokes e Revival...")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    existing_node_map = {n["id"]: n for n in nodes}
    existing_edges = {(e["source"], e["target"]) for e in edges}
    existing_edges.update({(e["target"], e["source"]) for e in edges})

    # =========================================================================
    # 1. Novas Entidades Históricas da Cena The Strokes & Revival
    # =========================================================================
    new_nodes_to_add = [
        # Integrantes e produtores do The Strokes
        {"id": "Nick_Valensi", "name": "Nick Valensi", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},
        {"id": "Nikolai_Fraiture", "name": "Nikolai Fraiture", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},
        {"id": "Fabrizio_Moretti", "name": "Fabrizio Moretti", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},

        # Cena Garage Rock Revival
        {"id": "Meg_White", "name": "Meg White", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},
        {"id": "The_Hives", "name": "The Hives", "type": "band", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "SE"},
        {"id": "Howlin_Pelle_Almqvist", "name": "Howlin' Pelle Almqvist", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "SE"},
        {"id": "The_Vines", "name": "The Vines", "type": "band", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "AU"},
        {"id": "The_Libertines", "name": "The Libertines", "type": "band", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "UK"},
        {"id": "Pete_Doherty", "name": "Pete Doherty", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "UK"},
        {"id": "Carl_Barât", "name": "Carl Barât", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "UK"},
        {"id": "The_Black_Keys", "name": "The Black Keys", "type": "band", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},
        {"id": "Dan_Auerbach", "name": "Dan Auerbach", "type": "person", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},
        {"id": "Kings_of_Leon", "name": "Kings of Leon", "type": "band", "genre": "Garage Rock Revival", "subgenre": "Garage Rock Revival", "country": "US"},

        # Cena Post-Punk Revival
        {"id": "Daniel_Kessler", "name": "Daniel Kessler", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "US"},
        {"id": "Sam_Fogarino", "name": "Sam Fogarino", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "US"},
        {"id": "Carlos_D", "name": "Carlos D", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "US"},
        {"id": "Peter_Katis", "name": "Peter Katis", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "US"},
        {"id": "Nick_Zinner", "name": "Nick Zinner", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "US"},
        {"id": "Brian_Chase", "name": "Brian Chase", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "US"},
        {"id": "Editors", "name": "Editors", "type": "band", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "UK"},
        {"id": "Bloc_Party", "name": "Bloc Party", "type": "band", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "UK"},
        {"id": "Kele_Okereke", "name": "Kele Okereke", "type": "person", "genre": "Post-Punk Revival", "subgenre": "Post-Punk Revival", "country": "UK"}
    ]

    added_nodes_count = 0
    for nd in new_nodes_to_add:
        if nd["id"] not in existing_node_map:
            nodes.append(nd)
            existing_node_map[nd["id"]] = nd
            added_nodes_count += 1

    print(f"[✓] {added_nodes_count} novos nós da cena The Strokes / Revival adicionados.")

    # =========================================================================
    # 2. Re-classificação Canônica de Gêneros / Subgêneros da Cena Revival
    # =========================================================================
    revival_genre_overrides = {
        # --- GARAGE ROCK REVIVAL ---
        "The_Strokes": "Garage Rock Revival",
        "Julian_Casablancas": "Garage Rock Revival",
        "Albert_Hammond_Jr": "Garage Rock Revival",
        "Nick_Valensi": "Garage Rock Revival",
        "Nikolai_Fraiture": "Garage Rock Revival",
        "Fabrizio_Moretti": "Garage Rock Revival",
        "Gordon_Raphael": "Garage Rock Revival",
        "The_White_Stripes": "Garage Rock Revival",
        "Jack_White": "Garage Rock Revival",
        "Meg_White": "Garage Rock Revival",
        "The_Hives": "Garage Rock Revival",
        "Howlin_Pelle_Almqvist": "Garage Rock Revival",
        "The_Vines": "Garage Rock Revival",
        "The_Libertines": "Garage Rock Revival",
        "Pete_Doherty": "Garage Rock Revival",
        "Carl_Barât": "Garage Rock Revival",
        "The_Black_Keys": "Garage Rock Revival",
        "Dan_Auerbach": "Garage Rock Revival",
        "Kings_of_Leon": "Garage Rock Revival",
        "The_Cramps": "Garage Rock Revival",
        "The_Fuzztones": "Garage Rock Revival",
        "The_Gories": "Garage Rock Revival",
        "Dead_Moon": "Garage Rock Revival",
        "Jon_Spencer_Blues_Explosion": "Garage Rock Revival",
        "Thee_Headcoats": "Garage Rock Revival",
        "Billy_Childish": "Garage Rock Revival",
        "Flat_Duo_Jets": "Garage Rock Revival",
        "The_Chesterfield_Kings": "Garage Rock Revival",

        # --- POST-PUNK REVIVAL ---
        "Interpol": "Post-Punk Revival",
        "Paul_Banks": "Post-Punk Revival",
        "Daniel_Kessler": "Post-Punk Revival",
        "Sam_Fogarino": "Post-Punk Revival",
        "Carlos_D": "Post-Punk Revival",
        "Peter_Katis": "Post-Punk Revival",
        "Yeah_Yeah_Yeahs": "Post-Punk Revival",
        "Karen_O": "Post-Punk Revival",
        "Nick_Zinner": "Post-Punk Revival",
        "Brian_Chase": "Post-Punk Revival",
        "TV_on_the_Radio": "Post-Punk Revival",
        "Dave_Sitek": "Post-Punk Revival",
        "Franz_Ferdinand": "Post-Punk Revival",
        "FFS": "Post-Punk Revival",
        "Arctic_Monkeys": "Post-Punk Revival",
        "Alex_Turner": "Post-Punk Revival",
        "The_Killers": "Post-Punk Revival",
        "LCD_Soundsystem": "Post-Punk Revival",
        "James_Murphy": "Post-Punk Revival",
        "Editors": "Post-Punk Revival",
        "Bloc_Party": "Post-Punk Revival",
        "Kele_Okereke": "Post-Punk Revival"
    }

    reclassified_count = 0
    for node in nodes:
        nid = node["id"]
        if nid in revival_genre_overrides:
            sg = revival_genre_overrides[nid]
            node["genre"] = sg
            node["subgenre"] = sg
            reclassified_count += 1

    print(f"[✓] {reclassified_count} nós re-classificados com precisão em 'Garage Rock Revival' e 'Post-Punk Revival'.")

    # =========================================================================
    # 3. Arestas de Colaboração Histórica e Produção de Estúdio
    # =========================================================================
    new_edges_to_add = [
        # The Strokes & Gordon Raphael
        {"source": "The_Strokes", "target": "Julian_Casablancas", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista e líder do The Strokes", "critic_score": 99, "works": ["Is This It"]},
        {"source": "The_Strokes", "target": "Albert_Hammond_Jr", "weight_count": 5, "relation_type": "member", "relation_desc": "Guitarrista rítmico e compositor", "critic_score": 98, "works": ["Room on Fire"]},
        {"source": "The_Strokes", "target": "Nick_Valensi", "weight_count": 5, "relation_type": "member", "relation_desc": "Guitarrista solo", "critic_score": 98, "works": ["Is This It"]},
        {"source": "The_Strokes", "target": "Nikolai_Fraiture", "weight_count": 5, "relation_type": "member", "relation_desc": "Baixista", "critic_score": 97, "works": ["Is This It"]},
        {"source": "The_Strokes", "target": "Fabrizio_Moretti", "weight_count": 5, "relation_type": "member", "relation_desc": "Baterista", "critic_score": 97, "works": ["Is This It"]},
        {"source": "Gordon_Raphael", "target": "The_Strokes", "weight_count": 4, "relation_type": "producer", "relation_desc": "Produção dos álbuns Is This It e Room on Fire", "critic_score": 99, "works": ["Is This It"]},
        {"source": "Julian_Casablancas", "target": "Regina_Spektor", "weight_count": 3, "relation_type": "guest", "relation_desc": "Dueto na faixa Modern Girls & Old Fashioned Men", "critic_score": 94, "works": ["Modern Girls"]},
        {"source": "Julian_Casablancas", "target": "Queens_of_the_Stone_Age", "weight_count": 2, "relation_type": "guest", "relation_desc": "Participação no álbum Era Vulgaris", "critic_score": 93, "works": ["Sick Sick Sick"]},

        # Garage Rock Revival Peers (White Stripes, Hives, Libertines, Black Keys)
        {"source": "The_White_Stripes", "target": "Meg_White", "weight_count": 5, "relation_type": "member", "relation_desc": "Baterista do duo The White Stripes", "critic_score": 98, "works": ["Elephant"]},
        {"source": "Jack_White", "target": "The_White_Stripes", "weight_count": 5, "relation_type": "member", "relation_desc": "Guitarrista e vocalista principal", "critic_score": 99, "works": ["White Blood Cells"]},
        {"source": "The_Strokes", "target": "The_White_Stripes", "weight_count": 3, "relation_type": "collaboration", "relation_desc": "Pioneiros da revolução Garage Rock Revival de 2001", "critic_score": 97, "works": ["2001 NYC/Detroit Revival"]},
        {"source": "The_Hives", "target": "Howlin_Pelle_Almqvist", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista performático", "critic_score": 95, "works": ["Veni Vidi Vicious"]},
        {"source": "The_Hives", "target": "The_Strokes", "weight_count": 2, "relation_type": "collaboration", "relation_desc": "Turnês conjuntas do Garage Rock Revival", "critic_score": 94, "works": ["US Tour 2002"]},
        {"source": "The_Libertines", "target": "Pete_Doherty", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista e compositor", "critic_score": 96, "works": ["Up the Bracket"]},
        {"source": "The_Libertines", "target": "Carl_Barât", "weight_count": 5, "relation_type": "member", "relation_desc": "Guitarrista e co-vocalista", "critic_score": 96, "works": ["Up the Bracket"]},
        {"source": "The_Libertines", "target": "Mick_Jones", "weight_count": 4, "relation_type": "producer", "relation_desc": "Mick Jones (The Clash) produziu Up the Bracket", "critic_score": 97, "works": ["Up the Bracket"]},
        {"source": "The_Black_Keys", "target": "Dan_Auerbach", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista e guitarrista", "critic_score": 96, "works": ["Brothers"]},
        {"source": "The_Black_Keys", "target": "Danger_Mouse", "weight_count": 4, "relation_type": "producer", "relation_desc": "Produção de Attack & Release e Brothers", "critic_score": 98, "works": ["Brothers"]},
        {"source": "The_Vines", "target": "The_Strokes", "weight_count": 3, "relation_type": "collaboration", "relation_desc": "Trinômio 'The' do Garage Rock Revival (Strokes, Hives, Vines)", "critic_score": 95, "works": ["Highly Evolved Tour 2002"]},
        {"source": "Kings_of_Leon", "target": "The_Strokes", "weight_count": 3, "relation_type": "collaboration", "relation_desc": "Turnês de abertura e cena Garage Rock/Southern Revival", "critic_score": 93, "works": ["US Revival Tour 2003"]},

        # Post-Punk Revival Peers (Interpol, Yeah Yeah Yeahs, TV on the Radio, Franz Ferdinand, Arctic Monkeys)
        {"source": "Interpol", "target": "Paul_Banks", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista e guitarrista", "critic_score": 98, "works": ["Turn On the Bright Lights"]},
        {"source": "Interpol", "target": "Daniel_Kessler", "weight_count": 5, "relation_type": "member", "relation_desc": "Guitarrista e fundador", "critic_score": 97, "works": ["Turn On the Bright Lights"]},
        {"source": "Interpol", "target": "Sam_Fogarino", "weight_count": 5, "relation_type": "member", "relation_desc": "Baterista", "critic_score": 96, "works": ["Antics"]},
        {"source": "Interpol", "target": "Carlos_D", "weight_count": 5, "relation_type": "member", "relation_desc": "Baixista icônico", "critic_score": 97, "works": ["Turn On the Bright Lights"]},
        {"source": "Peter_Katis", "target": "Interpol", "weight_count": 4, "relation_type": "producer", "relation_desc": "Produção e engenharia de Turn On the Bright Lights", "critic_score": 99, "works": ["Turn On the Bright Lights"]},
        {"source": "Peter_Katis", "target": "The_National", "weight_count": 4, "relation_type": "producer", "relation_desc": "Produção de All Gator e Boxer", "critic_score": 98, "works": ["Boxer"]},
        {"source": "Yeah_Yeah_Yeahs", "target": "Karen_O", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista e líder", "critic_score": 98, "works": ["Fever to Tell"]},
        {"source": "Yeah_Yeah_Yeahs", "target": "Nick_Zinner", "weight_count": 5, "relation_type": "member", "relation_desc": "Guitarrista", "critic_score": 97, "works": ["Fever to Tell"]},
        {"source": "Yeah_Yeah_Yeahs", "target": "Brian_Chase", "weight_count": 5, "relation_type": "member", "relation_desc": "Baterista", "critic_score": 96, "works": ["Show Your Bones"]},
        {"source": "Dave_Sitek", "target": "Yeah_Yeah_Yeahs", "weight_count": 4, "relation_type": "producer", "relation_desc": "Produção de Fever to Tell e It's Blitz!", "critic_score": 98, "works": ["Fever to Tell"]},
        {"source": "Dave_Sitek", "target": "TV_on_the_Radio", "weight_count": 5, "relation_type": "member", "relation_desc": "Membro fundador e produtor", "critic_score": 98, "works": ["Return to Cookie Mountain"]},
        {"source": "Franz_Ferdinand", "target": "Alex_Turner", "weight_count": 2, "relation_type": "collaboration", "relation_desc": "Cena Post-Punk Revival britânica dos anos 2000", "critic_score": 92, "works": ["NME Awards Live"]},
        {"source": "James_Ford", "target": "Arctic_Monkeys", "weight_count": 5, "relation_type": "producer", "relation_desc": "Produção de Favourite Worst Nightmare e AM", "critic_score": 99, "works": ["AM"]},
        {"source": "Bloc_Party", "target": "Kele_Okereke", "weight_count": 5, "relation_type": "member", "relation_desc": "Vocalista principal", "critic_score": 96, "works": ["Silent Alarm"]},
        {"source": "Editors", "target": "Interpol", "weight_count": 2, "relation_type": "collaboration", "relation_desc": "Parceria de turnê e influências cruzadas de Post-Punk", "critic_score": 91, "works": ["European Tour"]}
    ]

    added_edges_count = 0
    for eg in new_edges_to_add:
        src, tgt = eg["source"], eg["target"]
        if src in existing_node_map and tgt in existing_node_map:
            if (src, tgt) not in existing_edges:
                edges.append(eg)
                existing_edges.add((src, tgt))
                existing_edges.add((tgt, src))
                added_edges_count += 1

    print(f"[✓] {added_edges_count} novas arestas de colaboração e produção adicionadas.")

    # =========================================================================
    # 4. Gravar Dataset Enriquecido
    # =========================================================================
    data["nodes"] = nodes
    data["edges"] = edges

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[🎉] Re-classificação de The Strokes e Revival concluída! Total: {len(nodes)} nós e {len(edges)} arestas.")

if __name__ == "__main__":
    run_revival_enrichment()
