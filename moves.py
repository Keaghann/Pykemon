#Final Project - Keaghan Irwin - CS30
#This file is just one big dict storing every move and their functions
import pygame as pg
import pygame.math as pm
import pygame.image as pp
import pygame.display as pd
import random
import abilities
import items

stat_modifiers = [2/8, 2/7, 2/6, 2/5, 2/4, 2/3, 1, 3/2, 4/2, 5/2, 6/2, 7/2, 8/2]

class Move:
    def __init__(self, name, typing, category, pp, power, accuracy, gimmick, priority, contact, protect, magic_coat, snatch, mirror_move, kings_rock, effect):
        self.typing = typing; self.category = category;  self.name = name; self.pp = pp; self.power = power; self.accuracy = accuracy
        self.gimmick = gimmick; self.priority = priority; self.effect = effect; self.contact = contact; self.protect = protect; self.snatch = snatch
        self.magic_coat = magic_coat; self.mirror_move = mirror_move; self.kings_rock = kings_rock; self.current_pp = pp

def determine_effectiveness(opponent, move):
    effectiveness = 1; typing = move.typing
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): effectiveness = 0
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[203].name): typing = "Water"
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): effectiveness = 0
        if (i == "spore"):
            for j in opponent.typing:
                if (j == "Grass"): effectiveness *= 0
        if (i == "spore" and opponent.ability.name == abilities.ability_dex[141].name): effectiveness = 0
    for i in opponent.typing:
        if (i == 'Normal'):
            if (typing == 'Fighting'): effectiveness *= 2
            elif (typing == 'Ghost'): effectiveness *= 0
        elif (i == 'Fire'):
            if (typing == 'Water' or typing == 'Ground' or typing == 'Rock'): effectiveness *= 2
            elif (typing == 'Fire' or typing == 'Grass' or typing == 'Ice' or typing == 'Bug' or typing == 'Steel' or typing == 'Fairy'): effectiveness /= 2
        elif (i == 'Water'):
            if (typing == 'Grass' or typing == 'Electric'): effectiveness *= 2
            elif (typing == 'Fire' or typing == 'Water' or typing == 'Ice' or typing == 'Steel'): effectiveness /= 2
        elif (i == 'Grass'):
            if (typing == 'Fire' or typing == 'Ice' or typing == 'Poison' or typing == 'Flying' or typing == 'Bug'): effectiveness *= 2
            elif (typing == 'Water' or typing == 'Grass' or typing == 'Electric' or typing == 'Ground'): effectiveness /= 2
        elif (i == 'Electric'):
            if (typing == 'Ground'): effectiveness *= 2
            elif (typing == 'Electric' or  typing == 'Flying' or typing == 'Steel'): effectiveness /= 2
        elif (i == 'Ice'):
            if (typing == 'Fire' or typing == 'Fighting' or typing == 'Rock' or typing == 'Steel'): effectiveness *= 2
            elif (typing == 'Ice'): effectiveness /= 2
        elif (i == 'Fighting'):
            if (typing == 'Flying' or typing == 'Psychic' or typing == 'Fairy'): effectiveness *= 2
            elif (typing == 'Bug' or typing == 'Rock' or typing == 'Dark'): effectiveness /= 2
        elif (i == 'Poison'):
            if (typing == 'Ground' or typing == 'Psychic'): effectiveness *= 2
            elif (typing == 'Grass' or typing == 'Fighting' or typing == 'Poison' or typing == 'Bug' or typing == 'Fairy'): effectiveness /= 2
        elif (i == 'Ground'):
            if (typing == 'Water' or typing == 'Grass' or typing == 'Ice'): effectiveness *= 2
            elif (typing == 'Poison' or typing == 'Rock'): effectiveness /= 2
            elif (typing == 'Electric'): effectiveness *= 0
        elif (i == 'Flying'):
            if (typing == 'Electric' or typing == 'Ice' or typing == 'Rock'): effectiveness *= 2
            elif (typing == 'Grass' or typing == 'Fighting' or typing == 'Bug'): effectiveness /= 2
            elif (typing == 'Ground'): effectiveness *= 0
        elif (i == 'Psychic'):
            if (typing == 'Bug' or typing == 'Ghost' or typing == 'Dark'): effectiveness *= 2
            if (typing == 'Fighting' or typing == 'Psychic'): effectiveness /= 2
        elif (i == 'Bug'):
            if (typing == 'Fire' or typing == 'Flying' or typing == 'Rock'): effectiveness *= 2
            elif (typing == 'Grass' or typing == 'Fighting' or typing == 'Ground'): effectiveness /= 2
        elif (i == 'Rock'):
            if (typing == 'Water' or typing == 'Grass' or typing == 'Fighting' or typing == 'Ground' or typing == 'Steel'): effectiveness *= 2
            elif (typing == 'Normal' or typing == 'Fire' or typing == 'Poison' or typing == 'Flying'): effectiveness /= 2
        elif (i == 'Ghost'):
            if (typing == 'Normal' or typing == 'Fighting'): effectiveness *= 0
            elif (typing == 'Ghost' or typing == 'Dark'): effectiveness *= 2
            elif (typing == 'Poison' or typing == 'Bug'): effectiveness /= 2
        elif (i == 'Dragon'):
            if (typing == 'Ice' or typing == 'Dragon' or typing == 'Fairy'): effectiveness *= 2
            elif (typing == 'Fire' or typing == 'Water' or typing == 'Grass' or typing == 'Electric'): effectiveness /= 2
        elif (i == 'Dark'):
            if (typing == 'Fighting' or typing == 'Bug' or typing == 'Fairy'): effectiveness *= 2
            elif (typing == 'Ghost' or typing == 'Dark'): effectiveness /= 2
            elif (typing == 'Psychic'): effectiveness *= 0
        elif (i == 'Steel'):
            if (typing == 'Fire' or typing == 'Fighting' or typing == 'Ground'): effectiveness *= 2
            elif (typing == 'Normal' or typing == 'Grass' or typing == 'Ice' or typing == 'Flying' or typing == 'Psychic' or typing == 'Bug' or typing == 'Rock' or typing == 'Dragon'\
                or typing == 'Steel' or typing == 'Fairy'): effectiveness /= 2
            elif (typing == 'Poison'): effectiveness *= 0
        elif (i == 'Fairy'):
            if (typing == 'Poison' or typing == 'Steel'): effectiveness *= 2
            elif (typing == 'Fighting' or typing == 'Bug' or typing == 'Dark'): effectiveness /= 2
            elif (typing == 'Dragon'): effectiveness *= 0
    return effectiveness

def burn(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; burned = 0; rng = random.randint(1, 100); ability_block = 0
    if (move == move_dex[64] or move == move_dex[214] or move == move_dex[243] or move == move_dex[244] or move == move_dex[247] or move == move_dex[882] or move == move_dex[883]\
    or move == move_dex[884] or move == move_dex[333] or move == move_dex[585]): probability = 10
    elif (move == move_dex[70]): probability = 20
    elif (move == move_dex[361] or move == move_dex[372] or move == move_dex[397] or move == move_dex[637] or move == move_dex[641] or move == move_dex[644] or move == move_dex[647]\
    or move == move_dex[736]): probability = 30
    elif (move == move_dex[631]): probability = 50
    if (opponent.ability.name == abilities.ability_dex[101].name and weather == 'Harsh Sunlight'): probability = 0; ability_block = 1
    if (opponent.ability.name == abilities.ability_dex[40].name): probability = 0; ability_block = 1
    for i in opponent.typing:
        if (i == "Fire"): probability = 0
    if (rng <= probability): burned = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, "burn", burned, ability_block)

def freeze(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 10; frozen = 0; rng = random.randint(1, 100); ability_block = 0
    for i in opponent.typing:
        if (i == "Ice"): probability = 0
    if (weather == "Harsh Sunlight"): probability = 0
    for i in terrain:
        if (i == 'misty'): probability = 0
    if (opponent.ability.name == abilities.ability_dex[39].name): probability = 0; ability_block = 1
    if (rng <= probability): frozen = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, "freeze", frozen, ability_block)

def paralysis(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; paralysed = 0; rng = random.randint(1, 100); ability_block = 0
    if (move == move_dex[72] or move == move_dex[168] or move == move_dex[182] or move == move_dex[714] or move == move_dex[268] or move == move_dex[406] or move == move_dex[802]): probability = 30
    elif (move == move_dex[74] or move == move_dex[864]): probability = 20
    elif (move == move_dex[804] or move == move_dex[805] or move == move_dex[806] or move == move_dex[808]): probability = 10
    for i in opponent.typing:
        if (i == "Electric"): probability = 0
    for i in terrain:
        if (i == 'electric' or i == 'misty'): probability = 0
    if ((opponent.ability.name == abilities.ability_dex[101].name and weather == 'Harsh Sunlight') or opponent.ability.name == abilities.ability_dex[6].name): probability *= 0; ability_block = 1
    if (rng <= probability): paralysed = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, "paralysis", paralysed, ability_block)

def sleep(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; asleep = 0; rng = random.randint(1, 100); ability_block = 0
    if (move == move_dex[605]): probability = 10
    if (opponent.ability.name == abilities.ability_dex[14].name or opponent.ability.name == abilities.ability_dex[71].name or opponent.ability.name == abilities.ability_dex[174].name): probability *= 0
    if (opponent.ability.name == abilities.ability_dex[101].name and weather == 'Harsh Sunlight'): probability *= 0; ability_block = 1
    for i in terrain:
        if (i == 'electric' or i == 'misty'): probability = 0
    if (rng <= probability): asleep = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, "sleep", asleep, ability_block)

def poison(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; poisoned = 0; bad_poison = 0; rng = random.randint(1, 100); ability_block = 0
    if (move == move_dex[46]): probability = 50
    elif (move == move_dex[146] or move == move_dex[548] or move == move_dex[694]): probability = 10
    elif (move == move_dex[313] or move == move_dex[545] or move == move_dex[547] or move == move_dex[691] or move == move_dex[693]): probability = 30
    elif (move == move_dex[549]): probability = 30; bad_poison = 1
    elif (move == move_dex[698]): probability = 40
    elif (move == move_dex[815]): bad_poison = 1
    for i in opponent.typing:
        if (user.ability.name != abilities.ability_dex[211].name):
            if (i == 'Steel' or i == 'Poison'): probability = 0
    if (opponent.ability.name == abilities.ability_dex[16].name or opponent.ability.name == abilities.ability_dex[256].name): probability = 0; ability_block = 1
    if (opponent.ability.name == abilities.ability_dex[101].name and weather == 'Harsh Sunlight'): probability *= 0; ability_block = 1
    if (rng <= probability):
        if (bad_poison == 0): poisoned = 1
        else: poisoned = 2
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, "poison", poisoned, ability_block)

def confuse(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; rng = random.randint(1, 100); ability_block = 0; confusion = 0
    if (move == move_dex[42] or move == move_dex[108] or move == move_dex[347]): probability = 30
    elif (move == move_dex[128] or move == move_dex[568] or move == move_dex[672]): probability = 10
    elif (move == move_dex[170] or move == move_dex[617] or move == move_dex[750] or move == move_dex[850]): probability = 20
    if (opponent.ability.name == abilities.ability_dex[19].name): probability = 0; ability_block = 1
    if (rng <= probability): confusion = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, "confuse", confusion, ability_block)

def lower_atk(move, user, opponent, weather, trrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (move == move_dex[38] or move == move_dex[541]): probability = 10
    elif (move == move_dex[61] or move == move_dex[734]): probability = 30
    elif (move == move_dex[107] or move_dex == [235]): stage = 2
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and opponent.current_atk - stage >= 0): opponent.current_atk -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "loweratk", stage, 26, 32)

def lower_def(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (move == move_dex[147] or move == move_dex[411] or move == move_dex[656]): probability = 20
    elif (move == move_dex[148] or move == move_dex[620] or move == move_dex[598]): probability = 50
    elif (move == move_dex[381] or move == move_dex[824]): probability = 30
    elif (move == move_dex[646]): stage = 2
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and opponent.current_def - stage >= 0): opponent.current_def -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerdef", stage, 38, 44)

def lower_spatk(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (move == move_dex[101] or move == move_dex[205]): stage = 2
    elif (move == move_dex[482]): probability = 50
    elif (move == move_dex[485]): probability = 30
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and opponent.current_spatk - stage >= 0): opponent.current_spatk -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerspatk", stage, 50, 56)

def lower_spdef(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (move == move_dex[3] or move == move_dex[91] or move == move_dex[202] or move == move_dex[218] or move == move_dex[253] or move == move_dex[264] or move == move_dex[571]): probability = 10
    elif (move == move_dex[6] or move == move_dex[232] or move == move_dex[467]): stage = 2
    elif (move == move_dex[421]): probability = 50
    elif (move == move_dex[652]): probability = 40; stage = 2
    elif (move == move_dex[655]): probability = 20
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and opponent.current_spdef - stage >= 0): opponent.current_spdef -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerspdef", stage, 62, 68)

def lower_spd(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (move == move_dex[66]): probability = 30
    elif (move == move_dex[88] or move == move_dex[89] or move == move_dex[129]): probability = 10
    elif (move == move_dex[139] or move == move_dex[643] or move == move_dex[753]): stage = 2
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and opponent.current_spd - stage >= 0): opponent.current_spd -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerspd", stage, 74, 80)

