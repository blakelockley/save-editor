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

from encoding import CHAR_TO_BYTE, BYTE_TO_CHAR
import savefile


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

