"""
Script de Ramificação Profunda para Nós de Baixo Grau (Deep Branching Engine).
Identifica e ramifica nós periféricos/baixo grau (k <= 2), adicionando supergrupos,
projetos paralelos, instrumentistas de sessão e colaborações históricas comprovadas.
"""
import json

def deep_branching_low_degree_nodes(dataset_path="data/rock_collaborations_multi_genre.json"):
    print(f"[🔍] Carregando dataset {dataset_path} para ramificar nós de baixo grau...")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    node_map = {n["id"]: n for n in data["nodes"]}
    existing_edges = {(e["source"], e["target"]) for e in data["edges"]}
    existing_edges.update({(e["target"], e["source"]) for e in data["edges"]})

    # 1. Novas entidades lendárias para conectar ramificações
    new_branch_nodes = [
        {"id": "Peter_Hook", "name": "Peter Hook", "type": "person", "genre": "Post-Punk", "country": "UK"},
        {"id": "Mani", "name": "Mani (Gary Mounfield)", "type": "person", "genre": "Indie Rock", "country": "UK"},
        {"id": "Freebass", "name": "Freebass", "type": "band", "genre": "Post-Punk", "country": "UK", "formed_year": 2007},
        {"id": "Electronic", "name": "Electronic", "type": "band", "genre": "Post-Punk", "country": "UK", "formed_year": 1988},
        {"id": "DARK", "name": "DARK", "type": "band", "genre": "Alternative Rock", "country": "UK", "formed_year": 2014},
        {"id": "Dolores_ORiordan", "name": "Dolores O'Riordan (The Cranberries)", "type": "person", "genre": "Alternative Rock", "country": "Ireland"},
        {"id": "Adrian_Belew", "name": "Adrian Belew", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "King_Crimson", "name": "King Crimson", "type": "band", "genre": "Post-Punk", "country": "UK", "formed_year": 1968},
        {"id": "John_Frusciante", "name": "John Frusciante", "type": "person", "genre": "Alternative Rock", "country": "USA"},
        {"id": "Omar_Rodriguez_Lopez", "name": "Omar Rodríguez-López", "type": "person", "genre": "Alternative Rock", "country": "USA"},
        {"id": "Cedric_Bixler_Zavala", "name": "Cedric Bixler-Zavala", "type": "person", "genre": "Alternative Rock", "country": "USA"},
        {"id": "At_the_Drive_In", "name": "At the Drive-In", "type": "band", "genre": "Alternative Rock", "country": "USA", "formed_year": 1994},
        {"id": "The_Mars_Volta", "name": "The Mars Volta", "type": "band", "genre": "Alternative Rock", "country": "USA", "formed_year": 2001},
        {"id": "Sparks", "name": "Sparks", "type": "band", "genre": "Indie Rock", "country": "USA", "formed_year": 1968},
        {"id": "FFS", "name": "FFS (Franz Ferdinand + Sparks)", "type": "band", "genre": "Indie Rock", "country": "UK", "formed_year": 2014},
        {"id": "James_Ford", "name": "James Ford (Simian Mobile Disco)", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "UK"},
        {"id": "Danger_Mouse", "name": "Danger Mouse (Brian Burton)", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "USA"},
        {"id": "Karen_O", "name": "Karen O", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "Mike_Kinsella", "name": "Mike Kinsella", "type": "person", "genre": "Math Rock / Emo", "country": "USA"},
        {"id": "Cap_n_Jazz", "name": "Cap'n Jazz", "type": "band", "genre": "Math Rock / Emo", "country": "USA", "formed_year": 1989},
        {"id": "Owen", "name": "Owen", "type": "band", "genre": "Math Rock / Emo", "country": "USA", "formed_year": 2001},
        {"id": "Panda_Bear", "name": "Panda Bear (Noah Lennox)", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "Daft_Punk", "name": "Daft Punk", "type": "band", "genre": "Dance-Punk", "country": "France", "formed_year": 1993},
        {"id": "MGMT", "name": "MGMT", "type": "band", "genre": "Neo-Psychedelia", "country": "USA", "formed_year": 2002},
        {"id": "Stars", "name": "Stars", "type": "band", "genre": "Indie Rock", "country": "Canada", "formed_year": 2000}
    ]

    for n in new_branch_nodes:
        if n["id"] not in node_map:
            data["nodes"].append(n)
            node_map[n["id"]] = n

    # 2. Novas conexões profundas para integrar nós de baixo grau
    deep_edges = [
        # --- Super-Pontes de Baixistas de Manchester (Andy Rourke, Peter Hook, Mani) ---
        ("Andy_Rourke", "The_Smiths", "member", "Baixista Lendário do The Smiths", 98, ["The Queen Is Dead", "Meat Is Murder"]),
        ("Andy_Rourke", "Peter_Hook", "collaboration", "Co-fundadores da Superbanda de Baixistas Freebass", 95, ["Freebass"]),
        ("Andy_Rourke", "Mani", "collaboration", "Baixista dos Stone Roses integrado ao Freebass", 95, ["Freebass"]),
        ("Andy_Rourke", "Freebass", "member", "Baixista Oficial do Freebass com Peter Hook e Mani", 95, ["It's a Twin Thing"]),
        ("Peter_Hook", "Freebass", "member", "Baixista e Compositor do Freebass", 95, ["It's a Twin Thing"]),
        ("Mani", "Freebass", "member", "Baixista do Freebass", 94, ["It's a Twin Thing"]),
        ("Mani", "The_Stone_Roses", "member", "Baixista Principal do The Stone Roses", 97, ["The Stone Roses", "Second Coming"]),
        ("Mani", "Primal_Scream", "member", "Baixista Oficial do Primal Scream (1996-2011)", 96, ["XTRMNTR", "Evil Heat"]),
        ("Andy_Rourke", "Ian_Brown", "guest", "Baixista nas Faixas Solo de Ian Brown", 93, ["The World Is Yours"]),
        ("Andy_Rourke", "Dolores_ORiordan", "collaboration", "Parceria na Banda DARK", 94, ["Science Agrees"]),
        ("Dolores_ORiordan", "DARK", "member", "Vocalista da Banda DARK", 94, ["Science Agrees"]),

        # --- Johnny Marr & Electronic Supergroup ---
        ("Johnny_Marr", "Bernard_Sumner", "collaboration", "Co-fundadores da Superbanda Synth-Pop Electronic", 97, ["Electronic"]),
        ("Johnny_Marr", "Electronic", "member", "Guitarrista e Co-compositor do Electronic", 97, ["Electronic", "Raise the Pressure"]),
        ("Bernard_Sumner", "Electronic", "member", "Vocalista e Sintetizadores do Electronic", 97, ["Electronic"]),
        ("Johnny_Marr", "Modest_Mouse", "member", "Guitarrista Oficial e Compositor no Álbum 'We Were Dead Before the Ship Even Sank'", 96, ["We Were Dead Before the Ship Even Sank"]),
        ("Johnny_Marr", "The_Cribs", "member", "Guitarrista Oficial da Banda (2008-2011)", 93, ["Ignore the Ignorant"]),

        # --- Adrian Belew & Session Virtuosos ---
        ("Adrian_Belew", "Talking_Heads", "guest", "Solos de Guitarra Noise Marcantes em 'Remain in Light' e Turnê 1980", 98, ["Remain in Light", "The Name of This Band Is Talking Heads"]),
        ("Adrian_Belew", "Nine_Inch_Nails", "guest", "Guitarras Experimentais em 'The Downward Spiral', 'The Fragile' e 'Hesitation Marks'", 97, ["The Downward Spiral", "Hesitation Marks"]),
        ("Adrian_Belew", "David_Bowie", "guest", "Guitarrista Principal nas Turnês 'Isolar II' e 'Sound+Vision', Álbum 'Lodger'", 98, ["Lodger", "Stage"]),
        ("Adrian_Belew", "King_Crimson", "member", "Vocalista Principal e Guitarrista do King Crimson (1981-2008)", 98, ["Discipline", "Three of a Perfect Pair"]),

        # --- Red Hot Chili Peppers, John Frusciante & At the Drive-In / The Mars Volta ---
        ("John_Frusciante", "Red_Hot_Chili_Peppers", "member", "Guitarrista Clássico do Red Hot Chili Peppers", 99, ["Blood Sugar Sex Magik", "Californication", "Stadium Arcadium"]),
        ("John_Frusciante", "Johnny_Marr", "guest", "Solos de Guitarra no Álbum Solo 'The Empyrean'", 94, ["The Empyrean"]),
        ("John_Frusciante", "Omar_Rodriguez_Lopez", "collaboration", "Álbum Colaborativo de Guitarras e Feats no The Mars Volta", 95, ["Omar Rodriguez-Lopez & John Frusciante"]),
        ("Omar_Rodriguez_Lopez", "At_the_Drive_In", "member", "Guitarrista e Compositor do At the Drive-In", 97, ["Relationship of Command"]),
        ("Cedric_Bixler_Zavala", "At_the_Drive_In", "member", "Vocalista Principal do At the Drive-In", 97, ["Relationship of Command"]),
        ("Omar_Rodriguez_Lopez", "The_Mars_Volta", "member", "Guitarrista e Fundador do The Mars Volta", 97, ["De-Loused in the Comatorium"]),
        ("Cedric_Bixler_Zavala", "The_Mars_Volta", "member", "Vocalista do The Mars Volta", 97, ["De-Loused in the Comatorium"]),
        ("Rick_Rubin", "The_Mars_Volta", "producer", "Produtor do Álbum Obra-Prima 'De-Loused in the Comatorium'", 98, ["De-Loused in the Comatorium"]),

        # --- Franz Ferdinand, Sparks (FFS) & 2000s Garage Revival ---
        ("Alex_Kapranos", "Franz_Ferdinand", "member", "Frontman e Vocalista do Franz Ferdinand", 97, ["Franz Ferdinand", "You Could Have It So Much Better"]),
        ("Alex_Kapranos", "Sparks", "collaboration", "Parceria e Álbum Conjunto FFS com Ron & Russell Mael", 96, ["FFS"]),
        ("Alex_Kapranos", "FFS", "member", "Vocalista e Compositor no Supergrupo FFS", 96, ["FFS"]),
        ("Sparks", "FFS", "member", "Co-criadores do Supergrupo FFS com Franz Ferdinand", 96, ["FFS"]),
        ("Albert_Hammond_Jr", "The_Strokes", "member", "Guitarrista do The Strokes", 97, ["Is This It", "Room on Fire"]),
        ("Albert_Hammond_Jr", "Julian_Casablancas", "collaboration", "Parceria de Composição e Álbuns Solo na Cult Records", 95, ["Solo Projects / Cult Records"]),
        ("Alex_Turner", "James_Ford", "producer", "James Ford produziu os álbuns 'Favourite Worst Nightmare', 'AM' e 'Tranquility Base'", 98, ["AM", "Favourite Worst Nightmare"]),
        ("James_Ford", "Arctic_Monkeys", "producer", "Produtor de Longa Data do Arctic Monkeys", 98, ["AM"]),
        ("James_Ford", "Foals", "producer", "Produtor do Álbum 'What Went Down'", 94, ["What Went Down"]),
        ("James_Ford", "Depeche_Mode", "producer", "Produtor dos Álbuns 'Spirit' e 'Memento Mori'", 96, ["Memento Mori"]),

        # --- Yeah Yeah Yeahs, Karen O & Danger Mouse ---
        ("Karen_O", "Yeah_Yeah_Yeahs", "member", "Vocalista e Frontwoman do Yeah Yeah Yeahs", 97, ["Fever to Tell", "It's Blitz!"]),
        ("Karen_O", "Danger_Mouse", "collaboration", "Álbum Colaborativo Aclamado 'Lux Prima'", 96, ["Lux Prima"]),
        ("Danger_Mouse", "Gorillaz", "producer", "Produtor do Álbum Clássico 'Demon Days'", 99, ["Demon Days"]),
        ("Danger_Mouse", "The_Black_Keys", "producer", "Produtor do Álbum 'El Camino'", 97, ["El Camino"]),
        ("Danger_Mouse", "The_Brocade", "producer", "Produtor de 'Modern Guilt' do Beck", 95, ["Modern Guilt"]),
        ("Karen_O", "Trent_Reznor", "collaboration", "Cover de 'Immigrant Song' para a Trilha de David Fincher", 95, ["The Girl with the Dragon Tattoo Soundtrack"]),

        # --- Midwest Emo, Math Rock & Animal Collective (Mike Kinsella, Avey Tare, Panda Bear) ---
        ("Mike_Kinsella", "American_Football", "member", "Vocalista, Guitarrista e Fundador do American Football", 97, ["American Football (1999)"]),
        ("Mike_Kinsella", "Cap_n_Jazz", "member", "Baterista do Cap'n Jazz", 96, ["Analphabetapolothology"]),
        ("Mike_Kinsella", "Owen", "member", "Criador e Músico Solo do Projeto Owen", 95, ["At Home with Owen"]),
        ("Avey_Tare", "Animal_Collective", "member", "Vocalista e Co-fundador do Animal Collective", 96, ["Merriweather Post Pavilion"]),
        ("Panda_Bear", "Animal_Collective", "member", "Vocalista e Multi-instrumentista do Animal Collective", 97, ["Merriweather Post Pavilion", "Person Pitch"]),
        ("Panda_Bear", "Daft_Punk", "guest", "Vocalista Convidado na Faixa 'Doin' It Right'", 97, ["Random Access Memories"]),
        ("Andrew_VanWyngarden", "MGMT", "member", "Frontman e Vocalista do MGMT", 96, ["Oracular Spectacular"]),
        ("Dave_Fridmann", "MGMT", "producer", "Produtor de 'Oracular Spectacular' e 'Congratulations'", 97, ["Oracular Spectacular"]),

        # --- Canadenses (Broken Social Scene, Metric, Stars, Feist, Amy Millan, Andrew Whiteman) ---
        ("Kevin_Drew", "Broken_Social_Scene", "member", "Líder e Fundador do Broken Social Scene", 96, ["You Forgot It in People"]),
        ("Feist", "Broken_Social_Scene", "member", "Vocalista e Guitarrista no Broken Social Scene", 96, ["You Forgot It in People"]),
        ("Emily_Haines", "Metric", "member", "Vocalista Principal do Metric", 95, ["Fantasham", "Synthetica"]),
        ("Emily_Haines", "Broken_Social_Scene", "member", "Vocalista Convidada e Colaboradora", 95, ["You Forgot It in People"]),
        ("Amy_Millan", "Stars", "member", "Vocalista Principal do Stars", 94, ["Set Yourself on Fire"]),
        ("Amy_Millan", "Broken_Social_Scene", "member", "Vocalista e Guitarrista no Broken Social Scene", 94, ["You Forgot It in People"]),
        ("Andrew_Whiteman", "Broken_Social_Scene", "member", "Guitarrista Principal do Broken Social Scene", 94, ["You Forgot It in People"])
    ]

    added_edges = 0
    for src, tgt, rel_t, desc, score, works in deep_edges:
        if src in node_map and tgt in node_map:
            if (src, tgt) not in existing_edges:
                data["edges"].append({
                    "source": src,
                    "target": tgt,
                    "weight_count": 3,
                    "relation_type": rel_t,
                    "relation_label": rel_t,
                    "relation_desc": desc,
                    "critic_score": score,
                    "works": works
                })
                existing_edges.add((src, tgt))
                existing_edges.add((tgt, src))
                added_edges += 1

    data["metadata"] = {
        "total_nodes": len(data["nodes"]),
        "total_edges": len(data["edges"]),
        "version": "3.5.0-deep-branched"
    }

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[✅] Ramificação Profunda Concluída: +{added_edges} arestas de alto impacto injetadas para nós de baixo grau!")
    return data

if __name__ == "__main__":
    deep_branching_low_degree_nodes()
