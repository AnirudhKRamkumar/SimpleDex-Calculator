import math
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



def moveListGenerator(selected_user):
    cached = False
    movelist = []
    try:
        for j in pokemon_cache:
            if j["Name"] == selected_user.title():
                cached = True
                for move1 in j["Moves"]["TM Learnset"]:
                    if move1["Move"] not in movelist:
                        movelist.append(move1["Move"])
                for move2 in j["Moves"]["Level Up Learnset"]:
                    if move2["Move"] not in movelist:
                        movelist.append(move2["Move"])
        if cached == False:
            user = pb.pokemon(selected_user)
            for mov in user.moves:
                movelist.append((mov.move.name).replace('-', ' ').title()) 
        print(type(movelist))  
        return movelist
    except AttributeError:
        return None
    
    
# Function to calculate basic damage inflicted by a move
def basic_damage(selected_move, selected_user, selected_target):
    # Retrieve move, user, and target information from the Pokebase API
    move = pb.move(selected_move)
    user = pb.pokemon(selected_user)
    target = pb.pokemon(selected_target)
    
    # Initialize variables to track damage modifiers
    super_effective, not_very_effective, immune = False, False, False
    
    
    # Calculate maximum HP of the target Pokemon
    target_hp = (math.floor((2 * target.stats[0].base_stat + 31 + math.floor(0.25 * 252))) + 100 + 10)
    
    # Determine if the move is physical or special and calculate user's attack and target's defense accordingly
    if move.damage_class.name == 'special':
        user_attack = math.floor((2 * user.stats[3].base_stat + 31 + math.floor(0.25 * 252))) + 5
        target_defense = math.floor((2 * target.stats[4].base_stat + 31 + math.floor(0.25 * 252))) + 5
    elif move.damage_class.name == 'physical':     
        user_attack = math.floor((2 * user.stats[1].base_stat + 31 + math.floor(0.25 * 252))) + 5
        target_defense = math.floor((2 * target.stats[2].base_stat + 31 + math.floor(0.25 * 252))) + 5
    
    # Calculate damage using the damage formula
    damage = round(((((((2 * 100) / 5) + 2) * move.power * (user_attack / target_defense)) / 50) + 2))
    # Check for type effectiveness modifiers
    for i in range(len(target.types)):
        type_check = pb.APIResource('type', target.types[i].type.name)
        for j in range(len(type_check.damage_relations.double_damage_from)):
            if move.type.name == type_check.damage_relations.double_damage_from[j].name:
                damage *= 2
                super_effective = True
        for k in range(len(type_check.damage_relations.half_damage_from)):
            if move.type.name == type_check.damage_relations.half_damage_from[k].name:
                damage /= 2
                not_very_effective = True
        for l in range(len(type_check.damage_relations.no_damage_from)):
            if move.type.name == type_check.damage_relations.no_damage_from[l].name:
                damage = 0
                immune = True
                break
    if super_effective & not_very_effective:
        super_effective = not_very_effective = False
    if immune & (super_effective or not_very_effective):
        super_effective = not_very_effective = False
        immune = True
    
    
    # Apply same-type attack bonus (STAB) if the user's type matches the move's type
    if not immune:
        for m in range(len(user.types)):
            if move.type.name == user.types[m].type.name:
                damage *= 1.5
        
        damage = round(damage)

        # Calculate minimum and maximum HP remaining after damage
        min_hp_remaining = int(target_hp - damage)
        min_hp_remaining = max(0, min_hp_remaining)

        max_hp_remaining = int(target_hp - (damage * 0.85))
        max_hp_remaining = max(0, max_hp_remaining)
    else:
        # If the target is immune to the move, set both min and max HP remaining to current HP
        max_hp_remaining = min_hp_remaining = target_hp
    
    # Store damage information in a dictionary
    damage_info = {
        "Max HP Remaining": max_hp_remaining,
        "Min HP Remaining": min_hp_remaining,
        "Target Max HP": target_hp,
        "Super Effective": super_effective,
        "Not Very Effective": not_very_effective,
        "Immune": immune
    }
    return damage_info