BOX_OFFSET = 0x0004
POKEMON_SIZE = 80
BOX_SIZE = POKEMON_SIZE * 30

from menu import Menu
from pokemon import Pokemon

import savefile

def open_box(n):
    index = n - 1
    offset = savefile.section_table["PC_BUFFER_A"] + BOX_OFFSET + BOX_SIZE * index

    pkmns = []
    for pkmn_offset in range(offset, offset + BOX_SIZE, POKEMON_SIZE):
        pkmn = Pokemon(pkmn_offset)
        print(pkmn)

    input()


box_menu = Menu("Select Box")
for n in range(1, 15):
    box_menu.add_option(f"Box {str(n).zfill(2)}", n)

box_menu.set_callback(open_box)
box_menu.set_repeat_flag(False)
