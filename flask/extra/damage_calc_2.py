import math
import pokebase as pb

# Function to calculate stats of a Pokemon
def calculate_stats(pokemon, stat_index, iv, ev, level):
    base_stat = pokemon.stats[stat_index].base_stat
    stat = math.floor(((2 * base_stat + iv + math.floor(ev / 4)) * level) / 100) + 5
    return stat

# Function to calculate basic damage inflicted by a move
def basic_damage(selected_move, selected_user, selected_target):
    # Retrieve move, user, and target information from the Pokebase API
    used_move = pb.move(selected_move)
    chosen_user = pb.pokemon(selected_user)
    chosen_target = pb.pokemon(selected_target)
    
    # Initialize variables to track damage modifiers
    super_effective, not_very_effective, immune = False, False, False
    
    # Calculate maximum HP of the target Pokemon
    chosen_target_hp = math.floor(((2 * chosen_target.stats[0].base_stat + 31 + math.floor(0.25 * 252)) * 100) / 100) + 100 + 10
    
    # Determine if the move is physical or special and calculate user's attack and target's defense accordingly
    if used_move.damage_class.name == 'special':
        chosen_user_attack = calculate_stats(chosen_user, 3)
        chosen_target_defense = calculate_stats(chosen_target, 4)
    elif used_move.damage_class.name == 'physical':     
        chosen_user_attack = calculate_stats(chosen_user, 1)
        chosen_target_defense = calculate_stats(chosen_target, 2)
    
    # Calculate damage using the damage formula
    damage = round(((((((2 * 100) / 5) + 2) * used_move.power * (chosen_user_attack / chosen_target_defense)) / 50) + 2))
    
    # Check for type effectiveness modifiers
    for i in range(len(chosen_target.types)):
        type_check = pb.APIResource('type', chosen_target.types[i].type.name)
        for j in range(len(type_check.damage_relations.double_damage_from)):
            if used_move.type.name == type_check.damage_relations.double_damage_from[j].name:
                damage *= 2
                super_effective = True
        for k in range(len(type_check.damage_relations.half_damage_from)):
            if used_move.type.name == type_check.damage_relations.half_damage_from[k].name:
                damage /= 2
                not_very_effective = True
        for l in range(len(type_check.damage_relations.no_damage_from)):
            if used_move.type.name == type_check.damage_relations.no_damage_from[l].name:
                damage = 0
                immune = True
                break
    
    # Apply same-type attack bonus (STAB) if the user's type matches the move's type
    if not immune:
        for m in range(len(chosen_user.types)):
            if used_move.type.name == chosen_user.types[m].type.name:
                damage *= 1.5
        
        damage = round(damage)
        
        # Calculate minimum and maximum HP remaining after damage
        min_hp_remaining = int(chosen_target_hp - damage)
        min_hp_remaining = max(0, min_hp_remaining)
        
        max_hp_remaining = int(chosen_target_hp - damage) * 0.85
        max_hp_remaining = max(0, max_hp_remaining)
    else:
        # If the target is immune to the move, set both min and max HP remaining to current HP
        max_hp_remaining = min_hp_remaining = chosen_target_hp
    
    # Store damage information in a dictionary
    damage_info = {
        "Max HP Remaining": f"{max_hp_remaining}/{chosen_target_hp}",
        "Min HP Remaining": f"{min_hp_remaining}/{chosen_target_hp}",
        "Super Effective": super_effective,
        "Not Very Effective": not_very_effective,
        "Immune": immune
    }
    return damage_info