
TOTAL_SIZE   = 0x20000

SAVE_A_OFFEST = 0x000000
SAVE_B_OFFEST = 0x00E000

SECTION_SIZE  = 0x01000
SECTION_COUNT = 14

SECTION_ID         = 0x0FF4 # 2
SECTION_CHECKSUM   = 0x0FF6 # 2
SECTION_SAVE_INDEX = 0x0FFC # 4

SECTION_NAME_TABLE = {
    0:	"TRAINER_INFO",
    1:	"TEAM_ITEMS",
    2:	"GAME_STATE",
    3:	"MISC_DATA",
    4:	"RIVAL_INFO",
    5:	"PC_BUFFER_A",
    6:	"PC_BUFFER_B",
    7:	"PC_BUFFER_C",
    8:	"PC_BUFFER_D",
    9:	"PC_BUFFER_E",
    10:	"PC_BUFFER_F",
    11:	"PC_BUFFER_G",
    12:	"PC_BUFFER_H",
    13:	"PC_BUFFER_I",
}

SECTION_SIZE_TABLE = {
    0:	3884,   # Trainer info
    1:	3968,   # Team / items
    2:	3968,   # Game State
    3:	3968,   # Misc Data
    4:	3848,   # Rival info
    5:	3968,   # PC buffer A
    6:	3968,   # PC buffer B
    7:	3968,   # PC buffer C
    8:	3968,   # PC buffer D
    9:	3968,   # PC buffer E
    10:	3968,   # PC buffer F
    11:	3968,   # PC buffer G
    12:	3968,   # PC buffer H
    13:	2000,   # PC buffer I
}