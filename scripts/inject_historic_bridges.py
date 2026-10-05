"""
Script para Injeção das Maiores Pontes Históricas do Rock Alternativo/Indie/Post-Punk:
- Conexões do Sonic Youth (Kim Gordon, Thurston Moore, Jim O'Rourke)
- Conexões do John Cale & Lou Reed (Velvet Underground, Patti Smith, Iggy Pop, Gorillaz, Metric)
- Conexões do Kevin Shields & Creation Records (Primal Scream, Jesus and Mary Chain, Patti Smith, Sofia Coppola Lost in Translation)
"""
import json

def inject_historic_bridges(dataset_path="data/rock_collaborations_multi_genre.json"):
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_node_ids = {n["id"]: n for n in data["nodes"]}
    existing_edges = {(e["source"], e["target"]) for e in data["edges"]}
    existing_edges.update({(e["target"], e["source"]) for e in data["edges"]})

    new_legendary_nodes = [
        {"id": "Lou_Reed", "name": "Lou Reed", "type": "person", "genre": "Post-Punk", "country": "USA"},
        {"id": "Velvet_Underground", "name": "The Velvet Underground", "type": "band", "genre": "Post-Punk", "country": "USA", "formed_year": 1964},
        {"id": "Primal_Scream", "name": "Primal Scream", "type": "band", "genre": "Alternative Rock", "country": "UK", "formed_year": 1982},
        {"id": "Bobby_Gillespie", "name": "Bobby Gillespie", "type": "person", "genre": "Alternative Rock", "country": "UK"},
        {"id": "Jesus_and_Mary_Chain", "name": "The Jesus and Mary Chain", "type": "band", "genre": "Shoegaze", "country": "UK", "formed_year": 1983},
        {"id": "Jim_ORourke", "name": "Jim O'Rourke", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "USA"},
        {"id": "Wilco", "name": "Wilco", "type": "band", "genre": "Indie Rock", "country": "USA", "formed_year": 1994},
        {"id": "Jeff_Tweedy", "name": "Jeff Tweedy", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "Patti_Smith", "name": "Patti Smith", "type": "person", "genre": "Post-Punk", "country": "USA"},
        {"id": "Alan_McGee", "name": "Alan McGee (Creation Records)", "type": "person", "type_role": "producer", "genre": "Shoegaze", "country": "UK"},
        # Queens of the Stone Age & Desert Rock Super-Bridges
        {"id": "Kyuss", "name": "Kyuss", "type": "band", "genre": "Alternative Rock", "country": "USA", "formed_year": 1987},
        {"id": "Mark_Lanegan", "name": "Mark Lanegan", "type": "person", "genre": "Grunge", "country": "USA"},
        {"id": "Chris_Goss", "name": "Chris Goss (Masters of Reality)", "type": "person", "type_role": "producer", "genre": "Alternative Rock", "country": "USA"},
        {"id": "Them_Crooked_Vultures", "name": "Them Crooked Vultures", "type": "band", "genre": "Alternative Rock", "country": "USA", "formed_year": 2009},
        {"id": "Iggy_Pop", "name": "Iggy Pop", "type": "person", "genre": "Post-Punk", "country": "USA"},
        # Onda 1: Post-Punk 70s/80s
        {"id": "Joy_Division", "name": "Joy Division", "type": "band", "genre": "Post-Punk", "country": "UK", "formed_year": 1976},
        {"id": "New_Order", "name": "New Order", "type": "band", "genre": "Post-Punk", "country": "UK", "formed_year": 1980},
        {"id": "Bernard_Sumner", "name": "Bernard Sumner", "type": "person", "genre": "Post-Punk", "country": "UK"},
        {"id": "The_Cure", "name": "The Cure", "type": "band", "genre": "Post-Punk", "country": "UK", "formed_year": 1978},
        {"id": "Robert_Smith", "name": "Robert Smith", "type": "person", "genre": "Post-Punk", "country": "UK"},
        {"id": "Talking_Heads", "name": "Talking Heads", "type": "band", "genre": "Post-Punk", "country": "USA", "formed_year": 1975},
        {"id": "David_Byrne", "name": "David Byrne", "type": "person", "genre": "Post-Punk", "country": "USA"},
        {"id": "Martin_Hannett", "name": "Martin Hannett", "type": "person", "type_role": "producer", "genre": "Post-Punk", "country": "UK"},
        # Onda 5: Britpop & Trip-Hop (UK 90s)
        {"id": "Blur", "name": "Blur", "type": "band", "genre": "Britpop", "country": "UK", "formed_year": 1988},
        {"id": "Damon_Albarn", "name": "Damon Albarn", "type": "person", "genre": "Britpop", "country": "UK"},
        {"id": "Oasis", "name": "Oasis", "type": "band", "genre": "Britpop", "country": "UK", "formed_year": 1991},
        {"id": "Noel_Gallagher", "name": "Noel Gallagher", "type": "person", "genre": "Britpop", "country": "UK"},
        {"id": "Massive_Attack", "name": "Massive Attack", "type": "band", "genre": "Britpop", "country": "UK", "formed_year": 1988},
        {"id": "Portishead", "name": "Portishead", "type": "band", "genre": "Britpop", "country": "UK", "formed_year": 1991},
        {"id": "Radiohead", "name": "Radiohead", "type": "band", "genre": "Alternative Rock", "country": "UK", "formed_year": 1985},
        {"id": "Thom_Yorke", "name": "Thom Yorke", "type": "person", "genre": "Alternative Rock", "country": "UK"},
        # Onda 4: Post-Rock / Emo 90s
        {"id": "Slint", "name": "Slint", "type": "band", "genre": "Post-Rock", "country": "USA", "formed_year": 1986},
        {"id": "Mogwai", "name": "Mogwai", "type": "band", "genre": "Post-Rock", "country": "UK", "formed_year": 1995},
        {"id": "Tortoise", "name": "Tortoise", "type": "band", "genre": "Post-Rock", "country": "USA", "formed_year": 1990},
        {"id": "John_McEntire", "name": "John McEntire", "type": "person", "type_role": "producer", "genre": "Post-Rock", "country": "USA"},
        {"id": "Sunny_Day_Real_Estate", "name": "Sunny Day Real Estate", "type": "band", "genre": "Math Rock / Emo", "country": "USA", "formed_year": 1992},
        # Onda 6: 2000s Garage Revival & Post-Punk Revival
        {"id": "The_Strokes", "name": "The Strokes", "type": "band", "genre": "Indie Rock", "country": "USA", "formed_year": 1998},
        {"id": "Julian_Casablancas", "name": "Julian Casablancas", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "Interpol", "name": "Interpol", "type": "band", "genre": "Indie Rock", "country": "USA", "formed_year": 1997},
        {"id": "Paul_Banks", "name": "Paul Banks", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "Arctic_Monkeys", "name": "Arctic Monkeys", "type": "band", "genre": "Indie Rock", "country": "UK", "formed_year": 2002},
        {"id": "Alex_Turner", "name": "Alex Turner", "type": "person", "genre": "Indie Rock", "country": "UK"},
        {"id": "The_White_Stripes", "name": "The White Stripes", "type": "band", "genre": "Indie Rock", "country": "USA", "formed_year": 1997},
        {"id": "Jack_White", "name": "Jack White", "type": "person", "genre": "Indie Rock", "country": "USA"},
        {"id": "TV_on_the_Radio", "name": "TV on the Radio", "type": "band", "genre": "Indie Rock", "country": "USA", "formed_year": 2001},
        {"id": "Dave_Sitek", "name": "Dave Sitek", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "USA"},
        {"id": "LCD_Soundsystem", "name": "LCD Soundsystem", "type": "band", "genre": "Dance-Punk", "country": "USA", "formed_year": 2002},
        {"id": "James_Murphy", "name": "James Murphy (DFA)", "type": "person", "type_role": "producer", "genre": "Dance-Punk", "country": "USA"},
        {"id": "Gordon_Raphael", "name": "Gordon Raphael", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "USA"},
        {"id": "Dave_Fridmann", "name": "Dave Fridmann", "type": "person", "type_role": "producer", "genre": "Indie Rock", "country": "USA"}
    ]

    for n in new_legendary_nodes:
        if n["id"] not in existing_node_ids:
            data["nodes"].append(n)
            existing_node_ids[n["id"]] = n

    new_historic_edges = [
        # Queens of the Stone Age & Josh Homme Connections
        ("Dave_Grohl", "Queens_of_the_Stone_Age", "guest", "Baterista Principal no Álbum 'Songs for the Deaf' e Turnê", 97, ["Songs for the Deaf", "No One Knows"]),
        ("Dave_Grohl", "Them_Crooked_Vultures", "member", "Baterista e Vocalista de Apoio do Supergrupo", 96, ["Them Crooked Vultures"]),
        ("Josh_Homme", "Them_Crooked_Vultures", "member", "Vocalista, Guitarrista e Co-fundador com Dave Grohl e John Paul Jones", 96, ["Them Crooked Vultures"]),
        ("Josh_Homme", "Kyuss", "member", "Guitarrista Principal e Co-fundador do Kyuss (Pioneiro do Desert/Stoner Rock)", 95, ["Blues for the Red Sun", "Welcome to Sky Valley"]),
        ("Chris_Goss", "Queens_of_the_Stone_Age", "producer", "Produtor e Mentor dos Álbuns 'Rated R' e 'Songs for the Deaf'", 94, ["Rated R", "Songs for the Deaf"]),
        ("Chris_Goss", "Kyuss", "producer", "Produtor dos Álbuns Clássicos do Kyuss", 93, ["Blues for the Red Sun"]),
        ("Mark_Lanegan", "Queens_of_the_Stone_Age", "member", "Co-vocalista Oficial e Compositor nos Álbuns 'Rated R' e 'Songs for the Deaf'", 95, ["Songs for the Deaf", "In the Fade", "Hangin' Tree"]),
        ("Mark_Lanegan", "Nirvana", "collaboration", "Parceria de Gravação com Kurt Cobain e Krist Novoselic (The Jury)", 92, ["Where Did You Sleep Last Night", "The Winding Sheet"]),
        ("Josh_Homme", "Iggy_Pop", "producer", "Produtor, Co-compositor e Guitarrista do Álbum 'Post Pop Depression'", 95, ["Post Pop Depression", "Gardenia"]),
        ("Trent_Reznor", "Josh_Homme", "collaboration", "Parcerias de Trilha Sonora, Trilha 'Sound City (Mantra)' e Feat em '...Like Clockwork'", 93, ["Mantra", "...Like Clockwork"]),
        ("Trent_Reznor", "Queens_of_the_Stone_Age", "guest", "Vocais e Sintetizadores Convidado na Faixa 'Kalopsia'", 91, ["...Like Clockwork"]),

        # Post-Punk 70s / 80s Bridges
        ("Bernard_Sumner", "Joy_Division", "member", "Guitarrista e Co-fundador do Joy Division", 98, ["Unknown Pleasures", "Closer"]),
        ("Bernard_Sumner", "New_Order", "member", "Vocalista Principal e Co-fundador do New Order", 98, ["Blue Monday", "Power, Corruption & Lies"]),
        ("Martin_Hannett", "Joy_Division", "producer", "Produtor Lendário dos Álbuns 'Unknown Pleasures' e 'Closer'", 99, ["Unknown Pleasures", "Closer"]),
        ("Martin_Hannett", "New_Order", "producer", "Produtor do Single Estreia 'Movement'", 94, ["Movement"]),
        ("Martin_Hannett", "Happy_Mondays", "producer", "Produtor do Álbum 'Bummed'", 92, ["Bummed"]),
        ("Robert_Smith", "The_Cure", "member", "Líder, Vocalista e Compositor do The Cure", 98, ["Disintegration", "Boys Don't Cry"]),
        ("Robert_Smith", "Siouxsie_and_the_Banshees", "member", "Guitarrista Oficial da Banda (1982-1984)", 95, ["Hyaena", "Nocturne"]),
        ("David_Byrne", "Talking_Heads", "member", "Vocalista Principal e Frontman do Talking Heads", 97, ["Remain in Light", "Stop Making Sense"]),
        ("Brian_Eno", "Talking_Heads", "producer", "Produtor dos Álbuns Clássicos 'Remain in Light' e 'More Songs About Buildings and Food'", 99, ["Remain in Light", "Fear of Music"]),
        ("Brian_Eno", "David_Byrne", "collaboration", "Álbum Colaborativo Pioneiro 'My Life in the Bush of Ghosts'", 96, ["My Life in the Bush of Ghosts"]),
        ("Brian_Eno", "U2", "producer", "Co-produtor de 'The Joshua Tree' e 'Achtung Baby' com Daniel Lanois", 98, ["The Joshua Tree", "Achtung Baby"]),

        # Britpop, Trip-Hop & UK 90s Bridges
        ("Damon_Albarn", "Blur", "member", "Vocalista Principal e Co-fundador do Blur", 97, ["Parklife", "13"]),
        ("Damon_Albarn", "Gorillaz", "member", "Criador e Mente Criativa do Gorillaz", 98, ["Demon Days", "Plastic Beach"]),
        ("Damon_Albarn", "Massive_Attack", "guest", "Vocalista Convidado em Faixas do Massive Attack", 93, ["Heligoland"]),
        ("Noel_Gallagher", "Oasis", "member", "Compositor Principal e Guitarrista do Oasis", 97, ["Definitely Maybe", "(What's the Story) Morning Glory?"]),
        ("Noel_Gallagher", "Chemical_Brothers", "guest", "Vocal Convidado nas Faixas 'Setting Sun' e 'Let Forever Be'", 95, ["Setting Sun", "Let Forever Be"]),
        ("Thom_Yorke", "Radiohead", "member", "Vocalista e Compositor do Radiohead", 98, ["OK Computer", "Kid A"]),
        ("Nigel_Godrich", "Radiohead", "producer", "Considerado o 'Sexto Integrante' e Produtor de Todos os Álbuns desde OK Computer", 99, ["OK Computer", "Kid A", "In Rainbows"]),
        ("Nigel_Godrich", "Beck", "producer", "Produtor dos Álbuns 'Mutations' e 'Sea Change'", 96, ["Sea Change"]),
        ("Nigel_Godrich", "Air", "producer", "Produtor do Álbum 'Talkie Walkie'", 93, ["Talkie Walkie"]),
        ("3D_Robert_Del_Naja", "Massive_Attack", "member", "Fundador e Vocalista/Produtor do Massive Attack", 96, ["Blue Lines", "Mezzanine"]),
        ("Portishead", "Massive_Attack", "collaboration", "Pioneiros da Cena Trip-Hop de Bristol", 95, ["Bristol Trip-Hop Movement"]),

        # Post-Rock & Math Rock 90s Bridges
        ("Slint", "Tortoise", "collaboration", "Pioneiros do Post-Rock Americano nos Anos 90", 94, ["Spiderland", "Millions Now Living Will Never Die"]),
        ("John_McEntire", "Tortoise", "member", "Baterista, Produtor e Mente Criativa do Tortoise", 95, ["Millions Now Living Will Never Die"]),
        ("John_McEntire", "Stereolab", "producer", "Produtor do Álbum 'Emperor Tomato Ketchup'", 95, ["Emperor Tomato Ketchup"]),
        ("Sunny_Day_Real_Estate", "Foo_Fighters", "member", "Nate Mendel e William Goldsmith Migraram do SDRE para o Foo Fighters", 94, ["Diary", "Foo Fighters"]),

        # 2000s Garage Revival & Post-Punk Revival Bridges
        ("Julian_Casablancas", "The_Strokes", "member", "Vocalista e Compositor do The Strokes", 97, ["Is This It", "Room on Fire"]),
        ("Gordon_Raphael", "The_Strokes", "producer", "Produtor do Álbum de Estreia Revolucionário 'Is This It'", 98, ["Is This It", "Room on Fire"]),
        ("Paul_Banks", "Interpol", "member", "Vocalista e Guitarrista do Interpol", 95, ["Turn On the Bright Lights"]),
        ("Alex_Turner", "Arctic_Monkeys", "member", "Vocalista e Compositor do Arctic Monkeys", 97, ["Whatever People Say I Am...", "AM"]),
        ("Alex_Turner", "Miles_Kane", "member", "Membros do Supergrupo The Last Shadow Puppets", 94, ["The Age of the Understatement"]),
        ("Jack_White", "The_White_Stripes", "member", "Guitarrista, Vocalista e Co-fundador do The White Stripes", 98, ["White Blood Cells", "Elephant"]),
        ("Jack_White", "The_Raconteurs", "member", "Fundador do Supergrupo The Raconteurs", 95, ["Broken Boy Soldiers"]),
        ("Jack_White", "Beck", "producer", "Produtor e Colaborador de Singles", 93, ["Go It Alone"]),
        ("Dave_Sitek", "TV_on_the_Radio", "member", "Guitarrista e Produtor do TV on the Radio", 95, ["Dear Science"]),
        ("Dave_Sitek", "Foals", "producer", "Produtor do Álbum 'Antidotes'", 92, ["Antidotes"]),
        ("Dave_Sitek", "Yeah_Yeah_Yeahs", "producer", "Produtor do Álbum 'It's Blitz!'", 94, ["It's Blitz!"]),
        ("James_Murphy", "LCD_Soundsystem", "member", "Fundador e Líder do LCD Soundsystem", 97, ["Sound of Silver", "This Is Happening"]),
        ("James_Murphy", "Arcade_Fire", "producer", "Produtor do Álbum 'Reflektor'", 95, ["Reflektor"]),
        ("Dave_Fridmann", "The_Flaming_Lips", "producer", "Produtor dos Álbuns Clássicos 'The Soft Bulletin' e 'Yoshimi Battles the Pink Robots'", 98, ["The Soft Bulletin", "Yoshimi Battles the Pink Robots"]),
        ("Dave_Fridmann", "Weezer", "producer", "Produtor do 'Pinkerton'", 96, ["Pinkerton"]),
        ("Dave_Fridmann", "Mogwai", "producer", "Produtor de 'Come On Die Young' e 'Every Country's Sun'", 94, ["Come On Die Young"]),

        # Sonic Youth Bridges
        ("Sonic_Youth", "Nirvana", "member", "Mentoria, Turnê de 1991 e Filme '1991: The Year Punk Broke'", 95, ["1991: The Year Punk Broke", "Tour 1991"]),
        ("Kim_Gordon", "The_Breeders", "producer", "Produtora do Álbum de Estreia 'Pod' do Breeders", 92, ["Pod"]),
        ("Sonic_Youth", "Indie_Pavement", "guest", "Mentoria Inicial e Turnês Conjuntas nos Anos 90", 91, ["Pavement / SY Tours"]),
        ("Thurston_Moore", "Stephen_Malkmus", "collaboration", "Parcerias de Improviso Noise e Festivais", 89, ["Noise Sessions"]),
        ("Jim_ORourke", "Sonic_Youth", "member", "Integrante Oficial da Banda (1999-2005)", 93, ["NYC Ghosts & Flowers", "Sonic Nurse"]),
        ("Jim_ORourke", "Wilco", "producer", "Produtor e Mixador de 'Yankee Hotel Foxtrot'", 97, ["Yankee Hotel Foxtrot", "A Ghost Is Born"]),
        ("Jeff_Tweedy", "Wilco", "member", "Frontman e Compositor do Wilco", 95, ["Yankee Hotel Foxtrot", "Summerteeth"]),

        # John Cale & Lou Reed Bridges
        ("Lou_Reed", "Velvet_Underground", "member", "Vocalista, Guitarrista e Compositor Principal", 98, ["The Velvet Underground & Nico", "White Light/White Heat"]),
        ("John_Cale", "Velvet_Underground", "member", "Co-fundador, Viola Elétrica e Baixo", 98, ["The Velvet Underground & Nico"]),
        ("John_Cale", "Lou_Reed", "collaboration", "Álbum Conjunto Homenagem a Andy Warhol 'Songs for Drella'", 94, ["Songs for Drella"]),
        ("John_Cale", "Brian_Eno", "collaboration", "Álbum Conjunto 'Wrong Way Up'", 92, ["Wrong Way Up"]),
        ("Lou_Reed", "Gorillaz", "guest", "Vocal Convidado na Faixa 'Some Kind of Nature'", 89, ["Plastic Beach"]),
        ("Lou_Reed", "Metric", "guest", "Vocal Convidado na Faixa 'Wanderlust'", 87, ["Synthetica"]),

        # Kevin Shields & Creation Records Bridges
        ("Kevin_Shields", "Primal_Scream", "member", "Guitarrista e Produtor Oficial da Banda", 94, ["XTRMNTR", "Evil Heat"]),
        ("Bobby_Gillespie", "Primal_Scream", "member", "Vocalista e Líder do Primal Scream", 93, ["Screamadelica", "XTRMNTR"]),
        ("Bobby_Gillespie", "Jesus_and_Mary_Chain", "member", "Baterista Original no Álbum 'Psychocandy'", 95, ["Psychocandy"]),
        ("Jesus_and_Mary_Chain", "My_Bloody_Valentine", "collaboration", "Pioneiros da Cena Shoegaze / Turnês da Creation Records", 94, ["Creation Records Tours"]),
        ("Kevin_Shields", "Patti_Smith", "collaboration", "Álbum Colaborativo Duplo 'The Coral Sea'", 90, ["The Coral Sea"]),
        ("Kevin_Shields", "Yo_La_Tengo", "guest", "Remixes e Colaborações de Guitarra", 88, ["Yo La Tengo Remixes"]),
        ("Alan_McGee", "My_Bloody_Valentine", "producer", "Fundador da Creation Records e Produtor do MBV", 96, ["Loveless"]),
        ("Alan_McGee", "Oasis", "producer", "Descobridor e Assinador do Oasis na Creation Records", 95, ["Definitely Maybe"]),
        ("Alan_McGee", "Primal_Scream", "producer", "Produtor e Empresário da Banda", 94, ["Screamadelica"]),
        ("Alan_McGee", "Slowdive", "producer", "Assinador e Produtor da Banda na Creation", 92, ["Souvlaki"])
    ]

    added = 0
    for src, tgt, rel_t, desc, score, works in new_historic_edges:
        if src in existing_node_ids and tgt in existing_node_ids:
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
                added += 1

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Pontes Históricas Lendárias Injetadas: +{added} arestas vitais unificando Sonic Youth, Velvet Underground e MBV!")

if __name__ == "__main__":
    inject_historic_bridges()
