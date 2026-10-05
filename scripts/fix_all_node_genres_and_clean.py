"""
Script de Correção Canônica de Gêneros e Purificação do Banco de Dados.
Remove rotulagens aleatórias/incorretas de gêneros (ex: Alice in Chains como Britpop, Pearl Jam como Shoegaze)
e purifica a base de dados mantendo 100% de foco científico no Rock Alternativo dos Anos 80 e 90.
"""
import json

def fix_all_node_genres_and_clean(dataset_path="data/rock_collaborations_multi_genre.json"):
    print(f"[🔍] Lendo dataset {dataset_path} para correção canônica de gêneros...")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # Dicionário Canônico de Gêneros Autênticos
    canonical_genres = {
        # --- Grunge ---
        "Nirvana": "Grunge", "Pearl_Jam": "Grunge", "Soundgarden": "Grunge",
        "Alice_in_Chains": "Grunge", "Screaming_Trees": "Grunge", "Mudhoney": "Grunge",
        "Melvins": "Grunge", "Temple_of_the_Dog": "Grunge", "Mad_Season": "Grunge",
        "Stone_Temple_Pilots": "Grunge", "Hole": "Grunge", "Jack_Endino": "Grunge",
        "Kurt_Cobain": "Grunge", "Eddie_Vedder": "Grunge", "Chris_Cornell": "Grunge",
        "Layne_Staley": "Grunge", "Courtney_Love": "Grunge", "Mark_Lanegan": "Grunge",
        "Mike_McCready": "Grunge", "Sub_Pop": "Grunge",

        # --- Alternative Rock ---
        "Pixies": "Alternative Rock", "Smashing_Pumpkins": "Alternative Rock",
        "Jane's_Addiction": "Alternative Rock", "Red_Hot_Chili_Peppers": "Alternative Rock",
        "Faith_No_More": "Alternative Rock", "Rage_Against_the_Machine": "Alternative Rock",
        "Foo_Fighters": "Alternative Rock", "Audioslave": "Alternative Rock",
        "Queens_of_the_Stone_Age": "Alternative Rock", "Kyuss": "Alternative Rock",
        "Chris_Goss": "Alternative Rock", "Josh_Homme": "Alternative Rock",
        "Dave_Grohl": "Alternative Rock", "Billy_Corgan": "Alternative Rock",
        "Flea": "Alternative Rock", "Dave_Navarro": "Alternative Rock",
        "Tom_Morello": "Alternative Rock", "Butch_Vig": "Alternative Rock",
        "Steve_Albini": "Alternative Rock", "Flood": "Alternative Rock",
        "Alan_Moulder": "Alternative Rock", "Scott_Litt": "Alternative Rock",
        "Gil_Norton": "Alternative Rock", "Rick_Rubin": "Alternative Rock",
        "Them_Crooked_Vultures": "Alternative Rock", "Jane’s_Addiction": "Alternative Rock",

        # --- Post-Punk & New Wave ---
        "Joy_Division": "Post-Punk", "New_Order": "Post-Punk", "The_Cure": "Post-Punk",
        "Siouxsie_and_the_Banshees": "Post-Punk", "Talking_Heads": "Post-Punk",
        "Devo": "Post-Punk", "Television": "Post-Punk", "Wire": "Post-Punk",
        "Bauhaus": "Post-Punk", "Gang_of_Four": "Post-Punk", "The_Smiths": "Post-Punk",
        "Echo_&_the_Bunnymen": "Post-Punk", "The_Psychedelic_Furs": "Post-Punk",
        "Depeche_Mode": "Post-Punk", "Tears_for_Fears": "Post-Punk",
        "The_Chameleons": "Post-Punk", "The_Sisters_of_Mercy": "Post-Punk",
        "Killing_Joke": "Post-Punk", "David_Bowie": "Post-Punk", "Iggy_Pop": "Post-Punk",
        "Lou_Reed": "Post-Punk", "The_Velvet_Underground": "Post-Punk",
        "Patti_Smith": "Post-Punk", "New_York_Dolls": "Proto-Punk", "T_Rex": "Post-Punk",
        "Roxy_Music": "Post-Punk", "Bernard_Sumner": "Post-Punk", "Robert_Smith": "Post-Punk",
        "David_Byrne": "Post-Punk", "Martin_Hannett": "Post-Punk", "Brian_Eno": "Post-Punk",
        "Tony_Visconti": "Post-Punk", "Peter_Hook": "Post-Punk", "Andy_Rourke": "Post-Punk",
        "Johnny_Marr": "Post-Punk", "Electronic": "Post-Punk", "Freebass": "Post-Punk",
        "Marc_Bolan": "Post-Punk", "Bryan_Ferry": "Post-Punk", "Bob_Ezrin": "Post-Punk",
        "Adrian_Belew": "Post-Punk", "King_Crimson": "Post-Punk",

        # --- Shoegaze & Dream Pop ---
        "My_Bloody_Valentine": "Shoegaze", "Slowdive": "Shoegaze", "Ride": "Shoegaze",
        "Lush": "Shoegaze", "Swervedriver": "Shoegaze", "Chapterhouse": "Shoegaze",
        "Galaxie_500": "Shoegaze", "Mazzy_Star": "Shoegaze", "The_Jesus_and_Mary_Chain": "Shoegaze",
        "Cocteau_Twins": "Shoegaze", "Kevin_Shields": "Shoegaze", "Alan_McGee": "Shoegaze",
        "Bobby_Gillespie": "Alternative Rock", "Primal_Scream": "Alternative Rock",

        # --- Britpop & UK Alt ---
        "Blur": "Britpop", "Oasis": "Britpop", "Pulp": "Britpop", "Suede": "Britpop",
        "The_Stone_Roses": "Britpop", "Happy_Mondays": "Britpop", "The_Charlatans": "Britpop",
        "Radiohead": "Alternative Rock", "The_Verve": "Britpop", "Supergrass": "Britpop",
        "Manic_Street_Preachers": "Britpop", "Massive_Attack": "Britpop", "Portishead": "Britpop",
        "Damon_Albarn": "Britpop", "Noel_Gallagher": "Britpop", "Thom_Yorke": "Alternative Rock",
        "Nigel_Godrich": "Alternative Rock", "John_Leckie": "Britpop", "Stephen_Street": "Britpop",
        "Mani": "Britpop", "Alex_Kapranos": "Indie Rock", "FFS": "Indie Rock",

        # --- Industrial & Alt Metal ---
        "Nine_Inch_Nails": "Industrial", "Ministry": "Industrial", "Skinny_Puppy": "Industrial",
        "Tool": "Alternative Metal", "A_Perfect_Circle": "Alternative Metal",
        "Deftones": "Alternative Metal", "Korn": "Alternative Metal",
        "Type_O_Negative": "Industrial", "Rammstein": "Industrial", "Godflesh": "Industrial",
        "Helmet": "Alternative Metal", "System_of_a_Down": "Alternative Metal",
        "Slipknot": "Alternative Metal", "KMFDM": "Industrial", "Trent_Reznor": "Industrial",
        "Maynard_James_Keenan": "Alternative Metal", "Serj_Tankian": "Alternative Metal",
        "Corey_Taylor": "Alternative Metal",

        # --- Indie Rock & Lo-Fi ---
        "Sonic_Youth": "Indie Rock", "Dinosaur_Jr": "Indie Rock", "Pavement": "Indie Rock",
        "Guided_by_Voices": "Indie Rock", "Built_to_Spill": "Indie Rock", "Modest_Mouse": "Indie Rock",
        "Yo_La_Tengo": "Indie Rock", "Superchunk": "Indie Rock", "Neutral_Milk_Hotel": "Indie Rock",
        "The_Replacements": "Indie Rock", "Hüsker_Dü": "Indie Rock", "Minutemen": "Indie Rock",
        "Meat_Puppets": "Indie Rock", "Violent_Femmes": "Indie Rock", "Silver_Jews": "Indie Rock",
        "Death_Cab_for_Cutie": "Indie Rock", "The_Postal_Service": "Indie Rock", "Rilo_Kiley": "Indie Rock",
        "Arcade_Fire": "Indie Rock", "The_National": "Indie Rock", "Sufjan_Stevens": "Indie Folk / Baroque",
        "St_Vincent": "Indie Rock", "The_Strokes": "Indie Rock", "Interpol": "Indie Rock",
        "Arctic_Monkeys": "Indie Rock", "The_White_Stripes": "Indie Rock", "Franz_Ferdinand": "Indie Rock",
        "Yeah_Yeah_Yeahs": "Indie Rock", "TV_on_the_Radio": "Indie Rock", "The_Killers": "Indie Rock",
        "Foals": "Indie Rock", "J_Mascis": "Indie Rock", "Lou_Barlow": "Indie Rock",
        "Stephen_Malkmus": "Indie Rock", "Doug_Martsch": "Indie Rock", "Isaac_Brock": "Indie Rock",
        "Julian_Casablancas": "Indie Rock", "Alex_Turner": "Indie Rock", "Jack_White": "Indie Rock",
        "Dave_Sitek": "Indie Rock", "Gordon_Raphael": "Indie Rock", "Dave_Fridmann": "Indie Rock",
        "John_Frusciante": "Alternative Rock", "Omar_Rodriguez_Lopez": "Alternative Rock",
        "Cedric_Bixler_Zavala": "Alternative Rock", "At_the_Drive_In": "Alternative Rock",
        "The_Mars_Volta": "Alternative Rock",

        # --- Post-Rock, Math Rock & Emo ---
        "Slint": "Post-Rock", "Mogwai": "Post-Rock", "Tortoise": "Post-Rock",
        "Sigur_Rós": "Post-Rock", "Explosions_in_the_Sky": "Post-Rock",
        "American_Football": "Math Rock / Emo", "Sunny_Day_Real_Estate": "Math Rock / Emo",
        "Mineral": "Math Rock / Emo", "GYBE": "Post-Rock", "John_McEntire": "Post-Rock",
        "Mike_Kinsella": "Math Rock / Emo", "Cap_n_Jazz": "Math Rock / Emo", "Owen": "Math Rock / Emo",

        # --- Hardcore Punk ---
        "Black_Flag": "Hardcore Punk", "Minor_Threat": "Hardcore Punk", "Bad_Brains": "Hardcore Punk",
        "Dead_Kennedys": "Hardcore Punk", "Fugazi": "Hardcore Punk", "Ian_MacKaye": "Hardcore Punk",
        "Henry_Rollins": "Hardcore Punk", "HR_Bad_Brains": "Hardcore Punk", "Quicksand": "Hardcore Punk",
        "Walter_Schreifels": "Hardcore Punk", "Bad_Religion": "Hardcore Punk"
    }

    # 1. Aplicar gêneros canônicos estritos
    fixed_count = 0
    for n in nodes:
        nid = n["id"]
        if nid in canonical_genres:
            old_g = n.get("genre", "")
            new_g = canonical_genres[nid]
            if old_g != new_g:
                n["genre"] = new_g
                fixed_count += 1
        elif "genre" not in n or not n["genre"] or n["genre"] == "Unknown":
            n["genre"] = "Alternative Rock"

    print(f"[✓] Gêneros canônicos corrigidos para {fixed_count} nós!")

    # 2. Remover arestas fora do escopo do rock 80s/90s
    cleaned_edges = []
    removed_out_of_scope = 0

    for e in edges:
        desc = e.get("relation_desc", "")
        # Filtrar referências pop fora do escopo do rock
        if any(pop in desc for pop in ["Adele", "Lady Gaga", "Travis Scott", "Kanye West", "Hans Zimmer"]):
            removed_out_of_scope += 1
            print(f"[🗑️] Aresta fora do escopo de rock removida: {e['source']} <-> {e['target']} ({desc})")
        else:
            cleaned_edges.append(e)

    sanitized_data = {
        "metadata": {
            "total_nodes": len(nodes),
            "total_edges": len(cleaned_edges),
            "version": "5.0.0-strictly-canonical-rock"
        },
        "nodes": nodes,
        "edges": cleaned_edges
    }

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(sanitized_data, f, ensure_ascii=False, indent=2)

    print(f"[✅] Purificação Canônica Concluída: {len(nodes)} nós e {len(cleaned_edges)} arestas de puro Rock 80s/90s!")
    return sanitized_data

if __name__ == "__main__":
    fix_all_node_genres_and_clean()
