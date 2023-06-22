import os
import pygame as pg
import operator
from time import sleep, time
from math import *
import random as rng
from pygame.locals import *
import pygame.math as pm
import pygame.image as pp #pp: pygame picture, if it was pi then it would mess with math.pi
import pygame.display as pd
from pokemon import pokedex
from moves import move_dex, determine_effectiveness
from moves import dummy as dummy_move #imports this separately because many functions already use dummy as their input
from buttons import highlightInfo, set_button_highlight
from items import item_dex
from abilities import ability_dex
import threading
import gspread
import copy

#startup and netplay variables
pg.init() #initializes everything required for pygame
gs = gspread.service_account(filename='netplay\pykemon-bd3330a1994a.json')#connects to the google sheet to allow for online battling
dex = sorted(pokedex.values(), key=operator.attrgetter('dex')) #sorts the pokedex by dex number so they appear in order
online = None; room = None; pingtime = 5; room_code = [None, None, None]; host = False; weather = None; weather_countdown = -1
turn = 1; player_move = ""; opponent_move = ""; move_first = None; seed = rng.randint(1,100000000); terrain = {}
stat_modifiers = [2/8, 2/7, 2/6, 2/5, 2/4, 2/3, 1, 3/2, 4/2, 5/2, 6/2, 7/2, 8/2] #a table of stat modifiers that the pokemon accesses if it has a stat change
#menu variables
(width,height) = (1200,600); active_screen = "menu"; active_button = "menu_play"; can_interact = False; error_count = 0; global_offset = 2; active_party_slot = 0; active_nature = None
render_queue = []; active_move_slot = 0; global_move_offset = 0; active_mon = dex[1]; active_move = move_dex[1]; global_item_offset = 0; active_item = item_dex[0]; global_nature_offset = 0
#player variables
party = [None,None,None,None,None,None]; loaded_party_id = 0; loaded_party = [None, None, None, None, None, None]; field_pokemon = pokedex[8]
username = os.path.expanduser("~"); username = username[username.find("C:\\Users\\") + 9:].capitalize(); user_icon = str(rng.randint(0, 152))
#opponent variables
opponent_party = [None,None,None,None,None,None]; opponent_username = None; opponent_icon = None; opponent_field_pokemon = pokedex[6] #the default opponent pokemon is set to charizard
#renders everything to the screen
def render_screen(skip_screen_specific_render): #renders the screen
    global render_queue, active_button, window, active_screen
    try:
        window.fill((0, 0, 0)); window.blit(bg, (0, 0)) # resets the screen and draws the background before
        if (skip_screen_specific_render == False): #some functions rerender themselves, so if that is the case skip screen-specific rendering
            if (active_screen == "deck_builder_menu"): #renders the deck pokemon selection screen (the one with the six boxes)
                nickname_font = pg.font.Font('Bolgart.ttf', 6)
                incrementer = 0
                for i in party: #iterates through the party to display all the pokemon inside
                    def get_font_size(name): #resizes the font of the pokemon's name to account for the length of the name
                        if (len(name) <= 10): return pg.font.Font('Bolgart.ttf', 15)
                        elif (len(name) > 10 and len(i.nick) < 14): return pg.font.Font('Bolgart.ttf', 11)
                        elif (len(name) > 14 and len(i.nick) < 18): return pg.font.Font('Bolgart.ttf', 9)
                        else: return pg.font.Font('Bolgart.ttf', 6)
                    if (incrementer == 0): sprite_coords = (553, 65); text_coords = (601, 174)
                    elif (incrementer == 1): sprite_coords = (822, 132); text_coords = (870, 241)
                    elif (incrementer == 2): sprite_coords = (822, 324); text_coords = (870, 433)
                    elif (incrementer == 3): sprite_coords = (553, 391); text_coords = (601, 500)
                    elif (incrementer == 4): sprite_coords = (280, 324); text_coords = (328, 433)
                    elif (incrementer == 5): sprite_coords = (280, 132); text_coords = (328, 241)
                    if (i != None):
                        nickname_font = get_font_size(i.nick)
                        if (i.shiny == True): render_queue.append([pp.load("sprites\\shiny\\front\\" + str(i.dex) + "_" + i.form + ".png"), sprite_coords]) #renders the pokemon as either shiny or not depending on if it is
                        else: render_queue.append([pp.load("sprites\\pokemon\\front\\" + str(i.dex) + "_" + i.form + ".png"), sprite_coords])               #set as shiny or not
                        render_queue.append([nickname_font.render(i.nick, True, (0, 0, 0)), (text_coords[0] - nickname_font.size(i.nick)[0] / 2, text_coords[1])])
                    incrementer += 1
            elif (active_screen == "deck_builder_mon_select"): select_mon_menu(0) #renders the pokemon selection menu when putting a team together
            elif (active_screen == "deck_builder_edit_mon"): edit_mon_menu(0) #renders the edit pokemon menu
            elif (active_screen == "deck_builder_move_select"): move_select_menu(0) #renders the move selection menu for specific pokemon
            elif (active_screen == "deck_builder_edit_name"): edit_name_menu(0) #renders the pokemon rename menu
            elif (active_screen == "deck_builder_item_select"): item_select_menu(0) #renders the item selection menu for specific pokemon
            elif (active_screen == "decks_management"): decks_save_menu(0) #renders the team save and load menu
            elif (active_screen == "battle_menu"): battle_menu(0) #renders the online menu to allow players to join games
            elif (active_screen == "room_waiting"): waiting_room_menu(0) #renders the waiting room
            elif (active_screen == "battle"): battle_screen(0, -2) #renders battles
        for i in render_queue: window.blit(i[0], i[1]) #renders each item in the render queue to the screen
        render_queue = [] #clears the render queue for next frame
        if (active_button != "transition"): window.blit(set_button_highlight(active_button), highlightInfo.get(active_button)[1]) #so long as the button isn't supposed to be hidden, display a highlight over the selected one
        pd.flip()
    except: pass #if an error occurs in rendering, just ignore it
#handles the pokemon selection screen in the team builder menu
def select_mon_menu(offset): #renders the pokemon selection menu
    global global_offset, render_queue, active_button, active_mon
    mon_selection_font = pg.font.Font('Bolgart.ttf', 36); mon_preview_font = pg.font.Font('Bolgart.ttf', 26)
    if (global_offset >= 1 and global_offset <= 1233):
        global_offset += offset; offset = global_offset
        if (offset == 0):#                                                       if at the bottom or the top of the pokemon
            offset = 1233; global_offset = 1233; active_button = "mon_select_6"# selection menu, wrap back around to the other
        elif (offset == 1234):#                                                  end (missingno. to enamorous-therian)
            offset = 1; global_offset = 1; active_button = "mon_select_1"
        for i in range(6): render_queue.append([pp.load("sprites\\pokemon\\box\\" + str(dex[offset + 1 + i].dex) + "_" + dex[offset + 1 + i].form + ".png"), (28, 126 + (77 * i))])
        row_1_mon = dex[offset + 1]; row_2_mon = dex[offset + 2]; row_3_mon = dex[offset + 3]; row_4_mon = dex[offset + 4]; row_5_mon = dex[offset + 5]; row_6_mon = dex[offset + 6]
        rows = [row_1_mon,row_2_mon,row_3_mon,row_4_mon,row_5_mon,row_6_mon]
        incrementer = 0
        for i in rows: #renders each pokemon, their name, and their typing inside the row
            render_queue.append([mon_selection_font.render(i.name, True, (0, 0, 0)), (133, 143 + (77 * incrementer))])
            render_queue.append([pp.load("menus\\" + i.typing[0] + ".png"), (145 + mon_selection_font.size(i.name)[0], 126 + (77 * incrementer))])
            if (len(i.typing) == 2): render_queue.append([pp.load("menus\\" + i.typing[1] + ".png"), (215 + mon_selection_font.size(i.name)[0], 126 + (77 * incrementer))])
            incrementer += 1
        mon_select_front_sprite = pp.load('menus\\loading.png')
        rows = ['mon_select_1','mon_select_2','mon_select_3','mon_select_4','mon_select_5','mon_select_6']
        incrementer = 0
        for i in rows:
            if (active_button == i):
                active_mon = copy.deepcopy(dex[offset + 1 + incrementer]) #sets a deep copy (not a pointer to the list data) of the currently selected pokemon to active_mon
                mon_select_front_sprite = pp.load("sprites\\pokemon\\front\\" + str(active_mon.dex) + "_" + active_mon.form + ".png") #displays a full sprite of the pokemon in the large box in the sidebar
                render_queue.append([pg.transform.scale(mon_select_front_sprite, (288, 288)), (858, 195)])
                render_queue.append([mon_preview_font.render(active_mon.name, True, (0, 0, 0)),(1003 - mon_preview_font.size(active_mon.name)[0] / 2, 156)])
            else: incrementer += 1
    else: global_offset = 1
    if (offset != 0): render_screen(True) #if this screen is not being accessed by the movement keys, render the screen with the render_screen function
