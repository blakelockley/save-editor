
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

def party_menu():

    size = get_team_size()
    
    print("Party size:", size)

    print()
    print("Which pokemon would you like to edit?")

    pkmns = {}
    for i in range(size):
        key = i + 1
        
        pkmn = get_team_pokemon_at_index(i)
        pkmns[key] = pkmn
        
        print(f"{key}) {pkmn.get_nickname()}")

    print("q) Cancel")

    def select_pokemon():
        while True:
            selection = input("> ")

            if selection == "q":
                return None

            try:
                key = int(selection)

                if not (1 <= key <= size):
                    raise ValueError

                return pkmns[key]

            except Exception as e:
                print("Invalid input...")

    pkmn = select_pokemon()
    if not pkmn:
        return

    print()
    pokemon_menu(pkmn)

def get_team_size():
    return savefile.value_at(savefile.section_table["TEAM_ITEMS"] + PARTY_TABLE["TEAM_SIZE"], 2)


def get_team_pokemon_at_index(index):
    offset = savefile.section_table["TEAM_ITEMS"] + PARTY_TABLE["TEAM_LIST"]
    offset += 100 * index

    return Pokemon(offset)