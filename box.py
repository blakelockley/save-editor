BOX_OFFSET = 0x0004
POKEMON_SIZE = 80
BOX_SIZE = POKEMON_SIZE * 30

from menu import Menu
from pokemon import Pokemon, PokemonMenu
from maker import PokemonMaker

import savefile


class BoxMenu(Menu):
    def build(self):
        self.set_title("Select a Box")

        for n in range(1, 15):
            self.add_option(f"Box {str(n).zfill(2)}", n)

    def select(self, selection):
        SelectedBoxMenu(selection).show()


class SelectedBoxMenu(Menu):
    def build(self, selection):
        self.set_title("Select a Pokemon in this Box")

        index = selection - 1
        offset = savefile.section_table["PC_BUFFER_A"] + BOX_OFFSET + BOX_SIZE * index

        for pkmn_offset in range(offset, offset + BOX_SIZE, POKEMON_SIZE):
            pkmn = Pokemon(pkmn_offset)
            self.add_option(f"{pkmn}", pkmn)

    def select(self, selection):
        if selection.is_valid:
            PokemonMenu(selection).show()
        else:
            PokemonMaker(selection.offset).run()
