import pygame.image as pp

highlightInfo = {"menu_play":[1,(562, 313)], "menu_settings":[1,(562, 442)], "menu_decks":[0,(893, 312)], "decks_decks":[1,(700, 157)], "decks_edit":[1,(700, 270)], "decks_back":[1,(700, 383)],
 "deck_1":[2,(521, 56)], "deck_2":[2,(790, 123)], "deck_3":[2,(790, 314)], "deck_4":[2,(521, 382)], "deck_5":[2,(248, 315)], "deck_6":[2,(248, 123)], "deck_back":[1,(442, 255)],
 "mon_select_1":[3,(18, 121)], "mon_select_2":[3,(18, 198)], "mon_select_3":[3,(18, 275)], "mon_select_4":[3,(18, 352)], "mon_select_5":[3,(18, 429)], "mon_select_6":[3,(18, 506)],
 "mon_select_back":[1,(845, 482)], "edit_mon_name":[4,(229, 114)], "edit_mon_level":[5,(214, 247)], "edit_mon_shiny":[5,(371, 247)],"edit_mon_move_1":[6,(9, 312)],"edit_mon_move_2":[6,(9, 367)],
 "edit_mon_move_3":[6,(9, 422)],"edit_mon_move_4":[6,(9, 477)], "edit_mon_ability":[7,(9, 532)],"edit_mon_item":[8,(283, 532)], "edit_mon_nature":[9,(490, 533)],"edit_mon_back":[0,(920, 426)],
 "edit_mon_done":[0,(920, 513)],"move_select_1":[10,(14, 118)], "move_select_2":[10,(14, 196)],"move_select_3":[10,(14, 274)], "move_select_4":[10,(14, 352)],"move_select_5":[10,(14, 430)],
 "move_select_6":[10,(14, 508)],"move_select_back":[1,(783, 479)], "item_select_back":[1,(783, 479)],"item_select_1":[10,(14, 118)], "item_select_2":[10,(14, 196)],"item_select_3":[10,(14, 274)],
 "item_select_4":[10,(14, 352)],"item_select_5":[10,(14, 430)], "item_select_6":[10,(14, 508)],"ability_select_3_2":[11,(631,160)],"ability_select_3_3":[11,(477, 286)],"gimmick":[(18,(1100,600))],
 "ability_select_3_back":[0,(468,499)],"ability_select_1_1":[11,(471,227)],"ability_select_1_back":[0,(468,499)],"ability_select_2_1":[11,(319,227)],"ability_select_2_2":[11,(630,227)],
 "ability_select_2_back":[0,(468,499)],"ability_select_3_1":[11,(320, 160)],"nature_select_1":[10,(14, 118)], "nature_select_2":[10,(14, 196)],"nature_select_3":[10,(14, 274)],
 "nature_select_4":[10,(14, 352)],"nature_select_5":[10,(14, 430)],"nature_select_6":[10,(14, 508)],"name_letter_1":[12,(85, 268)],"name_letter_2":[12,(150, 268)],"name_letter_3":[12,(215, 268)],
 "name_letter_4":[12,(280, 268)],"name_letter_5":[12,(345, 268)], "name_letter_6":[12,(410, 268)],"name_letter_7":[12,(475, 268)], "name_letter_8":[12,(540, 268)],"name_letter_9":[12,(605, 268)],
 "name_letter_0":[12,(670, 268)],"name_letter_-":[12,(735, 268)], "name_letter__":[12,(800, 268)],"name_letter_!":[12,(865, 268)], "name_letter_?":[12,(930, 268)],"name_letter_.":[12,(995, 268)],
 "name_letter_'":[12,(1060, 268)],"name_letter_$":[12,(20, 313)],"name_letter_%":[12,(85, 313)],"name_letter_A":[12,(150, 313)],"name_letter_B":[12,(215, 313)],"name_letter_C":[12,(280, 313)],
 "name_letter_D":[12,(345, 313)],"name_letter_E":[12,(410, 313)],"name_letter_F":[12,(475, 313)],"name_letter_G":[12,(540, 313)],"name_letter_H":[12,(605, 313)],"name_letter_I":[12,(670, 313)],
 "name_letter_J":[12,(735, 313)],"name_letter_K":[12,(800, 313)],"name_letter_L":[12,(865, 313)],"name_letter_M":[12,(930, 313)],"name_letter_N":[12,(995, 313)],"name_letter_O":[12,(1060, 313)],
 "name_letter_P":[12,(1125, 313)],"name_letter_Q":[12,(20, 358)],"name_letter_R":[12,(85, 358)],"name_letter_S":[12,(150, 359)],"name_letter_T":[12,(215, 358)],"name_letter_U":[12,(280, 358)],
 "name_letter_V":[12,(345, 358)],"name_letter_W":[12,(410, 358)],"name_letter_X":[12,(475, 358)],"name_letter_Y":[12,(540, 358)],"name_letter_Z":[12,(605, 358)],"name_letter_a":[12,(670, 358)],
 "name_letter_b":[12,(735, 358)],"name_letter_c":[12,(800, 358)],"name_letter_d":[12,(865, 358)],"name_letter_e":[12,(930, 358)],"name_letter_f":[12,(995, 358)],"name_letter_g":[12,(1060, 358)],
 "name_letter_h":[12,(1125, 358)],"name_letter_i":[12,(20, 408)],"name_letter_j":[12,(85, 408)],"name_letter_k":[12,(150, 408)],"name_letter_l":[12,(215, 408)],"name_letter_m":[12,(280, 408)],
 "name_letter_n":[12,(345, 408)],"name_letter_o":[12,(410, 408)],"name_letter_p":[12,(475, 408)],"name_letter_q":[12,(540, 408)],"name_letter_r":[12,(605, 408)],"name_letter_s":[12,(670, 408)],
 "name_letter_t":[12,(735, 408)],"name_letter_u":[12,(800, 408)],"name_letter_v":[12,(865, 408)],"name_letter_w":[12,(930, 408)],"name_letter_x":[12,(995, 408)],"name_letter_y":[12,(1060, 408)],
 "name_letter_z":[12,(1125, 408)],"name_letter_ ":[13,(384, 450)],"edit_name_back":[0,(292, 494)],"edit_name_done":[0,(589, 494)], "name_letter_backspace":[12,(698, 450)],
 "decks_save":[0,(32, 218)], "decks_load":[0,(33, 359)],"decks_return":[0,(35, 500)], "decks_cycle":[14,(461, 344)],"battle_menu_back":[1,(16, 498)], "battle_menu_bot":[1,(420, 498)],
 "battle_menu_connect":[1,(808, 495)], "battle_menu_rc_1":[15,(850, 341)],"battle_menu_rc_2":[15,(936, 341)], "battle_menu_rc_3":[15,(1022, 341)],"waiting_cancel":[1,(20, 512)],
 "transition":[2,(-500, -500)],"move1":[16,(12, 540)],"move2":[16,(285,540)],"move3":[16,(558,540)],"move4":[16,(831,540)],"switch":[17,(1099,540)], "gimmick_switch":[18,(1100, 571)],
 "switch1":[19,(11,537)],"switch2":[19,(179,537)],"switch3":[19,(347,537)],"switch4":[19,(515,537)],"switch5":[19,(683,537)],"switch6":[19,(851,537)],"switch_cancel":[19,(1019,537)]}
