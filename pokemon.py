POKEMON_TABLE = {
    "PERSONALITY_VALUE": 0x0000,  # 4
    "OT_ID": 0x0004,  # 4
    "NICKNAME": 0x0008,  # 10
    "LANGUAGE": 0x0012,  # 2
    "OT_NAME": 0x0014,  # 7
    "MARKINGS": 0x001B,  # 1
    "CHECKSUM": 0x001C,  # 2
    "UNUSED_0": 0x001E,  # 2
    "DATA": 0x0020,  # 48
    # In-team data
    "STATUS": 0x0050,  # 2
    "LEVEL": 0x0054,  # 1
    "POKERUS_REMAINING": 0x0055,  # 1
    "CURRENT_HP": 0x0056,  # 2
    "TOTAL_HP": 0x0058,  # 2
    "ATTACK": 0x005A,  # 2
    "DEFENSE": 0x005C,  # 2
    "SPEED": 0x005E,  # 2
    "SP_ATTACK": 0x0060,  # 2
    "SP_DEFENSE": 0x0062,  # 2
}

GROWTH_TABLE = {
    "SPECIES": 0x0000,  # 2
    "ITEM": 0x0002,  # 2
    "EXPERIENCE": 0x0004,  # 4
    "PP_BONUSES": 0x0008,  # 1
    "FRIENDSHIP": 0x0009,  # 1
    "UNUSED_0": 0x000A,  # 2
}

ATTACKS_TABLE = {
    "MOVE_1": 0x0000,  # 2
    "MOVE_2": 0x0002,  # 2
    "MOVE_3": 0x0004,  # 2
    "MOVE_4": 0x0006,  # 2
    "PP_1": 0x0008,  # 1
    "PP_2": 0x0009,  # 1
    "PP_3": 0x000A,  # 1
    "PP_4": 0x000B,  # 1
}

EV_CONDITIONS_TABLE = {
    "HP_EV": 0x0000,  # 1
    "ATTACK_EV": 0x0001,  # 1
    "DEFENSE_EV": 0x0002,  # 1
    "SPEED_EV": 0x0003,  # 1
    "SP_ATTACK_EV": 0x0004,  # 1
    "SP_DEFENSE_EV": 0x0005,  # 1
    "COOLNESS": 0x0006,  # 1
    "BEAUTY": 0x0007,  # 1
    "CUTENESS": 0x0008,  # 1
    "SMARTNESS": 0x0009,  # 1
    "TOUGHNESS": 0x000A,  # 1
    "FEEL": 0x000B,  # 1
}

MISC_TABLE = {
    "POKERUS_STATUS": 0x0000,  # 1
    "MET_LOCATION": 0x0001,  # 1
    "ORIGINS_INFO": 0x0002,  # 2
    "IV_EGGS_ABILITY": 0x0004,  # 4
    "RIBBONS_OBEDIENCE": 0x0008,  # 4
}

DATA_TABLE_MAP = {
    "GROWTH": GROWTH_TABLE,
    "ATTACKS": ATTACKS_TABLE,
    "EV_CONDITIONS": EV_CONDITIONS_TABLE,
    "MISC": MISC_TABLE,
}

