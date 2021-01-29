POKEMON_TABLE = {
    "PERSONALITY_VALUE": 0x0000, # 4
    "OT_ID":             0x0004, # 4
    "NICKNAME":          0x0008, # 10
    "LANGUAGE":          0x0012, # 2
    "OT_NAME":           0x0014, # 7
    "MARKINGS":          0x001B, # 1
    "CHECKSUM":          0x001C, # 2
    "UNUSED_0":          0x001E, # 2
    "DATA":              0x0020, # 48
    "STATUS":            0x0050, # 2
    "LEVEL":             0x0054, # 1
    "POKERUS_REMAINING": 0x0055, # 1
    "CURRENT_HP":        0x0056, # 2
    "TOTAL_HP":          0x0058, # 2
    "ATTACK":            0x005A, # 2
    "DEFENSE":           0x005C, # 2
    "SPEED":             0x005E, # 2
    "SP_ATTACK":         0x0060, # 2
    "SP_DEFENSE":        0x0062, # 2
}

GROWTH_TABLE = {
    "SPECIES":      0x0000, # 2
    "ITEM":         0x0002, # 2
    "EXPERIENCE":   0x0004, # 4
    "PP_BONUSES":   0x0008, # 1
    "FRIENDSHIP":   0x0009, # 1
    "UNUSED_0":     0x000A, # 2
}

ATTACKS_TABLE = {
    "MOVE_1":      0x0000, # 2
    "MOVE_2":      0x0002, # 2
    "MOVE_3":      0x0004, # 2
    "MOVE_4":      0x0006, # 2
    "PP_1":        0x0008, # 1
    "PP_2":        0x0009, # 1
    "PP_3":        0x000A, # 1
    "PP_4":        0x000B, # 1
}

EV_CONDITIONS_TABLE = {
    "HP_EV":         0x0000, # 1
    "ATTACK_EV":     0x0001, # 1
    "DEFENSE_EV":    0x0002, # 1
    "SPEED_EV":      0x0003, # 1
    "SP_ATTACK_EV":  0x0004, # 1
    "SP_DEFENSE_EV": 0x0005, # 1
    "COOLNESS":      0x0006, # 1
    "COOLNESS":      0x0007, # 1
    "BEAUTY":        0x0008, # 1
    "CUTENESS":      0x0009, # 1
    "TOUGHNESS":     0x000A, # 1
    "FEEL":          0x000B, # 1
}

MISC_TABLE = {
    "POKERUS_STATUS":    0x0000, # 1
    "MET_LOCATION":      0x0001, # 1
    "ORIGINS_INFO":      0x0002, # 2
    "IV_EGGS_ABILITY":   0x0004, # 4
    "RIBBONS_OBEDIENCE": 0x0008, # 4
}


DATA_ORDER_MAP = [ # 24
    "GAEM", "GAME", "GEAM", "GEMA",
    "GMAE", "GMEA", "AGEM", "AGME",
    "AEGM", "AEMG", "AMGE", "AMEG",
    "EGAM", "EGMA", "EAGM", "EAMG",
    "EMGA", "EMAG", "MGAE", "MGEA",
    "MAGE", "MAEG", "MEGA", "MEAG",
]

from encoding import CHAR_TO_BYTE, BYTE_TO_CHAR
from lookups import SPECIES_LOOKUP

import savefile


def pokemon_menu(pkmn):
    print(pkmn)

class Pokemon():

    def __init__(self, offset):
        self.offset = offset        
        self.data_table = self.get_data_offset_table()
        self.decryption_key = self.get_decryption_key()

    def __str__(self):
        return f"{self.get_nickname()} ({self.get_species()})"
        
    def get_nickname(self):
        bs = savefile.bytes_at(self.offset + POKEMON_TABLE["NICKNAME"], 10)

        chars = []
        for b in bs: # Trim input to 7 bytes
            chars.append(BYTE_TO_CHAR[b])

        return "".join(chars)

    def get_data_offset_table(self):
        p_value = savefile.value_at(self.offset + POKEMON_TABLE["PERSONALITY_VALUE"], 4)
        order = DATA_ORDER_MAP[p_value % 24]

        return dict(zip(order, [0, 12, 24, 36]))

    def get_decryption_key(self):
        p_value = savefile.value_at(self.offset + POKEMON_TABLE["PERSONALITY_VALUE"], 4)
        ot_id = savefile.value_at(self.offset + POKEMON_TABLE["OT_ID"], 4)

        return p_value ^ ot_id

    @property
    def growth_table(self):
        return self.offset + POKEMON_TABLE["DATA"] + self.data_table["G"]

    @property
    def attacks_table(self):
        return self.offset + POKEMON_TABLE["DATA"] + self.data_table["A"]

    @property
    def ev_conditions_table(self):
        return self.offset + POKEMON_TABLE["DATA"] + self.data_table["E"]

    @property
    def misc_table(self):
        return self.offset + POKEMON_TABLE["DATA"] + self.data_table["M"]
    
    def get_species(self):
        offset = self.growth_table + GROWTH_TABLE["SPECIES"]
        encrypted = savefile.value_at(offset, 4)
        decrypted = encrypted ^ self.decryption_key

        bs = decrypted.to_bytes(4, "little")
        value = int.from_bytes(bs[0:2], "little")

        return SPECIES_LOOKUP[value]