def set_button_highlight(active_button):
    if (highlightInfo.get(active_button)[0] == 0):#••••••••••••••••••••••••••••• handles loading button highlights on the
        return pp.load("menus\\highlight_mini.png")#                             screen. highlightInfo stores information used
    elif (highlightInfo.get(active_button)[0] == 1):#                            to draw them in a list. the int determines
        return pp.load("menus\\highlight.png")#••••••••••••••••••••••••••••••••• variant and the tuple determines position.
    elif (highlightInfo.get(active_button)[0] == 2): return pp.load("menus\\highlight_square.png")
    elif (highlightInfo.get(active_button)[0] == 3): return pp.load("menus\\highlight_mon_select.png")
    elif (highlightInfo.get(active_button)[0] == 4): return pp.load("menus\\highlight_edit_mon_name.png")
    elif (highlightInfo.get(active_button)[0] == 5): return pp.load("menus\\highlight_edit_mon_small.png")
    elif (highlightInfo.get(active_button)[0] == 6): return pp.load("menus\\highlight_edit_mon_move.png")
    elif (highlightInfo.get(active_button)[0] == 7): return pp.load("menus\\highlight_edit_mon_ability.png")
    elif (highlightInfo.get(active_button)[0] == 8): return pp.load("menus\\highlight_edit_mon_item.png")
    elif (highlightInfo.get(active_button)[0] == 9): return pp.load("menus\\highlight_edit_mon_nature.png")
    elif (highlightInfo.get(active_button)[0] == 10): return pp.load("menus\\highlight_select_move.png")
    elif (highlightInfo.get(active_button)[0] == 11): return pp.load("menus\\highlight_select_ability.png")
    elif (highlightInfo.get(active_button)[0] == 12): return pp.load("menus\\highlight_name_letter.png")
    elif (highlightInfo.get(active_button)[0] == 13): return pp.load("menus\\highlight_name_spacebar.png")
    elif (highlightInfo.get(active_button)[0] == 14): return pp.load("menus\\highlight_cycle_decks.png")
    elif (highlightInfo.get(active_button)[0] == 15): return pp.load("menus\\highlight_room_code.png")
    elif (highlightInfo.get(active_button)[0] == 16): return pp.load("menus\\highlight_battle_move.png")
    elif (highlightInfo.get(active_button)[0] == 17): return pp.load("menus\\highlight_battle_switch.png")
    elif (highlightInfo.get(active_button)[0] == 18): return pp.load("menus\\highlight_battle_switch_gimmick.png")
    elif (highlightInfo.get(active_button)[0] == 19): return pp.load("menus\\highlight_switch.png")
