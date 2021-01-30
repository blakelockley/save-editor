import random

import savefile
from lookups import SPECIES_LOOKUP
from pokemon import Pokemon
from trainer import get_trainer_id, get_trainer_name

DEFAULT_EXPEREINCE = 200_000
DEFAULT_FRIENDSHIP = 100


class PokemonMaker:
    def __init__(self, offset):
        self.offset = offset

    def run(self):
        print("Create new Pokemon")

        # Clear data
        bs = [0xFF for _ in range(80)]
        savefile.set_bytes_at(self.offset, bs)

        self.pkmn = Pokemon(offset=self.offset)
        personality = random.randint(0, 2 ** 32 - 1)
        self.pkmn.set_personality_value(personality)
        self.pkmn.set_ot_id(*get_trainer_id())
        self.pkmn.set_ot_name(get_trainer_name())
        self.pkmn.set_language()
        self.pkmn.set_markings()
        self.pkmn.decrypt()

        print("Set species... use the decimal index number from the following link:")
        print(
            "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_(Generation_III)"
        )

        species = input(f"Species index number: ")
        species_value = int(species)
        self.pkmn.set_species(species_value)

        species_name = SPECIES_LOOKUP[species_value]
        print(f"Creating new Pokemon as: {species_name}")

        nickname = species_name.upper()
        self.pkmn.set_nickname(nickname)

        self.pkmn.set_item()
        self.pkmn.set_experience(DEFAULT_EXPEREINCE)
        self.pkmn.set_pp_bonuses()
        self.pkmn.set_friendship(DEFAULT_FRIENDSHIP)

        self.pkmn.set_move(1, 92)  # Toxic
        self.pkmn.set_move(2, 0)
        self.pkmn.set_move(3, 0)
        self.pkmn.set_move(4, 0)

        self.pkmn.set_pp(1, 5)
        self.pkmn.set_pp(2, 0)
        self.pkmn.set_pp(3, 0)
        self.pkmn.set_pp(4, 0)

        self.pkmn.set_ev_hp(0)
        self.pkmn.set_ev_attack(0)
        self.pkmn.set_ev_defense(0)
        self.pkmn.set_ev_speed(0)
        self.pkmn.set_ev_sp_attack(0)
        self.pkmn.set_ev_sp_defense(0)

        self.pkmn.set_coolness(0)
        self.pkmn.set_beauty(0)
        self.pkmn.set_cuteness(0)
        self.pkmn.set_smartness(0)
        self.pkmn.set_toughness(0)
        self.pkmn.set_feel(0)

        self.pkmn.set_coolness(0)
        self.pkmn.set_beauty(0)
        self.pkmn.set_cuteness(0)
        self.pkmn.set_smartness(0)
        self.pkmn.set_toughness(0)
        self.pkmn.set_feel(0)

        self.pkmn.set_pokerus_status(0)
        self.pkmn.set_met_location(255)  # Fateful encounter
        self.pkmn.set_origins_info(0b0010_0000_1000_0001)
        self.pkmn.set_iv(0)
        self.pkmn.set_ribbons(0)

        self.pkmn.write_encrypted_data()
        self.pkmn.set_checksum()

        input()
