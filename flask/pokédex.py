import pokebase as pb
import json


# File path to store the cached data
CACHE_FILE_PATH = 'pokemon_cache.json'

# Load cached data from file if it exists
try:
    with open(CACHE_FILE_PATH, 'r') as file:
        pokemon_cache = json.load(file)
except json.decoder.JSONDecodeError:
    pokemon_cache = []

# Save cached data to file when the server shuts down
def save_cache_to_file():
    with open(CACHE_FILE_PATH, 'w') as file:
        json.dump(pokemon_cache, file)
        file.close()

# Your existing dex function remains unchanged
def dex(selected_mon):
    no_sv = False
    cached = False
    if "alolan" in selected_mon:
        selected_mon = (selected_mon.split("-")[1] + "-alola")
    for j in pokemon_cache:
        if j["Name"] == selected_mon.title():
            cached = True
            attributes = j
    if cached == False:  
        pokemon = pb.pokemon(selected_mon)
        attributes = {
            "Abilities": {
                "Ability 1": "",
                "Ability 2": "N/A",
                "HA": "N/A"
            },
            "In Scarlet/Violet?": no_sv,
            "Dex Number": pokemon.order,
            "Height": f"{pokemon.height / 10} meters / {round((pokemon.height / 3.048), 2)} ft",  # Convert height from decimetres to metres
            "Weight": f"{pokemon.weight / 10} kilograms / {round((pokemon.weight / 4.536), 2)} pounds",
            "Sprites": {
                "Front Sprite": pokemon.sprites.front_default if not pokemon.sprites.other.showdown.front_default else pokemon.sprites.other.showdown.front_default,
                "Front Shiny Sprite": pokemon.sprites.front_shiny if not pokemon.sprites.other.showdown.front_shiny else pokemon.sprites.other.showdown.front_shiny, 
                "Back Sprite": pokemon.sprites.back_default if not pokemon.sprites.other.showdown.back_default else pokemon.sprites.other.showdown.back_default,
                "Back Shiny Sprite": pokemon.sprites.back_shiny if not pokemon.sprites.other.showdown.back_shiny else pokemon.sprites.other.showdown.back_shiny
            },
            "Moves": {
                "Level Up Learnset": [],
                "TM Learnset": [],
                "Breeding Learnset": [{
                            "TM": "",
                            "Move": "",
                            "Type": "",
                            "Category": "",
                            "Power": "",
                            "Accuracy": "",
                            "PP": ""
                        }]
                },
            "Name": (str(pokemon.name)).title().replace('-',' '),
            "Types": {
                "Type 1": (pokemon.types[0].type.name).capitalize() if len(pokemon.types) >= 1 else "",
                "Type 2": (pokemon.types[1].type.name).capitalize() if len(pokemon.types) >= 2 else ""
            },
            "Stats": {
                "HP": pokemon.stats[0].base_stat,
                "Attack": pokemon.stats[1].base_stat,
                "Defense": pokemon.stats[2].base_stat,
                "Special Attack": pokemon.stats[3].base_stat,
                "Special Defense": pokemon.stats[4].base_stat,
                "Speed": pokemon.stats[5].base_stat
            }
        }
        
        # Extract abilities
        for ability in pokemon.abilities:
            if ability.is_hidden:
                attributes["Abilities"]["HA"] = ability.ability.name.replace('-', ' ').title()
            elif not attributes["Abilities"]["Ability 1"]:
                attributes["Abilities"]["Ability 1"] = ability.ability.name.replace('-', ' ').title()
            else:
                attributes["Abilities"]["Ability 2"] = ability.ability.name.replace('-', ' ').title()
        
        if attributes["Abilities"]["HA"] == attributes["Abilities"]["Ability 1"]:
            attributes["Abilities"]["HA"] = "N/A"
                
        counter = 0
        # Iterate over each move associated with the Pokémon
        for i in range(len(pokemon.moves)):
            # Initialize dictionaries to store move details
            lvl_learnset = {}  # For level-up learnset
            tm_learnset = {}   # For TM learnset
            
            # Extract the move and its name
            pmi = pokemon.moves[i]
            movename = pmi.move
            
            # Iterate over version details of the move
            for j in range(len(pmi.version_group_details)):
                version = pmi.version_group_details[j]
                
                # Check if the move is available in the "scarlet-violet" version group
                if version.version_group.name == "scarlet-violet":
                    # Check the learning method of the move
                    if version.move_learn_method.name == "level-up":
                        # If the move is learned through level-up, populate lvl_learnset dictionary
                        lvl_learnset = {
                            "Level Learned": version.level_learned_at,
                            "Move": movename.name.replace('-', ' ').title(),
                            "Type": movename.type.name.replace('-', ' ').title(),
                            "Category": movename.damage_class.name.replace('-', ' ').title(),
                            "Power": movename.power,
                            "Accuracy": movename.accuracy,
                            "PP": movename.pp
                        }
                        # Append lvl_learnset to the list under "Level Up Learnset"
                        attributes["Moves"]["Level Up Learnset"].append(lvl_learnset)
                    elif version.move_learn_method.name == "machine":
                        # If the move is learned via TM, populate tm_learnset dictionary
                        if counter == 0:
                            attributes["Moves"]["TM Learnset"] = []  # Initialize TM Learnset list
                        tm_learnset = {
                            "TM": "N/A",
                            "Move": movename.name.replace('-', ' ').title(),
                            "Type": movename.type.name.replace('-', ' ').title(),
                            "Category": movename.damage_class.name.replace('-', ' ').title(),
                            "Power": movename.power,
                            "Accuracy": movename.accuracy,
                            "PP": movename.pp
                        }
                        # Append tm_learnset to the list under "TM Learnset"
                        attributes["Moves"]["TM Learnset"].append(tm_learnset)
                        counter += 1  # Increment counter to prevent re-initialization of TM Learnset list
        if len(attributes["Moves"]["Level Up Learnset"]) == 0:
            no_sv = True
             # Initialize dictionaries to store move details
            lvl_learnset = {}  # For level-up learnset
            tm_learnset = {}   # For TM learnset
            
            # Extract the move and its name
            pmi = pokemon.moves[i]
            movename = pmi.move
            
            # Iterate over version details of the move
            for j in range(len(pmi.version_group_details)):
                version = pmi.version_group_details[j]
                
                # Check if the move is available in the "sword-shield" version group
                if version.version_group.name == "sword-shield":
                    # Check the learning method of the move
                    if version.move_learn_method.name == "level-up":
                        # If the move is learned through level-up, populate lvl_learnset dictionary
                        lvl_learnset = {
                            "Level Learned": version.level_learned_at,
                            "Move": movename.name.replace('-', ' ').title(),
                            "Type": movename.type.name.replace('-', ' ').title(),
                            "Category": movename.damage_class.name.replace('-', ' ').title(),
                            "Power": movename.power,
                            "Accuracy": movename.accuracy,
                            "PP": movename.pp
                        }
                        # Append lvl_learnset to the list under "Level Up Learnset"
                        attributes["Moves"]["Level Up Learnset"].append(lvl_learnset)
                    elif version.move_learn_method.name == "machine":
                        # If the move is learned via TM, populate tm_learnset dictionary
                        if counter == 0:
                            attributes["Moves"]["TM Learnset"] = []  # Initialize TM Learnset list
                        tm_learnset = {
                            "TM": "N/A",
                            "Move": movename.name.replace('-', ' ').title(),
                            "Type": movename.type.name.replace('-', ' ').title(),
                            "Category": movename.damage_class.name.replace('-', ' ').title(),
                            "Power": movename.power,
                            "Accuracy": movename.accuracy,
                            "PP": movename.pp
                        }
                        # Append tm_learnset to the list under "TM Learnset"
                        attributes["Moves"]["TM Learnset"].append(tm_learnset)
                        counter += 1  # Increment counter to prevent re-initialization of TM Learnset list     

        attributes["Moves"]["Level Up Learnset"] = sorted(attributes["Moves"]["Level Up Learnset"], key=lambda x: x["Level Learned"])
        attributes["Moves"]["TM Learnset"] = sorted(attributes["Moves"]["TM Learnset"], key=lambda x: x["Type"])              
        pokemon_cache.append(attributes)
        save_cache_to_file()
    return attributes

