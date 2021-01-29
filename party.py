
PARTY_TABLE = {
    "TEAM_SIZE": 0x0234, # 4
    "TEAM_LIST": 0x0238, # 600
}

FRLG_PARTY_TABLE = {
    "TEAM_SIZE": 0x0034, # 4
    "TEAM_LIST": 0x0038, # 600
}

import savefile
from pokemon import Pokemon, pokemon_menu

from menu import Menu

def party_menu():

    size = get_team_size()
    print("Party size:", size, "\n")
    
    menu = Menu("Which pokemon would you like to edit?")

    pkmns = {}
    for i in range(size):
        pkmn = get_team_pokemon_at_index(i)
        pkmns[i] = pkmn

        menu.add_option(pkmn.get_nickname(), i)
    
    menu.set_callback(lambda s: pokemon_menu(pkmns[int(s)]))
    menu.show()

def get_team_size():
    return savefile.value_at(savefile.section_table["TEAM_ITEMS"] + PARTY_TABLE["TEAM_SIZE"], 2)

def get_team_pokemon_at_index(index):
    offset = savefile.section_table["TEAM_ITEMS"] + PARTY_TABLE["TEAM_LIST"]
    offset += 100 * index

    return Pokemon(offset)