DATA_ORDER_MAP = [  # 24
    ["GROWTH", "ATTACKS", "EV_CONDITIONS", "MISC"],
    ["GROWTH", "ATTACKS", "MISC", "EV_CONDITIONS"],
    ["GROWTH", "EV_CONDITIONS", "ATTACKS", "MISC"],
    ["GROWTH", "EV_CONDITIONS", "MISC", "ATTACKS"],
    ["GROWTH", "MISC", "ATTACKS", "EV_CONDITIONS"],
    ["GROWTH", "MISC", "EV_CONDITIONS", "ATTACKS"],
    ["ATTACKS", "GROWTH", "EV_CONDITIONS", "MISC"],
    ["ATTACKS", "GROWTH", "MISC", "EV_CONDITIONS"],
    ["ATTACKS", "EV_CONDITIONS", "GROWTH", "MISC"],
    ["ATTACKS", "EV_CONDITIONS", "MISC", "GROWTH"],
    ["ATTACKS", "MISC", "GROWTH", "EV_CONDITIONS"],
    ["ATTACKS", "MISC", "EV_CONDITIONS", "GROWTH"],
    ["EV_CONDITIONS", "GROWTH", "ATTACKS", "MISC"],
    ["EV_CONDITIONS", "GROWTH", "MISC", "ATTACKS"],
    ["EV_CONDITIONS", "ATTACKS", "GROWTH", "MISC"],
    ["EV_CONDITIONS", "ATTACKS", "MISC", "GROWTH"],
    ["EV_CONDITIONS", "MISC", "GROWTH", "ATTACKS"],
    ["EV_CONDITIONS", "MISC", "ATTACKS", "GROWTH"],
    ["MISC", "GROWTH", "ATTACKS", "EV_CONDITIONS"],
    ["MISC", "GROWTH", "EV_CONDITIONS", "ATTACKS"],
    ["MISC", "ATTACKS", "GROWTH", "EV_CONDITIONS"],
    ["MISC", "ATTACKS", "EV_CONDITIONS", "GROWTH"],
    ["MISC", "EV_CONDITIONS", "GROWTH", "ATTACKS"],
    ["MISC", "EV_CONDITIONS", "ATTACKS", "GROWTH"],
]

import savefile
from encoding import BYTE_TO_CHAR, CHAR_TO_BYTE
from lookups import LANGUAGE_LOOKUP, SPECIES_LOOKUP
from menu import Menu


def set_bit(value, bit):
    return value | (1 << (bit - 1))


def clear_bit(value, bit):
    return value & ~(1 << (bit - 1))


