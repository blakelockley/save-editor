BOX_OFFSET = 0x0004
POKEMON_SIZE = 80
BOX_SIZE = POKEMON_SIZE * 30

from menu import Menu
from pokemon import Pokemon, PokemonMenu

import savefile

class BoxMenu(Menu):
    
    def build(self):
        self.set_title("Select a Box")

        for n in range(1, 15):
            self.add_option(f"Box {str(n).zfill(2)}", n)

    def select(self, selection):
        index = selection - 1
        offset = savefile.section_table["PC_BUFFER_A"] + BOX_OFFSET + BOX_SIZE * index

        pkmns = []
        for pkmn_offset in range(offset, offset + BOX_SIZE, POKEMON_SIZE):
            pkmn = Pokemon(pkmn_offset)
            pkmns.append(pkmn)

        SelectedBoxMenu(pkmns).show()


class SelectedBoxMenu(Menu):
    
    def build(self, pkmns):
        self.set_title("Select a Pokemon in this Box")

        for pkmn in pkmns:
            self.add_option(f"{pkmn}", pkmn)

    def select(self, selection):
        PokemonMenu(selection).show()