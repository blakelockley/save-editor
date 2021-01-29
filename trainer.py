RS_TRAINER_TABLE = {
    "PLAYER_NAME":   0x0000, # 7
    "PLAYER_GENDER": 0x0008, # 1
    "UNUSED_0":      0x0009, # 1
    "TRAINER_ID":    0x000A, # 4
    "TIME_PLAYED":   0x000E, # 5
    "OPTIONS":       0x0013, # 3
    "GAME_CODE":     0x00AC, # 4
}

E_TRAINER_TABLE = {
    "PLAYER_NAME":   0x0000, # 7
    "PLAYER_GENDER": 0x0008, # 1
    "UNUSED_0":      0x0009, # 1
    "TRAINER_ID":    0x000A, # 4
    "TIME_PLAYED":   0x000E, # 5
    "OPTIONS":       0x0013, # 3
    "SECURITY_CODE": 0x00AC, # 4
}

FRLG_TRAINER_TABLE = {
    "PLAYER_NAME":   0x0000, # 7
    "PLAYER_GENDER": 0x0008, # 1
    "UNUSED_0":      0x0009, # 1
    "TRAINER_ID":    0x000A, # 4
    "TIME_PLAYED":   0x000E, # 5
    "OPTIONS":       0x0013, # 3
    "GAME_CODE":     0x00AC, # 4
    "SECURITY_CODE": 0x0AF8, # 4
}

VERSION_TABLE = {
    "RS": RS_TRAINER_TABLE,
    "E": E_TRAINER_TABLE,
    "FRLG": FRLG_TRAINER_TABLE,
}

from menu import Menu
from encoding import CHAR_TO_BYTE, BYTE_TO_CHAR
import savefile

def edit_name():
    new_name = input(f"Set name ({get_trainer_name()}): ")
    if len(new_name) > 0:
        print("Changing name to...", new_name)
        set_trainer_name(new_name)
        
def edit_gender():
    gender = get_trainer_gender()
    new_gender = input(f"Set gender M/F ({gender}): ")
    if len(new_gender) > 0:
        print("Changing gender to...", new_gender)
        set_trainer_gender(new_gender)
    
def edit_id():
    public_id, secret_id = get_trainer_id()

    new_id = input(f"Set ID SID ({public_id} {secret_id}): ")
    split_ids = new_id.split(" ")

    if len(split_ids) == 2:
        new_public_id = int(split_ids[0])
        new_secret_id = int(split_ids[1])
        
        print("Changing ID SID to...", new_public_id, new_secret_id)
        set_trainer_id(new_public_id, new_secret_id)


def print_trainer_summary():
    name = get_trainer_name()
    gender = get_trainer_gender()
    
    print("Trainer Name:", name + f" ({gender})")
    
    id = get_trainer_id()
    print("Trainer ID:", id)


def get_trainer_name():
    offset_table = VERSION_TABLE[savefile.version]
    section_offset = savefile.section_table["TRAINER_INFO"]

    bs = savefile.bytes_at(section_offset + offset_table["PLAYER_NAME"], 7)
    
    chars = []
    for b in bs: # Trim input to 7 bytes
        chars.append(BYTE_TO_CHAR[b])

    return "".join(chars)


def set_trainer_name(str):
    """
    String is trimmed to 7 characters.
    """

    bs = [0xFF for _ in range(7)]
    
    for i in range(len(str[:7])):
        bs[i] = CHAR_TO_BYTE[str[i]]

    offset = savefile.section_table["TRAINER_INFO"] + VERSION_TABLE[savefile.version]["PLAYER_NAME"]
    return savefile.set_bytes_at(offset, bs)


def get_trainer_gender():
    offset_table = VERSION_TABLE[savefile.version]
    section_offset = savefile.section_table["TRAINER_INFO"]

    b = savefile.bytes_at(section_offset + offset_table["PLAYER_GENDER"], 1)[0]

    return { 0x00: "M", 0x01: "F" }[b]


def set_trainer_gender(value):
    """
    String is trimmed to 7 characters.
    """

    b = { "M": 0x00, "F": 0x01 }[value]

    offset = savefile.section_table["TRAINER_INFO"] + VERSION_TABLE[savefile.version]["PLAYER_GENDER"]
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
    savefile.set_value_at(section_offset + offset_table["TRAINER_ID"] + 2, new_secret_id, 2)

    return savefile.bytes_at(section_offset + offset_table["TRAINER_ID"], 4)


trainer_menu = Menu("Edit trainer data?")
trainer_menu.add_option(f"Name", edit_name)
trainer_menu.add_option(f"Gender", edit_gender)
trainer_menu.add_option(f"ID SID", edit_id)