class Pokemon:
    def __init__(self, offset):
        self.offset = offset
        self.decrypt()

    def __str__(self):
        if self.is_valid:
            return f"{self.get_nickname()} ({self.get_species()})"
        return "---"

    # Decryption

    def decrypt(self):
        self.data_table = self.get_data_table()
        self.decryption_key = self.get_decryption_key()
        self.decrypted_data = self.get_decrypted_data()

        self.is_valid = self.check_validity()

    def get_data_table(self):
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

    def check_validity(self):
        bs = savefile.bytes_at(self.offset + POKEMON_TABLE["DATA"], 48)
        return any(bs)

    # Encapsulating data fields

    def set_personality_value(self, value):
        savefile.set_value_at(
            self.offset + POKEMON_TABLE["PERSONALITY_VALUE"], value, 4
        )

    def set_ot_id(self, new_public_id, new_secret_id):
        offset = self.offset + POKEMON_TABLE["OT_ID"]

        savefile.set_value_at(offset, new_public_id, 2)
        savefile.set_value_at(offset + 2, new_secret_id, 2)

    def get_ot_name(self):
        bs = savefile.bytes_at(self.offset + POKEMON_TABLE["OT_NAME"], 7)

        chars = []
        for b in bs:
            if b == 255:
                break
            chars.append(BYTE_TO_CHAR.get(b, "?"))

        return "".join(chars)

    def set_ot_name(self, new_name):
        bs = [0xFF for _ in range(7)]

        for i in range(len(new_name[:7])):
            bs[i] = CHAR_TO_BYTE[new_name[i]]

        offset = self.offset + POKEMON_TABLE["OT_NAME"]
        return savefile.set_bytes_at(offset, bs)

    def get_nickname(self):
        bs = savefile.bytes_at(self.offset + POKEMON_TABLE["NICKNAME"], 10)

        chars = []
        for b in bs:
            if b == 255:
                break
            chars.append(BYTE_TO_CHAR.get(b, "?"))

        return "".join(chars)

    def set_nickname(self, new_name):
        bs = [0xFF for _ in range(10)]

        for i in range(len(new_name[:10])):
            bs[i] = CHAR_TO_BYTE[new_name[i]]

        offset = self.offset + POKEMON_TABLE["NICKNAME"]
        return savefile.set_bytes_at(offset, bs)

    def set_language(self, language="ENGLISH"):
        value = LANGUAGE_LOOKUP[language]

        offset = self.offset + POKEMON_TABLE["LANGUAGE"]
        return savefile.set_value_at(offset, value, 2)

    def set_markings(self, value=0):
        offset = self.offset + POKEMON_TABLE["MARKINGS"]
        return savefile.set_value_at(offset, value)

    # Data operations

    def get_data_bytes(self, table, offset, n=1):
        offset = self.data_table[table] + DATA_TABLE_MAP[table][offset]
        return self.decrypted_data[offset : offset + n]

    def set_data_bytes(self, table, offset, bs):
        offset = self.data_table[table] + DATA_TABLE_MAP[table][offset]
        for index in range(len(bs)):
            self.decrypted_data[offset + index] = bs[index]

    def get_data_value(self, table, offset, n=1):
        bs = self.get_data_bytes(table, offset, n)
        return int.from_bytes(bs, "little")

    def set_data_value(self, table, offset, value, n):
        bs = value.to_bytes(n, "little")
        self.set_data_bytes(table, offset, bs)

    # Data fields

    # Growth

    def get_species(self):
        value = self.get_data_value("GROWTH", "SPECIES", 2)
        return SPECIES_LOOKUP[value]

    def set_species(self, value):
        return self.set_data_value("GROWTH", "SPECIES", value, 2)

    def get_item(self):
        return self.get_data_value("GROWTH", "ITEM", 2)

    def set_item(self, value=0):
        return self.set_data_value("GROWTH", "ITEM", value, 2)

    def get_experience(self):
        return self.get_data_value("GROWTH", "EXPERIENCE", 4)

    def set_experience(self, value=0):
        return self.set_data_value("GROWTH", "EXPERIENCE", value, 4)

    def get_pp_bonuses(self):
        return self.get_data_value("GROWTH", "PP_BONUSES", 1)

    def set_pp_bonuses(self, value=0):
        return self.set_data_value("GROWTH", "PP_BONUSES", value, 1)

    def get_friendship(self):
        return self.get_data_value("GROWTH", "FRIENDSHIP", 1)

    def set_friendship(self, value=0):
        return self.set_data_value("GROWTH", "FRIENDSHIP", value, 1)

    # Attacks

    def get_move(self, move):
        return self.get_data_value("ATTACKS", f"MOVE_{move}", 2)

    def set_move(self, move, attack_index):
        return self.set_data_value("ATTACKS", f"MOVE_{move}", attack_index, 2)

    def get_pp(self, move):
        return self.get_data_value("ATTACKS", f"PP_{move}", 1)

    def set_pp(self, move, pp=5):
        return self.set_data_value("ATTACKS", f"PP_{move}", pp, 1)

    # EV & Condition

    # EV

    def get_ev_hp(self):
        return self.get_data_value("EV_CONDITIONS", "HP_EV", 1)

    def set_ev_hp(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "HP_EV", value, 1)

    def get_ev_attack(self):
        return self.get_data_value("EV_CONDITIONS", "ATTACK_EV", 1)

    def set_ev_attack(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "ATTACK_EV", value, 1)

    def get_ev_defense(self):
        return self.get_data_value("EV_CONDITIONS", "DEFENSE_EV", 1)

    def set_ev_defense(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "DEFENSE_EV", value, 1)

    def get_ev_speed(self):
        return self.get_data_value("EV_CONDITIONS", "SPEED_EV", 1)

    def set_ev_speed(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "SPEED_EV", value, 1)

    def get_ev_sp_attack(self):
        return self.get_data_value("EV_CONDITIONS", "SP_ATTACK_EV", 1)

    def set_ev_sp_attack(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "SP_ATTACK_EV", value, 1)

    def get_ev_sp_defense(self):
        return self.get_data_value("EV_CONDITIONS", "SP_DEFENSE_EV", 1)

    def set_ev_sp_defense(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "SP_DEFENSE_EV", value, 1)

    # Conditions

    def get_coolness(self):
        return self.get_data_value("EV_CONDITIONS", "COOLNESS", 1)

    def set_coolness(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "COOLNESS", value, 1)

    def get_beauty(self):
        return self.get_data_value("EV_CONDITIONS", "BEAUTY", 1)

    def set_beauty(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "BEAUTY", value, 1)

    def get_cuteness(self):
        return self.get_data_value("EV_CONDITIONS", "CUTENESS", 1)

    def set_cuteness(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "CUTENESS", value, 1)

    def get_smartness(self):
        return self.get_data_value("EV_CONDITIONS", "SMARTNESS", 1)

    def set_smartness(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "SMARTNESS", value, 1)

    def get_toughness(self):
        return self.get_data_value("EV_CONDITIONS", "TOUGHNESS", 1)

    def set_toughness(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "TOUGHNESS", value, 1)

    def get_feel(self):
        return self.get_data_value("EV_CONDITIONS", "FEEL", 1)

    def set_feel(self, value=0):
        return self.set_data_value("EV_CONDITIONS", "FEEL", value, 1)

    # Miscellaneous

    def get_pokerus_status(self):
        return self.get_data_value("MISC", "POKERUS_STATUS", 1)

    def set_pokerus_status(self, value=0):
        return self.set_data_value("MISC", "POKERUS_STATUS", value, 1)

    def get_met_location(self):
        return self.get_data_value("MISC", "MET_LOCATION", 1)

    def set_met_location(self, value=0):
        return self.set_data_value("MISC", "MET_LOCATION", value, 1)

    def get_origins_info(self):
        return self.get_data_value("MISC", "ORIGINS_INFO", 2)

    def set_origins_info(self, value=0):
        return self.set_data_value("MISC", "ORIGINS_INFO", value, 2)

    def get_iv(self):
        return self.get_data_value("MISC", "IV_EGGS_ABILITY", 4)

    def set_iv(self, value=0):
        return self.set_data_value("MISC", "IV_EGGS_ABILITY", value, 4)

    def get_egg(self):
        return self.get_data_value("MISC", "IV_EGGS_ABILITY", 4)

    def set_egg(self, value=0):
        return self.set_data_value("MISC", "IV_EGGS_ABILITY", value, 4)

    def get_ability(self):
        return self.get_data_value("MISC", "IV_EGGS_ABILITY", 4)

    def set_ability(self, value=0):
        return self.set_data_value("MISC", "IV_EGGS_ABILITY", value, 4)

    def get_ribbons(self):
        return self.get_data_value("MISC", "RIBBONS_OBEDIENCE", 4)

    def set_ribbons(self, value=0):
        return self.set_data_value("MISC", "RIBBONS_OBEDIENCE", value, 4)

    # Checksum

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
            result %= 2 ** 16  # 16-bit word

        # This new 16-bit value is the checksum.
        return result


