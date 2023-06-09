#Final Project - Keaghan Irwin - CS30
#This file is just one big dict storing every ability and their functions
import pygame as pg
import pygame.math as pm
import pygame.image as pp
import pygame.display as pd

class Ability:
    def __init__(self, name, effect):
        self.name = name; self.effect = effect

def Dummy():
    pass

ability_dex = {
    -1:Ability('None', Dummy()),
    0:Ability("Stench", Dummy()),
    1:Ability("Drizzle", Dummy()),
    2:Ability("Speed Boost", Dummy()),
    3:Ability("Battle Armor", Dummy()),
    4:Ability("Sturdy", Dummy()),
    5:Ability("Damp", Dummy()),
    6:Ability("Limber", Dummy()),
    7:Ability("Sand Veil", Dummy()),
    8:Ability("Static", Dummy()),
    9:Ability("Volt Absorb", Dummy()),
    10:Ability("Water Absorb", Dummy()),
    11:Ability("Oblivious", Dummy()),
    12:Ability("Cloud Nine", Dummy()),
    13:Ability("Compound Eyes", Dummy()),
    14:Ability("Insomnia", Dummy()),
    15:Ability("Colour Change", Dummy()),
    16:Ability("Immunity", Dummy()),
    17:Ability("Flash Fire", Dummy()),
    18:Ability("Shield Dust", Dummy()),
    19:Ability("Own Tempo", Dummy()),
    20:Ability("Suction Cups", Dummy()),
    21:Ability("Intimidate", Dummy()),
    22:Ability("Shadow Tag", Dummy()),
    23:Ability("Rough Skin", Dummy()),
    24:Ability("Wonder Guard", Dummy()),
    25:Ability("Levitate", Dummy()),
    26:Ability("Effect Spore", Dummy()),
    27:Ability("Synchronize", Dummy()),
    28:Ability("Clear Body", Dummy()),
    29:Ability("Natural Cure", Dummy()),
    30:Ability("Lightning Rod", Dummy()),
    31:Ability("Serene Grace", Dummy()),
    32:Ability("Swift Swim", Dummy()),
    33:Ability("Chlorophyll", Dummy()),
    34:Ability("Illuminate", Dummy()),
    35:Ability("Trace", Dummy()),
    36:Ability("Huge Power", Dummy()),
    37:Ability("Poison Point", Dummy()),
    38:Ability("Inner Focus", Dummy()),
    39:Ability("Magma Armour", Dummy()),
    40:Ability("Water Veil", Dummy()),
    41:Ability("Magnet Pull", Dummy()),
    42:Ability("Soundproof", Dummy()),
    43:Ability("Rain Dish", Dummy()),
    44:Ability("Sand Stream", Dummy()),
    45:Ability("Pressure", Dummy()),
    46:Ability("Thick Fat", Dummy()),
    47:Ability("Early Bird", Dummy()),
    48:Ability("Flame Body", Dummy()),
    49:Ability("Run Away", Dummy()),
    50:Ability("Keen Eye", Dummy()),
    51:Ability("Hyper Cutter", Dummy()),
    52:Ability("Pickup", Dummy()),
    53:Ability("Truant", Dummy()),
    54:Ability("Hustle", Dummy()),
    55:Ability("Cute Charm", Dummy()),
    56:Ability("Plus", Dummy()),
    57:Ability("Minus", Dummy()),
    58:Ability("Forecast", Dummy()),
    59:Ability("Sticky Hold", Dummy()),
    60:Ability("Shed Skin", Dummy()),
    61:Ability("Guts", Dummy()),
    62:Ability("Marvel Scale", Dummy()),
    63:Ability("Liquid Ooze", Dummy()),
    64:Ability("Overgrow", Dummy()),
    65:Ability("Blaze", Dummy()),
    66:Ability("Torrent", Dummy()),
    67:Ability("Swarm", Dummy()),
    68:Ability("Rock Head", Dummy()),
    69:Ability("Drought", Dummy()),
    70:Ability("Arena Trap", Dummy()),
    71:Ability("Vital Spirit", Dummy()),
    72:Ability("White Smoke", Dummy()),
    73:Ability("Pure Power", Dummy()),
    74:Ability("Shell Armor", Dummy()),
    75:Ability("Air Lock", Dummy()),
    76:Ability("Tangled Feet", Dummy()),
    77:Ability("Motor Drive", Dummy()),
    78:Ability("Rivalry", Dummy()),
    79:Ability("Steadfast", Dummy()),
    80:Ability("Snow Cloak", Dummy()),
    81:Ability("Gluttony", Dummy()),
    82:Ability("Anger Point", Dummy()),
    83:Ability("Unburden", Dummy()),
    84:Ability("Heatproof", Dummy()),
    85:Ability("Simple", Dummy()),
    86:Ability("Dry Skin", Dummy()),
    87:Ability("Download", Dummy()),
    88:Ability("Iron Fist", Dummy()),
    89:Ability("Poison Heal", Dummy()),
    90:Ability("Adaptability", Dummy()),
    91:Ability("Skill Link", Dummy()),
    92:Ability("Hydration", Dummy()),
    93:Ability("Solar Power", Dummy()),
    94:Ability("Quick Feet", Dummy()),
    95:Ability("Normalize", Dummy()),
    96:Ability("Sniper", Dummy()),
    97:Ability("Magic Guard", Dummy()),
    98:Ability("No Guard", Dummy()),
    99:Ability("Stall", Dummy()),
    100:Ability("Technician", Dummy()),
    101:Ability("Leaf Guard", Dummy()),
    102:Ability("Klutz", Dummy()),
    103:Ability("Mold Breaker", Dummy()),
    104:Ability("Super Luck", Dummy()),
    105:Ability("Aftermath", Dummy()),
    106:Ability("Anticipation", Dummy()),
    107:Ability("Forewarn", Dummy()),
    108:Ability("Unaware", Dummy()),
    109:Ability("Tinted Lens", Dummy()),
    110:Ability("Filter", Dummy()),
    111:Ability("Slow Start", Dummy()),
    112:Ability("Scrappy", Dummy()),
    113:Ability("Storm Drain", Dummy()),
    114:Ability("Ice Body", Dummy()),
    115:Ability("Solid Rock", Dummy()),
    116:Ability("Snow Warning", Dummy()),
    117:Ability("Honey Gather", Dummy()),
    118:Ability("Frisk", Dummy()),
    119:Ability("Reckless", Dummy()),
    120:Ability("Multitype", Dummy()),
    121:Ability("Flower Gift", Dummy()),
    122:Ability("Bad Dreams", Dummy()),
    123:Ability("Pickpocket", Dummy()),
    124:Ability("Sheer Force", Dummy()),
    125:Ability("Contrary", Dummy()),
    126:Ability("Unnerve", Dummy()),
    127:Ability("Defiant", Dummy()),
    128:Ability("Defeatist", Dummy()),
    129:Ability("Cursed Body", Dummy()),
    130:Ability("Healer", Dummy()),
    131:Ability("Friend Guard", Dummy()),
    132:Ability("Weak Armour", Dummy()),
    133:Ability("Heavy Metal", Dummy()),
    134:Ability("Light Metal", Dummy()),
    135:Ability("Multiscale", Dummy()),
    136:Ability("Toxic Boost", Dummy()),
    137:Ability("Flare Boost", Dummy()),
    138:Ability("Harvest", Dummy()),
    139:Ability("Telepathy", Dummy()),
    140:Ability("Moody", Dummy()),
    141:Ability("Overcoat", Dummy()),
    142:Ability("Poison Touch", Dummy()),
    143:Ability("Regenerator", Dummy()),
    144:Ability("Big Pecks", Dummy()),
    145:Ability("Sand Rush", Dummy()),
    146:Ability("Wonder Skin", Dummy()),
    147:Ability("Analytic", Dummy()),
    148:Ability("Illusion", Dummy()),
    149:Ability("Impostor", Dummy()),
    150:Ability("Infiltrator", Dummy()),
    151:Ability("Mummy", Dummy()),
    152:Ability("Moxie", Dummy()),
    153:Ability("Justified", Dummy()),
    154:Ability("Rattled", Dummy()),
    155:Ability("Magic Bounce", Dummy()),
    156:Ability("Sap Sipper", Dummy()),
    157:Ability("Prankster", Dummy()),
    158:Ability("Sand Force", Dummy()),
    159:Ability("Iron Barbs", Dummy()),
    160:Ability("Zen Mode", Dummy()),
    161:Ability("Victory Star", Dummy()),
    162:Ability("Turboblaze", Dummy()),
    163:Ability("Teravolt", Dummy()),
    164:Ability("Aroma Veil", Dummy()),
    165:Ability("Flower Veil", Dummy()),
    166:Ability("Cheek Pouch", Dummy()),
    167:Ability("Protean", Dummy()),
    168:Ability("Fur Coat", Dummy()),
    169:Ability("Magician", Dummy()),
    170:Ability("Bulletproof", Dummy()),
    171:Ability("Competitive", Dummy()),
    172:Ability("Strong Jaw", Dummy()),
    173:Ability("Refrigerate", Dummy()),
    174:Ability("Sweet Veil", Dummy()),
    175:Ability("Stance Chance", Dummy()),
    176:Ability("Gale Wings", Dummy()),
    177:Ability("Mega Launcher", Dummy()),
    178:Ability("Grass Pelt", Dummy()),
    179:Ability("Symbiosis", Dummy()),
    180:Ability("Tough Claws", Dummy()),
    181:Ability("Pixilate", Dummy()),
    182:Ability("Gooey", Dummy()),
    183:Ability("Aerilate", Dummy()),
    184:Ability("Parental Bond", Dummy()),
    185:Ability("Dark Aura", Dummy()),
    186:Ability("Fairy Aura", Dummy()),
    187:Ability("Aura Break", Dummy()),
    188:Ability("Primordial Sea", Dummy()),
    189:Ability("Desolate Land", Dummy()),
    190:Ability("Delta Stream", Dummy()),
    191:Ability("Stamina", Dummy()),
    192:Ability("Wimp Out", Dummy()),
    193:Ability("Emergency Exit", Dummy()),
    194:Ability("Water Compaction", Dummy()),
    195:Ability("Merciless", Dummy()),
    196:Ability("Shields Down", Dummy()),
    197:Ability("Stakeout", Dummy()),
    198:Ability("Water Bubble", Dummy()),
    199:Ability("Steelworker", Dummy()),
    200:Ability("Berserk", Dummy()),
    201:Ability("Slush Rush", Dummy()),
    202:Ability("Long Reach", Dummy()),
    203:Ability("Liquid Voice", Dummy()),
    204:Ability("Triage", Dummy()),
    205:Ability("Galvanize", Dummy()),
    206:Ability("Surge Surfer", Dummy()),
    207:Ability("Schooling", Dummy()),
    208:Ability("Disguise", Dummy()),
    209:Ability("Battle Bond", Dummy()),
    210:Ability("Power Construct", Dummy()),
    211:Ability("Corrosion", Dummy()),
    212:Ability("Comatose", Dummy()),
    213:Ability("Queenly Majesty", Dummy()),
    214:Ability("Innards Out", Dummy()),
    215:Ability("Dancer", Dummy()),
    216:Ability("Battery", Dummy()),
    217:Ability("Fluffy", Dummy()),
    218:Ability("Dazzling", Dummy()),
    219:Ability("Soul-Heart", Dummy()),
    220:Ability("Tangling Hair", Dummy()),
    221:Ability("Receiver", Dummy()),
    222:Ability("Power of Alchemy", Dummy()),
    223:Ability("Beast Boost", Dummy()),
    224:Ability("RKS System", Dummy()),
    225:Ability("Electric Surge", Dummy()),
    226:Ability("Psychic Surge", Dummy()),
    227:Ability("Misty Surge", Dummy()),
    228:Ability("Grassy Surge", Dummy()),
    229:Ability("Full Metal Body", Dummy()),
    230:Ability("Shadow Shield", Dummy()),
    231:Ability("Prism Armor", Dummy()),
    232:Ability("Neuroforce", Dummy()),
    233:Ability("Intrepid Sword", Dummy()),
    234:Ability("Dauntless Shield", Dummy()),
    235:Ability("Libero", Dummy()),
    236:Ability("Ball Fetch", Dummy()),
    237:Ability("Cotton Down", Dummy()),
    238:Ability("Propeller Tail", Dummy()),
    239:Ability("Mirror Armour", Dummy()),
    240:Ability("Gulp Missile", Dummy()),
    241:Ability("Stalwart", Dummy()),
    242:Ability("Steam Engine", Dummy()),
    243:Ability("Punk Rock", Dummy()),
    244:Ability("Sand Spit", Dummy()),
    245:Ability("Ice Scales", Dummy()),
    246:Ability("Ripen", Dummy()),
    247:Ability("Ice Face", Dummy()),
    248:Ability("Power Spot", Dummy()),
    249:Ability("Mimicry", Dummy()),
    250:Ability("Screen Cleaner", Dummy()),
    251:Ability("Steely Spirit", Dummy()),
    252:Ability("Perish Body", Dummy()),
    253:Ability("Wandering Spirit", Dummy()),
    254:Ability("Gorilla Tactics", Dummy()),
    255:Ability("Neutralizing Gas", Dummy()),
    256:Ability("Pastel Veil", Dummy()),
    257:Ability("Hunger Switch", Dummy()),
    258:Ability("Quick Draw", Dummy()),
    259:Ability("Unseen Fist", Dummy()),
    260:Ability("Curious Medicine", Dummy()),
    261:Ability("Transistor", Dummy()),
    262:Ability("Dragon's Maw", Dummy()),
    263:Ability("Chilling Neigh", Dummy()),
    264:Ability("Grim Neigh", Dummy()),
    265:Ability("As One", Dummy()),
    266:Ability("As One", Dummy()),
    267:Ability("Lingering Aroma", Dummy()),
    268:Ability("Seed Sower", Dummy()),
    269:Ability("Thermal Exchange", Dummy()),
    270:Ability("Anger Shell", Dummy()),
    271:Ability("Purifying Salt", Dummy()),
    272:Ability("Well-Baked Body", Dummy()),
    273:Ability("Wind Rider", Dummy()),
    274:Ability("Guard Dog", Dummy()),
    275:Ability("Rocky Payload", Dummy()),
    276:Ability("Wind Power", Dummy()),
    277:Ability("Zero to Hero", Dummy()),
    278:Ability("Commander", Dummy()),
    279:Ability("Electromorphosis", Dummy()),
    280:Ability("Protosynthesis", Dummy()),
    281:Ability("Quark Drive", Dummy()),
    282:Ability("Good as Gold", Dummy()),
    283:Ability("Vessel of Ruin", Dummy()),
    284:Ability("Sword of Ruin", Dummy()),
    285:Ability("Tablets of Ruin", Dummy()),
    286:Ability("Beads of Ruin", Dummy()),
    287:Ability("Orichalcum Pulse", Dummy()),
    288:Ability("Hadron Engine", Dummy()),
    289:Ability("Opportunist", Dummy()),
    290:Ability("Cud Chew", Dummy()),
    291:Ability("Sharpness", Dummy()),
    292:Ability("Supreme Overlord", Dummy()),
    293:Ability("Costar", Dummy()),
    294:Ability("Toxic Debris", Dummy()),
    295:Ability("Armour Tail", Dummy()),
    296:Ability("Earth Eater", Dummy()),
    297:Ability("Mycelium Might", Dummy())
    }