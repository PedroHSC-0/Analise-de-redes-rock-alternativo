"""
Script para Injeção dos Maiores Produtores e Conectores Lendários do Rock Alternativo/Indie
(Flood, Alan Moulder, Gil Norton, Jon Brion, Stephen Street, John Cale, Daniel Lanois, Scott Litt).
"""
import json

def inject_master_producers(dataset_path="data/rock_collaborations_multi_genre.json"):
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_node_ids = {n["id"]: n for n in data["nodes"]}
    existing_edges = {(e["source"], e["target"]) for e in data["edges"]}
    existing_edges.update({(e["target"], e["source"]) for e in data["edges"]})

    master_producers = [
        {"id": "Flood", "name": "Flood (Mark Ellis)", "type": "person", "type_role": "producer", "genre": "Industrial", "country": "UK"},
        {"id": "Alan_Moulder", "name": "Alan Moulder", "type": "person", "type_role": "producer", "genre": "Shoegaze", "country": "UK"},
        {"id": "Gil_Norton", "name": "Gil Norton", "type": "person", "type_role": "producer", "genre": "Alternative Rock", "country": "UK"},
        {"id": "Jon_Brion", "name": "Jon Brion", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "USA"},
        {"id": "Stephen_Street", "name": "Stephen Street", "type": "person", "type_role": "producer", "genre": "Britpop", "country": "UK"},
        {"id": "John_Cale", "name": "John Cale", "type": "person", "type_role": "producer", "genre": "Post-Punk", "country": "UK"},
        {"id": "Scott_Litt", "name": "Scott Litt", "type": "person", "type_role": "producer", "genre": "Alternative Rock", "country": "USA"}
    ]

    for p in master_producers:
        if p["id"] not in existing_node_ids:
            data["nodes"].append(p)
            existing_node_ids[p["id"]] = p

    new_master_edges = [
        # Flood connections
        ("Flood", "Nine_Inch_Nails", "Produtor de 'The Downward Spiral' e 'Pretty Hate Machine'", 95, ["The Downward Spiral"]),
        ("Flood", "Smashing_Pumpkins", "Co-produtor de 'Mellon Collie and the Infinite Sadness'", 94, ["Mellon Collie"]),
        ("Flood", "Interpol", "Produtor de 'Our Love to Admire'", 86, ["Our Love to Admire"]),
        ("Flood", "PJ_Harvey", "Produtor de 'To Bring You My Love'", 93, ["To Bring You My Love"]),
        ("Flood", "Depeche_Mode", "Produtor do Álbum Marco 'Violator'", 96, ["Violator"]),
        ("Flood", "Foals", "Produtor de 'Holy Fire'", 88, ["Holy Fire"]),

        # Alan Moulder connections
        ("Alan_Moulder", "My_Bloody_Valentine", "Engenheiro e Mixador de 'Loveless'", 97, ["Loveless"]),
        ("Alan_Moulder", "Nine_Inch_Nails", "Mixador Principal dos Álbuns Clássicos", 93, ["The Fragile", "With Teeth"]),
        ("Alan_Moulder", "Smashing_Pumpkins", "Mixador de 'Mellon Collie' e 'Siamese Dream'", 94, ["Siamese Dream"]),
        ("Alan_Moulder", "Yeah_Yeah_Yeahs", "Mixagem de 'It's Blitz!'", 89, ["It's Blitz!"]),
        ("Alan_Moulder", "Arctic_Monkeys", "Mixador do Álbum 'Favourite Worst Nightmare'", 90, ["Favourite Worst Nightmare"]),

        # Gil Norton connections
        ("Gil_Norton", "Pixies", "Produtor de 'Doolittle' e 'Bossanova'", 96, ["Doolittle", "Bossanova"]),
        ("Gil_Norton", "Foo_Fighters", "Produtor de 'The Colour and the Shape'", 92, ["The Colour and the Shape"]),

        # Jon Brion connections
        ("Jon_Brion", "Fiona_Apple", "Produtor de 'When the Pawn...' e 'Tidal'", 94, ["When the Pawn..."]),
        ("Jon_Brion", "Elliott_Smith", "Produtor de 'From a Basement on the Hill'", 93, ["From a Basement..."]),
        ("Jon_Brion", "Mac_DeMarco", "Parceria e Produção em Estúdio", 86, ["Here Comes the Cowboy"]),
        ("Jon_Brion", "Spoon", "Produção e Arranjos", 89, ["They Want My Soul"]),

        # Stephen Street connections
        ("Stephen_Street", "The_Smiths", "Produtor de 'Strangeways, Here We Come' e Engenheiro dos Smiths", 95, ["Strangeways", "The Queen Is Dead"]),
        ("Stephen_Street", "Blur", "Produtor de 'Parklife' e 'Blur'", 93, ["Parklife", "Blur"]),
        ("Stephen_Street", "The_Cranberries", "Produtor de 'Everybody Else Is Doing It...'", 90, ["Everybody Else..."]),

        # John Cale connections
        ("John_Cale", "Patti_Smith", "Produtor do Álbum 'Horses'", 96, ["Horses"]),
        ("John_Cale", "The_Stooges", "Produtor do Álbum de Estreia 'The Stooges'", 95, ["The Stooges"]),

        # Scott Litt connections
        ("Scott_Litt", "REM", "Produtor de 'Automatic for the People' e 'Out of Time'", 95, ["Automatic for the People"]),
        ("Scott_Litt", "Nirvana", "Mixagem de 'In Utero' e Produtor de 'MTV Unplugged in New York'", 96, ["MTV Unplugged"])
    ]

    added = 0
    for src, tgt, desc, score, works in new_master_edges:
        if src in existing_node_ids and tgt in existing_node_ids:
            if (src, tgt) not in existing_edges:
                data["edges"].append({
                    "source": src,
                    "target": tgt,
                    "weight_count": 3,
                    "relation_type": "producer",
                    "relation_label": "produtor",
                    "relation_desc": desc,
                    "critic_score": score,
                    "works": works
                })
                existing_edges.add((src, tgt))
                existing_edges.add((tgt, src))
                added += 1

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Maiores Produtores Lendários Injetados: +{added} arestas de pontes de alta importância!")

if __name__ == "__main__":
    inject_master_producers()
