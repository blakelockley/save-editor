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

import savefile
from encoding import BYTE_TO_CHAR, CHAR_TO_BYTE
from lookups import SPECIES_LOOKUP
from menu import Menu


class Pokemon():

    def __init__(self, offset):
        self.offset = offset        
        self.data_table = self.get_data_offset_table()
        self.decryption_key = self.get_decryption_key()
        self.decrypted_data = self.get_decrypted_data()

    def __str__(self):
        try:    nickname = self.get_nickname()
        except: nickname = "-----"

        try:    species = self.get_species()
        except: species = "??????????"

        return f"{nickname} ({species})"
        
    def get_nickname(self):
        bs = savefile.bytes_at(self.offset + POKEMON_TABLE["NICKNAME"], 10)

        chars = []
        for b in bs:
            if b == 255: break
            chars.append(BYTE_TO_CHAR[b])
            
        return "".join(chars)
        
    def set_nickname(self, new_name):
        bs = [0xFF for _ in range(10)]
        
        for i in range(len(new_name[:10])):
            bs[i] = CHAR_TO_BYTE[new_name[i]]

        offset = self.offset + POKEMON_TABLE["NICKNAME"]
        return savefile.set_bytes_at(offset, bs)

    def get_data_offset_table(self):
        p_value = savefile.value_at(self.offset + POKEMON_TABLE["PERSONALITY_VALUE"], 4)
        order = DATA_ORDER_MAP[p_value % 24]

        return dict(zip(order, [0, 12, 24, 36]))

    def get_decryption_key(self):
        p_value = savefile.value_at(self.offset + POKEMON_TABLE["PERSONALITY_VALUE"], 4)
        ot_id = savefile.value_at(self.offset + POKEMON_TABLE["OT_ID"], 4)

        return p_value ^ ot_id

    def get_decrypted_data(self):
        bs = []
        offset = self.offset + POKEMON_TABLE["DATA"]

        for index in range(offset, offset + 48, 4):
            decrypted_values = self.decryption_key ^ savefile.value_at(index, 4)
            decrypted_bytes = decrypted_values.to_bytes(4, "little")

            bs.extend(decrypted_bytes)

        return bs

    def write_encrypted_data(self):
        offset = self.offset + POKEMON_TABLE["DATA"]

        for index in range(0, 48, 4):
            bs = self.decrypted_data[index : index + 4]
            values = int.from_bytes(bs, byteorder="little")

            encrypted_values = self.decryption_key ^ values
            encrypted_bytes = encrypted_values.to_bytes(4, "little")

            savefile.set_bytes_at(offset + index, encrypted_bytes)

    @property
    def growth_data_offset(self):
        return self.data_table["G"]

    @property
    def attacks_data_offset(self):
        return self.data_table["A"]

    @property
    def ev_conditions_data_offset(self):
        return self.data_table["E"]

    @property
    def misc_data_offset(self):
        return self.data_table["M"]
    
    def get_species(self):
        offset = self.growth_data_offset + GROWTH_TABLE["SPECIES"]
        
        bs = self.decrypted_data[offset : offset + 2]
        value = int.from_bytes(bs, "little")

        return SPECIES_LOOKUP[value]
    
    def set_species(self, value):
        bs = value.to_bytes(2, "little")
        offset = self.growth_data_offset + GROWTH_TABLE["SPECIES"]
        
        for index in range(len(bs)):
            self.decrypted_data[offset + index] = bs[index]

    def get_checksum(self):
        return savefile.value_at(self.offset + POKEMON_TABLE["CHECKSUM"], 2)

    def set_checksum(self):
        checksum = self.calculate_checksum()
        savefile.set_value_at(self.offset + POKEMON_TABLE["CHECKSUM"], checksum, 2)

    def calculate_checksum(self):
        # Initialize a 16-bit checksum variable to zero.
        result = 0

        # Read 2 bytes at a time as 16-bit word (little-endian) and add it to the variable.    
        for index in range(0, 48, 2):
            bs = self.decrypted_data[index : index + 2]
            value = int.from_bytes(bs, byteorder="little")
            
            result += value
            result %= 2**16 # 16-bit word
        
        # This new 16-bit value is the checksum.
        return result


class PokemonMenu(Menu):

    def build(self, pkmn: Pokemon):
        self.pkmn = pkmn

        self.set_title("Edit Pokemon")
        self.add_option(f"Nickname ({pkmn.get_nickname()})", self.edit_nickname)
        self.add_option(f"Species ({pkmn.get_species()})", self.edit_species)

    def close(self):
        self.pkmn.write_encrypted_data()
        self.pkmn.set_checksum()

    def select(self, selection):
        selection()

    def edit_nickname(self):
        new_name = input(f"Set nickname: ")
        if len(new_name) > 0:
            self.pkmn.set_nickname(new_name)

    def edit_species(self):
        print("Change species... use the decimal index number from the following link:")
        print("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_(Generation_III)")
        species = input(f"Species index number: ")
    
        if species:
            species_value = int(species)
            self.pkmn.set_species(species_value)
