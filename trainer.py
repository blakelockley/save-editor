RS_TRAINER_TABLE = {
    "PLAYER_NAME": 0x0000,  # 7
    "PLAYER_GENDER": 0x0008,  # 1
    "UNUSED_0": 0x0009,  # 1
    "TRAINER_ID": 0x000A,  # 4
    "TIME_PLAYED": 0x000E,  # 5
    "OPTIONS": 0x0013,  # 3
    "GAME_CODE": 0x00AC,  # 4
}

E_TRAINER_TABLE = {
    "PLAYER_NAME": 0x0000,  # 7
    "PLAYER_GENDER": 0x0008,  # 1
    "UNUSED_0": 0x0009,  # 1
    "TRAINER_ID": 0x000A,  # 4
    "TIME_PLAYED": 0x000E,  # 5
    "OPTIONS": 0x0013,  # 3
    "SECURITY_CODE": 0x00AC,  # 4
}

FRLG_TRAINER_TABLE = {
    "PLAYER_NAME": 0x0000,  # 7
    "PLAYER_GENDER": 0x0008,  # 1
    "UNUSED_0": 0x0009,  # 1
    "TRAINER_ID": 0x000A,  # 4
    "TIME_PLAYED": 0x000E,  # 5
    "OPTIONS": 0x0013,  # 3
    "GAME_CODE": 0x00AC,  # 4
    "SECURITY_CODE": 0x0AF8,  # 4
}

VERSION_TABLE = {
    "RS": RS_TRAINER_TABLE,
    "E": E_TRAINER_TABLE,
    "FRLG": FRLG_TRAINER_TABLE,
}

from menu import Menu
from encoding import CHAR_TO_BYTE, BYTE_TO_CHAR
import savefile


def print_trainer_summary():
    name = get_trainer_name()
    gender = get_trainer_gender()

    print("Trainer Name:", name + f" ({gender})")

    id = get_trainer_id()
    print("Trainer ID:", *id)


def get_trainer_name():
    offset_table = VERSION_TABLE[savefile.version]
    section_offset = savefile.section_table["TRAINER_INFO"]

    bs = savefile.bytes_at(section_offset + offset_table["PLAYER_NAME"], 7)

    chars = []
    for b in bs:  # Trim input to 7 bytes
        chars.append(BYTE_TO_CHAR[b])

    return "".join(chars)


def set_trainer_name(new_name):
    """
    String is trimmed to 7 characters.
    """

    bs = [0xFF for _ in range(7)]

    for i in range(len(new_name[:7])):
        bs[i] = CHAR_TO_BYTE[new_name[i]]

    offset = (
        savefile.section_table["TRAINER_INFO"]
        + VERSION_TABLE[savefile.version]["PLAYER_NAME"]
    )
    return savefile.set_bytes_at(offset, bs)


def get_trainer_gender():
    offset_table = VERSION_TABLE[savefile.version]
    section_offset = savefile.section_table["TRAINER_INFO"]

    b = savefile.bytes_at(section_offset + offset_table["PLAYER_GENDER"], 1)[0]

    return {0x00: "M", 0x01: "F"}[b]


def set_trainer_gender(value):
    """
    String is trimmed to 7 characters.
    """

    b = {"M": 0x00, "F": 0x01}[value]

    offset = (
        savefile.section_table["TRAINER_INFO"]
        + VERSION_TABLE[savefile.version]["PLAYER_GENDER"]
    )
    return savefile.set_bytes_at(offset, [b])


def get_trainer_id():
    offset_table = VERSION_TABLE[savefile.version]
    section_offset = savefile.section_table["TRAINER_INFO"]

    bs = savefile.bytes_at(section_offset + offset_table["TRAINER_ID"], 4)
    public_id = int.from_bytes(bs[0:2], "little")
    secret_id = int.from_bytes(bs[2:4], "little")

    return (public_id, secret_id)


def set_trainer_id(new_public_id, new_secret_id):
    offset_table = VERSION_TABLE[savefile.version]
    section_offset = savefile.section_table["TRAINER_INFO"]

    savefile.set_value_at(section_offset + offset_table["TRAINER_ID"], new_public_id, 2)
    savefile.set_value_at(
        section_offset + offset_table["TRAINER_ID"] + 2, new_secret_id, 2
    )

    return savefile.bytes_at(section_offset + offset_table["TRAINER_ID"], 4)


class TrainerMenu(Menu):
    def build(self):
        self.set_title("Edit Trainer?")
        self.add_option(f"Name ({get_trainer_name()})", self.edit_name)
        self.add_option(f"Gender ({get_trainer_gender()})", self.edit_gender)

        public_id, secret_id = get_trainer_id()
        self.add_option(f"ID ({public_id} {secret_id})", self.edit_id)

    def select(self, selection):
        selection()

    def edit_name(self):
        new_name = input(f"Set name: ")
        if len(new_name) > 0:
            set_trainer_name(new_name)

    def edit_gender(self):
        new_gender = input(f"Set gender M/F: ")
        if len(new_gender) > 0:
            set_trainer_gender(new_gender)

    def edit_id(self):
        new_id = input(f"Set ID: ")
        split_ids = new_id.split(" ")

        if len(split_ids) == 2:
            new_public_id = int(split_ids[0])
            new_secret_id = int(split_ids[1])

            set_trainer_id(new_public_id, new_secret_id)
