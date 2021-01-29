PARTY_TABLE = {
    "TEAM_SIZE": 0x0234, # 4
    "TEAM_LIST": 0x0238, # 600
}

FRLG_PARTY_TABLE = {
    "TEAM_SIZE": 0x0034, # 4
    "TEAM_LIST": 0x0038, # 600
}

PARTY_POKEMON_SIZE = 100

import savefile
from pokemon import Pokemon, PokemonMenu

from menu import Menu

def get_team_size():
    return savefile.value_at(savefile.section_table["TEAM_AND_ITEMS"] + PARTY_TABLE["TEAM_SIZE"], 2)

def get_team_pokemon_at_index(index):
    offset = savefile.section_table["TEAM_AND_ITEMS"] + PARTY_TABLE["TEAM_LIST"]
    offset += PARTY_POKEMON_SIZE * index

    return Pokemon(offset)

class PartyMenu(Menu):

    def build(self):
        self.set_title("Select a Pokemon in the Party")

        pkmns = {}
        for i in range(get_team_size()):
            pkmn = get_team_pokemon_at_index(i)
            pkmns[i] = pkmn

            self.add_option(str(pkmn), pkmn)
        
    def select(self, selection):
        PokemonMenu(selection).show()