class PokemonMenu(Menu):
    def build(self, pkmn: Pokemon):
        self.pkmn = pkmn

        self.set_title("Edit Pokemon")
        self.add_option(f"Nickname ({pkmn.get_nickname()})", self.edit_nickname)
        self.add_option(f"Species ({pkmn.get_species()})", self.edit_species)
        self.add_option(f"EXP ({pkmn.get_experience()})", self.edit_experience)
        self.add_option(f"Oringal Trainer ({pkmn.get_ot_name()})", self.edit_ot)

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
        print(
            "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_(Generation_III)"
        )
        species = input(f"Species index number: ")

        if species:
            species_value = int(species)
            self.pkmn.set_species(species_value)

    def edit_experience(self):
        new_exp = input(f"Set EXP: ")
        if len(new_exp) > 0:
            self.pkmn.set_experience(int(new_exp))

    def edit_ot(self):
        new_name = input(f"OT Name: ")
        if len(new_name) > 0:
            self.pkmn.set_ot_name(new_name)

        ot_gender = input(f"OT Gender (M)/F: ")
        origins = self.pkmn.get_origins_info()

        if ot_gender == "F":
            origins = set_bit(origins, 16)
        else:
            origins = clear_bit(origins, 16)

        self.pkmn.set_origins_info(origins)