def edit_mon_menu(dummy): #renders the pokemon edit menu
    global active_mon, render_queue, active_button
    mon_stats_font = pg.font.Font('Bolgart.ttf', 24); mon_name_font = pg.font.Font('Bolgart.ttf', 28); mon_item_font = pg.font.Font('Bolgart.ttf', 15)
    if (active_mon.shiny): render_queue.append([pg.transform.scale(pp.load("sprites\\shiny\\front\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (192, 192)), (8, 114)])
    else: render_queue.append([pg.transform.scale(pp.load("sprites\\pokemon\\front\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (192, 192)), (8, 114)])
    if (len(active_mon.ability_set) == 1): active_mon.ability = active_mon.ability_set[0] #if a pokemon only has one available ability, set its ability to that by default
    if ('-Mega' in active_mon.name and active_mon.dex != 384): #checks if a pokemon is a mega pokemon (excluding mega rayquaza)
        for i in item_dex:
            if (item_dex[i].category == 7): #finds the pokemon's specific mega stone in the item dex
                if (active_mon.dex in item_dex[i].restrictions):
                    if ('Mega-X' in active_mon.name):
                        if (' X' in item_dex[i].name): active_mon.held_item = item_dex[i] #special case for mega mewtwo x and mega charizard x but does the same thing as the comment says below
                    else: active_mon.held_item = item_dex[i] #if a pokemon is a mega pokemon, set it to be holding its mega stone by default
    render_queue.append([pp.load("menus\\" + active_mon.typing[0] + "_bar.png"), (307, 193)])
    if (len(active_mon.typing) == 2): render_queue.append([pp.load("menus\\" + active_mon.typing[1] + "_bar.png"), (465, 193)])
    render_queue.append([mon_stats_font.render(str(active_mon.hp), True, (0, 0, 0)), (824, 140)])      #renders the pokemon's base HP stat
    render_queue.append([mon_stats_font.render(str(active_mon.atk), True, (0, 0, 0)), (832, 194)])     #renders the pokemon's base ATK stat
    render_queue.append([mon_stats_font.render(str(active_mon.defense), True, (0, 0, 0)), (831, 248)]) #renders the pokemon's base DEF stat
    render_queue.append([mon_stats_font.render(str(active_mon.spd), True, (0, 0, 0)), (824, 315)])     #renders the pokemon's base SPD stat
    render_queue.append([mon_stats_font.render(str(active_mon.spatk), True, (0, 0, 0)), (826, 371)])   #renders the pokemon's base SPATK stat
    render_queue.append([mon_stats_font.render(str(active_mon.spdef), True, (0, 0, 0)), (827, 418)])   #renders the pokemon's base SPDEF stat
    render_queue.append([mon_name_font.render(active_mon.name, True, (0, 0, 0)), (18, 67)])
    render_queue.append([mon_stats_font.render(active_mon.nick, True, (0, 0, 0,)), (249, 141)])
    render_queue.append([mon_stats_font.render(str(active_mon.shiny), True, (0,0, 0)), (445 - mon_stats_font.size(str(active_mon.shiny))[0] / 2, 274)])
    render_queue.append([mon_stats_font.render(str(active_mon.level), True, (0,0, 0)), (288 - mon_stats_font.size(str(active_mon.level))[0] / 2, 273)])
    incrementer = 0
    for i in active_mon.moves:#iterates through all the pokemon's moves
        if (i is None): incrementer += 1; continue #if there is no move in this slot, skip rendering it and go to the next one
        else:
            render_queue.append([mon_stats_font.render(i.name, True, (0, 0, 0)), (37, 326 + (55 * incrementer))]) #render the move name on the move list
            render_queue.append([pg.transform.scale(pp.load("menus\\" + i.typing + ".png"), (38, 38)), (40 + mon_stats_font.size(i.name)[0], 318 + (55 * incrementer))])
            incrementer += 1
    if (active_mon.held_item is not None): render_queue.append([mon_item_font.render(active_mon.held_item.name, True, (0,0,0)), (385 - mon_item_font.size(active_mon.held_item.name)[0] / 2, 561)])
    if (active_mon.ability is not None): render_queue.append([mon_item_font.render(active_mon.ability.name, True, (0,0,0)), (138 - mon_item_font.size(active_mon.ability.name)[0] / 2, 561)])
    if (active_mon.nature is not None): render_queue.append([mon_item_font.render(active_mon.nature[0], True, (0,0,0)), (583 - mon_item_font.size(active_mon.nature[0])[0] / 2, 561)])
    if (dummy != 0): render_screen(True) #if this function was accessed by the movement keys, render it with render_screen
def move_select_menu(offset): #renders the move selection menu
    global active_mon, render_queue, active_button, global_move_offset, active_move
    original_input = offset
    if (offset == ""): offset = 0
    if (active_button == "move_select_back"): render_screen(True)
    move_name_font = pg.font.Font('Bolgart.ttf', 26)
    if (active_mon.shiny): render_queue.append([pp.load("sprites\\shiny\\box\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (26, 55)]) #renders the pokemon in the top left corner
    else: render_queue.append([pp.load("sprites\\pokemon\\box\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (26, 55)])
    if (global_move_offset >= -1 and global_move_offset <= len(active_mon.move_pool)):
        global_move_offset += offset; offset = global_move_offset
        if (offset == -1): offset = len(active_mon.move_pool) - 6; global_move_offset = offset; active_button = "move_select_6" #if at the top of the list, wrap back around to the bottom
        elif (offset == len(active_mon.move_pool)): offset = 0; global_move_offset = 0; active_button = "move_select_1" #if at the bottom of the list, wrap back around to the top
        moveset = sorted(active_mon.move_pool, key=operator.attrgetter('name')) #sorts the pokemon's move pool alphabetically
        row_1_move = moveset[offset % len(moveset)]; row_2_move = moveset[(offset + 1) % len(moveset)] #sets the pokemon's moves in the rows but using modulo - if a pokemon has less than six moves, it won't be able to fill
        row_3_move = moveset[(offset + 2) % len(moveset)]; row_4_move = moveset[(offset + 3) % len(moveset)] #up the six rows that are available to select from. with this implementation, if a pokemon has less than six moves
        row_5_move = moveset[(offset + 4) % len(moveset)]; row_6_move = moveset[(offset + 5) % len(moveset)] #it will wrap around the move pool within the rows themselves (see metapod to see it in action)
        rows = [row_1_move,row_2_move,row_3_move,row_4_move,row_5_move,row_6_move]
        incrementer = 0
        for i in rows:
            render_queue.append([pg.transform.scale(pp.load("menus\\" + i.typing + ".png"), (59, 59)), (21, 124 + (78 * incrementer))])
            render_queue.append([move_name_font.render(str(i.name), True, (0, 0, 0)), (84, 142 + (78 * incrementer))])
            incrementer += 1
        rows = ['move_select_1','move_select_2','move_select_3','move_select_4','move_select_5','move_select_6']
        incrementer = 0
        for i in rows:
            if (active_button == i):
                active_move = moveset[offset + incrementer % len(moveset)] #gets the currently selected move
                if (active_move.category == 0): render_queue.append([pp.load("menus\\Physical.png"), (891, 123)])  #if the selected move is a physical move, display the physical symbol
                elif (active_move.category == 1): render_queue.append([pp.load("menus\\Special.png"), (891, 123)]) #if the selected move is a special move, display the special symbol
                elif (active_move.category == 2): render_queue.append([pp.load("menus\\Status.png"), (891, 123)])  #if the selected move is a status move, display the status symbol
                else: render_queue.append([pp.load("menus\\Miscellanous.png"), (891, 123)])                        #if the move somehow does not fall into any category, this is a failsafe to prevent crashing
                render_queue.append([move_name_font.render(active_move.name, True, (0, 0, 0)), (955 - move_name_font.size(active_move.name)[0] / 2, 71)])
                render_queue.append([move_name_font.render(str(active_move.pp) + " PP", True, (0, 0, 0)), (955 - move_name_font.size(str(active_move.pp) + " PP")[0] / 2, 257)]) #renders the move's max PP
                if (active_move.power != 0): #↓ if the move has power (i.e., if the move is not a status move), render the move's power
                    render_queue.append([move_name_font.render(str(active_move.power) + " Power", True, (0, 0, 0)), (955-move_name_font.size(str(active_move.power) + " Power")[0] / 2, 198)])
                else: #↓ if the move is a status move, or does not have any power, display two dashes in place of a number
                    render_queue.append([move_name_font.render("--", True, (0, 0, 0)), (955-move_name_font.size(str(active_move.power) + "--")[0] / 2, 198)])
                if (active_move.accuracy != 0): #↓ if the move has accuracy, render the chance of it hitting (accuracy is not actually implemented in this game)
                    render_queue.append([move_name_font.render(str(active_move.accuracy) + "% Accuracy", True, (0, 0, 0)), (955 - move_name_font.size(str
                     (active_move.accuracy) + "% Accuracy")[0] / 2, 316)])
                else:#↓ if the move does not have accuracy, uses a different accuracy system, or bypasses the accuracy check, display two dashes in place of a chance
                    render_queue.append([move_name_font.render("--", True, (0, 0, 0)), (955 - move_name_font.size(str(active_move.accuracy) + "--")[0] / 2, 316)])
                if (active_move.effect == dummy_move): render_queue.append([move_name_font.render("Unimplemented", True, (255, 0, 0)), (955 - move_name_font.size('Unimplemented')[0] / 2, 400)])
            else: #^ if the move has no code associated with it, display a red warning labelling it as unimplemented
                incrementer += 1
    if (original_input != 0): render_screen(True) #if this screen is not being accessed by the movement keys, render it with render_screen
def nature_select_menu(offset): #render the nature selection menu
    global active_mon, render_queue, active_button, global_nature_offset, active_nature
    nature_dex = {0:["Hardy","",""],1:["Lonely","atk","def"],2:["Brave","atk","spe"],3:["Adamant","atk","spa"],4:["Naughty","atk","spd"],5:["Bold","def","atk"],6:["Docile","",""],
     7:["Relaxed","def","spd"],8:["Impish","def","spa"],9:["Lax","def","spd"],10:["Timid","spe","atk"],11:["Hasty","spe","def"],12:["Serious","",""],13:["Jolly","spe","spa"],14:["Naive","spe","spd"],
     15:["Modest","spa","atk"],16:["Mild","spa","def"],17:["Quiet","spa","spe"],18:["Bashful","",""],19:["Rash","spa","spd"],20:["Calm","spd","atk"],21:["Gentle","spd","def"],22:["Sassy","spd","spe"],
     23:["Careful","spd","spa"],24:["Quirky","",""]} #a list of every nature and the specific stats they boost or decrease
    if (active_button == "nature_select_back"): render_screen(False)
    nature_name_font = pg.font.Font('Bolgart.ttf', 26)
    if (active_mon.shiny): render_queue.append([pp.load("sprites\\shiny\\box\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (26, 55)]) #renders the pokemon in the top left corner
    else: render_queue.append([pp.load("sprites\\pokemon\\box\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (26, 55)])
    if (global_nature_offset >= -1 and global_nature_offset <= 25):
        global_nature_offset += offset; offset = global_nature_offset
        if (offset == -1): offset = 24 - 6; global_nature_offset = offset; active_button = "nature_select_6" #if at the bottom of the list, wrap around back to the top
        elif (offset >= 20): offset = 0; global_nature_offset = 0; active_button = "nature_select_1" #vice versa
        row_1_nature = nature_dex[offset]; row_2_nature = nature_dex[offset + 1]; row_3_nature = nature_dex[offset + 2]
        row_4_nature = nature_dex[offset + 3]; row_5_nature = nature_dex[offset + 4]; row_6_nature = nature_dex[offset + 5]
        rows = [row_1_nature,row_2_nature,row_3_nature,row_4_nature, row_5_nature,row_6_nature]
        incrementer = 0
        for i in rows: render_queue.append([nature_name_font.render(i[0], True, (0, 0, 0)), (84, 142 + (78 * incrementer))]); incrementer += 1
        rows = ['nature_select_1','nature_select_2','nature_select_3','nature_select_4', 'nature_select_5','nature_select_6']; incrementer = 0
        for i in rows:
            if (active_button == i):
                active_nature = nature_dex[offset + incrementer]
                if (active_nature[1] == "atk"): render_queue.append([pg.transform.scale(pp.load("menus\\atk_up.png"), (128, 128)), (810, 192)])    #if the nature increases ATK, display the ATK UP icon
                elif (active_nature[1] == "def"): render_queue.append([pg.transform.scale(pp.load("menus\\def_up.png"), (128, 128)), (810, 192)])  #if the nature increases DEF, display the DEF UP icon
                elif (active_nature[1] == "spe"): render_queue.append([pg.transform.scale(pp.load("menus\\spe_up.png"), (128, 128)), (810, 192)])  #if the nature increases SPD, display the SPD UP icon
                elif (active_nature[1] == "spa"): render_queue.append([pg.transform.scale(pp.load("menus\\spa_up.png"), (128, 128)), (810, 192)])  #if the nature increases SPATK, display the SPATK UP icon
                elif (active_nature[1] == "spd"): render_queue.append([pg.transform.scale(pp.load("menus\\spd_up.png"), (128, 128)), (810, 192)])  #if the nature increases SPDEF, display the SPDEF UP icon
                else: render_queue.append([pg.transform.scale(pp.load("menus\\no.png"), (128, 128)), (810, 192)])                                  #if the nature increases and decreases the same stat, display "No change"
                if (active_nature[2] == "atk"): render_queue.append([pg.transform.scale(pp.load("menus\\atk_down.png"), (128, 128)), (940, 192)])  #if the nature decreases ATK, display the ATK DOWN icon
                elif (active_nature[2] == "def"): render_queue.append([pg.transform.scale(pp.load("menus\\def_down.png"), (128, 128)), (940, 192)])#if the nature decreases DEF, display the DEF DOWN icon
                elif (active_nature[2] == "spe"): render_queue.append([pg.transform.scale(pp.load("menus\\spe_down.png"), (128, 128)), (940, 192)])#if the nature decreases SPD, display the SPD DOWN icon
                elif (active_nature[2] == "spa"): render_queue.append([pg.transform.scale(pp.load("menus\\spa_down.png"), (128, 128)), (940, 192)])#if the nature decreases SPATK, display the SPATK DOWN icon
                elif (active_nature[2] == "spd"): render_queue.append([pg.transform.scale(pp.load("menus\\spd_down.png"), (128, 128)), (940, 192)])#if the nature decreases SPDEF, display the SPDEF DOWN icon
                else: render_queue.append([pg.transform.scale(pp.load("menus\\change.png"), (128, 128)), (940, 192)])                              #if the nature increases and decreases the same stat, display "No change"
            else: incrementer += 1
    render_screen(False) #renders the screen through render screen
def ability_select_menu(screen): #render the ability selection menu
    global active_mon, render_queue, active_button
    ability_name_font = pg.font.Font('Bolgart.ttf', 19); ability_set = active_mon.ability_set
    if (screen == 1): render_queue.append([ability_name_font.render(ability_set[0].name, True, (0, 0, 0)), (600-ability_name_font.size(ability_set[0].name)[0] / 2, 273)]) #if there is only one ability, display the one ability
    elif (screen == 2):
        render_queue.append([ability_name_font.render(ability_set[0].name, True, (0, 0, 0)), (448-ability_name_font.size(ability_set[0].name)[0] / 2, 273)]) #if there are two abilities, show one on the left and the other
        render_queue.append([ability_name_font.render(ability_set[1].name, True, (0, 0, 0)), (759-ability_name_font.size(ability_set[1].name)[0] / 2, 273)]) #ability on the right
    else:
        render_queue.append([ability_name_font.render(ability_set[0].name, True, (0, 0, 0)), (449-ability_name_font.size(ability_set[0].name)[0] / 2, 206)]) #if there are three abilities, show one on the left, one on the
        render_queue.append([ability_name_font.render(ability_set[1].name, True, (0, 0, 0)), (760-ability_name_font.size(ability_set[1].name)[0] / 2, 206)]) #right, and the third one on the bottom between the other two
        render_queue.append([ability_name_font.render(ability_set[2].name, True, (0, 0, 0)), (606-ability_name_font.size(ability_set[2].name)[0] / 2, 332)])
    if (screen <= 3): render_screen(True) #if the screen is not accessed by another function, render the screen with render_screen
def item_select_menu(offset):#render the item selection menu
    global active_mon, render_queue, active_button, global_item_offset, active_item
    original_input = offset; item_name_font = pg.font.Font('Bolgart.ttf', 26); item_list = sorted(item_dex.values(), key=operator.attrgetter('category')) #sorts the item list by item type (mega stone, battle item, etc)
    if (offset == ""): offset = 0
    if (active_mon.shiny): render_queue.append([pp.load("sprites\\shiny\\box\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (26, 55)]) #renders the pokemon in the top left corner
    else: render_queue.append([pp.load("sprites\\pokemon\\box\\" + str(active_mon.dex) + "_" + active_mon.form + ".png"), (26, 55)])
    if (global_item_offset >= -1 and global_item_offset <= 312):
        global_item_offset += offset; offset = global_item_offset
        if (offset == -1): offset = 305; global_item_offset = offset; active_button = "item_select_6" #wrap around the top and bottom etc same as every other selection menu
        elif (offset >= 306): offset = 0; global_item_offset = 0; active_button = "item_select_1"
        row_1_item = item_list[offset]; row_2_item = item_list[offset + 1]; row_3_item = item_list[offset + 2]; row_4_item = item_list[offset + 3]; row_5_item = item_list[offset + 4]; row_6_item = item_list[offset + 5]
        rows = [row_1_item,row_2_item,row_3_item,row_4_item,row_5_item,row_6_item]; incrementer = 0
        for i in rows: #for each row, render the item's sprite and its name
            render_queue.append([pg.transform.scale(pp.load("sprites\\items\\" + i.name + ".png"), (59, 59)), (21, 124 + (78 * incrementer))])
            render_queue.append([item_name_font.render(i.name, True, (0, 0, 0)), (84, 142 + (78 * incrementer))]); incrementer += 1
        rows = ['item_select_1','item_select_2','item_select_3','item_select_4','item_select_5','item_select_6']; incrementer = 0
        for i in rows:
            if (active_button == i): #gets the currently selected item
                active_item = item_list[offset + incrementer]
                render_queue.append([item_name_font.render(active_item.name, True, (0, 0, 0)),(955 - item_name_font.size(active_item.name)[0] / 2, 71)])
                render_queue.append([pg.transform.scale(pp.load("sprites\\items\\" + active_item.name + ".png"), (128, 128)),(891, 123)])
                category_name_dict = {0:"Berry",1:"Primal Orb",2:"Drive",3:"Power Item",4:"Evolution Item",5:"Gem",6:"Incense",7:"Mega Stone",8:"Memory",9:"Plate",10:"Stat-Enhancing Item",
                 11:"Type-Enhancing Item",12:"Z-Crystal",13:"Battle Item"} #↓ renders the item categoyr
                render_queue.append([item_name_font.render(category_name_dict[active_item.category], True, (0, 0, 0)),(955 - item_name_font.size(category_name_dict[active_item.category])[0] / 2, 257)])
            else: incrementer += 1
    if (original_input != 0): render_screen(True) #render screen yada yada yada
def decks_save_menu(dummy): #renders the team save and load menu
    global party, render_queue, active_button, loaded_party, loaded_party_id
    incrementer = 0; selection_font = pg.font.Font('Bolgart.ttf', 22)
    for i in party:
        if (i is not None):
            if (i.shiny == True): render_queue.append([pp.load("sprites\\shiny\\front\\" + str(i.dex) + "_" + i.form + ".png"), (78 + (incrementer * 98), 52)])
            else: render_queue.append([pp.load("sprites\\pokemon\\front\\" + str(i.dex) + "_" + i.form + ".png"), (78 + (incrementer * 98), 52)])
        incrementer += 1
    if (loaded_party_id == -1 or loaded_party_id == 0): render_queue.append([selection_font.render("No file loaded", True, (0, 0, 0)), (586 - selection_font.size("No file loaded")[0] / 2, 403)])
    #^ if there is no file currently loaded, or the loaded file is the .README file, mark it as no file loaded
    else: render_queue.append([selection_font.render(str(loaded_party_id), True, (0, 0, 0)), (586 - selection_font.size(str(loaded_party_id))[0] / 2, 403)])
    #^ display the loaded party ID
    incrementer = 0; loaded_party_x = 376; loaded_party_y = 303
    for i in loaded_party:
        if (i is not None): #render each pokemon in the loaded party in the boxes to the sides
            if (i.shiny == True): render_queue.append([pp.load("sprites\\shiny\\box\\" + str(i.dex) + "_" + i.form + ".png"), (loaded_party_x, loaded_party_y)])
            else: render_queue.append([pp.load("sprites\\pokemon\\box\\" + str(i.dex) + "_" + i.form + ".png"), (loaded_party_x, loaded_party_y)])
        incrementer += 1; loaded_party_y += 75
        if (incrementer == 3): loaded_party_x = 728; loaded_party_y = 303
    if (dummy != 0): render_screen(True) #not commenting these anymore they're all the same
def convert_pokemon_to_string(pokemon, party_slot): #converts a pokemon class into a long string of data
    if (pokemon is not None):
        dex = str(pokemon.dex); nick = pokemon.nick; level = str(pokemon.level); form = pokemon.form; shiny = str(pokemon.shiny) #pokemon dex number, nickname, level, form, and if they are shiny or not is saved
        if (pokemon.ability is not None): ability = pokemon.ability.name #saves the ability if there is one, otherwise set it to NoAbility
        else: ability = "NoAbility"
        if (pokemon.moves[0] is not None): move1 = pokemon.moves[0].name #saves the move in slot 1 if there is one, otherwise set it to NoMove
        else: move1 = "NoMove"
        if (pokemon.moves[1] is not None): move2 = pokemon.moves[1].name #saves the move in slot 2 if there is one, otherwise set it to NoMove
        else: move2 = "NoMove"
        if (pokemon.moves[2] is not None): move3 = pokemon.moves[2].name #saves the move in slot 3 if there is one, otherwise set it to NoMove
        else: move3 = "NoMove"
        if (pokemon.moves[3] is not None): move4 = pokemon.moves[3].name #saves the move in slot 4 if there is one, otherwise set it to NoMove
        else: move4 = "NoMove"
        if (pokemon.held_item is not None): item = pokemon.held_item.name #saves the held item if there is one, otherwise set it to NoItem
        else: item = "NoItem"
        if (pokemon.nature is not None): nature = pokemon.nature #saves the pokemon's nature if there is one, otherwise set it to Hardy (no change)
        else: nature = "Hardy"
        output = f"&&&,{party_slot}\n0---{dex}\n1---{nick}\n2---{ability}\n3---{move1}\n4---{move2}\n5---{move3}\n6---{move4}\n7---{level}\n8---{nature}\n9---{form}\n10---{shiny}\n11---{item}\n{party_slot}!!!,\n"
        return(output) #returns the converted pokemon as a string
    else: return None
def convert_string_to_pokemon(string): #reconverts a converted pokemon from a string back into a pokemon
    try:
        for i in pokedex:
            if (pokedex[i].dex == int(string[string.find('0---') + 4:string.find('\n1---')])):
                if (pokedex[i].form == string[string.find('9---') + 4:string.find('\n10---')]):
                    pokemon = copy.deepcopy(pokedex.get(i)) #finds the pokemon that was saved based on its dex number and form
        for i in ability_dex:
            if (ability_dex[i].name == string[string.find('2---') + 4:string.find('\n3---')]): pokemon.ability = ability_dex[i] #sets the new pokemon's ability to the one that had been saved
        for i in item_dex:
            if (item_dex[i].name == string[string.find('11---') + 4:]): pokemon.held_item = item_dex[i] #sets the new pokemon's held item to the one that had been saved
        for i in move_dex:
            if (move_dex[i].name == string[string.find('3---') + 4:string.find('\n4---')]): pokemon.moves[0] = move_dex[i] #sets the pokemon's move in the first slot
            if (move_dex[i].name == string[string.find('4---') + 4:string.find('\n5---')]): pokemon.moves[1] = move_dex[i] #sets the pokemon's move in the second slot
            if (move_dex[i].name == string[string.find('5---') + 4:string.find('\n6---')]): pokemon.moves[2] = move_dex[i] #sets the pokemon's move in the third slot
            if (move_dex[i].name == string[string.find('6---') + 4:string.find('\n7---')]): pokemon.moves[3] = move_dex[i] #sets the pokemon's move in the fourth slot
        if (string[string.find('10---') + 5:string.find('\n11---')] == 'True'): pokemon.shiny = True #sets whether or not the pokemon is shiny
        else: pokemon.shiny = False
        pokemon.nick = string[string.find('1---') + 4:string.find('\n2---')]; pokemon.level = string[string.find('7---') + 4:string.find('\n8---')]; pokemon.nature = string[string.find('8---') + 4:string.find('\n9---')]
        return (pokemon)#returns the reconverted pokemon as a pokemon
    except: return None #if there is an error, ignore it
def save_party(dummy): #saves the party to a txt file in the parties folder
    global party
    null_check = 0
    for i in party:
        if (i is None): null_check += 1
    if (null_check != 6): #stops a party from being saved if it is empty
        dir_path = r'parties\\'; count = 0 #some convenient code i copied from the internet
        for path in os.listdir(dir_path):  #to count the number of files in a given directory
            if os.path.isfile(os.path.join(dir_path, path)): count += 1
        saved_party = open('parties\\' + str(count) + '.txt', 'a'); incrementer = 0 #creates a new party file in the folder
        for i in party:
            if (i is not None): saved_party.write(convert_pokemon_to_string(i, incrementer)) #converts each pokemon in the party to a string and then appends it to the file
            incrementer += 1
def load_party(offset): #loads a saved party from a txt file in the parties folder
    global loaded_party, loaded_party_id
    dir_path = r'parties\\'; count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)): count += 1
    if (count < 2): loaded_party = [None, None, None, None, None, None] #if the file being loaded is not a valid slot, ignore it and set it to be empty
    else:
        if (loaded_party_id == -1): loaded_party_id = 0 #prevents the file index from being negative (there is no check for it being out of bounds while positive)
        else:
            loaded_party = [None, None, None, None, None, None]; loaded_party_id += offset; active_loaded_party = open('parties\\' + str(loaded_party_id) + '.txt'); party_info = active_loaded_party.read()
            for i in range(6):
                if (party_info.find('&&&,' + str(i)) != -1): #reads the file and sets each party member of the loaded party to be those saved in the file
                    mon_info = party_info[party_info.find('&&&,' + str(i)):party_info.find('\n' + str(i) + '!!!,')]; loaded_party[i] = convert_string_to_pokemon(mon_info)
            decks_save_menu(-1)
def display_text_based_on_client(target, player_line, opponent_line): #renders text during a battle dependent on whether the user is the host or the challenger
    if (target == field_pokemon): battle_screen(-1, player_line) #if the currently targeted pokemon is the user's own, use the first given line
    else: battle_screen(-1, opponent_line) #if the currently targeted pokemon is the opponent's, use the second given line
def set_loaded_party(dummy): #sets the current party to the one currently loaded in from a file
    global party, loaded_party
    party = loaded_party; decks_save_menu(-1)
def determine_health_bar_size(): #determine how full a pokemon's health bar should be during a battle
    global render_queue, field_pokemon, opponent_field_pokemon
    player_max_hp = (field_pokemon.hp * 2) + 110; opponent_max_hp = (opponent_field_pokemon.hp * 2) + 110 #calculate the maximum HP for both the user and opponent
    if (field_pokemon.current_hp <= 0): field_pokemon.current_hp = 0 #if the user's pokemon or the opponent's pokemon has a current HP less than zero, set it to zero (fainted)
    if (opponent_field_pokemon.current_hp < 0): opponent_field_pokemon.current_hp = 0
    if (field_pokemon.current_hp >= (player_max_hp / 1.5)): colour = pp.load('menus\\online\\hp_green.png') #if the health of the user's pokemon is greater than a certain percentage, the health bar will be green
    elif (field_pokemon.current_hp >= player_max_hp / 3): colour = pp.load('menus\\online\\hp_yellow.png')  #if the health bar of the user's pokemon is greater than a third, the health bar will be yellow
    elif (field_pokemon.current_hp >= player_max_hp / 5): colour = pp.load('menus\\online\\hp_orange.png')  #if the health bar of the user's pokemon is greater than a fifth, the health bar will be orange
    else: colour = pp.load('menus\\online\\hp_red.png')                                                     #otherwise, the health bar will be red
    if (opponent_field_pokemon.current_hp >= (opponent_max_hp / 1.5)): opponent_colour = pp.load('menus\\online\\hp_green.png') #the exact same thing as before but for the opponent
    elif (opponent_field_pokemon.current_hp >= opponent_max_hp / 3): opponent_colour = pp.load('menus\\online\\hp_yellow.png')
    elif (opponent_field_pokemon.current_hp >= opponent_max_hp / 5): opponent_colour = pp.load('menus\\online\\hp_orange.png')
    else: opponent_colour = pp.load('menus\\online\\hp_red.png')
    render_queue.append([pg.transform.scale(colour, (284 * (field_pokemon.current_hp / player_max_hp), 15)), (259, 505)]) #scales the healthbar to be the size it should be (current hp divided by max hp)
    render_queue.append([pg.transform.scale(opponent_colour, (188 * (opponent_field_pokemon.current_hp / opponent_max_hp), 15)), (701, 323)]) #ditto for the opponent
def battle_screen(dummy, state): #renders a battle
    global render_queue, username, user_icon, party, opponent_username, opponent_icon, opponent_party, active_button
    username_font = pg.font.Font('Bolgart.ttf', 30); move_font = pg.font.Font('Bolgart.ttf', 14); PP_font = pg.font.Font('Bolgart.ttf', 13)
    render_queue.append([pp.load("sprites\\trainers\\" + user_icon + ".png"), (17, 6)]); render_queue.append([opponent_icon, (1102, 6)]) #renders the icons of the players
    render_queue.append([username_font.render(username, True, (255, 255, 255)), (141, 12)]) #renders the username of the player
    render_queue.append([username_font.render(opponent_username, True, (255, 255, 255)), (1058 - username_font.size(opponent_username)[0], 12)]) #renders the username of the opponent
    render_queue.append([pp.load('menus\\online\\health_bar.png'), (257, 503)]); render_queue.append([pp.load('menus\\online\\opponent_health_bar.png'), (699, 321)]); determine_health_bar_size() #renders health bars
    render_queue.append([pp.load("menus\\" + field_pokemon.typing[0] + "_bar.png"), (256, 179)]) #renders the pokemon's types above them (if there are two, display two)
    if (len(field_pokemon.typing) == 2): render_queue.append([pp.load("menus\\" + field_pokemon.typing[1] + "_bar.png"), (441, 179)])
    render_queue.append([pg.transform.scale(pp.load("menus\\" + opponent_field_pokemon.typing[0] + "_bar.png"), (76, 18)), (699, 111)])
    if (len(opponent_field_pokemon.typing) == 2): render_queue.append([pg.transform.scale(pp.load("menus\\" + opponent_field_pokemon.typing[1] + "_bar.png"), (76, 18)), (779, 111)]) #ditto for the opponent
    if (field_pokemon.shiny == True): image = pg.transform.scale(pp.load("sprites\\shiny\\back\\" + str(field_pokemon.dex) + "_" + field_pokemon.form + ".png"), (288, 288)) #render the pokemon themselves
    else: image = pg.transform.scale(pp.load("sprites\\pokemon\\back\\" + str(field_pokemon.dex) + "_" + field_pokemon.form + ".png"), (288, 288))
    render_queue.append([image, (257, 215)])
    if (opponent_field_pokemon.shiny == True): opponent_image = pg.transform.scale(pp.load("sprites\\shiny\\front\\" + str(opponent_field_pokemon.dex) + "_" + opponent_field_pokemon.form + ".png"), (192,192))
    else: opponent_image = pg.transform.scale(pp.load("sprites\\pokemon\\front\\" + str(opponent_field_pokemon.dex) + "_" + opponent_field_pokemon.form + ".png"), (192, 192)) #ditto for the opponent
    render_queue.append([opponent_image, (699, 129)])
    for i in field_pokemon.status_effects: #if the pokemon has a status condition, display the icon for it
        if (i == 'Burn'): render_queue.append([pp.load('menus\\online\\burn.png'), (256, 220)])                  #if the user's pokemon is burned, display the burn icon
        elif (i == 'Poison'): render_queue.append([pp.load('menus\\online\\poison.png'), (256, 220)])            #if the user's pokemon is poisoned, display the poison icon
        elif (i == 'Lethal Poison'): render_queue.append([pp.load('menus\\online\\bad_poison.png'), (256, 220)]) #if the user's pokemon is badly poisoned, display the fatal poison icon
        elif (i == 'Sleep'): render_queue.append([pp.load('menus\\online\\sleep.png'), (256, 220)])              #if the user's pokemon is asleep, display the sleep icon
        elif (i == 'Paralysed'): render_queue.append([pp.load('menus\\online\\paralysis.png'), (256, 220)])      #if the user's pokemon is paralysed, display the paralysis icon
        elif (i == 'Frozen'): render_queue.append([pp.load('menus\\online\\frozen.png'), (256, 220)])            #if the user's pokemon is frozen, display the frozen icon
    for i in opponent_field_pokemon.status_effects: #ditto for the opponent
        if (i == 'Burn'): render_queue.append([pg.transform.scale(pp.load('menus\\online\\burn.png'), (66, 16)), (699, 134)])
        elif (i == 'Poison'): render_queue.append([pg.transform.scale(pp.load('menus\\online\\poison.png'), (66, 16)), (699, 134)])
        elif (i == 'Lethal Poison'): render_queue.append([pg.transform.scale(pp.load('menus\\online\\bad_poison.png'), (66, 16)), (699, 134)])
        elif (i == 'Sleep'): render_queue.append([pg.transform.scale(pp.load('menus\\online\\sleep.png'), (66, 16)), (699, 134)])
        elif (i == 'Paralysed'): render_queue.append([pg.transform.scale(pp.load('menus\\online\\paralysis.png'), (66, 16)), (699, 134)])
        elif (i == 'Frozen'): render_queue.append([pg.transform.scale(pp.load('menus\\online\\frozen.png'), (66, 16)), (699, 134)])
    for i in range(6):
        try:
            if (party[i] is not None): #displays the pokeballs showing how many pokemon are in either side's party down the sides
                if (party[i].current_hp > 0): render_queue.append([pp.load("menus\\online\\party_alive.png"), (25, 115 + (i * 64))]) #if the pokemon is alive, use a normal pokeball
                else: render_queue.append([pp.load("menus\\online\\party_fainted.png"), (25, 115 + (i * 64))]) #if they are fainted, use a greyed-out pokeball
            else: render_queue.append([pp.load("menus\\online\\party_empty.png"), (25, 115 + (i * 64))]) #if there is no pokemon in that slot, use a pokeball silhouette
        except: render_queue.append([pp.load("menus\\online\\party_empty.png"), (1111, 115 + (i * 64))]) #if there is an error, use a pokeball silhouette
        try:
            if (opponent_party[i] is not None): #ditto for the opponent
                if (opponent_party[i].current_hp > 0): render_queue.append([pp.load("menus\\online\\party_alive.png"), (1111, 115 + (i * 64))])
                else: render_queue.append([pp.load("menus\\online\\party_fainted.png"), (1111, 115 + (i * 64))])
            else: render_queue.append([pp.load("menus\\online\\party_empty.png"), (1111, 115 + (i * 64))])
        except: render_queue.append([pp.load("menus\\online\\party_empty.png"), (1111, 115 + (i * 64))])
    if (state == 2): battle_text(state, 0) #when finished showing the two pokemon being sent out at the beginning of the game, start the battle
    elif (state > -1): battle_text(state, 3) #when a state is given, display its associated piece of text
    if (weather == 'Harsh Sunlight'): render_queue.append([pp.load('menus\\online\\sunny.png'), (120, 0)]) #if the weather is sunny, display a sunny filter over the battle
    elif (weather == 'Rain'): render_queue.append([pp.load('menus\\online\\rainy.png'), (120, 0)])         #if the weather is rainy, display a rainy filter over the battle
    elif (weather == 'Sandstorm'): render_queue.append([pp.load('menus\\online\\sandstorm.png'), (120, 0)])#if the weather is a sandstorm, display a sandstormy filter over the battle
    elif (weather == 'Hail'): render_queue.append([pp.load('menus\\online\\hail.png'), (120, 0)])          #if the weather is hail, display a haily filter over the battle
    if (active_button == 'switch1' or active_button == 'switch2' or active_button == 'switch3' or active_button == 'switch4' or active_button == 'switch5' or active_button == 'switch6' or active_button == 'switch_cancel'):
        for i in range(7): #if the pokemon is being switched, display the switch buttons
            render_queue.append([pp.load('menus\\online\\switch_pokemon.png'), (10 + (i * 168), 537)])
            if (i < 6):
                if (party[i] is not None): #display the pokemon to be switched into
                    if (party[i].shiny == True): render_queue.append([pp.load("sprites\\shiny\\box\\" + str(party[i].dex) + "_" + party[i].form + ".png"), (17 + (i * 168), 539)])
                    else: render_queue.append([pp.load("sprites\\pokemon\\box\\" + str(party[i].dex) + "_" + party[i].form + ".png"), (17 + (i * 168), 539)])
                    if (party[i].current_hp == 0): render_queue.append([pp.load('menus\\online\\switch_fainted.png'), (14 + (i * 168), 542)])
            else: #^ if the pokemon is fainted, display a red line going through it
                render_queue.append([username_font.render('Cancel', True, (0, 0, 0)), (1034, 553)])
                if (field_pokemon.current_hp == 0): render_queue.append([pp.load('menus\\online\\switch_fainted.png'), (14 + (i * 168), 542)])
    elif (active_button != "transition"): #if text is not currently being displayed, render the battle buttons
        render_queue.append([pp.load('menus\\online\\battle_move.png'), (12, 540)]); render_queue.append([pp.load('menus\\online\\battle_move.png'), (285, 540)]) #render the move buttons
        render_queue.append([pp.load('menus\\online\\battle_move.png'), (831, 540)]); render_queue.append([pp.load('menus\\online\\battle_move.png'), (558, 540)])
        incrementer = 0
        for i in field_pokemon.moves: #render the pokemon's moves and their information
            if (i is not None):
                render_queue.append([move_font.render(i.name, True, (0, 0, 0)), (65 + (273 * incrementer), 552)]) #renders name
                render_queue.append([PP_font.render(str(i.current_pp) + "PP", True, (0, 0, 0)), (109 + (273 * incrementer), 575)]) #renders PP
                render_queue.append([pg.transform.scale(pp.load("menus\\" + i.typing + ".png"), (40, 40)), (18 + (273 * incrementer), 549)]) #renders typing
                if (i.category == 0): render_queue.append([pg.transform.scale(pp.load("menus\\Physical.png"), (43, 22)), (62 + (273 * incrementer), 569)]) #renders category
                elif (i.category == 1): render_queue.append([pg.transform.scale(pp.load("menus\\Special.png"), (43, 22)), (62 + (273 * incrementer), 569)])
                elif (i.category == 2): render_queue.append([pg.transform.scale(pp.load("menus\\Status.png"), (43, 22)), (62 + (273 * incrementer), 569)])
                else: render_queue.append([pg.transform.scale(pp.load("menus\\Miscellaneous.png"), (43, 22)), (62 + (273 * incrementer), 569)])
            incrementer += 1
        if (field_pokemon.held_item is not None): #if the pokemon's held item is a gimmick item, add a gimmick button over the switch button so it can be used (not functional)
            if (field_pokemon.held_item.category == 7 or field_pokemon.held_item.category == 12): render_queue.append([pp.load('menus\\online\\battle_switch_gimmick.png'), (1099, 540)])
            else: render_queue.append([pp.load('menus\\online\\battle_switch.png'), (1099, 540)])
        else: render_queue.append([pp.load('menus\\online\\battle_switch.png'), (1099, 540)])
    if (dummy != 0): render_screen(False)
def battle_menu(dummy): #displays the battle connection menu
    global username, render_queue, user_icon
    if (active_screen != "battle"):
        name_font = pg.font.Font('Bolgart.ttf', 30); render_queue.append([name_font.render(username, True, (0, 0, 0)), (325, 63)]); render_queue.append([pg.transform.scale(pp.load("sprites\\trainers\\"
         + user_icon + ".png"), (240, 240)), (51, 52)])
        incrementer = 0
        for i in room_code: #displays the room code
            if (i is not None): render_queue.append([pp.load("menus\\online\\" + str(i + 1) + ".png"), (853 + (incrementer * 86), 344)])
            incrementer += 1
    if (dummy != 0): render_screen(True)
def complete_turn(dummy): #ends a turn
    global opponent_field_pokemon, field_pokemon, player_move, opponent_move, move_first, host, turn, weather_countdown, weather, active_button
    if (dummy != 0): #once the ping thread has completed, run the following
        opponent_action = ""; player_action = ""
        try:
            if (host):
                values = room.batch_get(['T' + str(turn + 1), 'U' + str(turn + 1), 'V' + str(turn + 1), 'W' + str(turn + 1)])
                player_move = values[0][0][0]; opponent_move = values[1][0][0]; player_action = values[2][0][0]; opponent_action = values[3][0][0] #get the challenger's action's information
            else:
                values = room.batch_get(['T' + str(turn + 1), 'U' + str(turn + 1), 'V' + str(turn + 1), 'W' + str(turn + 1)])
                player_move = values[1][0][0]; opponent_move = values[0][0][0]; player_action = values[3][0][0]; opponent_action = values[2][0][0] #get the host's action's information
        except: battle_screen(-1, 115); cancel_room(0) #if there is an error gathering the information, return the player to the battle connection menu
        if (player_action == "Switch"): battle_screen(-1, 11) #if the player switched their pokemon, display the switch text
        if (opponent_action == "Switch"): #if the opponent switched, display the switch text
            opponent_field_pokemon = opponent_party[int(opponent_move)]; battle_screen(-1, 12)
            if (player_action == "Move"): move_first = opponent_field_pokemon; battle_screen(-1, 3) #if the player used a move that turn, always use it after the opponent switches
            else: active_button = 'move1'; battle_screen(-1, -1)
        if (opponent_action == "Move"): #if the opponent used a move
            if (player_action == "Move"):
                for i in move_dex:
                    if (move_dex[i].name == player_move): player_used_move = move_dex[i]
                for i in move_dex:
                    if (move_dex[i].name == opponent_move): opponent_used_move = move_dex[i]
                nature = field_pokemon.nature[0]; opponent_nature = opponent_field_pokemon.nature[0]; nature_modifier = 1; opponent_nature_modifier = 1
                if (nature == 'Timid' or nature == 'Hasty' or nature == 'Jolly' or nature == 'Naive'): nature_modifier = 1.1 #determines the modifier of the two pokemon's natures
                elif (nature == 'Brave' or nature == 'Relaxed' or nature == 'Quiet' or nature == 'Sassy'): nature_modifier = 0.9
                if (opponent_nature == 'Timid' or opponent_nature == 'Hasty' or opponent_nature == 'Jolly' or opponent_nature == 'Naive'): opponent_nature_modifier = 1.1
                elif (opponent_nature == 'Brave' or opponent_nature == 'Relaxed' or opponent_nature == 'Quiet' or opponent_nature == 'Sassy'): opponent_nature_modifier = 0.9
                if (player_used_move.priority > opponent_used_move.priority): move_first = field_pokemon; battle_screen(-1, 3) #if a priority move is used, ensure it is used before the move with lower priority
                elif (player_used_move.priority < opponent_used_move.priority): move_first = opponent_field_pokemon; battle_screen(-1, 4)
                else: #if no priority move is used, check the following
                    if (((field_pokemon.spd * 2) + 5) * nature_modifier * stat_modifiers[field_pokemon.current_spd] > ((opponent_field_pokemon.spd * 2) + 5) * opponent_nature_modifier * stat_modifiers[opponent_field_pokemon.current_spd]):
                        move_first = field_pokemon; battle_screen(-1, 3) #if the user's pokemon is faster than the opponent's pokemon, taking natures and stat modifiers into account, the user goes first
                    elif (((field_pokemon.spd * 2) + 5) * nature_modifier * stat_modifiers[field_pokemon.current_spd] == ((opponent_field_pokemon.spd * 2) + 5) * opponent_nature_modifier * stat_modifiers[opponent_field_pokemon.current_spd]):
                        if (host): move_first = field_pokemon; battle_screen(-1, 3) #if there is a speed tie, the host always goes first
                        else: move_first = opponent_field_pokemon; battle_screen(-1, 4)
                    else: move_first = opponent_field_pokemon; battle_screen(-1, 4) #otherwise, the opponent goes first
            else: move_first = field_pokemon; battle_screen(-1, 4)
        turn += 1 #increment the turn counter
        if (weather_countdown > -1): weather_countdown -= 1 #if there is weather, tick the weather countdown by 1
        if (weather_countdown == -1):
            if (weather == 'Harsh Sunlight'): battle_screen(-1, 91) #if the weather is sunny and it ends, display its associated text
            elif (weather == 'Rain'): battle_screen(-1, 96)         #if the weather is rainy and it ends, display its associated text
            elif (weather == 'Sandstorm'): battle_screen(-1, 103)   #if the weather is a sandstorm and it ends, display its associated text
            elif (weather == 'Hail'): battle_screen(-1, 107)        #if the weather is hail and it ends, display its associated text
    else: render_screen(False)
def initial_connection_to_battle(dummy):#code for handling the start of a battle
    global active_screen, active_button, render_queue, opponent_username, opponent_icon
    active_screen = "transition"; active_button = "transition" #removes the battle buttons at the start
    if (host):
        name_font = pg.font.Font('Bolgart.ttf', 30); render_queue.append([name_font.render('Connected with', True, (0, 0, 0)), (606, 178)]); sleep(0.7) #displays who the player is connected to
        render_queue.append([name_font.render(opponent_username, True, (0, 0, 0)), (735 - name_font.size(opponent_username)[0] / 2, 221)]); render_queue.append([pg.transform.scale(opponent_icon, (160, 160)), (656, 264)])
        render_screen(True)
    if (dummy != 0): render_queue = []; Open_Screen(12)
def get_switch_in(dummy): #get the opponent pokemon when it is being switched
    global opponent_field_pokemon, opponent_party, active_button
    cell_coordinate = turn + 1
    if (dummy != -1): #if the ping thread has found the pokemon
        if (opponent_field_pokemon.current_hp == 0): cell_coordinate -= 1 #if the pokemon has fainted, check for it on the current turn (might be the cause of a bug probably maybe)
        if (host): room.update_acell('Q' + str(cell_coordinate), '.') #once the pokemon has been received, tell the server it has the pokemon
        else: room.update_acell('R' + str(cell_coordinate), '.')
        opponent_field_pokemon = opponent_party[int(dummy)] #set the pokemon that the opponent has switched into
        battle_screen(-1, 12); active_button = "move1"; battle_screen(-1, -1)
    else: battle_screen(-1, -1); render_screen(True)
def switch_pokemon(slot): #switch the user's own pokemon
    global active_button, render_queue, party, field_pokemon, turn
    error_font = pg.font.Font('Bolgart.ttf', 24); hp = field_pokemon.current_hp
    if (slot == -1): #↓ prevents the user from cancelling if they are switching after a faint
        if (hp == 0): window.blit(error_font.render('You must select one of your remaining Pokemon', True, (255, 255, 255)), (127, 54)); pd.flip()
        else: active_button = "move1"; battle_screen(-1, -1)
    try: #↓ prevents the user from switching into a pokemon that has fainted or the one that is already out
        if (party[slot] == field_pokemon): window.blit(error_font.render('You can\'t switch into a Pokemon that is already out!', True, (255, 255, 255)), (127, 54)); pd.flip()
        elif (party[slot].current_hp == 0): window.blit(error_font.render('That Pokemon has fainted!', True, (255, 255, 255)), (127, 54)); pd.flip()
        else:
            if (host):#tells the server which pokemon the player is switching into and switches it on their end
                room.batch_update([{'range':'Q' + str(turn + 1), 'values':[['.']]},
                 {'range':'V'+ str(turn + 1), 'values':[['Switch']]},{'range':'T' + str(turn + 1), 'values':[[str(slot)]]},{'range':'X' + str(turn + 1), 'values':[['0']]}])
                if (hp != 0): create_ping_thread('R' + str(turn + 1), complete_turn, 0); active_button = "transition"; field_pokemon = party[slot]
                else: active_button = 'move1'; field_pokemon = party[slot]; battle_screen(-1, -1)
            else:
                room.batch_update([{'range':'R' + str(turn + 1), 'values':[['.']]},
                 {'range':'W'+ str(turn + 1), 'values':[['Switch']]},{'range':'U' + str(turn + 1), 'values':[[str(slot)]]},{'range':'Y' + str(turn + 1), 'values':[['0']]}])
                if (hp != 0): create_ping_thread('Q' + str(turn + 1), complete_turn, 0); active_button = "transition"; field_pokemon = party[slot]
                else: active_button = 'move1'; field_pokemon = party[slot]; battle_screen(-1, -1)
    except: window.blit(error_font.render('You have no Pokemon in that slot!', True, (255, 255, 255)), (127, 54)); pd.flip() #if there is no pokemon in that slot, prevent the player from switching into it
def waiting_room_menu(dummy):#renders the waiting room menu
    global room_code, room, username, user_icon, opponent_username, opponent_icon, opponent_party, opponent_field_pokemon
    name_font = pg.font.Font('Bolgart.ttf', 30)
    if (type(dummy) == str):
        opponent_username = dummy; opponent_icon = pp.load('sprites\\trainers\\' + room.acell('J1').value + '.png'); room.update_acell('Q1', '.'); create_ping_thread('Q1', initial_connection_to_battle, 0)
        party_temp = room.get('K1:P1')[0]; party_index = 0; opponent_party = []
        for i in party_temp:
            if (i is not None): opponent_party.append(convert_string_to_pokemon(party_temp[party_index]))
            else: opponent_party.append(None)
            party_index += 1
        for i in opponent_party:
            if (i is not None): opponent_field_pokemon = i; break
    incrementer = 0;
    for i in room_code:
        render_queue.append([pp.load("menus\\online\\" + str(i + 1) + ".png"), (30 + (incrementer * 86), 12)])
        incrementer += 1
    render_queue.append([pg.transform.scale(pp.load("sprites\\trainers\\" + user_icon + ".png"), (240, 240)), (38, 135)]); render_queue.append([name_font.render(username, True, (0, 0, 0)), (48, 420)])
    if (dummy != 0): render_screen(True)
def swap_shiny(dummy): #switches a pokemon from shiny to not shiny and vice versa
    global active_mon
    if (active_mon.shiny): active_mon.shiny = False #not shiny
    else: active_mon.shiny = True #shiny
    edit_mon_menu(1)
def select_move(dummy): #sets the selected move to the move in that pokemon's selected slot
    global active_move, active_move_slot, active_mon, global_move_offset
    active_mon.moves[int(active_move_slot) - 1] = active_move; global_move_offset = 0; Open_Screen(4)
def select_item(dummy): #sets the selected item to that pokemon's selected item
    global active_item, active_mon, global_item_offset
    active_mon.held_item = active_item; global_item_offset = 0; Open_Screen(4)
def select_nature(dummy): #sets the selected nature to that pokemon's selected nature
    global active_mon, active_button, active_nature, global_nature_offset
    active_mon.nature = active_nature; global_nature_offset = 0; Open_Screen(4)
def cancel_room(dummy): #ends/cancels a game
    global online, room, room_code, host, opponent_icon, opponent_username, opponent_party, weather, weather_countdown, turn, active_button, active_screen
    try: online.del_worksheet(room) #deletes the room in the server
    except: pass #if the room does not exist (already deleted by the other player), ignore it
    room_code = [None, None, None]; room = None; host = False; opponent_icon = pp.load('menus\\online\\ping 0.png'); opponent_username = ""; opponent_party = [None,None,None,None,None,None]; weather = None; weather_countdown = -1; turn = 1;  terrain = []
    active_button = "battle_menu_connect"; active_screen = 'battle_menu' #resets all associated variables
    for i in party:
        if (i is not None): #reset all status effects and stat changes to the pokemon in the user's party
            i.current_atk = 6; i.current_def = 6; i.current_spatk = 6; i.current_spdef = 6; i.current_spd = 6; i.status_effects = []
            if (i.dex != 316): i.current_hp = 110 + (i.hp * 2)
    Open_Screen(11)
def select_ability(dummy): #sets the selected ability to that pokemon's selected ability
    global active_mon, active_button
    if (active_button[len(active_button) - 1] == '1'): active_mon.ability = active_mon.ability_set[0]
    elif (active_button[len(active_button) - 1] == '2'): active_mon.ability = active_mon.ability_set[1]
    else: active_mon.ability = active_mon.ability_set[2]
    Open_Screen(4)
def edit_level(direction): #changes the pokemon's level
    global active_mon
    active_mon.level += direction
    if (active_mon.level <= 0): active_mon.level = 100 #when it hits zero, wrap around to 100
    edit_mon_menu(1)
def edit_name_menu(letter): #renders the pokemon nickname menu
    nickname_font = pg.font.Font('Bolgart.ttf', 28); render_queue.append([nickname_font.render(active_mon.nick, True, (0, 0, 0)), (290, 186)])
    if (letter != 0): render_screen(False)
def generate_room(dummy): #generates a new game in the server
    global room, room_code, active_button, active_screen, bg, host, opponent_username, opponent_icon, field_pokemon, opponent_field_pokemon, opponent_party
    null_check = False
    for i in room_code:
        if (i is None): null_check = True #makes sure the room code has all three symbols before the game starts
    if (null_check == False):
        try:
            if (online.worksheet(str(room_code[0]) + ":" + str(room_code[1]) + ":" + str(room_code[2])) is not None): #if the room does not already exist
                if (online.worksheet(str(room_code[0]) + ":" + str(room_code[1]) + ":" + str(room_code[2])).acell('I1').value is None): #if the room does not have a second player in it
                    for i in party:
                        if (i is not None): field_pokemon = i; break #sets the first available pokemon in the party to be the field pokemon
                    #↓ joins the existing room on the server and inserts initial information into it (username, icon, party)
                    room = online.worksheet(str(room_code[0]) + ":" + str(room_code[1]) + ":" + str(room_code[2])); room.update('I1:P1', [[username, str(user_icon), convert_pokemon_to_string(party[0], 0),
                    convert_pokemon_to_string(party[1], 1), convert_pokemon_to_string(party[2], 2), convert_pokemon_to_string(party[3], 3), convert_pokemon_to_string(party[4], 4), convert_pokemon_to_string(party[5], 5)]])
                    bg = pp.load("menus\\battle_connecting.png"); window.blit(bg, (0, 0)); pd.flip(); opponent_customized_info = room.get('A1:H1')
                    opponent_username = opponent_customized_info[0][0]; opponent_icon = pp.load('sprites\\trainers\\' + opponent_customized_info[0][1] + '.png') #gets and sets the opponent's information from the server
                    party_temp = opponent_customized_info[0][2:]; party_index = 0; opponent_party = []
                    for i in party_temp:
                        if (i is not None): opponent_party.append(convert_string_to_pokemon(party_temp[party_index]))
                        else: opponent_party.append(None) #converts each of the opponent's pokemon from a string back into a pokemon and builds the party on the user's side
                        party_index += 1
                    for i in opponent_party:
                        if (i is not None): opponent_field_pokemon = i; break
                    room.update_acell('R1', '.'); create_ping_thread('Q1', initial_connection_to_battle, 0) #tells the server that everything is ready for the game to start
        except: #if a room does not exist, create one
            for i in party:
                if (i is not None): field_pokemon = i; break #sets the first available pokemon in the party to be the field pokemon
            room = online.add_worksheet(str(room_code[0]) + ":" + str(room_code[1]) + ":" + str(room_code[2]), 1000, 128) #creates a room on the server
            room.update('A1:H1', [[username, str(user_icon), convert_pokemon_to_string(party[0], 0), convert_pokemon_to_string(party[1], 1), convert_pokemon_to_string(party[2], 2), convert_pokemon_to_string(party[3], 3),
             convert_pokemon_to_string(party[4], 4), convert_pokemon_to_string(party[5], 5)]]); create_ping_thread('I1', waiting_room_menu, -1); host = True
            #^ inserts initial information into the room (party, username, etc)
            active_screen = "room_waiting"; bg = pp.load("menus\\room_waiting.png"); active_button = "waiting_cancel"; waiting_room_menu(-1) #sends the host to the waiting room menu
def create_ping_thread(cell, menu, args): #creates a new thread to ping the server in the background for information
    ping_thread = threading.Thread(target=ping, args=(cell, menu, args), daemon=True); ping_thread.start()
def ping(cell, menu, default_args): #pings the server with the specified function
    global room, render_queue, pingtime
    try:
        test = room.acell(cell).value
        while (test is None):
            sleep(1); pingtime -= 1
            if (pingtime == 0): pingtime = 5; print(cell); print(str(menu)); test = room.acell(cell).value
            render_queue.append([pp.load('menus\\online\\ping ' + str(pingtime) + '.png'), (1136, 536)]); menu(default_args)
        else: return menu(test)
    except: battle_screen(-1, 115); cancel_room(0); Open_Screen(11); return
def format_line(line, line_num):
    line = line.replace('{player}', username); line = line.replace('{active_mon}', str(field_pokemon.nick))
    line = line.replace('{opponent}', str(opponent_username)); line = line.replace('{opponent_mon}', str(opponent_field_pokemon.nick))
    line = line.replace('{move}', player_move); line = line.replace('{opponent_move}', opponent_move)
    if (field_pokemon.ability is not None): line = line.replace('{ability}', str(field_pokemon.ability.name))
    if (opponent_field_pokemon.ability is not None): line = line.replace('{opponent_ability}', str(opponent_field_pokemon.ability.name))
    if (field_pokemon.held_item is not None): line = line.replace('{item}', str(field_pokemon.held_item.name))
    if (opponent_field_pokemon.held_item is not None): line = line.replace('{opponent_item}', str(opponent_field_pokemon.held_item.name))
    return(line)
def check_win(selected_party):
    real_count = 0; fainted = 0
    for i in selected_party:
        if (i is not None):
            if (i.current_hp <= 0): fainted += 1
            real_count += 1
    if (fainted == real_count): return True
    else: return False
def use_move(move_index):
    global opponent_field_pokemon, field_pokemon, active_button
    field_pokemon.moves[move_index].current_pp -= 1; active_button = 'transition'
    if (host):
        room.update_acell('Q' + str(turn + 1), '.'); room.update_acell('V' + str(turn + 1), 'Move'); room.update_acell('T' + str(turn + 1), field_pokemon.moves[move_index].name)
        room.update_acell('X' + str(turn + 1), str(seed)); create_ping_thread('R' + str(turn + 1), complete_turn, 0)
    else:
        room.update_acell('R' + str(turn + 1), '.'); room.update_acell('W' + str(turn + 1), 'Move'); room.update_acell('U' + str(turn + 1), field_pokemon.moves[move_index].name)
        room.update_acell('Y' + str(turn + 1), str(seed)); create_ping_thread('Q' + str(turn + 1), complete_turn, 0)
    battle_screen(-1, 2)
def battle_text(line_num, display_time):
    global username, opponent_username, party, opponent_party, active_button, player_move, opponent_move, turn, field_pokemon, opponent_field_pokemon
    try:
        text = open('netplay\\flavour_text.txt', 'r'); incrementer = 0; text_font = pg.font.Font('Bolgart.ttf', 18); line_text = ''; win = False; lose = False
        for i in text:
            if (incrementer == line_num): line_text = i; break
            incrementer += 1
        if (field_pokemon.current_hp <= 0 and line_num != 9 and line_num != 114):
            battle_text(9, 3)
            if (check_win(party) == False):
                active_button = "switch1"; battle_screen(-1, -1)
            else: cancel_room(0); return
        elif (opponent_field_pokemon.current_hp <= 0 and line_num != 10 and line_num != 113):
            battle_text(10, 3)
            if (check_win(opponent_party) == False):
                if (host):room.update_acell('Q' + str(turn + 2), '.'); create_ping_thread('U' + str(turn + 2), get_switch_in, -1)
                else: room.update_acell('R' + str(turn + 2), '.'); create_ping_thread('T' + str(turn + 2), get_switch_in, -1)
            else: battle_text(113, 5); cancel_room(0); return
                #turn -= 1
        else:
            render_queue.append([text_font.render(format_line(line_text, line_num), True, (255, 255, 255)), (25, 560)]); battle_screen(-1, -1); sleep(display_time)
            if (line_num == 0): battle_screen(-1, 1)
            elif (line_num == 1): active_button = 'move1'; battle_screen(-1, -1)
            elif (line_num == 3):
                if (move_first == field_pokemon): animate_move(opponent_field_pokemon, player_move); battle_screen(-1, 4)
                else:
                    animate_move(opponent_field_pokemon, player_move)
                    for i in field_pokemon.status_effects:
                        if (i == 'Burn'):
                            field_pokemon.current_hp -= field_pokemon.hp / 16
                            if (field_pokemon.current_hp <= 0): field_pokemon.current_hp = 1
                            battle_screen(-1, 117)
                        if (i == 'Poison'):
                            field_pokemon.current_hp -= field_pokemon.hp / 8
                            if (field_pokemon.current_hp <= 0): field_pokemon.current_hp = 1
                            battle_screen(-1, 118)
                    for i in opponent_field_pokemon.status_effects:
                        if (i == 'Burn'):
                            opponent_field_pokemon.current_hp -= opponent_field_pokemon.hp / 16
                            if (opponent_field_pokemon.current_hp <= 0): opponent_field_pokemon.current_hp = 1
                            battle_screen(-1, 116)
                        if (i == 'Poison'):
                            opponent_field_pokemon.current_hp -= opponent_field_pokemon.hp / 8
                            if (opponent_field_pokemon.current_hp <= 0): opponent_field_pokemon.current_hp = 1
                            battle_screen(-1, 119)
                    active_button = "move1"; battle_screen(-1, -1)
            elif (line_num == 4):
                if (move_first == opponent_field_pokemon): animate_move(field_pokemon, opponent_move); battle_screen(-1, 3)
                else:
                    animate_move(field_pokemon, opponent_move)
                    for i in field_pokemon.status_effects:
                        if (i == 'Burn'):
                            field_pokemon.current_hp -= field_pokemon.hp / 16
                            if (field_pokemon.current_hp <= 0): field_pokemon.current_hp = 1
                            battle_screen(-1, 117)
                        if (i == 'Poison'):
                            field_pokemon.current_hp -= field_pokemon.hp / 8
                            if (field_pokemon.current_hp <= 0): field_pokemon.current_hp = 1
                            battle_screen(-1, 118)
                    for i in opponent_field_pokemon.status_effects:
                        if (i == 'Burn'):
                            opponent_field_pokemon.current_hp -= opponent_field_pokemon.hp / 16
                            if (opponent_field_pokemon.current_hp <= 0): opponent_field_pokemon.current_hp = 1
                            battle_screen(-1, 116)
                        if (i == 'Poison'):
                            opponent_field_pokemon.current_hp -= opponent_field_pokemon.hp / 8
                            if (opponent_field_pokemon.current_hp <= 0): opponent_field_pokemon.current_hp = 1
                            battle_screen(-1, 119)
                    active_button = "move1"; battle_screen(-1, -1)
            else: pass
    except Exception as e: print(repr(e))
def animate_move(target, used_move):
    global field_pokemon, opponent_field_pokemon, host, player_move, opponent_move, turn, seed, weather, weather_countdown
    if (host): seeds = room.get('X' + str(turn + 1) + ':Y' + str(turn + 1)); player_seed = int(seeds[0][0]); opponent_seed = int(seeds[0][1])
    else: seeds = room.get('X' + str(turn + 1) + ':Y' + str(turn + 1)); player_seed = int(seeds[0][1]); opponent_seed = int(seeds[0][0])
    if (target == field_pokemon): user = opponent_field_pokemon; move_seed = opponent_seed
    else: user = field_pokemon; move_seed = player_seed
    for i in move_dex:
        if (move_dex[i].name == used_move): used_move = move_dex[i]
    if (determine_effectiveness(target, used_move) > 1):
        if (used_move.category != 2): battle_text(5, 2)
    elif (determine_effectiveness(target, used_move) == 0):
        if (target == opponent_field_pokemon):
            if (used_move.category != 2): battle_text(7, 2)
        else: battle_text(8, 2)
    elif (determine_effectiveness(target, used_move) < 1): battle_text(6, 2)
    if (opponent_field_pokemon == target):
        if (used_move.category == 0): window.blit(pp.load('sprites\\attack animations\\physical\\' + used_move.typing.lower() + " 1.png"), (699, 129))
        elif (used_move.category == 1): window.blit(pp.load('sprites\\attack animations\\special\\' + used_move.typing.lower() + " 1.png"), (699, 129))
        elif (used_move.category == 2): window.blit(pg.transform.scale(pp.load('sprites\\attack animations\\status\\' + used_move.typing.lower() + " 1.png"), (288, 288)), (256, 215))
    else:
        if (used_move.category == 0): window.blit(pg.transform.scale(pp.load("sprites\\attack animations\\physical\\" + used_move.typing.lower() + " 1.png"), (288, 288)), (256, 215))
        elif (used_move.category == 1): window.blit(pg.transform.scale(pp.load("sprites\\attack animations\\special\\" + used_move.typing.lower() + " 1.png"), (288, 288)), (256, 215))
        elif (used_move.category == 2): window.blit(pp.load("sprites\\attack animations\\status\\" + used_move.typing.lower() + " 1.png"), (699, 129))
    pd.flip(); sleep(0.1); battle_screen(-1, -1)
    if (opponent_field_pokemon == target):
        if (used_move.category == 0): window.blit(pp.load('sprites\\attack animations\\physical\\' + used_move.typing.lower() + " 2.png"), (699, 129))
        elif (used_move.category == 1): window.blit(pp.load('sprites\\attack animations\\special\\' + used_move.typing.lower() + " 2.png"), (699, 129))
        elif (used_move.category == 2): window.blit(pg.transform.scale(pp.load('sprites\\attack animations\\status\\' + used_move.typing.lower() + " 2.png"), (288, 288)), (256, 215))
    else:
        if (used_move.category == 0): window.blit(pg.transform.scale(pp.load("sprites\\attack animations\\physical\\" + used_move.typing.lower() + " 2.png"), (288, 288)), (256, 215))
        elif (used_move.category == 1): window.blit(pg.transform.scale(pp.load("sprites\\attack animations\\special\\" + used_move.typing.lower() + " 2.png"), (288, 288)), (256, 215))
        elif (used_move.category == 2): window.blit(pp.load("sprites\\attack animations\\status\\" + used_move.typing.lower() + " 2.png"), (699, 129))
    pd.flip()
    damage = used_move.effect(used_move, user, target, weather, terrain, move_seed)
    if (type(damage) is int): target.current_hp -= damage
    else:
        target.current_hp -= damage[0]
        if (damage[1] == "burn"):
            if (damage[2] == 1): target.status_effects.append('Burn'); display_text_based_on_client(target, 13, 14)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'freeze'):
            if (damage[2] == 1): target.status_effects.append('Frozen'); display_text_based_on_client(target, 19, 20)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'paralysis'):
            if (damage[2] == 1): target.status_effects.append('Paralysed'); display_text_based_on_client(target, 120, 121)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'sleep'):
            if (damage[2] == 1): target.status_effects.append('Sleep'); display_text_based_on_client(target, 21, 22)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'poison'):
            if (damage[2] == 1): target.status_effects.append('Poison'); display_text_based_on_client(target, 15, 16)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'poison'):
            if (damage[2] == 2): target.status_effects.append('Lethal Poison'); display_text_based_on_client(target, 17, 18)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'confuse'):
            if (damage[2] == 1): target.status_effects.append('Confused'); display_text_based_on_client(target, 108, 110)
            elif (damage[3] == 1): display_text_based_on_client(target, 83, 84)
        elif (damage[1] == 'splash'): battle_screen(-1, 87)
        elif (damage[1] == 'recoil'):
            display_text_based_on_client(target, 89, 88)
            if (target == field_pokemon): opponent_field_pokemon.current_hp -= damage[2]
            else: field_pokemon.current_hp -= damage[2]
        elif (damage[1] == 'Harsh Sunlight'): battle_screen(-1, 90); weather = 'Harsh Sunlight'; weather_countdown = damage[2]
        elif (damage[1] == 'Rain'): battle_screen(-1, 95); weather = 'Rain'; weather_countdown = damage[2]
        elif (damage[1] == 'Sandstorm'): battle_screen(-1, 100); weather = 'Sandstorm'; weather_countdown = damage[2]
        elif (damage[1] == 'Hail'): battle_screen(-1, 104); weather = 'Hail'; weather_countdown = damage[2]
        elif (damage[1] == 'Electric Terrain'): battle_screen(-1, 108); terrain['electric'] = damage[2]
        elif (damage[1] == 'Grassy Terrain'): battle_screen(-1, 109); terrain['grassy'] = damage[2]
        elif (damage[1] == 'Psychic Terrain'): battle_screen(-1, 110); terrain['psychic'] = damage[2]
        elif (damage[1] == 'Misty Terrain'): battle_screen(-1, 111); terrain['misty'] = damage[2]
        elif (damage[1] == 'after you'): display_text_based_on_client(target, 122, 123)
        elif (damage[1] == 'clear smog'): display_text_based_on_client(target, 124, 125)
        elif (damage[1] == 'guard swap'): display_text_based_on_client(target, 126, 127)
        elif (damage[1] == 'loweratk' or damage[1] == 'lowerdef' or damage[1] == 'lowerspatk' or damage[1] == 'lowerspdef' or damage[1] == 'lowerspd' or damage[1] or damage[1] == 'raiseatk' or damage[1] == 'raisedef' or\
            damage[1] == 'raisespatk' or damage[1] == 'raisespdef' or damage[1] == 'raisespd'):
            for i in range(3):
                if (damage[2] == i + 1): display_text_based_on_client(target, damage[4] + i, damage[3] + i); break
                if (damage[2] == 0): display_text_based_on_client(target, 83, 84); break
        elif (damage[1] == 'lowerowndef' or damage[1] == 'lowerownspatk' or damage[1] or damage[1] == 'lowerownspd'):
            for i in range(3):
                if (damage[2] == i + 1): display_text_based_on_client(target, damage[3] + i, damage[4] + i); break
                if (damage[2] == 0): display_text_based_on_client(target, 83, 84); break

    seed = rng.randint(1, 10000000)
def set_letter(letter):
    global active_mon, active_button
    if (letter == "back"): active_mon.nick = active_mon.name; edit_mon_menu(1); Open_Screen(4)
    else:
        if (letter == "done" and len(active_mon.nick) > 0): edit_mon_menu(1); Open_Screen(4)
        else:
            if (active_mon.nick == active_mon.name and letter != " " and letter != "backspace" and letter != "done"): active_mon.nick = letter
            else:
                if (letter == "backspace" and len(active_mon.nick) > 0): active_mon.nick = active_mon.nick[:len(active_mon.nick) - 1]
                if (len(active_mon.nick) <= 18 and letter != "backspace" and letter != "done"): active_mon.nick += letter
            edit_name_menu(1)
def done_pokemon(dummy):
    global active_party_slot, active_mon, global_move_offset, global_nature_offset, global_item_offset
    has_moves_check = 0
    for i in active_mon.moves:
        if (i is None): has_moves_check += 1
    if (has_moves_check != 4):
        if (active_mon.nature is None): active_mon.nature = "Hardy"
        party[int(active_party_slot[5]) - 1] = active_mon; Open_Screen(2); render_screen(False)
def open_switch_menu(dummy):
    global active_button
    active_button = "switch1"; battle_screen(-1, -1)
def generate_room_code(dummy):
    global room_code, active_button
    if (active_button == "battle_menu_rc_1"): index = 0
    elif (active_button == "battle_menu_rc_2"): index = 1
    else: index = 2
    if (room_code[index] is None or room_code[index] == 11): room_code[index] = 0
    else: room_code[index] += 1
    battle_menu(-1)
#handles opening a specific screen (main menu, settings, battle screen, etc.)
def Open_Screen(screen):
    #using local functions to save time and space
    def Main_Menu():
        global active_screen, active_button, bg
        active_screen = "main_menu"; bg = menuImageDict[rng.randint(0, 13)]; active_button = "menu_play"; render_screen(False)
    def Decks_Menu():
        global active_screen, active_button, bg
        active_screen = "decks_menu"; bg = pp.load("menus\\decks.png"); active_button = "decks_decks"; render_screen(False)
    def Deck_Builder_Menu():
        global active_screen, active_button, bg
        active_screen = "deck_builder_menu"; bg = pp.load("menus\\deck_builder.png"); active_button = "deck_1"; render_screen(False)
    def Deck_Builder_Mon_Select():
        global active_screen, active_button, bg, active_party_slot
        if (active_button != "edit_mon_back"): active_party_slot = active_button
        active_screen = "deck_builder_mon_select"; bg = pp.load("menus\\deck_builder_mon_select.png"); active_button = "mon_select_1"; select_mon_menu(0)
    def Deck_Builder_Edit_Mon():
        global active_screen, active_button, bg, global_move_offset
        active_screen = "deck_builder_edit_mon"; bg = pp.load("menus\\edit_mon.png"); active_button = "edit_mon_name"; global_move_offset = 0; edit_mon_menu(1)
    def Deck_Builder_Move_Select():
        global active_screen, active_button, bg, active_move_slot
        active_move_slot = int(active_button[len(active_button) - 1:]); active_screen = "deck_builder_move_select"
        bg = pp.load("menus\\deck_builder_move_select.png"); active_button = "move_select_1"; move_select_menu("")
    def Deck_Builder_Item_Select():
        global active_screen, active_button, bg
        active_screen = "deck_builder_item_select"; bg = pp.load("menus\\deck_builder_move_select.png"); active_button = "item_select_1"; item_select_menu("")
    def Deck_Builder_Ability_Select():
        global active_screen, active_button, bg, active_mon
        active_screen = "deck_builder_ability_select"
        if (len(active_mon.ability_set) == 1): bg = pp.load("menus\\deck_builder_ability_select_one.png"); active_button = "ability_select_1_1"; ability_select_menu(1)
        elif (len(active_mon.ability_set) == 2): bg = pp.load("menus\\deck_builder_ability_select_two.png"); active_button = "ability_select_2_1"; ability_select_menu(2)
        else: bg = pp.load("menus\\deck_builder_ability_select_three.png"); active_button = "ability_select_3_1"; ability_select_menu(3)
    def Deck_Builder_Nature_Select():
        global active_screen, active_button, bg
        active_screen = "deck_builder_nature_select"; bg = pp.load("menus\\deck_builder_move_select.png"); active_button = "nature_select_1"; nature_select_menu(0)
    def Deck_Builder_Edit_Nickname():
        global active_screen, active_button, bg
        active_screen = "deck_builder_edit_name"; bg = pp.load("menus\\deck_builder_edit_name.png"); active_button = "name_letter_1"; edit_name_menu(-1)
    def Decks_Management():
        global active_screen, active_button, bg
        bg = pp.load("menus\\decks_save_load.png"); active_screen = "decks_management"; active_button = "decks_save"; decks_save_menu(-1)
    def Battle_Menu():
        global active_screen, active_button, bg, online, gs
        error_font = pg.font.Font('Bolgart.ttf', 24)
        if (party == [None, None, None, None, None, None]): window.blit(error_font.render('You have no Pokemon in your party', True, (255, 0, 0)), (26, 16)); pd.flip()
        else:
            if (online is None):
                try: active_screen = "battle_menu"; window.fill((0,0,0)); bg = pp.load("menus\\battle_connecting.png"); window.blit(bg, (0, 0)); pd.flip(); online = gs.open("Pykemon")
                except: Open_Screen(0); window.blit(error_font.render('Failed to connect', True, (255, 0, 0)), (26, 16)); pd.flip()
            if (online is not None): #not an else statement so it runs after connecting to the server
                Open_Screen(0); error_font = pg.font.Font('Bolgart.ttf', 24); window.blit(error_font.render('Failed to connect', True, (255, 0, 0)), (26, 16)); pd.flip()
                bg = pp.load('menus\\battle_menu.png'); active_button = "battle_menu_back"; active_screen = "battle_menu"; render_queue = []; battle_menu(-1)
    def Battle():
        global active_screen, active_button, bg, render_queue
        bg = pp.load("menus\\battle.png"); active_screen = "battle"; battle_screen(-1, 0)
    screenDict = {0:Main_Menu, 1:Decks_Menu, 2:Deck_Builder_Menu, 3:Deck_Builder_Mon_Select, 4:Deck_Builder_Edit_Mon, 5:Deck_Builder_Move_Select, 6:Deck_Builder_Item_Select,
     7:Deck_Builder_Ability_Select, 8:Deck_Builder_Nature_Select, 9:Deck_Builder_Edit_Nickname, 10:Decks_Management, 11:Battle_Menu, 12:Battle}
    screenDict[screen]();
#control functions
window = pd.set_mode((width, height))
menuImageDict = {0:pp.load("menus\\menu1.png"),1:pp.load("menus\\menu2.png"), 2:pp.load("menus\\menu3.png"),3:pp.load("menus\\menu4.png"), 4:pp.load("menus\\menu5.png"),5:pp.load("menus\\menu6.png"),
 6:pp.load("menus\\menu7.png"),7:pp.load("menus\\menu8.png"), 8:pp.load("menus\\menu9.png"),9:pp.load("menus\\menu10.png"), 10:pp.load("menus\\menu11.png"),11:pp.load("menus\\menu12.png"),
 12:pp.load("menus\\menu13.png"),13:pp.load("menus\\menu14.png")}
#^ creates a dictionary storing each different variation of the menu background image for the random number generator to pull from
#^ so that i don't have to use a really big ugly if statement containing everything
bg = menuImageDict[rng.randint(0, 13)]; Open_Screen(0)
inputU = {"menu_play":"menu_settings", "menu_settings":"menu_play","decks_decks":"decks_back", "decks_edit":"decks_decks", "decks_back":"decks_edit", "deck_1":"deck_4", "deck_2":"deck_1","deck_6":"deck_1","deck_3":"deck_2",
 "deck_4":"deck_back", "deck_5":"deck_6","deck_back":"deck_1", "edit_mon_ability":"edit_mon_move_4","edit_mon_item":"edit_mon_move_4","edit_mon_nature":"edit_mon_move_4","edit_mon_done":"edit_mon_back",
 "edit_mon_move_4":"edit_mon_move_3", "edit_mon_move_3":"edit_mon_move_2","edit_mon_move_2":"edit_mon_move_1","edit_mon_move_1":"edit_mon_level","edit_mon_level":"edit_mon_name","edit_mon_shiny":"edit_mon_name",
 "mon_select_2":"mon_select_1","mon_select_3":"mon_select_2","mon_select_4":"mon_select_3","mon_select_5":"mon_select_4","mon_select_6":"mon_select_5","mon_select_1":[select_mon_menu, -1],"move_select_1":[move_select_menu, -1],
 "move_select_2":"move_select_1","move_select_3":"move_select_2","move_select_4":"move_select_3","move_select_5":"move_select_4","move_select_6":"move_select_5","item_select_1":[item_select_menu, -1],
 "item_select_2":"item_select_1","item_select_3":"item_select_2","item_select_4":"item_select_3","item_select_5":"item_select_4","item_select_6":"item_select_5","edit_mon_back":"edit_mon_back","edit_mon_name":"edit_mon_name",
 "ability_select_1_back":[ability_select_menu, 1, "ability_select_1_1"],"ability_select_2_back":[ability_select_menu, 2, "ability_select_2_1"],"decks_cycle":[load_party,1],
 "ability_select_3_back":[ability_select_menu, 3, "ability_select_3_3"],"ability_select_3_3":[ability_select_menu, 3, "ability_select_3_1"],"nature_select_1":[nature_select_menu, -1],
 "nature_select_2":[nature_select_menu, 0, "nature_select_1"],"nature_select_3":[nature_select_menu, 0, "nature_select_2"],"nature_select_4":[nature_select_menu, 0, "nature_select_3"],
 "nature_select_5":[nature_select_menu, 0, "nature_select_4"],"nature_select_6":[nature_select_menu, 0, "nature_select_5"],"name_letter_$":"name_letter_1","name_letter_%":"name_letter_1","name_letter_A":"name_letter_2",
 "name_letter_B":"name_letter_3","name_letter_C":"name_letter_4","name_letter_D":"name_letter_5","name_letter_E":"name_letter_6","name_letter_F":"name_letter_7","name_letter_G":"name_letter_8","name_letter_H":"name_letter_9",
 "name_letter_I":"name_letter_0","name_letter_J":"name_letter_-","name_letter_K":"name_letter__","name_letter_L":"name_letter_!","name_letter_M":"name_letter_?","name_letter_N":"name_letter_.","name_letter_O":"name_letter_'",
 "name_letter_P":"name_letter_'","name_letter_Q":"name_letter_$","name_letter_R":"name_letter_%","name_letter_S":"name_letter_A","name_letter_T":"name_letter_B","name_letter_U":"name_letter_C","name_letter_V":"name_letter_D",
 "name_letter_W":"name_letter_E","name_letter_X":"name_letter_F","name_letter_Y":"name_letter_G","name_letter_Z":"name_letter_H","name_letter_a":"name_letter_I","name_letter_b":"name_letter_J","name_letter_c":"name_letter_K",
 "name_letter_d":"name_letter_L","name_letter_e":"name_letter_M","name_letter_f":"name_letter_N","name_letter_g":"name_letter_O","name_letter_h":"name_letter_P","name_letter_i":"name_letter_Q","name_letter_j":"name_letter_R",
 "name_letter_k":"name_letter_S","name_letter_l":"name_letter_T","name_letter_m":"name_letter_U","name_letter_n":"name_letter_V","name_letter_o":"name_letter_W","name_letter_p":"name_letter_X","name_letter_q":"name_letter_Y",
 "name_letter_r":"name_letter_Z","name_letter_s":"name_letter_a","name_letter_t":"name_letter_b","name_letter_u":"name_letter_c","name_letter_v":"name_letter_d","name_letter_w":"name_letter_e","name_letter_x":"name_letter_f",
 "name_letter_y":"name_letter_g","name_letter_z":"name_letter_h","name_letter_ ":"name_letter_p","name_letter_backspace":"name_letter_s","edit_name_back":"name_letter_ ","edit_name_done":"name_letter_backspace",
 "decks_load":"decks_save","decks_return":"decks_load","decks_save":"decks_return","battle_menu_connect":"battle_menu_rc_1"}
inputL = {"menu_play":"menu_decks","menu_settings":"menu_decks", "menu_decks":"menu_play", "deck_1":"deck_6", "deck_4":"deck_5", "deck_2":"deck_1", "deck_3":"deck_4","mon_select_back":"mon_select_1","switch2":"switch1",
 "mon_select_back":"mon_select_6","edit_mon_done":"edit_mon_nature","edit_mon_back":"edit_mon_move_4","edit_mon_nature":"edit_mon_item","edit_mon_item":"edit_mon_ability","switch3":"switch2","switch4":"switch3",
 "edit_mon_shiny":"edit_mon_level","move_select_back":"move_select_1","item_select_back":"item_select_1","edit_mon_move_4":"edit_mon_move_4","edit_mon_ability":"edit_mon_ability","switch5":"switch4","switch6":"switch5",
 "ability_select_2_2":[ability_select_menu, 2, "ability_select_2_1"],"ability_select_2_3":[ability_select_menu, 3, "ability_select_1_3"],"nature_select_back":[nature_select_menu, 0, "nature_select_1"],
 "name_letter_2":"name_letter_1","name_letter_3":"name_letter_2","name_letter_4":"name_letter_3","name_letter_5":"name_letter_4","name_letter_6":"name_letter_5","name_letter_7":"name_letter_6","switch_cancel":"switch6",
 "name_letter_8":"name_letter_7","name_letter_9":"name_letter_8","name_letter_0":"name_letter_9","name_letter_-":"name_letter_0","name_letter__":"name_letter_-","name_letter_!":"name_letter__","switch":"move4",
 "name_letter_?":"name_letter_!","name_letter_.":"name_letter_?","name_letter_'":"name_letter_.","name_letter_%":"name_letter_$","name_letter_A":"name_letter_%","name_letter_B":"name_letter_A",
 "name_letter_C":"name_letter_B","name_letter_D":"name_letter_C","name_letter_E":"name_letter_D","name_letter_F":"name_letter_E","name_letter_G":"name_letter_F","name_letter_H":"name_letter_G",
 "name_letter_I":"name_letter_H","name_letter_J":"name_letter_I","name_letter_K":"name_letter_J","name_letter_L":"name_letter_K","name_letter_M":"name_letter_L","name_letter_N":"name_letter_M",
 "name_letter_O":"name_letter_N","name_letter_P":"name_letter_O","name_letter_R":"name_letter_Q","name_letter_S":"name_letter_R","name_letter_T":"name_letter_S","name_letter_U":"name_letter_T",
 "name_letter_V":"name_letter_U","name_letter_W":"name_letter_V","name_letter_X":"name_letter_W","name_letter_Y":"name_letter_X","name_letter_Z":"name_letter_Y","name_letter_a":"name_letter_Z",
 "name_letter_b":"name_letter_a","name_letter_c":"name_letter_b","name_letter_d":"name_letter_c","name_letter_e":"name_letter_d","name_letter_f":"name_letter_e","name_letter_g":"name_letter_f",
 "name_letter_h":"name_letter_g","name_letter_j":"name_letter_h","name_letter_j":"name_letter_i","name_letter_k":"name_letter_j","name_letter_l":"name_letter_k","name_letter_m":"name_letter_l",
 "name_letter_n":"name_letter_m","name_letter_o":"name_letter_n","name_letter_p":"name_letter_o","name_letter_q":"name_letter_p","name_letter_r":"name_letter_q","name_letter_s":"name_letter_r",
 "name_letter_t":"name_letter_s","name_letter_u":"name_letter_t","name_letter_v":"name_letter_u","name_letter_w":"name_letter_v","name_letter_x":"name_letter_w","name_letter_y":"name_letter_x",
 "name_letter_z":"name_letter_y","name_letter_backspace":"name_letter_ ","edit_name_done":"edit_name_back","decks_cycle":"decks_load","battle_menu_connect":"battle_menu_bot","move4":"move3","move3":"move2","move2":"move1",
 "battle_menu_bot":"battle_menu_back","battle_menu_rc_2":"battle_menu_rc_1","battle_menu_rc_3":"battle_menu_rc_2"}
inputR = {"menu_play":"menu_decks", "menu_settings":"menu_decks", "menu_decks":"menu_play", "deck_1":"deck_2", "deck_6":"deck_1","deck_4":"deck_3", "deck_5":"deck_4","move1":"move2","move2":"move3","move3":"move4",
 "mon_select_1":"mon_select_back", "mon_select_2":"mon_select_back", "mon_select_3":"mon_select_back", "mon_select_4":"mon_select_back", "mon_select_5":"mon_select_back","mon_select_6":"mon_select_back","switch3":"switch4",
 "edit_mon_level":"edit_mon_shiny","edit_mon_ability":"edit_mon_item","edit_mon_item":"edit_mon_nature","edit_mon_nature":"edit_mon_done","edit_mon_move_1":"edit_mon_back","edit_mon_move_2":"edit_mon_back","switch4":"switch5",
 "edit_mon_move_3":"edit_mon_back","edit_mon_move_4":"edit_mon_back","edit_mon_back":"edit_mon_back","move_select_1":"move_select_back","move_select_2":"move_select_back","move_select_3":"move_select_back","switch5":"switch6",
 "move_select_4":"move_select_back","move_select_5":"move_select_back","move_select_6":"move_select_back","move_select_back":"move_select_back","item_select_1":"item_select_back","item_select_2":"item_select_back",
 "item_select_3":"item_select_back","item_select_4":"item_select_back","item_select_5":"item_select_back","item_select_6":"item_select_back","item_select_back":"item_select_back","edit_mon_done":"edit_mon_done",
 "mon_select_back":"mon_select_back","ability_select_2_1":[ability_select_menu, 2, "ability_select_2_2"],"ability_select_3_1":[ability_select_menu, 3, "ability_select_3_2"], "move4":"switch","switch2":"switch3",
 "nature_select_1":[nature_select_menu, 0, "nature_select_back"],"nature_select_2":[nature_select_menu, 0, "nature_select_back"],"nature_select_3":[nature_select_menu, 0, "nature_select_back"],"switch6":"switch_cancel",
 "nature_select_4":[nature_select_menu, 0, "nature_select_back"],"nature_select_5":[nature_select_menu, 0, "nature_select_back"],"nature_select_6":[nature_select_menu, 0, "nature_select_back"],
 "nature_select_back":"nature_select_back","name_letter_1":"name_letter_2","name_letter_2":"name_letter_3","name_letter_3":"name_letter_4","name_letter_4":"name_letter_5","switch1":"switch2",
 "name_letter_5":"name_letter_6","name_letter_6":"name_letter_7","name_letter_7":"name_letter_8","name_letter_8":"name_letter_9","name_letter_9":"name_letter_0","name_letter_0":"name_letter_-",
 "name_letter_-":"name_letter__","name_letter__":"name_letter_!","name_letter_!":"name_letter_?","name_letter_?":"name_letter_.","name_letter_.":"name_letter_'","name_letter_$":"name_letter_%",
 "name_letter_%":"name_letter_A","name_letter_A":"name_letter_B","name_letter_B":"name_letter_C","name_letter_C":"name_letter_D","name_letter_D":"name_letter_E","name_letter_E":"name_letter_F",
 "name_letter_F":"name_letter_G","name_letter_G":"name_letter_H","name_letter_H":"name_letter_I","name_letter_I":"name_letter_J","name_letter_J":"name_letter_K","name_letter_K":"name_letter_L",
 "name_letter_L":"name_letter_M","name_letter_M":"name_letter_N","name_letter_N":"name_letter_O","name_letter_O":"name_letter_P","name_letter_Q":"name_letter_R","name_letter_R":"name_letter_S",
 "name_letter_S":"name_letter_T","name_letter_T":"name_letter_U","name_letter_U":"name_letter_V","name_letter_V":"name_letter_W","name_letter_W":"name_letter_X","name_letter_X":"name_letter_Y",
 "name_letter_Y":"name_letter_Z","name_letter_Z":"name_letter_a","name_letter_a":"name_letter_b","name_letter_b":"name_letter_c","name_letter_c":"name_letter_d","name_letter_d":"name_letter_e",
 "name_letter_e":"name_letter_f","name_letter_f":"name_letter_g","name_letter_g":"name_letter_h","name_letter_i":"name_letter_j","name_letter_j":"name_letter_k","name_letter_k":"name_letter_l",
 "name_letter_l":"name_letter_m","name_letter_m":"name_letter_n","name_letter_n":"name_letter_o","name_letter_o":"name_letter_p","name_letter_p":"name_letter_q","name_letter_q":"name_letter_r",
 "name_letter_r":"name_letter_s","name_letter_s":"name_letter_t","name_letter_t":"name_letter_u","name_letter_u":"name_letter_v","name_letter_v":"name_letter_w","name_letter_w":"name_letter_x",
 "name_letter_x":"name_letter_y","name_letter_y":"name_letter_z","name_letter_ ":"name_letter_backspace","edit_name_back":"edit_name_done","decks_save":"decks_cycle","decks_load":"decks_cycle",
 "decks_return":"decks_cycle","battle_menu_back":"battle_menu_bot","battle_menu_bot":"battle_menu_connect","battle_menu_rc_1":"battle_menu_rc_2","battle_menu_rc_2":"battle_menu_rc_3"}
inputD = {"menu_play":"menu_settings", "menu_settings":"menu_play", "decks_decks":"decks_edit", "decks_edit":"decks_back", "decks_back": "decks_decks", "deck_1":"deck_back", "deck_2":"deck_3",
 "deck_4":"deck_1", "deck_6":"deck_5", "deck_3":"deck_4", "deck_5":"deck_4","deck_back":"deck_4","mon_select_1":"mon_select_2","mon_select_2":"mon_select_3",
 "mon_select_3":"mon_select_4","mon_select_4":"mon_select_5","mon_select_5":"mon_select_6","mon_select_6":[select_mon_menu, 1],"edit_mon_name":"edit_mon_level","edit_mon_level":"edit_mon_move_1",
 "edit_mon_move_1":"edit_mon_move_2","edit_mon_move_3":"edit_mon_move_4","edit_mon_move_4":"edit_mon_ability","edit_mon_shiny":"edit_mon_move_1",
 "edit_mon_back":"edit_mon_done","edit_mon_move_2":"edit_mon_move_3", "move_select_1":"move_select_2","move_select_2":"move_select_3","move_select_3":"move_select_4","move_select_4":"move_select_5",
 "move_select_5":"move_select_6","move_select_6":[move_select_menu, 1],"item_select_1":"item_select_2","item_select_2":"item_select_3","item_select_3":"item_select_4","item_select_4":"item_select_5",
 "item_select_5":"item_select_6","item_select_6":[item_select_menu, 1],"edit_mon_done":"edit_mon_done","edit_mon_ability":"edit_mon_ability","decks_load":"decks_return","decks_return":"decks_save",
 "ability_select_1_1":[ability_select_menu, 1, "ability_select_1_back"],"ability_select_2_1":[ability_select_menu, 2, "ability_select_2_back"],"battle_menu_rc_3":"battle_menu_connect",
 "ability_select_2_2":[ability_select_menu, 2, "ability_select_2_back"],"ability_select_3_1":[ability_select_menu, 3, "ability_select_3_3"],"decks_cycle":[load_party, -1],
 "ability_select_3_2":[ability_select_menu, 3, "ability_select_3_3"],"ability_select_3_3":[ability_select_menu, 3, "ability_select_3_back"],
 "nature_select_1":[nature_select_menu, 0, "nature_select_2"],"nature_select_2":[nature_select_menu, 0, "nature_select_3"],"nature_select_3":[nature_select_menu, 0, "nature_select_4"],
 "nature_select_4":[nature_select_menu, 0, "nature_select_5"],"nature_select_5":[nature_select_menu, 0, "nature_select_6"],"nature_select_6":[nature_select_menu, 1],
 "name_letter_1":"name_letter_%","name_letter_2":"name_letter_A","name_letter_3":"name_letter_B","name_letter_4":"name_letter_C","name_letter_5":"name_letter_D","name_letter_6":"name_letter_E",
 "name_letter_7":"name_letter_F","name_letter_8":"name_letter_G","name_letter_9":"name_letter_H","name_letter_0":"name_letter_I","name_letter_-":"name_letter_J","name_letter__":"name_letter_K",
 "name_letter_!":"name_letter_L","name_letter_?":"name_letter_M","name_letter_.":"name_letter_N","name_letter_'":"name_letter_O","name_letter_$":"name_letter_Q","name_letter_%":"name_letter_R",
 "name_letter_A":"name_letter_S","name_letter_B":"name_letter_T","name_letter_C":"name_letter_U","name_letter_D":"name_letter_V","name_letter_E":"name_letter_W","name_letter_F":"name_letter_X",
 "name_letter_G":"name_letter_Y","name_letter_H":"name_letter_Z","name_letter_I":"name_letter_a","name_letter_J":"name_letter_b","name_letter_K":"name_letter_c","name_letter_L":"name_letter_d",
 "name_letter_M":"name_letter_e","name_letter_N":"name_letter_f","name_letter_O":"name_letter_g","name_letter_P":"name_letter_h","name_letter_Q":"name_letter_i","name_letter_R":"name_letter_j",
 "name_letter_S":"name_letter_k","name_letter_T":"name_letter_l","name_letter_U":"name_letter_m","name_letter_V":"name_letter_n","name_letter_W":"name_letter_o","name_letter_X":"name_letter_p",
 "name_letter_Y":"name_letter_q","name_letter_Z":"name_letter_r","name_letter_a":"name_letter_s","name_letter_b":"name_letter_t","name_letter_c":"name_letter_u","name_letter_d":"name_letter_v",
 "name_letter_e":"name_letter_w","name_letter_f":"name_letter_x","name_letter_g":"name_letter_y","name_letter_h":"name_letter_z","name_letter_n":"name_letter_ ","name_letter_o":"name_letter_ ",
 "name_letter_p":"name_letter_ ","name_letter_q":"name_letter_ ","name_letter_r":"name_letter_ ","name_letter_s":"name_letter_backspace","name_letter_t":"name_letter_backspace",
 "name_letter_ ":"edit_name_back","name_letter_backspace":"edit_name_done","decks_save":"decks_load","battle_menu_rc_1":"battle_menu_connect","battle_menu_rc_2":"battle_menu_connect"}
inputE = {"menu_decks":[Open_Screen, 1], "decks_back":[Open_Screen, 0], "decks_edit":[Open_Screen, 2], "deck_back":[Open_Screen, 1], "deck_1":[Open_Screen, 3], "deck_2":[Open_Screen, 3],
 "deck_3":[Open_Screen, 3],"deck_4":[Open_Screen, 3], "deck_5":[Open_Screen, 3], "deck_6":[Open_Screen, 3], "mon_select_back":[Open_Screen, 2], "mon_select_1":[Open_Screen, 4],
 "mon_select_2":[Open_Screen, 4], "mon_select_3":[Open_Screen, 4], "mon_select_4":[Open_Screen, 4], "mon_select_5":[Open_Screen, 4], "mon_select_6":[Open_Screen, 4],"edit_mon_move_1":[Open_Screen, 5],
 "edit_mon_move_2":[Open_Screen, 5], "edit_mon_move_3":[Open_Screen, 5], "edit_mon_move_4":[Open_Screen, 5], "edit_mon_shiny":[swap_shiny, 0], "edit_mon_back":[Open_Screen, 3],
 "move_select_back":[Open_Screen, 4], "move_select_1":[select_move, 0], "move_select_2":[select_move, 0], "move_select_3":[select_move, 0], "move_select_4":[select_move, 0],
 "move_select_5":[select_move, 0], "move_select_6":[select_move, 0], "edit_mon_item":[Open_Screen, 6], "item_select_back":[Open_Screen, 4], "item_select_1":[select_item, 0],
 "item_select_2":[select_item, 0],"item_select_3":[select_item, 0],"item_select_4":[select_item, 0],"item_select_5":[select_item, 0],"item_select_6":[select_item, 0],"decks_decks":[Open_Screen, 10],
 "edit_mon_ability":[Open_Screen, 7], "ability_select_1_back":[Open_Screen, 4], "ability_select_1_1":[Open_Screen, 4],"ability_select_2_back":[Open_Screen, 4],"ability_select_3_back":[Open_Screen, 4],
 "ability_select_2_1":[select_ability, 0], "ability_select_2_2":[select_ability, 0],"ability_select_3_1":[select_ability, 0],"ability_select_3_2":[select_ability, 0], "menu_play":[Open_Screen, 11],
 "ability_select_3_3":[select_ability,0],"edit_mon_nature":[Open_Screen,8],"nature_select_1":[select_nature,0],"nature_select_2":[select_nature,0],"nature_select_3":[select_nature,0],
 "nature_select_4":[select_nature,0],"nature_select_5":[select_nature,0],"nature_select_6":[select_nature,0],"edit_mon_level":[edit_level,-1],"edit_mon_name":[Open_Screen,9],
 "edit_name_back":[set_letter, "back"],"name_letter_1":[set_letter, "1"], "name_letter_2":[set_letter, "2"],"name_letter_3":[set_letter, "3"], "name_letter_4":[set_letter, "4"],
 "name_letter_5":[set_letter, "5"], "name_letter_6":[set_letter, "6"],"name_letter_7":[set_letter, "7"], "name_letter_8":[set_letter, "8"],"name_letter_9":[set_letter, "9"],"battle_menu_back":[Open_Screen, 0],
 "name_letter_0":[set_letter, "0"],"name_letter_-":[set_letter, "-"], "name_letter__":[set_letter, "_"],"name_letter_!":[set_letter, "!"], "name_letter_?":[set_letter, "?"],"decks_load":[set_loaded_party, 0],
 "name_letter_.":[set_letter, "."], "name_letter_'":[set_letter, '"'],"name_letter_$":[set_letter, "$"], "name_letter_%":[set_letter, "%"],"name_letter_A":[set_letter, "A"],"switch1":[switch_pokemon, 0],
 "name_letter_B":[set_letter, "B"],"name_letter_C":[set_letter, "C"], "name_letter_D":[set_letter, "D"],"name_letter_E":[set_letter, "E"], "name_letter_F":[set_letter, "F"],"switch2":[switch_pokemon, 1],
 "name_letter_G":[set_letter, "G"], "name_letter_H":[set_letter, "H"],"name_letter_I":[set_letter, "I"], "name_letter_J":[set_letter, "J"],"name_letter_K":[set_letter, "K"],"switch3":[switch_pokemon, 2],
 "name_letter_L":[set_letter, "L"],"name_letter_M":[set_letter, "M"], "name_letter_N":[set_letter, "N"],"name_letter_O":[set_letter, "O"], "name_letter_P":[set_letter, "P"],"switch4":[switch_pokemon, 3],
 "name_letter_Q":[set_letter, "Q"], "name_letter_R":[set_letter, "R"],"name_letter_S":[set_letter, "S"], "name_letter_T":[set_letter, "T"],"name_letter_U":[set_letter, "U"],"switch5":[switch_pokemon, 4],
 "name_letter_V":[set_letter, "V"],"name_letter_W":[set_letter, "W"], "name_letter_X":[set_letter, "X"],"name_letter_Y":[set_letter, "Y"], "name_letter_Z":[set_letter, "Z"],"switch6":[switch_pokemon, 5],
 "name_letter_a":[set_letter, "a"], "name_letter_b":[set_letter, "b"],"name_letter_c":[set_letter, "c"], "name_letter_d":[set_letter, "d"],"name_letter_e":[set_letter, "e"],"switch_cancel":[switch_pokemon, -1],
 "name_letter_f":[set_letter, "f"],"name_letter_g":[set_letter, "g"], "name_letter_h":[set_letter, "h"],"name_letter_i":[set_letter, "i"], "name_letter_j":[set_letter, "j"],"switch":[open_switch_menu, 0],
 "name_letter_k":[set_letter, "k"], "name_letter_l":[set_letter, "l"],"name_letter_m":[set_letter, "m"], "name_letter_n":[set_letter, "n"],"name_letter_o":[set_letter, "o"],
 "name_letter_p":[set_letter, "p"],"name_letter_q":[set_letter, "q"], "name_letter_r":[set_letter, "r"],"name_letter_s":[set_letter, "s"], "name_letter_t":[set_letter, "t"],
 "name_letter_u":[set_letter, "u"], "name_letter_v":[set_letter, "v"],"name_letter_w":[set_letter, "w"], "name_letter_x":[set_letter, "x"],"name_letter_y":[set_letter, "y"],
 "name_letter_z":[set_letter, "z"],"name_letter_ ":[set_letter, " "], "edit_mon_done":[done_pokemon, 0], "name_letter_backspace":[set_letter, "backspace"], "edit_name_done":[set_letter, "done"],
 "battle_menu_rc_1":[generate_room_code, 0],"battle_menu_rc_2":[generate_room_code, 0],"battle_menu_rc_3":[generate_room_code, 0], "battle_menu_connect":[generate_room, 0],
 "decks_save":[save_party, 0], "decks_return":[Open_Screen, 1], "waiting_cancel":[cancel_room, 1], "move1":[use_move, 0], "move2":[use_move, 1], "move3":[use_move, 2], "move4":[use_move, 3]}
programRunning = True
while programRunning:
    keys=pg.key.get_pressed()
    if (can_interact):
        try:
        #if True:
            if (keys[K_SPACE]):
                inputE[active_button][0](inputE[active_button][1]); can_interact = False
            previous_button = active_button
            if (keys[K_UP] or keys[K_w]):
                if (type(inputU[active_button]) is str): active_button = inputU[active_button]; render_screen(False)
                else:
                    if (len(inputU[active_button]) == 3): active_button = inputU[active_button][2]
                    inputU[previous_button][0](inputU[previous_button][1])
                can_interact = False
            elif (keys[K_LEFT] or keys[K_a]):
                if (type(inputL[active_button]) is str): active_button = inputL[active_button]; render_screen(False)
                else:
                    if (len(inputL[active_button]) == 3): active_button = inputL[active_button][2];
                    inputL[previous_button][0](inputL[previous_button][1])
                can_interact = False
            elif (keys[K_RIGHT] or keys[K_d]):
                if (type(inputR[active_button]) is str): active_button = inputR[active_button]; render_screen(False)
                else:
                    if (len(inputR[active_button]) == 3): active_button = inputR[active_button][2]
                    inputR[previous_button][0](inputR[previous_button][1])
                can_interact = False
            elif (keys[K_DOWN] or keys[K_s]):
                if (type(inputD[active_button]) is str): active_button = inputD[active_button]; render_screen(False)
                else:
                    if (len(inputD[active_button]) == 3): active_button = inputD[active_button][2];
                    inputD[previous_button][0](inputD[previous_button][1])
                can_interact = False
            elif (keys[K_m]): cancel_room(0)
        except Exception as e: print(repr(e)); error_count += 1
    if (can_interact != True): sleep(0.15); can_interact = True
    for event in pg.event.get():
        if (event.type == pg.QUIT or keys[K_p]):
            if (online is not None and room is not None): cancel_room(0)
            programRunning = False; pg.quit()