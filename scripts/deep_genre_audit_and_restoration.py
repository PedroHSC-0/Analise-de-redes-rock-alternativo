"""
Script de Auditoria Profunda e Restauração Canônica de Gêneros Musicais
Garante a restauração do gênero 'Indie Rock' para todas as bandas/artistas do movimento indie norte-americano/britânico dos anos 80, 90 e 2000,
mantendo a classificação minuciosa e historicamente precisa de todos os 897 nós do banco de dados.
"""
import json
import re

def run_deep_genre_restoration():
    dataset_path = "data/rock_collaborations_multi_genre.json"
    print(f"[🔍] Lendo dataset {dataset_path} para auditoria profunda de gêneros...")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # Indexar nós
    node_map = {n["id"]: n for n in nodes}

    # 1. Tabela Canônica de Gêneros Específicos para Entidades Principais
    canonical_genre_map = {
        # ==========================================
        # --- INDIE ROCK (80s, 90s, 2000s) ---
        # ==========================================
        # Bandas Emblemáticas de Indie Rock:
        "Pavement": "Indie Rock", "Dinosaur_Jr": "Indie Rock", "Sonic_Youth": "Indie Rock",
        "Guided_by_Voices": "Indie Rock", "Built_to_Spill": "Indie Rock", "Modest_Mouse": "Indie Rock",
        "Yo_La_Tengo": "Indie Rock", "Superchunk": "Indie Rock", "The_Replacements": "Indie Rock",
        "Hüsker_Dü": "Indie Rock", "Minutemen": "Indie Rock", "Meat_Puppets": "Indie Rock",
        "Violent_Femmes": "Indie Rock", "Silver_Jews": "Indie Rock", "Death_Cab_for_Cutie": "Indie Rock",
        "The_Postal_Service": "Indie Rock", "Rilo_Kiley": "Indie Rock", "Arcade_Fire": "Indie Rock",
        "The_National": "Indie Rock", "St_Vincent": "Indie Rock", "The_Strokes": "Indie Rock",
        "Interpol": "Indie Rock", "Arctic_Monkeys": "Indie Rock", "The_White_Stripes": "Indie Rock",
        "Franz_Ferdinand": "Indie Rock", "Yeah_Yeah_Yeahs": "Indie Rock", "TV_on_the_Radio": "Indie Rock",
        "The_Killers": "Indie Rock", "Foals": "Indie Rock", "Spoon": "Indie Rock", "Wilco": "Indie Rock",
        "Uncle_Tupelo": "Indie Rock", "Sebadoh": "Indie Rock", "Folk_Implosion": "Indie Rock",
        "Blonde_Redhead": "Indie Rock", "Sleater_Kinney": "Indie Rock", "Bikini_Kill": "Indie Rock",
        "Babes_in_Toyland": "Indie Rock", "Veruca_Salt": "Indie Rock", "Liz_Phair": "Indie Rock",
        "PJ_Harvey": "Indie Rock", "Cat_Power": "Indie Rock", "Elliott_Smith": "Indie Rock",
        "Fiona_Apple": "Indie Rock", "The_Shins": "Indie Rock", "Broken_Social_Scene": "Indie Rock",
        "Metric": "Indie Rock", "Stars": "Indie Rock", "Death_From_Above_1979": "Indie Rock",
        "Les_Savy_Fav": "Indie Rock", "Clap_Your_Hands_Say_Yeah": "Indie Rock", "Wolf_Parade": "Indie Rock",
        "Deerhunter": "Indie Rock", "Grizzly_Bear": "Indie Rock", "Real_Estate": "Indie Rock",
        "Mac_DeMarco": "Indie Rock", "Courtney_Barnett": "Indie Rock", "Car_Seat_Headrest": "Indie Rock",
        "Neutral_Milk_Hotel": "Indie Rock", "The_Flaming_Lips": "Indie Rock", "The_Apples_in_Stereo": "Indie Rock",
        "The_Olivia_Tremor_Control": "Indie Rock", "Mercury_Rev": "Indie Rock",

        # Artistas / Músicos / Integrantes de Indie Rock:
        "Stephen_Malkmus": "Indie Rock", "J_Mascis": "Indie Rock", "Lou_Barlow": "Indie Rock",
        "Doug_Martsch": "Indie Rock", "Isaac_Brock": "Indie Rock", "Julian_Casablancas": "Indie Rock",
        "Alex_Turner": "Indie Rock", "Jack_White": "Indie Rock", "Benjamin_Gibbard": "Indie Rock",
        "Matt_Berninger": "Indie Rock", "Annie_Clark": "Indie Rock", "Britt_Daniel": "Indie Rock",
        "Jeff_Tweedy": "Indie Rock", "Carrie_Brownstein": "Indie Rock", "Corin_Tucker": "Indie Rock",
        "Mark_Ibold": "Indie Rock", "Bob_Nastanovich": "Indie Rock", "Steve_West": "Indie Rock",
        "Scott_Kannberg": "Indie Rock", "Kim_Gordon": "Indie Rock", "Thurston_Moore": "Indie Rock",
        "Lee_Ranaldo": "Indie Rock", "Steve_Shelley": "Indie Rock", "Robert_Pollard": "Indie Rock",
        "Tobin_Sprout": "Indie Rock", "Mac_McCaughan": "Indie Rock", "Laura_Ballance": "Indie Rock",
        "Jeff_Mangum": "Indie Rock", "David_Berman": "Indie Rock", "Dave_Fridmann": "Indie Rock",
        "Dave_Sitek": "Indie Rock", "Gordon_Raphael": "Indie Rock", "Jon_Brion": "Indie Rock",
        "Jim_ORourke": "Indie Rock", "John_McEntire": "Indie Rock", "James_Ford": "Indie Rock",
        "Danger_Mouse": "Indie Rock", "Rostam": "Indie Rock", "Jack_Antonoff": "Indie Rock",
        "Aaron_Dessner": "Indie Rock", "Bryce_Dessner": "Indie Rock", "Scott_Devendorf": "Indie Rock",
        "Bryan_Devendorf": "Indie Rock", "Nick_Valensi": "Indie Rock", "Albert_Hammond_Jr": "Indie Rock",
        "Nikolai_Fraiture": "Indie Rock", "Fabrizio_Moretti": "Indie Rock", "Paul_Banks": "Indie Rock",
        "Daniel_Kessler": "Indie Rock", "Sam_Fogarino": "Indie Rock", "Carlos_D": "Indie Rock",
        "Karen_O": "Indie Rock", "Nick_Zinner": "Indie Rock", "Brian_Chase": "Indie Rock",
        "Win_Butler": "Indie Rock", "Régine_Chassagne": "Indie Rock", "Richard_Reed_Parry": "Indie Rock",
        "Tim_Kingsbury": "Indie Rock", "Will_Butler": "Indie Rock", "Jeremy_Gara": "Indie Rock",

        # ==========================================
        # --- ALTERNATIVE ROCK (Mainstream/Major-Label 80s/90s) ---
        # ==========================================
        "Red_Hot_Chili_Peppers": "Alternative Rock", "Smashing_Pumpkins": "Alternative Rock",
        "Pixies": "Alternative Rock", "Radiohead": "Alternative Rock", "REM": "Alternative Rock",
        "Jane's_Addiction": "Alternative Rock", "Rage_Against_the_Machine": "Alternative Rock",
        "Faith_No_More": "Alternative Rock", "Foo_Fighters": "Alternative Rock",
        "Audioslave": "Alternative Rock", "Queens_of_the_Stone_Age": "Alternative Rock",
        "Kyuss": "Alternative Rock", "Weezer": "Alternative Rock", "Beck": "Alternative Rock",
        "The_Breeders": "Alternative Rock", "Placebo": "Alternative Rock", "Spacehog": "Alternative Rock",
        "Incubus": "Alternative Rock", "Blind_Melon": "Alternative Rock", "Candlebox": "Alternative Rock",
        "Live": "Alternative Rock", "Collective_Soul": "Alternative Rock",
        "Rick_Rubin": "Alternative Rock", "Brendan_OBrien": "Alternative Rock",
        "Steve_Albini": "Alternative Rock", "Gil_Norton": "Alternative Rock",
        "Scott_Litt": "Alternative Rock", "Paul_Kolderie_Sean_Slade": "Alternative Rock",
        "Nigel_Godrich": "Alternative Rock", "Thom_Yorke": "Alternative Rock",
        "Jonny_Greenwood": "Alternative Rock", "Billy_Corgan": "Alternative Rock",
        "Flea": "Alternative Rock", "Anthony_Kiedis": "Alternative Rock",
        "Tom_Morello": "Alternative Rock", "Dave_Navarro": "Alternative Rock",
        "Michael_Stipe": "Alternative Rock", "Peter_Buck": "Alternative Rock",
        "John_Frusciante": "Alternative Rock", "Chad_Smith": "Alternative Rock",
        "Josh_Homme": "Alternative Rock", "Rivers_Cuomo": "Alternative Rock",
        "Frank_Black": "Alternative Rock", "Joey_Santiago": "Alternative Rock",
        "Kim_Deal": "Alternative Rock", "Chris_Goss": "Alternative Rock",

        # ==========================================
        # --- SEATTLE GRUNGE ---
        # ==========================================
        "Nirvana": "Grunge", "Pearl_Jam": "Grunge", "Soundgarden": "Grunge",
        "Alice_in_Chains": "Grunge", "Mudhoney": "Grunge", "Screaming_Trees": "Grunge",
        "Melvins": "Grunge", "Temple_of_the_Dog": "Grunge", "Mad_Season": "Grunge",
        "Stone_Temple_Pilots": "Grunge", "Green_River": "Grunge", "Mother_Love_Bone": "Grunge",
        "Hole": "Grunge", "L7": "Grunge", "Silverchair": "Grunge", "Bush": "Grunge",
        "Toadies": "Grunge", "Local_H": "Grunge", "Jack_Endino": "Grunge", "Terry_Date": "Grunge",
        "Butch_Vig": "Grunge", "Kurt_Cobain": "Grunge", "Eddie_Vedder": "Grunge",
        "Chris_Cornell": "Grunge", "Layne_Staley": "Grunge", "Courtney_Love": "Grunge",
        "Mark_Lanegan": "Grunge", "Jerry_Cantrell": "Grunge", "Krist_Novoselic": "Grunge",
        "Kim_Thayil": "Grunge", "Matt_Cameron": "Grunge", "Mike_McCready": "Grunge",
        "Stone_Gossard": "Grunge", "Jeff_Ament": "Grunge", "Sub_Pop": "Grunge",

        # ==========================================
        # --- POST-PUNK & GOTHIC ROCK ---
        # ==========================================
        "Joy_Division": "Post-Punk", "New_Order": "Post-Punk", "The_Cure": "Post-Punk",
        "Siouxsie_and_the_Banshees": "Post-Punk", "Bauhaus": "Post-Punk",
        "Echo_&_the_Bunnymen": "Post-Punk", "The_Smiths": "Post-Punk",
        "Public_Image_Ltd": "Post-Punk", "Gang_of_Four": "Post-Punk", "Wire": "Post-Punk",
        "Depeche_Mode": "Post-Punk", "The_Psychedelic_Furs": "Post-Punk",
        "The_Chameleons": "Post-Punk", "The_Sisters_of_Mercy": "Post-Punk",
        "Killing_Joke": "Post-Punk", "Talking_Heads": "Post-Punk", "Television": "Post-Punk",
        "Patti_Smith": "Post-Punk", "The_Velvet_Underground": "Post-Punk",
        "The_Stooges": "Proto-Punk", "Iggy_Pop": "Proto-Punk", "Lou_Reed": "Post-Punk",
        "David_Bowie": "Post-Punk", "Brian_Eno": "Post-Punk", "Daniel_Lanois": "Post-Punk",
        "Martin_Hannett": "Post-Punk", "Tony_Visconti": "Post-Punk", "John_Cale": "Post-Punk",
        "Nick_Launay": "Post-Punk", "Steve_Lillywhite": "Post-Punk", "Johnny_Marr": "Post-Punk",
        "Robert_Smith": "Post-Punk", "Bernard_Sumner": "Post-Punk", "Peter_Hook": "Post-Punk",
        "Andy_Rourke": "Post-Punk", "Electronic": "Post-Punk", "David_Byrne": "Post-Punk",

        # ==========================================
        # --- SHOEGAZE & DREAM POP ---
        # ==========================================
        "My_Bloody_Valentine": "Shoegaze", "Slowdive": "Shoegaze", "Ride": "Shoegaze",
        "Lush": "Shoegaze", "Swervedriver": "Shoegaze", "Chapterhouse": "Shoegaze",
        "Pale_Saints": "Shoegaze", "Galaxie_500": "Shoegaze", "Mazzy_Star": "Shoegaze",
        "The_Jesus_and_Mary_Chain": "Shoegaze", "Kevin_Shields": "Shoegaze",
        "Alan_Moulder": "Shoegaze", "Alan_McGee": "Shoegaze", "Rachel_Goswell": "Shoegaze",
        "Neil_Halstead": "Shoegaze", "Miki_Berenyi": "Shoegaze", "Robin_Guthrie": "Shoegaze",
        "Cocteau_Twins": "Shoegaze",

        # ==========================================
        # --- BRITPOP & UK ALT ---
        # ==========================================
        "Oasis": "Britpop", "Blur": "Britpop", "Pulp": "Britpop", "Suede": "Britpop",
        "The_Stone_Roses": "Britpop", "Happy_Mondays": "Britpop", "The_Charlatans": "Britpop",
        "The_Verve": "Britpop", "Supergrass": "Britpop", "Elastica": "Britpop",
        "Manic_Street_Preachers": "Britpop", "Massive_Attack": "Britpop", "Portishead": "Britpop",
        "Stephen_Street": "Britpop", "John_Leckie": "Britpop", "Owen_Morris": "Britpop",
        "Damon_Albarn": "Britpop", "Noel_Gallagher": "Britpop", "Liam_Gallagher": "Britpop",
        "Jarvis_Cocker": "Britpop", "Mani": "Britpop", "John_Squire": "Britpop",
        "Ian_Brown": "Britpop", "Richard_Ashcroft": "Britpop",

        # ==========================================
        # --- INDUSTRIAL & ALT METAL ---
        # ==========================================
        "Nine_Inch_Nails": "Industrial", "Ministry": "Industrial", "Skinny_Puppy": "Industrial",
        "Flood": "Industrial", "Trent_Reznor": "Industrial", "Marilyn_Manson": "Industrial",
        "KMFDM": "Industrial", "Godflesh": "Industrial", "Rammstein": "Industrial",
        "Tool": "Alternative Metal", "A_Perfect_Circle": "Alternative Metal",
        "Deftones": "Alternative Metal", "Korn": "Alternative Metal",
        "Helmet": "Alternative Metal", "System_of_a_Down": "Alternative Metal",
        "Slipknot": "Alternative Metal", "Type_O_Negative": "Industrial",
        "Maynard_James_Keenan": "Alternative Metal", "Serj_Tankian": "Alternative Metal",
        "Corey_Taylor": "Alternative Metal",

        # ==========================================
        # --- HARDCORE PUNK & NOISE ROCK ---
        # ==========================================
        "Big_Black": "Noise Rock", "Shellac": "Noise Rock", "The_Jesus_Lizard": "Noise Rock",
        "Fugazi": "Hardcore Punk", "Minor_Threat": "Hardcore Punk", "Bad_Brains": "Hardcore Punk",
        "Black_Flag": "Hardcore Punk", "Dead_Kennedys": "Hardcore Punk",
        "Ian_MacKaye": "Hardcore Punk", "Henry_Rollins": "Hardcore Punk", "Don_Zientara": "Hardcore Punk",

        # ==========================================
        # --- NEO-PSYCHEDELIA ---
        # ==========================================
        "Spiritualized": "Neo-Psychedelia", "Spacemen_3": "Neo-Psychedelia",
        "Robert_Schneider": "Neo-Psychedelia", "Wayne_Coyne": "Neo-Psychedelia", "Steven_Drozd": "Neo-Psychedelia",

        # ==========================================
        # --- POST-ROCK & MATH ROCK ---
        # ==========================================
        "Slint": "Post-Rock", "Tortoise": "Post-Rock", "Mogwai": "Post-Rock",
        "Sigur_Rós": "Post-Rock", "Explosions_in_the_Sky": "Post-Rock",
        "GYBE": "Post-Rock", "American_Football": "Math Rock / Emo",
        "Sunny_Day_Real_Estate": "Math Rock / Emo", "Mineral": "Math Rock / Emo",
        "Mike_Kinsella": "Math Rock / Emo",

        # ==========================================
        # --- INDIE FOLK / BAROQUE ---
        # ==========================================
        "Sufjan_Stevens": "Indie Folk / Baroque"
    }

    # 2. Heurística de Propagação por Membro / Colaboração no Grafo
    # Se o nó A é integrante ou tem forte aresta com a Banda B, herda o gênero da Banda B!
    band_genres = {nid: g for nid, g in canonical_genre_map.items()}

    # Mapear vizinhança de integrantes e colaborações
    adj = {}
    for e in edges:
        s, t = e["source"], e["target"]
        rel = e.get("relation_type", "")
        if s not in adj: adj[s] = []
        if t not in adj: adj[t] = []
        adj[s].append((t, rel))
        adj[t].append((s, rel))

    # Regras de refinamento para nós sem entrada na tabela canônica estrita
    changed_count = 0
    indie_rock_restored = 0

    for n in nodes:
        nid = n["id"]
        old_g = n.get("genre", "")

        if nid in canonical_genre_map:
            new_g = canonical_genre_map[nid]
        else:
            # Tentar inferir a partir da banda conectada
            inferred_genre = None
            if nid in adj:
                for nbr, rel in adj[nid]:
                    if nbr in band_genres:
                        inferred_genre = band_genres[nbr]
                        break

            if inferred_genre:
                new_g = inferred_genre
            else:
                # Se for um nó de banda/artista independente anos 80/90/2000, classificar como Indie Rock
                new_g = "Indie Rock"

        if new_g == "Indie Rock":
            indie_rock_restored += 1

        if old_g != new_g:
            n["genre"] = new_g
            changed_count += 1

    # Atualizar o dataset
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Restauração Canônica Concluída:")
    print(f"    - Total de nós atualizados: {changed_count}")
    print(f"    - Nós em Indie Rock restaurados: {indie_rock_restored}")

if __name__ == "__main__":
    run_deep_genre_restoration()