def lower_self_def(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and user.current_def - stage >= 0): user.current_def -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and user.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and user.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (user.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in user.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerowndef", stage, 44, 38)

def lower_self_spatk(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (move == move_dex[180] or move == move_dex[255] or move == move_dex[399] or move == move_dex[525] or move == move_dex[574]): stage = 2
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and user.current_spatk - stage >= 0): user.current_spatk -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and user.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and user.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (user.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in user.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerownspatk", stage, 56, 50)

def lower_self_spd(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); lower_stat = 0
    if (rng <= probability): lower_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (lower_stat == 1 and user.current_spd - stage >= 0): user.current_spd -= stage
    if (lower_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and user.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and user.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (user.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in user.typing:
                if (j == "Grass"): stage = 0
    return (damage, "lowerownspd", stage, 80, 74)

def aromatic_mist(move, user, opponent, weather, terrain, seed):
    if (opponent.current_spdef + stage <= 12): opponent.current_spdef += stage
    return (0, "aromaticmist", 1)

def raise_atk(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); raise_stat = 0
    if (move == move_dex[466]): probability = 10
    elif (move == move_dex[470]): probability = 20
    elif (move == move_dex[776]): stage = 2
    if (rng <= probability): raise_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (raise_stat == 1 and opponent.current_atk + stage <= 12): user.current_atk += stage
    if (raise_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "raiseatk", stage, 23, 29)

def raise_def(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); raise_stat = 0
    if (move == move_dex[4] or move == move_dex[48] or move == move_dex[379] or move == move_dex[668]): stage = 2
    elif (move == move_dex[138]): stage = 3
    elif (move == move_dex[163]): probability = 50; stage = 2
    elif (move == move_dex[740]): probability = 10
    if (rng <= probability): raise_stat = 1
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (raise_stat == 1 and opponent.current_def + stage <= 12): user.current_def += stage
    if (raise_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "raisedef", stage, 35, 41)

def raise_spatk(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); raise_stat = 0
    if (move == move_dex[239]): probability = 50
    elif (move == move_dex[499]): stage = 2
    elif (move == move_dex[780]): stage = 3
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (raise_stat == 1 and opponent.current_spatk + stage <= 12): user.current_spatk += stage
    if (raise_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "raisespatk", stage, 47, 53)

def amnesia(move, user, opponent, weather, terrain, seed):
    if (opponent.current_spdef + 1 <= 12): user.current_spdef += 2
    return (0, "raisespdef", 2, 59, 66)

def guard_swap(move, user, opponent, weather, terrain, seed):
    temp_def = opponent.current_def; temp_spdef = opponent.current_spdef
    opponent.current_def = user.current_def; opponent.current_spdef = user.current_def
    user.current_def = temp_def; user.current_spdef = temp_spdef
    return (0, "guard swap")

def raise_spd(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; stage = 1; rng = random.randint(1, 100); raise_stat = 0
    if (move == move_dex[12]): stage = 2
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    if (raise_stat == 1 and opponent.current_spd + stage <= 12): user.current_spd += stage
    if (raise_stat == 0): stage = -1
    for i in move.gimmick:
        if (i == "sound" and opponent.ability.name == abilities.ability_dex[42].name): stage = 0
        if (i == "ball" and opponent.ability.name == abilities.ability_dex[170].name): stage = 0
        if (i == "spore"):
            if (opponent.ability.name == abilities.ability_dex[141].name): stage = 0
            for j in opponent.typing:
                if (j == "Grass"): stage = 0
    return (damage, "raisespd", stage, 71, 78)

def recoil(move, user, opponent, weather, terrain, seed):
    random.seed(seed); probability = 100; rng = random.randint(1, 100); recoil = 1
    if (move == move_dex[82] or move == move_dex[855] or move == move_dex[870] or move == move_dex[179] or move == move_dex[846]): recoil = (1/3)
    elif (move == move_dex[321] or move == move_dex[784] or move == move_dex[863] or move == move_dex[758]): recoil = 0.25
    elif (move == move_dex[322] or move == move_dex[408]): recoil = 0.5
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    recoil_damage = recoil * damage
    return (damage, "recoil", recoil_damage)

def splash(move, user, opponent, weather, terrain, seed): return (0, "splash")

def clear_smog(move, user, opponent, weather, terrain, seed):
    opponent.current_atk = 6; opponent.current_def = 6; opponent.current_spd = 6; opponent.current_spatk = 6; opponent.current_spdef = 6
    return (deal_damage(move, user, opponent, weather, terrain, seed), "clear smog")

def set_weather(move, user, opponent, weather, terrain, seed):
    new_weather = ''; turn_count = 0
    if (move == move_dex[762]):
        new_weather = 'Harsh Sunlight'
        if (user.held_item == items.item_dex[282]): turn_count = 8
        else: turn_count = 5
    elif (move == move_dex[595]):
        new_weather = 'Rain'
        if (user.held_item == items.item_dex[272]): turn_count = 8
        else: turn_count = 5
    elif (move == move_dex[638]):
        new_weather = 'Sandstorm'
        if (user.held_item == items.item_dex[303]): turn_count = 8
        else: turn_count = 5
    elif (move == move_dex[316]):
        new_weather = 'Hail'
        if (user.held_item == items.item_dex[284]): turn_count = 8
        else: turn_count = 5
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, new_weather, turn_count)

def set_terrain(move, user, opponent, weather, terrain, seed):
    new_terrain = 'no terrain'; turn_count = 0
    if (move == move_dex[208]): new_terrain = 'Electric Terrain'
    elif (move == move_dex[303]): new_terrain = 'Grassy Terrain'
    elif (move == move_dex[484]): new_terrain = 'Misty Terrain'
    elif (move == move_dex[573]): new_terrain = 'Psychic Terrain'
    if (user.held_item == items.item_dex[305]): turn_count = 8
    else: turn_count = 5
    if (move.category != 2): damage = deal_damage(move, user, opponent, weather, terrain, seed)
    else: damage = 0
    return (damage, new_terrain, turn_count)

def multihit(move, user, opponent, weather, terrain, seed):
    random.seed(seed); hit_count = (2, 5); damage = 0
    if (move == move_dex[77] or move == move_dex[173] or move == move_dex[174] or move == move_dex[175] or move == move_dex[185] or move == move_dex[198] or move == move_dex[199] or move == move_dex[286]\
        or move == move_dex[830] or move == move_dex[831]): hit_count = (2, 2)
    elif (move == move_dex[769] or move == move_dex[827]): hit_count = (3, 3)
    hit_count = random.choice((hit_count[0], hit_count[1] + 1))
    for i in range(hit_count):
        if (move.category != 2): damage += deal_damage(move, user, opponent, weather, terrain, seed)
    return (damage)

def after_you(move, user, opponent, weather, terrain, seed): return (0, "after you")

def deal_damage(move, user, opponent, weather, terrain, seed):
    random.seed(seed); attack = 1; defense = 1; stab = 1; effectiveness = determine_effectiveness(opponent, move); burn = 1; power = move.power; weather_multiplier = 1
    for i in user.status_effects:
        if (i == 'Burn' and user.ability.name != abilities.ability_dex[61].name and move.category == 0):
            burn = 0.5
    for i in user.typing:
        if (i == move.typing): stab = 1.5
    if (move.category == 0):
        nature = user.nature[0]; opponent_nature = opponent.nature[0]; nature_modifier = 1; opponent_nature_modifier = 1
        if (nature == 'Lonely' or nature == 'Adamant' or nature == 'Naughty' or nature == 'Brave'): nature_modifier = 1.1
        elif (nature == 'Bold' or nature == 'Modest' or nature == 'Calm' or nature == 'Timid'): nature_modifier = 0.9
        if (opponent_nature == 'Bold' or opponent_nature == 'Impish' or opponent_nature == 'Lax' or opponent_nature == 'Relaxed'): opponent_nature_modifier = 1.1
        elif (opponent_nature == 'Lonely' or opponent_nature == 'Mild' or opponent_nature == 'Gentle' or opponent_nature == 'Hasty'): opponent_nature_modifier = 0.9
        attack = ((user.atk * 2) + 5) * nature_modifier * stat_modifiers[user.current_atk]; defense = ((user.defense * 2) + 5) * opponent_nature_modifier * stat_modifiers[opponent.current_def]
    elif (move.category == 1):
        nature = user.nature[0]; opponent_nature = opponent.nature[0]; nature_modifier = 1; opponent_nature_modifier = 1
        if (nature == 'Modest' or nature == 'Mild' or nature == 'Rash' or nature == 'Quiet'): nature_modifier = 1.1
        elif (nature == 'Adamant' or nature == 'Impish' or nature == 'Careful' or nature == 'Jolly'): nature_modifier = 0.9
        if (opponent_nature == 'Calm' or opponent_nature == 'Gentle' or opponent_nature == 'Careful' or opponent_nature == 'Sassy'): opponenet_nature_modifier = 1.1
        elif (opponent_nature == 'Naughty' or opponent_nature == 'Lax' or opponent_nature == 'Rash' or opponent_nature == 'Naive'): opponent_nature_modifier = 0.9
        attack = ((user.spatk * 2) + 5) * nature_modifier * stat_modifiers[user.current_spatk]; defense = ((user.spdef * 2) + 5) * opponent_nature_modifier * stat_modifiers[opponent.current_spdef]
    for i in opponent.status_effects:
        if (i == "dig" and move == move_dex[203]): power *= 2
    for i in terrain:
        if (i == "grassy"):
            if (move == move_dex[93] or move == move_dex[203] or move == move_dex[433]): power /= 2
    for i in move.gimmick:
        if (i == "sound"):
            if (user.ability.name == abilities.ability_dex[243].name): power *= 1.3
            if (opponent.ability.name == abilities.ability_dex[243].name): power *= 0.7
        if (i == "aura" and user.ability.name == abilities.ability_dex[177].name): power *= 1.5
        if (i == "bite" and user.ability.name == abilities.ability_dex[172].name): power *= 1.5
        if (i == "punch" and user.ability.name == abilities.ability_dex[88].name): power *= 1.2
        if (i == "slice" and user.ability.name == abilities.ability_dex[291].name): power *= 1.5
    if ((weather == 'Rain' and move.typing == "Water") or (weather == 'Harsh Sunlight' and move.typing == "Fire")): weather_mulitplier = 1.5
    if ((weather == 'Rain' and move.typing == "Fire") or (weather == 'Harsh Sunlight' and move.typing == "Water")): weather_multiplier = 0.5
    damage = int(opponent.level) * 2
    damage /= 5
    damage += 2
    damage *= power
    damage *= attack
    damage /= defense
    damage /= 50
    damage += 2
    damage *= random.randint(85, 100)/100
    damage *= stab * effectiveness * burn * weather_multiplier
    damage = round(damage)
    return damage

def dummy(move, user, opponent, weather, terrain, seed):
    return (0, "splash")

move_dex = {
    0:Move("10,000,000 Volt Thunderbolt", "Electric", 1, 1, 195, 101, [""], 0,
        False, False, False, False, False, True, dummy),
    1:Move("Absorb", "Grass", 1, 40, 20, 100, ["mouth"], 0,
		False, True, False, False, True, True, dummy),
    2:Move("Accelerock", "Rock", 0, 32, 40, 100, [""], 1,
		True, True, False, False, True, True, dummy),
    3:Move("Acid", "Poison", 1, 30, 48, 100, [""], 0,
		False, True, False, False, True, False, lower_spdef),
    4:Move("Acid Armor", "Poison", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, raise_def),
    5:Move("Acid Downpour", "Poison", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    6:Move("Acid Spray", "Poison", 1, 32, 40, 100, ["ball"], 0,
		False, True, False, False, True, True, lower_spdef),
    7:Move("Acrobatics", "Flying", 0, 24, 55, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    8:Move("Acupressure", "Normal", 2, 48, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    9:Move("Aerial Ace", "Flying", 0, 32, 60, 0, ["slice"], 0,
		True, True, False, False, True, True, deal_damage),
    10:Move("Aeroblast", "Flying", 1, 8, 100, 95, [""], 0,
		False, True, False, False, True, True, deal_damage),
    11:Move("After You", "Normal", 2, 24, 0, 0, [""], 12,
		False, False, False, False, False, False, after_you),
    12:Move("Agility", "Psychic", 2, 48, 0, 0, [""], 0,
		False, False, False, True, False, False, raise_spd),
    13:Move("Air Cutter", "Flying", 1, 40, 60, 95, ["slice", "wind"], 0,
		False, True, False, False, True, True, deal_damage),
    14:Move("Air Slash", "Flying", 1, 24, 75, 95, ["slice"], 0,
		False, True, False, False, True, False, deal_damage),
    15:Move("All-Out Pummeling", "Fighting", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    16:Move("Ally Switch", "Psychic", 2, 24, 0, 0, [""], 2,
		False, False, False, False, False, False, dummy),
    17:Move("Amnesia", "Psychic", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, amnesia),
    18:Move("Anchor Shot", "Steel", 0, 32, 80, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    19:Move("Ancient Rock", "Rock", 1, 8, 60, 100, [""], 0,
		False, True, False, False, True, False, dummy),
    20:Move("Apple Acid", "Grass", 1, 16, 80, 100, [""], 0,
		False, True, False, False, True, True, lower_spatk),
    21:Move("Aqua Cutter", "Water", 0, 32, 70, 100, ["slice"], 0,
		False, True, False, False, True, True, deal_damage),
    22:Move("Aqua Jet", "Water", 0, 32, 40, 100, [""], 1,
		True, True, False, False, True, True, dummy),
    23:Move("Aqua Ring", "Water", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    24:Move("Aqua Step", "Water", 0, 16, 80, 100, ["dance"], 0,
		True, True, False, False, True, True, dummy),
    25:Move("Aqua Tail", "Water", 0, 16, 90, 90, [""], 0,
		True, True, False, False, True, True, deal_damage),
    26:Move("Arm Thrust", "Fighting", 0, 32, 15, 100, [""], 0,
		True, True, False, False, True, True, multihit),
    27:Move("Armor Cannon", "Fire", 1, 8, 120, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    28:Move("Aromatherapy", "Grass", 2, 8, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    29:Move("Aromatic Mist", "Fairy", 2, 32, 0, 0, [""], 0,
		False, False, False, False, False, False, aromatic_mist),
    30:Move("Assist", "Normal", 2, 32, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    31:Move("Assurance", "Dark", 0, 16, 60, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    32:Move("Astonish", "Ghost", 0, 40, 30, 100, [""], 0,
		True, True, False, False, True, False, deal_damage),
    33:Move("Astral Barrage", "Ghost", 1, 8, 120, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    34:Move("Attack Order", "Bug", 0, 24, 90, 100, [""], 0,
		False, True, False, False, True, True, deal_damage),
    35:Move("Attract", "Normal", 2, 24, 0, 100, [""], 0,
		False, True, True, False, True, False, dummy),
    36:Move("Aura Sphere", "Fighting", 1, 32, 80, 0, ["aura", "ball"], 0,
		False, True, False, False, True, True, deal_damage),
    37:Move("Aura Wheel", "Electric", 0, 16, 110, 100, [""], 0,
		False, True, False, False, True, True, raise_spd),
    38:Move("Aurora Beam", "Ice", 1, 32, 65, 100, [""], 0,
		False, True, False, False, True, False, lower_atk),
    39:Move("Aurora Veil", "Ice", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    40:Move("Autotomize", "Steel", 2, 24, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    41:Move("Avalanche", "Ice", 0, 16, 60, 100, [""], -4,
		True, True, False, False, True, True, dummy),
    42:Move("Axe Kick", "Fighting", 0, 16, 120, 90, [""], 0,
		True, True, False, False, True, True, confuse),
    43:Move("Baby-Doll Eyes", "Fairy", 2, 48, 0, 0, [""], 1,
		False, True, True, False, True, False, lower_atk),
    44:Move("Baddy Bad", "Dark", 1, 24, 80, 95, [""], 0,
		False, True, False, False, False, True, dummy),
    45:Move("Baneful Bunker", "Poison", 2, 16, 0, 0, [""], 4,
		False, False, False, False, False, False, dummy),
    46:Move("Barb Barrage", "Poison", 0, 16, 60, 100, [""], 0,
		False, True, False, False, True, True, poison),
    47:Move("Barrage", "Normal", 0, 32, 15, 85, ["ball"], 0,
		False, True, False, False, True, True, multihit),
    48:Move("Barrier", "Psychic", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, raise_def),
    49:Move("Baton Pass", "Normal", 2, 64, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    50:Move("Beak Blast", "Flying", 0, 24, 100, 100, ["ball"], -3,
		False, True, False, False, False, True, dummy),
    51:Move("Beat Up", "Dark", 0, 16, 0, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    52:Move("Behemoth Bash", "Steel", 0, 8, 100, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    53:Move("Behemoth Blade", "Steel", 0, 8, 100, 100, ["slice"], 0,
		True, True, False, False, True, True, dummy),
    54:Move("Belch", "Poison", 1, 16, 120, 90, [""], 0,
		False, True, False, False, False, True, dummy),
    55:Move("Belly Drum", "Normal", 2, 16, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    56:Move("Bestow", "Normal", 2, 24, 0, 0, [""], 0,
		False, False, False, False, True, False, dummy),
    57:Move("Bide", "Normal", 0, 16, 0, 0, [""], 1,
		True, True, False, False, False, True, dummy),
    58:Move("Bind", "Normal", 0, 32, 15, 85, [""], 0,
		True, True, False, False, True, True, dummy),
    59:Move("Bite", "Dark", 0, 40, 60, 100, ["bite", "mouth"], 0,
		True, True, False, False, True, False, deal_damage),
    60:Move("Bitter Blade", "Fire", 0, 16, 90, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    61:Move("Bitter Malice", "Ghost", 1, 16, 75, 100, [""], 0,
		False, True, False, False, True, True, lower_atk),
    62:Move("Black Hole Eclipse", "Dark", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    63:Move("Blast Burn", "Fire", 1, 8, 150, 90, ["mouth"], 0,
		False, True, False, False, True, True, dummy),
    64:Move("Blaze Kick", "Fire", 0, 16, 85, 90, [""], 0,
		True, True, False, False, True, False, burn),
    65:Move("Blazing Torque", "Fire", 0, 16, 80, 100, [""], 0,
		False, True, False, False, False, False, dummy),
    66:Move("Bleakwind Storm", "Flying", 1, 16, 100, 80, ["wind"], 0,
		False, True, False, False, True, True, lower_spd),
    67:Move("Blizzard", "Ice", 1, 8, 110, 70, ["wind"], 0,
		False, True, False, False, True, False, freeze),
    68:Move("Block", "Normal", 2, 8, 0, 0, [""], 0,
		False, False, True, False, True, False, dummy),
    69:Move("Bloom Doom", "Grass", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    70:Move("Blue Flare", "Fire", 1, 8, 130, 85, [""], 0,
		False, True, False, False, True, True, burn),
    71:Move("Body Press", "Fighting", 0, 16, 80, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    72:Move("Body Slam", "Normal", 0, 24, 85, 100, [""], 0,
		True, True, False, False, True, False, paralysis),
    73:Move("Bolt Beak", "Electric", 0, 16, 85, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    74:Move("Bolt Strike", "Electric", 0, 8, 130, 85, [""], 0,
		True, True, False, False, True, True, paralysis),
    75:Move("Bone Club", "Ground", 0, 32, 65, 85, [""], 0,
		False, True, False, False, True, False, deal_damage),
    76:Move("Bone Rush", "Ground", 0, 16, 25, 90, [""], 0,
		False, True, False, False, True, True, multihit),
    77:Move("Bonemerang", "Ground", 0, 16, 50, 90, [""], 0,
		False, True, False, False, True, True, multihit),
    78:Move("Boomburst", "Normal", 1, 16, 140, 100, ["sound"], 0,
		False, True, False, False, True, True, deal_damage),
    79:Move("Bounce", "Flying", 0, 8, 85, 85, [""], 0,
		True, True, False, False, True, True, dummy),
    80:Move("Bouncy Bubble", "Water", 1, 24, 60, 100, [""], 0,
		False, True, False, False, False, True, dummy),
    81:Move("Branch Poke", "Grass", 0, 64, 40, 100, [""], 0,
		True, True, False, False, True, True, deal_damage),
    82:Move("Brave Bird", "Flying", 0, 24, 120, 100, [""], 0,
		True, True, False, False, True, True, recoil),
    83:Move("Breaking Swipe", "Dragon", 0, 24, 60, 100, [""], 0,
		True, True, False, False, True, True, lower_atk),
    84:Move("Breakneck Blitz", "Normal", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    85:Move("Brick Break", "Fighting", 0, 24, 75, 100, [""], 0,
		True, True, False, False, True, True, deal_damage),
    86:Move("Brine", "Water", 1, 16, 65, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    87:Move("Brutal Swing", "Dark", 0, 32, 60, 100, [""], 0,
		True, True, False, False, True, True, deal_damage),
    88:Move("Bubble", "Water", 1, 48, 40, 100, [""], 0,
		False, True, False, False, True, False, lower_spd),
    89:Move("Bubble Beam", "Water", 1, 32, 65, 100, [""], 0,
		False, True, False, False, True, False, lower_spd),
    90:Move("Bug Bite", "Bug", 0, 32, 60, 100, ["mouth"], 0,
		True, True, False, False, True, True, dummy),
    91:Move("Bug Buzz", "Bug", 1, 16, 90, 100, ["sound"], 0,
		False, True, False, False, True, True, lower_spdef),
    92:Move("Bulk Up", "Fighting", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    93:Move("Bulldoze", "Ground", 0, 32, 60, 100, [""], 0,
		False, True, False, False, True, True, lower_spd),
    94:Move("Bullet Punch", "Steel", 0, 48, 40, 100, ["punch"], 1,
		True, True, False, False, True, True, dummy),
    95:Move("Bullet Seed", "Grass", 0, 48, 25, 100, ["ball"], 0,
		False, True, False, False, True, True, multihit),
    96:Move("Burn Up", "Fire", 1, 8, 130, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    97:Move("Burning Jealousy", "Fire", 1, 8, 70, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    98:Move("Buzzy Buzz", "Electric", 1, 24, 60, 100, [""], 0,
		False, True, False, False, False, True, paralysis),
    99:Move("Calm Mind", "Psychic", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    100:Move("Camouflage", "Normal", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    101:Move("Captivate", "Normal", 2, 32, 0, 100, [""], 0,
		False, True, True, False, True, False, lower_spatk),
    102:Move("Catastropika", "Electric", 0, 1, 210, 0, [""], 0,
		True, False, False, False, False, True, dummy),
    103:Move("Ceaseless Edge", "Dark", 0, 24, 65, 90, ["slice"], 0,
		True, True, False, False, True, True, dummy),
    104:Move("Celebrate", "Normal", 2, 64, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    105:Move("Charge", "Electric", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    106:Move("Charge Beam", "Electric", 1, 16, 50, 90, [""], 0,
		False, True, False, False, True, True, dummy),
    107:Move("Charm", "Fairy", 2, 32, 0, 100, [""], 0,
		False, True, True, False, True, False, lower_atk),
    108:Move("Chatter", "Flying", 1, 32, 65, 100, ["sound", "mouth"], 0,
		False, True, False, False, True, False, confuse),
    109:Move("Chilling Water", "Water", 1, 32, 50, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    110:Move("Chilly Reception", "Ice", 2, 16, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    111:Move("Chip Away", "Normal", 0, 32, 70, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    112:Move("Chloroblast", "Grass", 1, 8, 150, 95, [""], 0,
		False, True, False, False, True, True, dummy),
    113:Move("Circle Throw", "Fighting", 0, 16, 60, 90, [""], -6,
		True, True, False, False, True, False, dummy),
    114:Move("Clamp", "Water", 0, 24, 35, 85, [""], 0,
		True, True, False, False, True, True, dummy),
    115:Move("Clanging Scales", "Dragon", 1, 8, 110, 100, ["sound"], 0,
		False, True, False, False, True, True, lower_self_def),
    116:Move("Clangorous Soul", "Dragon", 2, 8, 0, 0, ["sound", "dance"], 0,
		False, False, False, True, False, False, dummy),
    117:Move("Clangorous Soulblaze", "Dragon", 1, 1, 185, 0, ["sound"], 0,
		False, False, False, False, False, True, dummy),
    118:Move("Clear Smog", "Poison", 1, 24, 50, 0, [""], 0,
		False, True, False, False, True, True, clear_smog),
    119:Move("Close Combat", "Fighting", 0, 8, 120, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    120:Move("Coaching", "Fighting", 2, 16, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    121:Move("Coil", "Poison", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    122:Move("Collision Course", "Fighting", 0, 8, 100, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    123:Move("Combat Torque", "Fighting", 0, 16, 100, 100, [""], 0,
		False, True, False, False, False, False, dummy),
    124:Move("Comet Punch", "Normal", 0, 24, 18, 85, ["punch"], 0,
		True, True, False, False, True, True, multihit),
    125:Move("Comeuppance", "Dark", 0, 16, 0, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    126:Move("Confide", "Normal", 2, 32, 0, 0, ["sound"], 0,
		False, False, True, False, True, False, lower_spatk),
    127:Move("Confuse Ray", "Ghost", 2, 16, 0, 100, [""], 0,
		False, True, True, False, True, False, confuse),
    128:Move("Confusion", "Psychic", 1, 40, 50, 100, [""], 0,
		False, True, False, False, True, False, confuse),
    129:Move("Constrict", "Normal", 0, 56, 10, 100, [""], 0,
		True, True, False, False, True, False, lower_spd),
    130:Move("Continental Crush", "Rock", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    131:Move("Conversion", "Normal", 2, 48, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    132:Move("Conversion 2", "Normal", 2, 48, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    133:Move("Copycat", "Normal", 2, 32, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    134:Move("Core Enforcer", "Dragon", 1, 16, 100, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    135:Move("Corkscrew Crash", "Steel", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    136:Move("Corrosive Gas", "Poison", 2, 64, 0, 100, [""], 0,
		False, True, True, False, True, False, dummy),
    137:Move("Cosmic Power", "Psychic", 2, 32, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    138:Move("Cotton Guard", "Grass", 2, 16, 0, 0, [""], 0,
		False, False, False, True, False, False, raise_def),
    139:Move("Cotton Spore", "Grass", 2, 64, 0, 100, ["spore"], 0,
		False, True, True, False, True, False, lower_spd),
    140:Move("Counter", "Fighting", 0, 32, 0, 100, [""], -5,
		True, True, False, False, False, True, dummy),
    141:Move("Court Change", "Normal", 2, 16, 0, 100, [""], 0,
		False, False, False, False, True, False, dummy),
    142:Move("Covet", "Normal", 0, 40, 60, 100, [""], 0,
		True, True, False, False, True, False, dummy),
    143:Move("Crabhammer", "Water", 0, 16, 100, 90, [""], 0,
		True, True, False, False, True, True, deal_damage),
    144:Move("Crafty Shield", "Fairy", 2, 16, 0, 0, [""], 3,
		False, False, False, False, False, False, dummy),
    145:Move("Cross Chop", "Fighting", 0, 8, 100, 80, [""], 0,
		True, True, False, False, True, True, deal_damage),
    146:Move("Cross Poison", "Poison", 0, 32, 70, 100, ["slice"], 0,
		True, True, False, False, True, True, poison),
    147:Move("Crunch", "Dark", 0, 24, 80, 100, ["bite", "mouth"], 0,
		True, True, False, False, True, False, lower_def),
    148:Move("Crush Claw", "Normal", 0, 16, 75, 95, [""], 0,
		True, True, False, False, True, False, lower_def),
    149:Move("Crush Grip", "Normal", 0, 8, 0, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    150:Move("Curse", "Ghost", 2, 16, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    151:Move("Cut", "Normal", 0, 48, 50, 95, ["slice"], 0,
		True, True, False, False, True, True, deal_damage),
    152:Move("Dark Pulse", "Dark", 1, 24, 80, 100, ["aura"], 0,
		False, True, False, False, True, False, deal_damage),
    153:Move("Dark Void", "Dark", 2, 16, 0, 50, [""], 0,
		False, True, True, False, True, False, sleep),
    154:Move("Darkest Lariat", "Dark", 0, 16, 85, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    155:Move("Dazzling Gleam", "Fairy", 1, 16, 80, 100, [""], 0,
		False, True, False, False, True, True, deal_damage),
    156:Move("Decorate", "Fairy", 2, 24, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    157:Move("Defend Order", "Bug", 2, 16, 0, 0, [""], 0,
		False, False, False, True, False, False, dummy),
    158:Move("Defense Curl", "Normal", 2, 64, 0, 0, [""], 0,
		False, False, False, True, False, False, raise_def),
    159:Move("Defog", "Flying", 2, 24, 0, 0, [""], 0,
		False, True, True, False, True, False, dummy),
    160:Move("Destiny Bond", "Ghost", 2, 8, 0, 0, [""], 0,
		False, False, False, False, False, False, dummy),
    161:Move("Detect", "Fighting", 2, 8, 0, 0, [""], 4,
		False, False, False, False, False, False, dummy),
    162:Move("Devastating Drake", "Dragon", 3, 1, 0, 0, [""], 0,
		False, False, False, False, False, True, dummy),
    163:Move("Diamond Storm", "Rock", 0, 8, 100, 95, [""], 0,
		False, True, False, False, True, True, raise_def),
    164:Move("Dig", "Ground", 0, 16, 80, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    165:Move("Dire Claw", "Poison", 0, 24, 80, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    166:Move("Disable", "Normal", 2, 32, 0, 100, [""], 0,
		False, True, True, False, True, False, dummy),
    167:Move("Disarming Voice", "Fairy", 1, 24, 40, 0, ["sound"], 0,
		False, True, False, False, False, True, deal_damage),
    168:Move("Discharge", "Electric", 1, 24, 80, 100, [""], 0,
		False, True, False, False, True, True, paralysis),
    169:Move("Dive", "Water", 0, 16, 80, 100, [""], 0,
		True, True, False, False, True, True, dummy),
    170:Move("Dizzy Punch", "Normal", 0, 16, 70, 100, ["punch"], 0,
		True, True, False, False, True, False, confuse),
    171:Move("Doodle", "Normal", 2, 16, 0, 100, [""], 0,
		False, False, False, False, False, False, dummy),
    172:Move("Doom Desire", "Steel", 1, 5, 140, 100, [""], 0,
		False, False, False, False, False, False, dummy),
    173:Move("Double Hit", "Normal", 0, 16, 35, 90, [""], 0,
		True, True, False, False, True, True, multihit),
    174:Move("Double Iron Bash", "Steel", 0, 8, 60, 100, ["punch"], 0,
		True, True, False, False, True, False, multihit),
    175:Move("Double Kick", "Fighting", 0, 48, 30, 100, [""], 0,
		True, True, False, False, True, True, multihit),
    176:Move("Double Shock", "Electric", 0, 8, 120, 100, [""], 0,
		False, True, False, False, True, True, dummy),
    177:Move("Double Slap", "Normal", 0, 16, 15, 85, [""], 0,
        True, True, False, False, True, True, multihit),
    178:Move("Double Team", "Normal", 2, 24, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    179:Move("Double-Edge", "Normal", 0, 24, 120, 100, [""], 0,
        True, True, False, False, True, True, recoil),
    180:Move("Draco Meteor", "Dragon", 1, 8, 130, 90, [""], 0,
        False, True, False, False, True, True, lower_self_spatk),
    181:Move("Dragon Ascent", "Flying", 0, 8, 120, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    182:Move("Dragon Breath", "Dragon", 1, 32, 60, 100, ["mouth"], 0,
        False, True, False, False, True, True, paralysis),
    183:Move("Dragon Claw", "Dragon", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    184:Move("Dragon Dance", "Dragon", 2, 32, 0, 0, ["dance"], 0,
        False, False, False, True, False, False, dummy),
    185:Move("Dragon Darts", "Dragon", 0, 16, 50, 100, [""], 0,
        False, True, False, False, True, True, multihit),
    186:Move("Dragon Energy", "Dragon", 1, 8, 150, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    187:Move("Dragon Hammer", "Dragon", 0, 24, 90, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    188:Move("Dragon Pulse", "Dragon", 1, 16, 85, 100, ["aura"], 0,
        False, True, False, False, True, True, deal_damage),
    189:Move("Dragon Rage", "Dragon", 1, 16, 0, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    190:Move("Dragon Rush", "Dragon", 0, 16, 100, 75, [""], 0,
        True, True, False, False, True, False, deal_damage),
    191:Move("Dragon Tail", "Dragon", 0, 16, 60, 90, [""], -6,
        True, True, False, False, True, False, dummy),
    192:Move("Drain Punch", "Fighting", 0, 16, 75, 100, ["punch"], 0,
        True, True, False, False, True, True, dummy),
    193:Move("Draining Kiss", "Fairy", 1, 16, 50, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    194:Move("Dream Eater", "Psychic", 1, 24, 100, 100, ["mouth"], 0,
        False, True, False, False, True, False, dummy),
    195:Move("Drill Peck", "Flying", 0, 32, 80, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    196:Move("Drill Run", "Ground", 0, 16, 80, 95, [""], 0,
        True, True, False, False, True, True, deal_damage),
    197:Move("Drum Beating", "Grass", 0, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, lower_spd),
    198:Move("Dual Chop", "Dragon", 0, 24, 40, 90, [""], 0,
        True, True, False, False, True, True, multihit),
    199:Move("Dual Wingbeat", "Flying", 0, 16, 40, 90, [""], 0,
        True, True, False, False, True, True, multihit),
    200:Move("Dynamax Cannon", "Dragon", 1, 8, 100, 100, [""], 0,
        False, True, False, False, False, True, dummy),
    201:Move("Dynamic Punch", "Fighting", 0, 8, 100, 50, ["punch"], 0,
        True, True, False, False, True, False, confuse),
    202:Move("Earth Power", "Ground", 1, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, lower_spdef),
    203:Move("Earthquake", "Ground", 0, 16, 100, 100, [""], 0,
        False, True, False, False, True, True, deal_damage),
    204:Move("Echoed Voice", "Normal", 1, 24, 40, 100, ["sound"], 0,
        False, True, False, False, True, True, dummy),
    205:Move("Eerie Impulse", "Electric", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, lower_spatk),
    206:Move("Eerie Spell", "Psychic", 1, 8, 80, 100, ["sound"], 0,
        False, True, False, False, True, True, dummy),
    207:Move("Egg Bomb", "Normal", 0, 16, 100, 75, ["ball"], 0,
        False, True, False, False, True, True, deal_damage),
    208:Move("Electric Terrain", "Electric", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, set_terrain),
    209:Move("Electrify", "Electric", 2, 32, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    210:Move("Electro Ball", "Electric", 1, 16, 0, 100, ["ball"], 0,
        False, True, False, False, True, True, dummy),
    211:Move("Electro Drift", "Electric", 1, 8, 100, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    212:Move("Electroweb", "Electric", 1, 24, 55, 95, [""], 0,
        False, True, False, False, True, True, lower_spd),
    213:Move("Embargo", "Dark", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    214:Move("Ember", "Fire", 1, 40, 40, 100, [""], 0,
        False, True, False, False, True, False, burn),
    215:Move("Encore", "Normal", 2, 8, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    216:Move("Endeavor", "Normal", 0, 8, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    217:Move("Endure", "Normal", 2, 16, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    218:Move("Energy Ball", "Grass", 1, 16, 90, 100, ["ball"], 0,
        False, True, False, False, True, False, lower_spdef),
    219:Move("Entrainment", "Normal", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    220:Move("Eruption", "Fire", 1, 8, 150, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    221:Move("Esper Wing", "Psychic", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, raise_spd),
    222:Move("Eternabeam", "Dragon", 1, 8, 160, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    223:Move("Expanding Force", "Psychic", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    224:Move("Explosion", "Normal", 0, 8, 250, 100, ["explosive"], 0,
        False, True, False, False, True, True, dummy),
    225:Move("Extrasensory", "Psychic", 1, 32, 80, 100, [""], 0,
        False, True, False, False, True, False, deal_damage),
    226:Move("Extreme Evoboost", "Normal", 2, 1, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    227:Move("Extreme Speed", "Normal", 0, 8, 80, 100, [""], 2,
        True, True, False, False, True, True, deal_damage),
    228:Move("Facade", "Normal", 0, 32, 70, 100, [""], 0,
        True, True, False, False, True, False, dummy),
    229:Move("Fairy Lock", "Fairy", 2, 16, 0, 0, [""], 0,
        False, False, False, False, True, False, dummy),
    230:Move("Fairy Wind", "Fairy", 1, 48, 40, 100, ["wind"], 0,
        False, True, False, False, True, True, deal_damage),
    231:Move("Fake Out", "Normal", 0, 16, 40, 100, [""], 3,
        True, True, False, False, True, False, deal_damage),
    232:Move("Fake Tears", "Dark", 2, 32, 0, 100, ["mouth"], 0,
        False, True, True, False, True, False, lower_spdef),
    233:Move("False Surrender", "Dark", 0, 16, 80, 0, [""], 0,
        True, True, False, False, True, True, deal_damage),
    234:Move("False Swipe", "Normal", 0, 64, 40, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    235:Move("Feather Dance", "Flying", 2, 24, 0, 100, ["dance"], 0,
        False, True, True, False, True, False, lower_atk),
    236:Move("Feint", "Normal", 0, 16, 30, 100, [""], 2,
        False, False, False, False, True, False, dummy),
    237:Move("Feint Attack", "Dark", 0, 32, 60, 0, [""], 0,
        True, True, False, False, True, True, deal_damage),
    238:Move("Fell Stinger", "Bug", 0, 40, 50, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    239:Move("Fiery Dance", "Fire", 1, 16, 80, 100, ["dance"], 0,
        False, True, False, False, True, True, raise_spatk),
    240:Move("Fiery Wrath", "Dark", 1, 16, 90, 100, [""], 0,
        False, True, False, False, True, False, deal_damage),
    241:Move("Fillet Away", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    242:Move("Final Gambit", "Fighting", 1, 8, 0, 100, [""], 0,
        False, True, False, False, False, True, dummy),
    243:Move("Fire Blast", "Fire", 1, 8, 110, 85, [""], 0,
        False, True, False, False, True, False, burn),
    244:Move("Fire Fang", "Fire", 0, 24, 65, 95, ["bite", "mouth"], 0,
        True, True, False, False, True, False, burn),
    245:Move("Fire Lash", "Fire", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, True, lower_def),
    246:Move("Fire Pledge", "Fire", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    247:Move("Fire Punch", "Fire", 0, 24, 75, 100, ["punch"], 0,
        True, True, False, False, True, False, burn),
    248:Move("Fire Spin", "Fire", 1, 24, 35, 85, [""], 0,
        False, True, False, False, True, True, dummy),
	249:Move("First Impression", "Bug", 0, 16, 90, 100, [""], 2,
        True, True, False, False, True, True, dummy),
	250:Move("Fishious Rend", "Water", 0, 16, 85, 100, ["bite"], 0,
        True, True, False, False, True, True, dummy),
    251:Move("Fissure", "Ground", 0, 8, 0, 30, [""], 0,
        False, True, False, False, False, False, dummy),
    252:Move("Flash", "Normal", 2, 32, 0, 100, [""], 0,
        False, True, True, False,  True, False, dummy),
    253:Move("Flash Cannon", "Steel", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, lower_spdef),
    254:Move("Flatter", "Dark", 2, 24, 0, 100, ["mouth"], 0,
        False, True, True, False, True, False, dummy),
    255:Move("Fleur Cannon", "Fairy", 1, 8, 130, 90, [""], 0,
        False, True, False, False, True, True, lower_self_spatk),
    256:Move("Fling", "Dark", 0, 16, 0, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    257:Move("Flip Turn", "Water", 0, 32, 60, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    258:Move("Floaty Fall", "Flying", 0, 24, 90, 95, [""], 0,
        True, True, False, False, False, False, deal_damage),
    259:Move("Floral Healing", "Fairy", 2, 16, 0, 0, [""], 0,
        False, True, True, False, False, False, dummy),
    260:Move("Flower Shield", "Fairy", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    261:Move("Flower Trick", "Grass", 0, 16, 70, 0, [""], 0,
        False, True, False, False, True, True, dummy),
    262:Move("Fly", "Flying", 0, 24, 90, 95, [""], 0,
        True, True, False, False, True, True, dummy),
    263:Move("Flying Press", "Fighting", 0, 16, 100, 95, [""], 0,
        True, True, False, False, True, True, deal_damage),
    264:Move("Focus Blast", "Fighting", 1, 8, 120, 70, ["ball"], 0,
        False, True, False, False, True, False, lower_spdef),
    265:Move("Focus Energy", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    266:Move("Focus Punch", "Fighting", 0, 32, 150, 100, ["punch"], -3,
        True, True, False, False, False, False, dummy),
    267:Move("Follow Me", "Normal", 2, 32, 0, 0, [""], 2,
        False, False, False, False, False, False, dummy),
    268:Move("Force Palm", "Fighting", 0, 16, 60, 100, [""], 0,
        True, True, False, False, True, True, paralysis),
    269:Move("Foresight", "Normal", 2, 64, 0, 0, [""], 0,
        False, True, True, False, True, False, dummy),
    270:Move("Forest's Curse", "Grass", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    271:Move("Foul Play", "Dark", 0, 24, 95, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    272:Move("Freeze Shock", "Ice", 0, 8, 140, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    273:Move("Freeze-Dry", "Ice", 1, 32, 70, 100, [""], 0,
        False, True, False, False, True, True, freeze),
    274:Move("Freezing Glare", "Psychic", 1, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, freeze),
    275:Move("Freezy Frost", "Ice", 1, 24, 90, 100, [""], 0,
        False, True, False, False, False, True, dummy),
    276:Move("Frenzy Plant", "Grass", 1, 8, 150, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    277:Move("Frost Breath", "Ice", 1, 16, 60, 90, [""], 0,
        False, True, False, False, True, True, deal_damage),
    278:Move("Frustration", "Normal", 0, 32, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    279:Move("Fury Attack", "Normal", 0, 32, 15, 85, [""], 0,
        True, True, False, False, True, True, multihit),
    280:Move("Fury Cutter", "Bug", 0, 32, 40, 95, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    281:Move("Fury Swipes", "Normal", 0, 24, 18, 80, [""], 0,
        True, True, False, False, True, True, multihit),
    282:Move("Fusion Bolt", "Electric", 0, 8, 100, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    283:Move("Fusion Flare", "Fire", 1, 8, 100, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    284:Move("Future Sight", "Psychic", 1, 16, 120, 100, [""], 0,
        False, False, False, False, False, False, dummy),
    285:Move("Gastro Acid", "Poison", 2, 16, 0, 100, ["mouth"], 0,
        False, True, True, False, True, False, dummy),
    286:Move("Gear Grind", "Steel", 0, 24, 50, 85, [""], 0,
        True, True, False, False, True, True, multihit),
    287:Move("Gear Up", "Steel", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    288:Move("Genesis Supernova", "Psychic", 1, 1, 185, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    289:Move("Geomancy", "Fairy", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    290:Move("Giga Drain", "Grass", 1, 16, 75, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    291:Move("Giga Impact", "Normal", 0, 8, 150, 90, [""], 0,
        True, True, False, False, True, True, dummy),
    292:Move("Gigaton Hammer", "Steel", 0, 8, 160, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    293:Move("Gigavolt Havoc", "Electric", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    294:Move("Glacial Lance", "Ice", 0, 8, 120, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    295:Move("Glaciate", "Ice", 1, 16, 65, 95, [""], 0,
        False, True, False, False, True, False, lower_spd),
    296:Move("Glaive Rush", "Dragon", 0, 8, 120, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    297:Move("Glare", "Normal", 2, 48, 0, 100, [""], 0,
        False, True, True, False, True, False, paralysis),
    298:Move("Glitzy Glow", "Fairy", 1, 24, 90, 100, [""], 0,
        False, True, False, False, False, True, dummy),
    299:Move("Grass Knot", "Grass", 1, 32, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    300:Move("Grass Pledge", "Grass", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    301:Move("Grass Whistle", "Grass", 2, 24, 0, 55, ["sound", "mouth"], 0,
        False, True, True, False, True, False, sleep),
    302:Move("Grassy Glide", "Grass", 0, 32, 60, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    303:Move("Grassy Terrain", "Grass", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, set_terrain),
    304:Move("Grav Apple", "Grass", 0, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, lower_def),
    305:Move("Gravity", "Psychic", 2, 8, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    306:Move("Growl", "Normal", 2, 64, 0, 100, ["sound", "mouth"], 0,
        False, True, True, False, True, False, lower_atk),
    307:Move("Growth", "Normal", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    308:Move("Grudge", "Ghost", 2, 8, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    309:Move("Guard Split", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, False, False, dummy),
    310:Move("Guard Swap", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    311:Move("Guardian of Alola", "Fairy", 1, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    312:Move("Guillotine", "Normal", 0, 8, 0, 30, [""], 0,
        True, True, False, False, False, False, dummy),
    313:Move("Gunk Shot", "Poison", 0, 8, 120, 80, [""], 0,
        False, True, False, False, True, True, poison),
    314:Move("Gust", "Flying", 1, 56, 40, 100, ["wind"], 0,
        False, True, False, False, True, True, deal_damage),
    315:Move("Gyro Ball", "Steel", 0, 8, 0, 100, ["ball"], 0,
        True, True, False, False, True, True, dummy),
    316:Move("Hail", "Ice", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, set_weather),
    317:Move("Hammer Arm", "Fighting", 0, 16, 100, 90, ["punch"], 0,
        True, True, False, False, True, True, lower_self_spd),
    318:Move("Happy Hour", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    319:Move("Harden", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_def),
    320:Move("Haze", "Ice", 2, 48, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    321:Move("Head Charge", "Normal", 0, 24, 120, 100, [""], 0,
        True, True, False, False, True, True, recoil),
    322:Move("Head Smash", "Rock", 0, 8, 150, 80, [""], 0,
        True, True, False, False, True, True, recoil),
    323:Move("Headbutt", "Normal", 0, 24, 70, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    324:Move("Headlong Rush", "Ground", 0, 8, 120, 100, ["punch"], 0,
        True, True, False, False, True, True, dummy),
    325:Move("Heal Bell", "Normal", 2, 8, 0, 0, ["sound"], 0,
        False, False, False, True, False, False, dummy),
    326:Move("Heal Block", "Psychic", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    327:Move("Heal Order", "Bug", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    328:Move("Heal Pulse", "Psychic", 2, 16, 0, 0, ["aura"], 0,
        False, True, True, False, False, False, dummy),
    329:Move("Healing Wish", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    330:Move("Heart Stamp", "Psychic", 0, 40, 60, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    331:Move("Heart Swap", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    332:Move("Heat Crash", "Fire", 0, 16, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    333:Move("Heat Wave", "Fire", 1, 16, 95, 90, ["wind"], 0,
        False, True, False, False, True, True, burn),
    334:Move("Heavy Slam", "Steel", 0, 16, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    335:Move("Helping Hand", "Normal", 2, 32, 0, 0, [""], 5,
        False, False, False, False, False, False, dummy),
    336:Move("Hex", "Ghost", 1, 16, 65, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    337:Move("Hidden Power", "Normal", 1, 24, 50, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    338:Move("High Horsepower", "Ground", 0, 16, 95, 95, [""], 0,
        True, True, False, False, True, True, deal_damage),
    339:Move("High Jump Kick", "Fighting", 0, 16, 130, 90, [""], 0,
        True, True, False, False, True, True, deal_damage),
    340:Move("Hold Back", "Normal", 0, 64, 40, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    341:Move("Hold Hands", "Normal", 2, 64, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    342:Move("Hone Claws", "Dark", 2, 24, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    343:Move("Horn Attack", "Normal", 0, 40, 65, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    344:Move("Horn Drill", "Normal", 0, 8, 0, 30, [""], 0,
        True, True, False, False, False, False, dummy),
    345:Move("Horn Leech", "Grass", 0, 16, 75, 100, [""], 0,
        True, True, False, False, True, False, dummy),
    346:Move("Howl", "Normal", 2, 64, 0, 0, ["mouth", "sound"], 0,
        False, False, False, True, False, False, raise_atk),
    347:Move("Hurricane", "Flying", 1, 16, 110, 70, ["wind"], 0,
        False, True, False, False, True, True, confuse),
    348:Move("Hydro Cannon", "Water", 1, 8, 150, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    349:Move("Hydro Pump", "Water", 1, 8, 110, 80, [""], 0,
        False, True, False, False, True, True, dummy),
    350:Move("Hydro Steam", "Water", 1, 24, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    351:Move("Hydro Vortex", "Water", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    352:Move("Hyper Beam", "Normal", 1, 8, 150, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    353:Move("Hyper Drill", "Normal", 0, 8, 100, 100, [""], 0,
        True, False, False, False, True, True, dummy),
    354:Move("Hyper Fang", "Normal", 0, 24, 80, 90, ["bite", "mouth"], 0,
        True, True, False, False, True, False, deal_damage),
    355:Move("Hyper Voice", "Normal", 1, 16, 90, 100, ["mouth", "sound"], 0,
        False, True, False, False, True, False, deal_damage),
    356:Move("Hyperspace Fury", "Dark", 0, 8, 100, 0, [""], 0,
        False, False, False, False, True, True, lower_self_def),
    357:Move("Hyperspace Hole", "Psychic", 1, 8, 80, 0, [""], 0,
        False, False, False, False, True, True, dummy),
    358:Move("Hypnosis", "Psychic", 2, 32, 0, 60, [""], 0,
        False, True, True, False, True, False, sleep),
    359:Move("Ice Ball", "Ice", 0, 32, 30, 90, ["ball"], 0,
        True, True, False, False, True, True, dummy),
    360:Move("Ice Beam", "Ice", 1, 16, 90, 100, [""], 0,
        False, True, False, False, True, False, freeze),
    361:Move("Ice Burn", "Ice", 1, 8, 140, 90, [""], 0,
        False, True, False, False, True, True, burn),
    362:Move("Ice Fang", "Ice", 0, 24, 65, 95, ["bite", "mouth"], 0,
        True, True, False, False, True, False, freeze),
    363:Move("Ice Hammer", "Ice", 0, 16, 100, 90, ["punch"], 0,
        True, True, False, False, True, True, lower_self_spd),
    364:Move("Ice Punch", "Ice", 0, 24, 75, 100, ["punch"], 0,
        True, True, False, False, True, False, freeze),
    365:Move("Ice Shard", "Ice", 0, 48, 40, 100, [""], 1,
        False, True, False, False, True, True, dummy),
    366:Move("Ice Spinner", "Ice", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, True, set_terrain),
    367:Move("Icicle Crash", "Ice", 0, 16, 85, 90, [""], 0,
        False, True, False, False, True, False, deal_damage),
    368:Move("Icicle Spear", "Ice", 0, 48, 25, 100, [""], 0,
        False, True, False, False, True, True, multihit),
    369:Move("Icy Wind", "Ice", 1, 24, 55, 95, ["wind"], 0,
        False, True, False, False, True, False, lower_spd),
    370:Move("Imprison", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    371:Move("Incinerate", "Fire", 1, 24, 60, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    372:Move("Infernal Parade", "Ghost", 1, 15, 60, 100, [""], 0,
        False, True, False, False, True, True, burn),
    373:Move("Inferno", "Fire", 1, 8, 100, 50, [""], 0,
        False, True, False, False, True, False, burn),
    374:Move("Inferno Overdrive", "Fire", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    375:Move("Infestation", "Bug", 1, 32, 20, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    376:Move("Ingrain", "Grass", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    377:Move("Instruct", "Psychic", 2, 24, 0, 0, [""], 0,
        False, True, False, False, False, False, dummy),
    378:Move("Ion Deluge", "Electric", 2, 40, 0, 0, [""], 1,
        False, False, False, False, False, False, dummy),
    379:Move("Iron Defense", "Steel", 2, 24, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_def),
    380:Move("Iron Head", "Steel", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    381:Move("Iron Tail", "Steel", 0, 24, 100, 75, [""], 0,
        True, True, False, False, True, False, lower_def),
    382:Move("Jaw Lock", "Dark", 0, 16, 80, 100, ["bite"], 0,
        True, True, False, False, True, True, dummy),
    383:Move("Jet Punch", "Water", 0, 24, 60, 100, ["punch"], 1,
        True, True, False, False, True, True, dummy),
    384:Move("Judgement", "Normal", 1, 16, 100, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    385:Move("Jump Kick", "Fighting", 0, 16, 100, 95, [""], 0,
        True, True, False, False, True, True, deal_damage),
    387:Move("Jungle Healing", "Grass", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    388:Move("Karate Chop", "Fighting", 0, 40, 50, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    389:Move("Kinesis", "Psychic", 2, 24, 0, 80, [""], 0,
        False, True, True, False, True, False, dummy),
    390:Move("King's Shield", "Steel", 2, 16, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    391:Move("Knock Off", "Dark", 0, 32, 65, 100, [""], 0,
        True, True, False, False, True, False, dummy),
    392:Move("Kowtow Cleave", "Dark", 0, 16, 85, 0, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    393:Move("Land's Wrath", "Ground", 0, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, deal_damage),
    394:Move("Lash Out", "Dark", 0, 8, 75, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    395:Move("Last Resort", "Normal", 0, 8, 140, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    396:Move("Last Respects", "Ghost", 0, 16, 50, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    397:Move("Lava Plume", "Fire", 1, 24, 80, 100, [""], 0,
        False, True, False, False, True, True, burn),
    398:Move("Leaf Blade", "Grass", 0, 24, 90, 100, ["slice"], 0,
        True, True, False, False, True, True, deal_damage),
    399:Move("Leaf Storm", "Grass", 1, 8, 130, 90, [""], 0,
        False, True, False, False, True, True, lower_self_spatk),
    400:Move("Leaf Tornado", "Grass", 1, 16, 65, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    401:Move("Leafage", "Grass", 0, 64, 40, 100, [""], 0,
        False, True, False, False, True, True, deal_damage),
    402:Move("Leech Life", "Bug", 0, 16, 80, 100, ["mouth"], 0,
        True, True, False, False, True, True, dummy),
    403:Move("Leech Seed", "Grass", 2, 16, 0, 90, [""], 0,
        False, True, True, False, True, False, dummy),
    404:Move("Leer", "Normal", 2, 48, 0, 100, [""], 0,
        False, True, True, False, True, False, lower_def),
    405:Move("Let's Snuggle Forever", "Fairy", 0, 1, 190, 0, [""], 0,
        True, False, False, False, False, True, dummy),
    406:Move("Lick", "Ghost", 0, 48, 30, 100, ["mouth"], 0,
        True, True, False, False, True, False, paralysis),
    407:Move("Life Dew", "Water", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    408:Move("Light of Ruin", "Fairy", 1, 8, 140, 90, [""], 0,
        False, True, False, False, True, True, recoil),
    409:Move("Light Screen", "Psychic", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    410:Move("Light That Burns the Sky", "Psychic", 1, 1, 200, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    411:Move("Liquidation", "Water", 0, 16, 85, 100, [""], 0,
        True, True, False, False, True, True, lower_def),
    412:Move("Lock-On", "Normal", 2, 8, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    413:Move("Lovely Kiss", "Normal", 2, 16, 0, 75, ["mouth"], 0,
        False, True, True, False, True, False, sleep),
    414:Move("Low Kick", "Fighting", 0, 32, 0, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    415:Move("Low Sweep", "Fighting", 0, 32, 65, 100, [""], 0,
        True, True, False, False, True, True, lower_spd),
    416:Move("Lucky Chant", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    417:Move("Lumina Crash", "Psychic", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    418:Move("Lunar Blessing", "Psychic", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    419:Move("Lunar Dance", "Psychic", 2, 16, 0, 0, ["dance"], 0,
        False, False, False, True, False, False, dummy),
    420:Move("Lunge", "Bug", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, True, lower_atk),
    421:Move("Luster Purge", "Psychic", 1, 8, 70, 100, [""], 0,
        False, True, False, False, True, False, lower_spdef),
    422:Move("Mach Punch", "Fighting", 0, 48, 40, 100, ["punch"], 1,
        True, True, False, False, True, True, dummy),
    423:Move("Magic Coat", "Psychic", 2, 24, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    424:Move("Magic Powder", "Psychic", 2, 32, 0, 100, ["spore"], 0,
        False, True, True, False, True, False, dummy),
    425:Move("Magic Room", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, False, True, False, dummy),
    427:Move("Magical Leaf", "Grass", 1, 32, 60, 0, [""], 0,
        False, True, False, False, True, True, dummy),
    428:Move("Magical Torque", "Fairy", 0, 16, 100, 100, [""], 0,
        False, True, False, False, False, False, dummy),
    429:Move("Magma Storm", "Fire", 1, 8, 100, 75, [""], 0,
        False, True, False, False, True, True, dummy),
    430:Move("Magnet Bomb", "Steel", 0, 32, 60, 0, ["ball"], 0,
        False, True, False, False, True, True, dummy),
    431:Move("Magnet Rise", "Electric", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    432:Move("Magnetic Flux", "Electric", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    433:Move("Magnitude", "Ground", 0, 48, 0, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    434:Move("Make It Rain", "Steel", 1, 8, 120, 100, [""], 0,
        False, True, False, False, True, True, lower_self_spatk),
    435:Move("Malicious Moonsault", "Dark", 0, 1, 180, 0, [""], 0,
        True, False, False, False, False, True, dummy),
    436:Move("Mat Block", "Fighting", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    437:Move("Max Airstream", "Flying", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    438:Move("Max Darkness", "Dark", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    439:Move("Max Flare", "Fire", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    440:Move("Max Flutterby", "Bug", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    441:Move("Max Geyser", "Water", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    442:Move("Max Guard", "Normal", 2, 10, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    443:Move("Max Hailstorm", "Ice", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    444:Move("Max Knuckle", "Fighting", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    445:Move("Max Lightning", "Electric", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    446:Move("Max Mindstorm", "Psychic", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    447:Move("Max Ooze", "Poison", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    448:Move("Max Overgrowth", "Grass", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    449:Move("Max Phantasm", "Ghost", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    450:Move("Max Quake", "Ground", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    451:Move("Max Rockfall", "Rock", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    452:Move("Max Starfall", "Fairy", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    453:Move("Max Steelspike", "Steel", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    454:Move("Max Strike", "Normal", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    455:Move("Max Wyrmwind", "Dragon", 3, 10, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    456:Move("Me First", "Normal", 2, 32, 0, 0, [""], 0,
        False, True, False, False, False, False, dummy),
    457:Move("Mean Look", "Normal", 2, 8, 0, 0, [""], 0,
        False, False, True, False, True, False, dummy),
    458:Move("Meditate", "Psychic", 2, 64, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_atk),
    459:Move("Mega Drain", "Grass", 1, 24, 40, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    460:Move("Mega Kick", "Normal", 0, 8, 120, 75, [""], 0,
        True, True, False, False, True, True, deal_damage),
    461:Move("Mega Punch", "Normal", 0, 32, 80, 85, ["punch"], 0,
        True, True, False, False, True, True, deal_damage),
    462:Move("Megahorn", "Bug", 0, 16, 120, 85, [""], 0,
        True, True, False, False, True, True, deal_damage),
    463:Move("Memento", "Dark", 2, 16, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    464:Move("Menacing Moonraze Maelstrom", "Ghost", 1, 1, 200, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    465:Move("Metal Burst", "Steel", 0, 16, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    466:Move("Metal Claw", "Steel", 0, 56, 50, 95, [""], 0,
        True, True, False, False, True, False, raise_atk),
    467:Move("Metal Sound", "Steel", 2, 64, 0, 85, ["sound"], 0,
        False, True, True, False, True, False, lower_spdef),
    468:Move("Meteor Assault", "Fighting", 0, 8, 150, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    469:Move("Meteor Beam", "Rock", 1, 16, 120, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    470:Move("Meteor Mash", "Steel", 0, 16, 90, 90, ["punch"], 0,
        True, True, False, False, True, True, raise_atk),
    471:Move("Metronome", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    472:Move("Milk Drink", "Normal", 2, 8, 0, 0, ["mouth"], 0,
        False, False, False, True, False, False, dummy),
    473:Move("Mimic", "Normal", 2, 16, 0, 0, [""], 0,
        False, True, False, False, False, False, dummy),
    474:Move("Mind Blown", "Fire", 1, 8, 150, 100, ["explosive"], 0,
        False, True, False, False, True, True, dummy),
    475:Move("Mind Reader", "Normal", 2, 8, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    476:Move("Minimize", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    477:Move("Miracle Eye", "Psychic", 2, 64, 0, 0, [""], 0,
        False, True, True, False, True, False, dummy),
    478:Move("Mirror Coat", "Psychic", 1, 32, 0, 100, [""], -5,
        False, True, False, False, False, True, dummy),
    479:Move("Mirror Move", "Flying", 2, 32, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    480:Move("Mirror Shot", "Steel", 1, 16, 65, 85, [""], 0,
        False, True, False, False, True, True, dummy),
    481:Move("Mist", "Ice", 2, 48, 0, 0, ["ball"], 0,
        False, False, False, True, False, False, dummy),
    482:Move("Mist Ball", "Psychic", 1, 8, 70, 100, [""], 0,
        False, True, False, False, True, False, lower_spatk),
    483:Move("Misty Explosion", "Fairy", 1, 8, 100, 100, ["explosive"], 0,
        False, True, False, False, True, True, dummy),
    484:Move("Misty Terrain", "Fairy", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, set_terrain),
    485:Move("Moonblast", "Fairy", 1, 24, 95, 100, [""], 0,
        False, True, False, False, True, True, lower_spatk),
    486:Move("Moongeist Beam", "Ghost", 1, 8, 100, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    487:Move("Moonlight", "Fairy", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    488:Move("Morning Sun", "Normal", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    489:Move("Mortal Spin", "Poison", 0, 24, 30, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    490:Move("Mountain Gale", "Ice", 0, 16, 100, 85, [""], 0,
        False, True, False, False, True, True, deal_damage),
    491:Move("Mud Bomb", "Ground", 1, 16, 65, 85, ["ball"], 0,
        False, True, False, False, True, True, dummy),
    492:Move("Mud Shot", "Ground", 1, 24, 55, 95, [""], 0,
        False, True, False, False, True, True, lower_spd),
    493:Move("Mud Sport", "Ground", 2, 24, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    494:Move("Mud-Slap", "Ground", 1, 16, 20, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    495:Move("Muddy Water", "Water", 1, 16, 90, 85, [""], 0,
        False, True, False, False, True, True, dummy),
    496:Move("Multi-Attack", "Normal", 0, 16, 120, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    497:Move("Mystical Fire", "Fire", 1, 16, 75, 100, [""], 0,
        False, True, False, False, True, True, lower_spatk),
    498:Move("Mystical Power", "Psychic", 1, 10, 70, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    499:Move("Nasty Plot", "Dark", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_spatk),
    500:Move("Natural Gift", "Normal", 0, 24, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    501:Move("Nature Power", "Normal", 2, 32, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    502:Move("Nature's Madness", "Fairy", 1, 16, 0, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    503:Move("Needle Arm", "Grass", 0, 24, 60, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    504:Move("Never-Ending Nightmare", "Ghost", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    505:Move("Night Daze", "Dark", 1, 16, 85, 95, [""], 0,
        False, True, False, False, True, True, dummy),
    506:Move("Night Shade", "Ghost", 1, 24, 0, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    507:Move("Night Slash", "Dark", 0, 24, 70, 100, ["slice"], 0,
        True, True, False, False, True, True, deal_damage),
    508:Move("Nightmare", "Ghost", 2, 24, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    510:Move("No Retreat", "Fighting", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    511:Move("Noble Roar", "Normal", 2, 48, 0, 100, ["sound"], 0,
        False, True, True, False, True, False, dummy),
    512:Move("Noxious Torque", "Poison", 0, 16, 100, 100, [""], 0,
        False, True, False, False, False, False, dummy),
    513:Move("Nuzzle", "Electric", 0, 32, 20, 100, [""], 0,
        True, True, False, False, True, True, paralysis),
    514:Move("Oblivion Wing", "Flying", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    515:Move("Obstruct", "Dark", 2, 16, 0, 100, [""], 4,
        False, False, False, False, False, False, dummy),
    516:Move("Oceanic Operetta", "Water", 1, 1, 195, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    517:Move("Octazooka", "Water", 1, 16, 65, 85, ["ball", "mouth"], 0,
        False, True, False, False, True, False, dummy),
    518:Move("Octolock", "Fighting", 2, 24, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    519:Move("Odour Sleuth", "Normal", 2, 64, 0, 0, [""], 0,
        False, True, True, False, True, False, dummy),
    520:Move("Ominous Wind", "Ghost", 1, 24, 60, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    521:Move("Order Up", "Dragon", 0, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    522:Move("Origin Pulse", "Water", 1, 16, 110, 85, ["aura"], 0,
        False, True, False, False, True, True, dummy),
    523:Move("Outrage", "Dragon", 0, 16, 120, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    524:Move("Overdrive", "Electric", 1, 16, 80, 100, ["sound"], 0,
        False, True, False, False, True, True, deal_damage),
    525:Move("Overheat", "Fire", 1, 8, 130, 90, [""], 0,
        False, True, False, False, True, True, lower_self_spatk),
    526:Move("Pain Split", "Normal", 2, 32, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    527:Move("Parabolic Charge", "Electric", 1, 32, 65, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    528:Move("Parting Shot", "Dark", 2, 32, 0, 100, ["sound"], 0,
        False, True, True, False, True, False, dummy),
    529:Move("Pay Day", "Normal", 0, 32, 40, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    530:Move("Payback", "Dark", 0, 16, 50, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    531:Move("Peck", "Flying", 0, 56, 35, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    532:Move("Perish Song", "Normal", 2, 8, 0, 0, ["mouth", "sound"], 0,
        False, False, False, False, False, False, dummy),
    533:Move("Petal Blizzard", "Grass", 0, 24, 90, 100, ["wind"], 0,
        False, True, False, False, True, True, deal_damage),
    534:Move("Petal Dance", "Grass", 1, 16, 120, 100, ["dance"], 0,
        True, True, False, False, True, True, dummy),
    535:Move("Phantom Force", "Ghost", 0, 16, 90, 100, [""], 0,
        True, False, False, False, True, True, dummy),
    536:Move("Photon Geyser", "Psychic", 1, 8, 100, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    537:Move("Pika Papow", "Electric", 1, 32, 0, 0, [""], 0,
        False, True, False, False, False, True, dummy),
    538:Move("Pin Missile", "Bug", 0, 32, 25, 95, [""], 0,
        False, True, False, False, True, True, multihit),
    539:Move("Plasma Fists", "Electric", 0, 24, 100, 100, ["punch"], 0,
        True, True, False, False, True, True, dummy),
    540:Move("Play Nice", "Normal", 2, 32, 0, 0, [""], 0,
        False, False, True, False, True, False, dummy),
    541:Move("Play Rough", "Fairy", 0, 16, 90, 90, [""], 0,
        True, True, False, False, True, True, lower_atk),
    542:Move("Pluck", "Flying", 0, 32, 60, 100, ["mouth"], 0,
        True, True, False, False, True, True, dummy),
    543:Move("Poison Fang", "Poison", 0, 24, 50, 100, ["bite"], 0,
        True, True, False, False, True, False, poison),
    544:Move("Poison Gas", "Poison", 2, 64, 0, 90, [""], 0,
        False, True, True, False, True, False, poison),
    545:Move("Poison Jab", "Poison", 0, 32, 80, 100, [""], 0,
        True, True, False, False, True, True, poison),
    546:Move("Poison Powder", "Poison", 2, 56, 0, 75, ["spore"], 0,
        False, True, True, False, True, False, poison),
    547:Move("Poison Sting", "Poison", 0, 56, 15, 100, [""], 0,
        False, True, False, False, True, False, poison),
    548:Move("Poison Tail", "Poison", 0, 40, 50, 100, [""], 0,
        True, True, False, False, True, True, poison),
    549:Move("Pollen Puff", "Bug", 1, 24, 90, 100, ["ball"], 0,
        False, True, False, False, True, True, dummy),
    550:Move("Poltergeist", "Ghost", 0, 8, 110, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    551:Move("Population Bomb", "Normal", 0, 16, 20, 90, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    552:Move("Pounce", "Bug", 0, 32, 50, 100, [""], 0,
        True, True, False, False, True, True, lower_spd),
    553:Move("Pound", "Normal", 0, 56, 40, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    554:Move("Powder", "Bug", 2, 32, 0, 100, ["spore"], 1,
        False, True, True, False, True, False, dummy),
    555:Move("Powder Snow", "Ice", 1, 40, 40, 100, [""], 0,
        False, True, False, False, True, False, freeze),
    556:Move("Power Gem", "Rock", 1, 32, 80, 100, [""], 0,
        False, True, False, False, True, True, deal_damage),
    557:Move("Power Shift", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, True, False, dummy),
    558:Move("Power Split", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, False, False, dummy),
    559:Move("Power Swap", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    560:Move("Power Trick", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    561:Move("Power Trip", "Dark", 0, 16, 20, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    562:Move("Power Whip", "Grass", 0, 16, 120, 85, [""], 0,
        True, True, False, False, True, True, deal_damage),
    563:Move("Power-Up Punch", "Fighting", 0, 32, 40, 100, ["punch"], 0,
        True, True, False, False, True, True, raise_atk),
    564:Move("Precipice Blades", "Ground", 0, 16, 120, 85, [""], 0,
        False, True, False, False, True, True, deal_damage),
    565:Move("Present", "Normal", 0, 24, 0, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    566:Move("Prismatic Laser", "Psychic", 1, 16, 160, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    567:Move("Protect", "Normal", 2, 16, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    568:Move("Psybeam", "Psychic", 1, 32, 65, 100, [""], 0,
        False, True, False, False, True, False, confuse),
    569:Move("Psyblade", "Psychic", 0, 24, 80, 100, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    570:Move("Psych Up", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    571:Move("Psychic", "Psychic", 1, 16, 90, 100, [""], 0,
        False, True, False, False, True, False, lower_spdef),
    572:Move("Psychic Fangs", "Psychic", 0, 16, 85, 100, ["bite"], 0,
        True, True, False, False, True, True, deal_damage),
    573:Move("Psychic Terrain", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, set_terrain),
    574:Move("Psycho Boost", "Psychic", 1, 8, 140, 90, [""], 0,
        False, True, False, False, True, True, lower_self_spatk),
    575:Move("Psycho Cut", "Psychic", 0, 32, 70, 100, ["slice"], 0,
        False, True, False, False, True, True, deal_damage),
    576:Move("Psycho Shift", "Psychic", 2, 16, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    577:Move("Psyshield Bash", "Psychic", 0, 16, 70, 90, [""], 0,
        True, True, False, False, True, True, raise_def),
    578:Move("Psyshock", "Psychic", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    579:Move("Psystrike", "Psychic", 1, 16, 100, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    580:Move("Psywave", "Psychic", 1, 24, 0, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    581:Move("Pulverizing Pancake", "Normal", 0, 1, 210, 0, [""], 0,
        True, False, False, False, False, True, dummy),
    582:Move("Punishment", "Dark", 0, 8, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    583:Move("Purify", "Poison", 2, 32, 0, 0, [""], 0,
        False, True, True, False, False, False, dummy),
    584:Move("Pursuit", "Dark", 0, 32, 40, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    585:Move("Pyro Ball", "Fire", 0, 8, 120, 90, ["ball"], 0,
        False, True, False, False, True, True, burn),
    586:Move("Quash", "Dark", 2, 24, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    587:Move("Quick Attack", "Normal", 0, 48, 40, 100, [""], 1,
        True, True, False, False, True, True, deal_damage),
    588:Move("Quick Guard", "Fighting", 2, 24, 0, 0, [""], 3,
        False, False, False, True, False, False, dummy),
    589:Move("Quiver Dance", "Bug", 2, 32, 0, 0, ["dance"], 0,
        False, False, False, True, False, False, dummy),
    590:Move("Rage", "Normal", 0, 32, 20, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    591:Move("Rage Fist", "Ghost", 0, 16, 50, 100, ["punch"], 0,
        True, True, False, False, True, True, dummy),
    592:Move("Rage Powder", "Bug", 2, 32, 0, 0, ["spore"], 2,
        False, False, False, False, False, False, dummy),
    593:Move("Raging Bull", "Normal", 0, 16, 90, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    594:Move("Raging Fury", "Fire", 0, 16, 120, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    595:Move("Rain Dance", "Water", 2, 8, 0, 0, [""], 0,
        False, False, False, False, False, False, set_weather),
    596:Move("Rapid Spin", "Normal", 0, 64, 50, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    597:Move("Razor Leaf", "Grass", 0, 40, 55, 95, ["slice"], 0,
        False, True, False, False, True, True, deal_damage),
    598:Move("Razor Shell", "Water", 0, 16, 75, 95, ["slice"], 0,
        True, True, False, False, True, False, lower_def),
    599:Move("Razor Wind", "Normal", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    600:Move("Recover", "Normal", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    601:Move("Recycle", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    602:Move("Reflect", "Psychic", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    603:Move("Reflect Type", "Normal", 2, 24, 0, 0, [""], 0,
        False, True, False, False, False, False, dummy),
    604:Move("Refresh", "Normal", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    605:Move("Relic Song", "Normal", 1, 16, 75, 100, ["sound"], 0,
        False, True, False, False, True, False, sleep),
    606:Move("Rest", "Psychic", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    607:Move("Retaliate", "Normal", 0, 8, 70, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    608:Move("Return", "Normal", 0, 32, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    609:Move("Revelation Dance", "Normal", 1, 24, 90, 100, ["dance"], 0,
        False, True, False, False, True, True, dummy),
    610:Move("Revenge", "Fighting", 0, 16, 60, 100, [""], -4,
        True, True, False, False, True, True, dummy),
    611:Move("Reversal", "Fighting", 0, 24, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    612:Move("Revival Blessing", "Normal", 2, 1, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    613:Move("Rising Voltage", "Electric", 1, 32, 70, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    614:Move("Roar", "Normal", 2, 32, 0, 0, ["mouth", "sound"], -6,
        False, False, True, False, True, False, dummy),
    615:Move("Roar of Time", "Dragon", 1, 8, 150, 90, ["mouth"], 0,
        False, True, False, False, True, True, dummy),
    616:Move("Rock Blast", "Rock", 0, 16, 25, 90, ["ball"], 0,
        False, True, False, False, True, True, multihit),
    617:Move("Rock Climb", "Normal", 0, 32, 90, 85, [""], 0,
        True, True, False, False, True, True, confuse),
    618:Move("Rock Polish", "Rock", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    619:Move("Rock Slide", "Rock", 0, 16, 75, 90, [""], 0,
        False, True, False, False, True, False, deal_damage),
    620:Move("Rock Smash", "Fighting", 0, 24, 40, 100, [""], 0,
        True, True, False, False, True, False, lower_def),
    621:Move("Rock Throw", "Rock", 0, 24, 50, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    622:Move("Rock Tomb", "Rock", 0, 24, 60, 95, [""], 0,
        False, True, False, False, True, False, lower_spd),
    623:Move("Rock Wrecker", "Rock", 0, 8, 150, 90, ["ball"], 0,
        False, True, False, False, True, True, dummy),
    624:Move("Role Play", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    625:Move("Rolling Kick", "Fighting", 0, 24, 60, 85, [""], 0,
        True, True, False, False, True, False, deal_damage),
    626:Move("Rollout", "Rock", 0, 32, 30, 90, [""], 0,
        True, True, False, False, True, True, dummy),
    627:Move("Roost", "Flying", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    628:Move("Rototiller", "Ground", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    629:Move("Round", "Normal", 1, 24, 60, 100, ["sound"], 0,
        False, True, False, False, True, True, dummy),
    630:Move("Ruination", "Dark", 1, 16, 0, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    631:Move("Sacred Fire", "Fire", 0, 8, 100, 95, [""], 0,
        False, True, False, False, True, False, burn),
    632:Move("Sacred Sword", "Fighting", 0, 24, 90, 100, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    633:Move("Safeguard", "Normal", 2, 40, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    634:Move("Salt Cure", "Rock", 0, 24, 40, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    635:Move("Sand Attack", "Ground", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    636:Move("Sand Tomb", "Ground", 0, 24, 35, 85, [""], 0,
        False, True, False, False, True, True, dummy),
    637:Move("Sandsear Storm", "Ground", 1, 16, 100, 80, ["wind"], 0,
        False, True, False, False, True, True, burn),
    638:Move("Sandstorm", "Rock", 2, 16, 0, 0, ["wind"], 0,
        False, False, False, False, False, False, set_weather),
    639:Move("Sappy Seed", "Grass", 0, 24, 90, 100, [""], 0,
        False, True, True, False, False, False, dummy),
    640:Move("Savage Spin-Out", "Bug", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    641:Move("Scald", "Water", 1, 24, 80, 100, [""], 0,
        False, True, False, False, True, True, burn),
    642:Move("Scale Shot", "Dragon", 0, 32, 25, 90, [""], 0,
        False, True, False, False, True, True, multihit),
    643:Move("Scary Face", "Normal", 2, 16, 0, 100, [""], 0,
        False, True, True, False, True, False, lower_spd),
    644:Move("Scorching Sands", "Ground", 1, 16, 70, 100, [""], 0,
        False, True, False, False, True, True, burn),
    645:Move("Scratch", "Normal", 0, 56, 40, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    646:Move("Screech", "Normal", 2, 64, 0, 85, ["mouth", "sound"], 0,
        False, True, True, False, True, False, lower_def),
    647:Move("Searing Shot", "Fire", 1, 8, 100, 100, ["ball"], 0,
        False, True, False, False, True, True, burn),
    648:Move("Searing Sunraze Smash", "Steel", 0, 1, 200, 0, [""], 0,
        True, False, False, False, False, True, dummy),
    649:Move("Secret Power", "Normal", 0, 32, 70, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    650:Move("Secret Sword", "Fighting", 1, 16, 85, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    651:Move("Seed Bomb", "Grass", 0, 24, 80, 100, ["ball"], 0,
        False, True, False, False, True, True, deal_damage),
    652:Move("Seed Flare", "Grass", 1, 8, 120, 85, [""], 0,
        False, True, False, False, True, True, lower_spdef),
    653:Move("Seismic Toss", "Fighting", 0, 32, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    654:Move("Self-Destruct", "Normal", 0, 8, 200, 100, ["explosive"], 0,
        False, True, False, False, True, True, dummy),
    655:Move("Shadow Ball", "Ghost", 1, 24, 80, 100, ["ball"], 0,
        False, True, False, False, True, False, lower_spdef),
    656:Move("Shadow Bone", "Ghost", 0, 16, 85, 100, [""], 0,
        False, True, False, False, True, True, lower_def),
    657:Move("Shadow Claw", "Ghost", 0, 24, 70, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    658:Move("Shadow Force", "Ghost", 0, 8, 120, 100, [""], 0,
        True, False, False, False, True, True, dummy),
    659:Move("Shadow Punch", "Ghost", 0, 32, 60, 0, ["punch"], 0,
        True, True, False, False, True, True, dummy),
    660:Move("Shadow Sneak", "Ghost", 0, 48, 40, 100, [""], 1,
        True, True, False, False, True, True, dummy),
    661:Move("Sharpen", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_atk),
    662:Move("Shattered Psyche", "Psychic", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    663:Move("Shed Tail", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    664:Move("Sheer Cold", "Ice", 1, 8, 0, 30, [""], 0,
        False, True, False, False, False, False, dummy),
    665:Move("Shell Side Arm", "Poison", 1, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    666:Move("Shell Smash", "Normal", 2, 24, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    667:Move("Shell Trap", "Fire", 1, 8, 150, 100, [""], -3,
        False, True, False, False, False, True, dummy),
    668:Move("Shelter", "Steel", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_def),
    669:Move("Shift Gear", "Steel", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    670:Move("Shock Wave", "Electric", 1, 32, 60, 0, [""], 0,
        False, True, False, False, True, True, dummy),
    671:Move("Shore Up", "Ground", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    672:Move("Signal Beam", "Bug", 1, 24, 75, 100, [""], 0,
        False, True, False, False, True, True, confuse),
    673:Move("Silk Trap", "Bug", 2, 16, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    674:Move("Silver Wind", "Bug", 1, 8, 60, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    675:Move("Simple Beam", "Normal", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    676:Move("Sing", "Normal", 2, 24, 0, 55, ["mouth", "sound"], 0,
        False, True, True, False, True, False, sleep),
    677:Move("Sinister Arrow Raid", "Ghost", 0, 1, 180, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    678:Move("Sizzly Slide", "Fire", 0, 24, 90, 100, [""], 0,
        True, True, False, False, False, True, burn),
    679:Move("Sketch", "Normal", 2, 1, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    680:Move("Skill Swap", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    681:Move("Skitter Smack", "Bug", 0, 16, 70, 90, [""], 0,
        True, True, False, False, True, True, lower_spatk),
    682:Move("Skull Bash", "Normal", 0, 16, 130, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    683:Move("Sky Attack", "Flying", 0, 8, 140, 90, [""], 0,
        False, True, False, False, True, False, dummy),
    684:Move("Sky Drop", "Flying", 0, 16, 60, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    685:Move("Sky Uppercut", "Fighting", 0, 24, 85, 90, ["punch"], 0,
        True, True, False, False, True, True, dummy),
    686:Move("Slack Off", "Normal", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    687:Move("Slam", "Normal", 0, 32, 80, 75, [""], 0,
        True, True, False, False, True, True, deal_damage),
    688:Move("Slash", "Normal", 0, 32, 70, 100, ["slice"], 0,
        True, True, False, False, True, True, deal_damage),
    689:Move("Sleep Powder", "Grass", 2, 24, 0, 75, ["spore"], 0,
        False, True, True, False, True, False, sleep),
    690:Move("Sleep Talk", "Normal", 2, 16, 0, 0, ["mouth"], 0,
        False, False, False, False, False, False, dummy),
    691:Move("Sludge", "Poison", 1, 32, 65, 100, [""], 0,
        False, True, False, False, True, False, poison),
    693:Move("Sludge Bomb", "Poison", 1, 16, 90, 100, ["ball"], 0,
        False, True, False, False, True, False, poison),
    694:Move("Sludge Wave", "Poison", 1, 16, 95, 100, [""], 0,
        False, True, False, False, True, False, poison),
    695:Move("Smack Down", "Rock", 0, 24, 50, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    696:Move("Smart Strike", "Steel", 0, 16, 70, 0, [""], 0,
        True, True, False, False, True, True, dummy),
    697:Move("Smelling Salts", "Normal", 0, 16, 70, 100, [""], 0,
        True, True, False, False, True, False, dummy),
    698:Move("Smog", "Poison", 1, 32, 30, 70, [""], 0,
        False, True, False, False, True, False, poison),
    699:Move("Smokescreen", "Normal", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    700:Move("Snap Trap", "Grass", 0, 24, 35, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    701:Move("Snarl", "Dark", 1, 24, 55, 95, ["sound"], 0,
        False, True, False, False, True, True, lower_spatk),
    702:Move("Snatch", "Dark", 2, 16, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    704:Move("Snipe Shot", "Water", 1, 24, 80, 100, [""], 0,
        False, True, False, False, True, True, deal_damage),
    705:Move("Snore", "Normal", 1, 24, 50, 100, ["mouth", "sound"], 0,
        False, True, False, False, True, False, dummy),
    706:Move("Snowscape", "Ice", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    707:Move("Soak", "Water", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    708:Move("Soft-Boiled", "Normal", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    709:Move("Solar Beam", "Grass", 1, 16, 120, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    710:Move("Solar Blade", "Grass", 0, 16, 125, 100, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    711:Move("Sonic Boom", "Normal", 1, 32, 0, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    712:Move("Soul-Stealing 7-Star Strike", "Ghost", 0, 1, 195, 0, [""], 0,
        True, False, False, False, False, True, dummy),
    713:Move("Spacial Rend", "Dragon", 1, 8, 100, 95, [""], 0,
        False, True, False, False, True, True, deal_damage),
    714:Move("Spark", "Electric", 0, 32, 65, 100, [""], 0,
        True, True, False, False, True, False, paralysis),
    715:Move("Sparkling Aria", "Water", 1, 16, 90, 100, ["sound"], 0,
        False, True, False, False, True, True, dummy),
    716:Move("Sparkly Swirl", "Fairy", 1, 24, 90, 100, [""], 0,
        False, True, False, False, False, True, dummy),
    717:Move("Spectral Thief", "Ghost", 0, 16, 90, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    718:Move("Speed Swap", "Psychic", 2, 16, 0, 0, [""], 0,
        False, True, False, False, True, False, dummy),
    719:Move("Spicy Extract", "Grass", 2, 24, 0, 0, [""], 0,
        False, True, True, False, True, False, dummy),
    720:Move("Spider Web", "Bug", 2, 16, 0, 0, [""], 0,
        False, False, True, False, True, False, dummy),
    721:Move("Spike Cannon", "Normal", 0, 24, 20, 100, [""], 0,
        False, True, False, False, True, True, multihit),
    722:Move("Spikes", "Ground", 2, 32, 0, 0, [""], 0,
        False, False, True, False, False, False, dummy),
    723:Move("Spiky Shield", "Grass", 2, 16, 0, 0, [""], 4,
        False, False, False, False, False, False, dummy),
    724:Move("Spin Out", "Steel", 0, 8, 100, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    725:Move("Spirit Break", "Fairy", 0, 24, 75, 100, [""], 0,
        True, True, False, False, True, True, lower_spatk),
    726:Move("Spirit Shackle", "Ghost", 0, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    727:Move("Spit Up", "Normal", 1, 16, 0, 100, ["mouth"], 0,
        False, True, False, False, False, True, dummy),
    728:Move("Spite", "Ghost", 2, 16, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    729:Move("Splash", "Normal", 2, 64, 0, 0, [""], 0,
        False, False, False, False, False, False, splash),
    730:Move("Splintered Stormshards", "Rock", 0, 1, 190, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    731:Move("Splishy Splash", "Water", 1, 24, 90, 100, [""], 0,
        False, True, False, False, False, False, paralysis),
    732:Move("Spore", "Grass", 2, 24, 0, 100, ["spore"], 0,
        False, True, True, False, True, False, sleep),
    733:Move("Spotlight", "Normal", 2, 24, 0, 0, [""], 3,
        False, True, True, False, False, False, dummy),
    734:Move("Springtide Storm", "Fairy", 1, 8, 100, 80, ["wind"], 0,
        False, True, False, False, True, False, lower_atk),
    735:Move("Stealth Rock", "Rock", 2, 32, 0, 0, [""], 0,
        False, False, True, False, False, False, dummy),
    736:Move("Steam Eruption", "Water", 1, 8, 110, 95, [""], 0,
        False, True, False, False, True, True, burn),
    737:Move("Steamroller", "Bug", 0, 32, 65, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    738:Move("Steel Beam", "Steel", 1, 8, 140, 95, [""], 0,
        False, True, False, False, True, True, dummy),
    739:Move("Steel Roller", "Steel", 0, 8, 130, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    740:Move("Steel Wing", "Steel", 0, 40, 70, 90, [""], 0,
        True, True, False, False, True, True, raise_def),
    741:Move("Sticky Web", "Bug", 2, 32, 0, 0, [""], 0,
        False, False, True, False, False, False, dummy),
    742:Move("Stockpile", "Normal", 2, 32, 0, 0, ["mouth"], 0,
        False, False, False, True, False, False, dummy),
    743:Move("Stoked Sparksurfer", "Electric", 1, 1, 175, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    744:Move("Stomp", "Normal", 0, 32, 65, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    745:Move("Stomping Tantrum", "Ground", 0, 16, 75, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    746:Move("Stone Axe", "Rock", 0, 24, 65, 90, ["slice"], 0,
        True, True, False, False, True, True, dummy),
    747:Move("Stone Edge", "Rock", 0, 8, 100, 80, [""], 0,
        False, True, False, False, True, True, deal_damage),
    748:Move("Stored Power", "Psychic", 1, 16, 20, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    749:Move("Storm Throw", "Fighting", 0, 16, 60, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    750:Move("Strange Steam", "Fairy", 1, 16, 90, 95, [""], 0,
        False, True, False, False, True, True, confuse),
    751:Move("Strength", "Normal", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    752:Move("Strength Sap", "Grass", 2, 16, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    753:Move("String Shot", "Bug", 2, 64, 0, 95, [""], 0,
        False, True, True, False, True, False, lower_spd),
    754:Move("Struggle", "Normal", 0, 1, 50, 0, [""], 0,
        True, True, False, False, False, True, dummy),
    755:Move("Struggle Bug", "Bug", 1, 32, 50, 100, [""], 0,
        False, True, False, False, True, False, lower_spatk),
    756:Move("Stuff Cheeks", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    757:Move("Stun Spore", "Grass", 2, 48, 0, 75, ["spore"], 0,
        False, True, True, False, True, False, paralysis),
    758:Move("Submission", "Fighting", 0, 32, 80, 80, [""], 0,
        True, True, False, False, True, True, recoil),
    759:Move("Substitute", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    760:Move("Subzero Slammer", "Ice", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    761:Move("Sucker Punch", "Dark", 0, 8, 70, 100, [""], 1,
        True, True, False, False, True, True, dummy),
    762:Move("Sunny Day", "Fire", 2, 8, 0, 0, [""], 0,
        False, False, False, False, False, False, set_weather),
    763:Move("Sunsteel Strike", "Steel", 0, 8, 100, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    764:Move("Super Fang", "Normal", 0, 16, 0, 90, ["mouth"], 0,
        True, True, False, False, True, False, dummy),
    765:Move("Superpower", "Fighting", 0, 8, 120, 100, [""], 0,
        True, True, False, False, True, False, dummy),
    766:Move("Supersonic", "Normal", 2, 32, 0, 55, ["mouth", "sound"], 0,
        False, True, True, False, True, False, confuse),
    767:Move("Supersonic Skystrike", "Flying", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    768:Move("Surf", "Water", 1, 24, 90, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    769:Move("Surging Strikes", "Water", 0, 8, 25, 100, ["punch"], 0,
        True, True, False, False, True, True, multihit),
    770:Move("Swagger", "Normal", 2, 24, 0, 85, [""], 0,
        False, True, True, False, True, False, dummy),
    771:Move("Swallow", "Normal", 2, 16, 0, 0, ["mouth"], 0,
        False, False, False, True, False, False, dummy),
    772:Move("Sweet Kiss", "Fairy", 2, 16, 0, 75, ["mouth"], 0,
        False, True, True, False, True, False, confuse),
    773:Move("Sweet Scent", "Normal", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    774:Move("Swift", "Normal", 1, 32, 60, 0, [""], 0,
        False, True, False, False, True, True, dummy),
    775:Move("Switcheroo", "Dark", 2, 16, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    776:Move("Swords Dance", "Normal", 2, 32, 0, 0, ["dance"], 0,
        False, False, False, True, False, False, raise_atk),
    777:Move("Synchronoise", "Psychic", 1, 16, 120, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    778:Move("Synthesis", "Grass", 2, 8, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    779:Move("Tackle", "Normal", 0, 56, 40, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    780:Move("Tail Glow", "Bug", 2, 32, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_spatk),
    781:Move("Tail Slap", "Normal", 0, 16, 25, 85, [""], 0,
        True, True, False, False, True, True, multihit),
    782:Move("Tail Whip", "Normal", 2, 48, 0, 100, [""], 0,
        False, True, True, False, True, False, lower_def),
    783:Move("Tailwind", "Flying", 2, 24, 0, 0, ["wind"], 0,
        False, False, False, True, False, False, dummy),
    784:Move("Take Down", "Normal", 0, 32, 90, 85, [""], 0,
        True, True, False, False, True, True, recoil),
    785:Move("Take Heart", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    786:Move("Tar Shot", "Rock", 2, 24, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    787:Move("Taunt", "Dark", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    788:Move("Tearful Look", "Normal", 2, 32, 0, 0, [""], 0,
        False, False, True, False, True, False, dummy),
    789:Move("Teatime", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    790:Move("Techno Blast", "Normal", 1, 8, 120, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    791:Move("Tectonic Rage", "Ground", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    792:Move("Teeter Dance", "Normal", 2, 32, 0, 100, ["dance"], 0,
        False, True, False, False, True, False, confuse),
    793:Move("Telekinesis", "Psychic", 2, 24, 0, 0, [""], 0,
        False, True, True, False, False, False, dummy),
    794:Move("Teleport", "Psychic", 2, 32, 0, 0, [""], -6,
        False, False, False, False, False, False, dummy),
    795:Move("Tera Blast", "Normal", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    796:Move("Terrain Pulse", "Normal", 1, 16, 50, 100, ["aura"], 0,
        False, True, False, False, True, True, dummy),
    797:Move("Thief", "Dark", 0, 40, 60, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    798:Move("Thousand Arrows", "Ground", 0, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    799:Move("Thousand Waves", "Ground", 0, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    800:Move("Thrash", "Normal", 0, 16, 120, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    801:Move("Throat Chop", "Dark", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    802:Move("Thunder", "Electric", 1, 16, 110, 70, [""], 0,
        False, True, False, False, True, False, paralysis),
    803:Move("Thunder Cage", "Electric", 1, 24, 80, 90, [""], 0,
        False, True, False, False, True, True, dummy),
    804:Move("Thunder Fang", "Electric", 0, 24, 65, 95, ["bite", "mouth"], 0,
        True, True, False, False, True, False, paralysis),
    805:Move("Thunder Punch", "Electric", 0, 24, 75, 100, ["punch"], 0,
        True, True, False, False, True, False, paralysis),
    806:Move("Thunder Shock", "Electric", 1, 48, 40, 100, [""], 0,
        False, True, False, False, True, False, paralysis),
    807:Move("Thunder Wave", "Electric", 2, 32, 0, 90, [""], 0,
        False, True, True, False, True, False, paralysis),
    808:Move("Thunderbolt", "Electric", 1, 24, 90, 100, [""], 0,
        False, True, False, False, True, False, paralysis),
    809:Move("Thunderous Kick", "Fighting", 0, 16, 90, 100, [""], 0,
        True, True, False, False, True, True, lower_def),
    810:Move("Tickle", "Normal", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    811:Move("Tidy Up", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    812:Move("Topsy-Turvy", "Dark", 2, 32, 0, 0, [""], 0,
        False, True, True, False, True, False, dummy),
    813:Move("Torch Song", "Fire", 1, 16, 80, 100, ["sound"], 0,
        False, True, False, False, True, True, raise_spatk),
    814:Move("Torment", "Dark", 2, 24, 0, 100, ["mouth"], 0,
        False, True, True, False, True, False, dummy),
    815:Move("Toxic", "Poison", 2, 16, 0, 90, [""], 0,
        False, True, True, False, True, False, poison),
    816:Move("Toxic Spikes", "Poison", 2, 32, 0, 0, [""], 0,
        False, False, True, False, False, False, dummy),
    817:Move("Toxic Thread", "Poison", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    818:Move("Trailblaze", "Grass", 0, 32, 50, 100, [""], 0,
        True, True, False, False, True, True, raise_spd),
    819:Move("Transform", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    820:Move("Tri Attack", "Normal", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    821:Move("Trick", "Psychic", 2, 16, 0, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    822:Move("Trick Room", "Psychic", 2, 8, 0, 0, [""], -7,
        False, False, False, False, True, False, dummy),
    823:Move("Trick-or-Treat", "Ghost", 2, 32, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    824:Move("Triple Arrows", "Fighting", 0, 16, 90, 100, [""], 0,
        False, True, False, False, True, True, lower_def),
    825:Move("Triple Axel", "Ice", 0, 16, 20, 90, [""], 0,
        True, True, False, False, True, True, dummy),
    826:Move("Triple Dive", "Water", 0, 16, 30, 95, [""], 0,
        True, True, False, False, True, True, dummy),
    827:Move("Triple Kick", "Fighting", 0, 16, 10, 90, [""], 0,
        True, True, False, False, True, True, multihit),
    828:Move("Trop Kick", "Grass", 0, 24, 70, 100, [""], 0,
        True, True, False, False, True, True, lower_atk),
    829:Move("Trump Card", "Normal", 1, 8, 0, 0, [""], 0,
        True, True, False, False, True, True, dummy),
    830:Move("Twin Beam", "Psychic", 1, 16, 40, 100, [""], 0,
        False, True, False, False, True, True, multihit),
    831:Move("Twineedle", "Bug", 0, 32, 25, 100, [""], 0,
        False, True, False, False, True, True, multihit),
    832:Move("Twinkle Tackle", "Fairy", 3, 1, 0, 0, [""], 0,
        False, False, False, False, False, True, dummy),
    833:Move("Twister", "Dragon", 1, 32, 40, 100, ["wind"], 0,
        False, True, False, False, True, False, deal_damage),
    834:Move("U-turn", "Bug", 0, 32, 70, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    835:Move("Uproar", "Normal", 1, 16, 90, 100, ["mouth", "sound"], 0,
        False, True, False, False, True, True, dummy),
    836:Move("V-create", "Fire", 0, 8, 180, 95, [""], 0,
        True, True, False, False, True, True, dummy),
    837:Move("Vacuum Wave", "Fighting", 1, 48, 40, 100, [""], 1,
        False, True, False, False, True, True, dummy),
    838:Move("Veevee Volley", "Normal", 0, 32, 0, 0, [""], 0,
        True, True, False, False, False, True, dummy),
    839:Move("Venom Drench", "Poison", 2, 32, 0, 100, [""], 0,
        False, True, True, False, False, False, dummy),
    840:Move("Venoshock", "Poison", 1, 24, 65, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    841:Move("Victory Dance", "Fighting", 2, 16, 0, 0, ["dance"], 0,
        False, False, False, True, False, False, dummy),
    842:Move("Vine Whip", "Grass", 0, 40, 45, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    843:Move("Vise Grip", "Normal", 0, 48, 55, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    844:Move("Vital Throw", "Fighting", 0, 16, 70, 0, [""], -1,
        True, True, False, False, True, True, dummy),
    845:Move("Volt Switch", "Electric", 1, 32, 70, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    846:Move("Volt Tackle", "Electric", 0, 24, 120, 100, [""], 0,
        True, True, False, False, True, True, recoil),
    847:Move("Wake-Up Slap", "Fighting", 0, 16, 70, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    848:Move("Water Gun", "Water", 1, 40, 40, 100, [""], 0,
        False, True, False, False, True, True, deal_damage),
    849:Move("Water Pledge", "Water", 1, 16, 80, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    850:Move("Water Pulse", "Water", 1, 32, 60, 100, ["aura"], 0,
        False, True, False, False, True, True, confuse),
    851:Move("Water Shuriken", "Water", 1, 32, 15, 100, [""], 1,
        False, True, False, False, True, True, multihit),
    852:Move("Water Sport", "Water", 2, 24, 0, 0, [""], 0,
        False, False, False, False, False, False, dummy),
    853:Move("Water Spout", "Water", 1, 8, 150, 100, [""], 0,
        False, True, False, False, True, False, dummy),
    854:Move("Waterfall", "Water", 0, 24, 80, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    855:Move("Wave Crash", "Water", 0, 16, 120, 100, [""], 0,
        True, True, False, False, True, True, recoil),
    856:Move("Weather Ball", "Normal", 1, 16, 50, 100, ["ball"], 0,
        False, True, False, False, True, True, dummy),
    857:Move("Whirlpool", "Water", 1, 24, 35, 85, [""], 0,
        False, True, False, False, True, True, dummy),
    858:Move("Flail", "Normal", 0, 24, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    859:Move("Whirlwind", "Flying", 2, 32, 0, 0, ["wind"], -6,
        False, False, True, False, True, False, dummy),
    860:Move("Wicked Blow", "Dark", 0, 8, 75, 100, ["punch"], 0,
        True, True, False, False, True, True, deal_damage),
    861:Move("Wicked Torque", "Dark", 0, 16, 80, 100, [""], 0,
        False, True, False, False, False, False, dummy),
    862:Move("Wide Guard", "Rock", 2, 16, 0, 0, [""], 3,
        False, False, False, True, False, False, dummy),
    863:Move("Wild Charge", "Electric", 0, 24, 90, 100, [""], 0,
        True, True, False, False, True, True, recoil),
    864:Move("Wildbolt Storm", "Electric", 1, 16, 100, 80, ["wind"], 0,
        False, True, False, False, True, True, paralysis),
    865:Move("Will-O-Wisp", "Fire", 2, 24, 0, 85, [""], 0,
        False, True, True, False, True, False, burn),
    866:Move("Wing Attack", "Flying", 0, 56, 60, 100, [""], 0,
        True, True, False, False, True, True, deal_damage),
    867:Move("Wish", "Normal", 2, 16, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    868:Move("Withdraw", "Water", 2, 64, 0, 0, [""], 0,
        False, False, False, True, False, False, raise_def),
    869:Move("Wonder Room", "Psychic", 2, 16, 0, 0, [""], 0,
        False, False, False, False, True, False, dummy),
    870:Move("Wood Hammer", "Grass", 0, 24, 120, 100, [""], 0,
        True, True, False, False, True, True, recoil),
    871:Move("Work Up", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    872:Move("Worry Seed", "Grass", 2, 16, 0, 100, [""], 0,
        False, True, True, False, True, False, dummy),
    873:Move("Wrap", "Normal", 0, 32, 15, 90, [""], 0,
        True, True, False, False, True, True, dummy),
    874:Move("Wring Out", "Normal", 1, 8, 0, 100, [""], 0,
        True, True, False, False, True, True, dummy),
    875:Move("X-Scissor", "Bug", 0, 24, 80, 100, ["slice"], 0,
        True, True, False, False, True, True, deal_damage),
    876:Move("Yawn", "Normal", 2, 16, 0, 0, ["mouth"], 0,
        False, True, True, False, True, False, dummy),
    877:Move("Zap Cannon", "Electric", 1, 8, 120, 50, ["ball"], 0,
        False, True, False, False, True, False, paralysis),
    878:Move("Zen Headbutt", "Psychic", 0, 24, 80, 90, [""], 0,
        True, True, False, False, True, False, deal_damage),
    879:Move("Zippy Zap", "Electric", 0, 24, 50, 100, [""], 2,
        True, True, False, False, False, False, dummy),
    880:Move("Flame Burst", "Fire", 1, 24, 70, 100, [""], 0,
        False, True, False, False, True, True, dummy),
    881:Move("Flame Charge", "Fire", 0, 32, 50, 100, [""], 0,
        True, True, False, False, True, True, raise_spd),
    882:Move("Flame Wheel", "Fire", 0, 40, 60, 100, [""], 0,
        True, True, False, False, True, False, burn),
    883:Move("Flamethrower", "Fire", 1, 24, 90, 100, [""], 0,
        False, True, False, False, True, False, burn),
    884:Move("Flare Blitz", "Fire", 0, 24, 120, 100, [""], 0,
        True, True, False, False, True, True, burn),
    885:Move("Laser Focus", "Normal", 2, 48, 0, 0, [""], 0,
        False, False, False, True, False, False, dummy),
    886:Move("Zing Zap", "Electric", 0, 16, 80, 100, [""], 0,
        True, True, False, False, True, False, deal_damage),
    887:Move("Ancient Power", "Rock", 1, 8, 60, 100, [""], 0,
        False, True, False, False, True, False, dummy)
}