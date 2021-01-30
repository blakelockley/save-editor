from offsets import *

version = None
data = None
save_offset = None
section_table = None


VERSION_NAMES = {
    "R": "RS",
    "S": "RS",
    "RS": "RS",
    "RUBY": "RS",
    "SAPHIRE": "RS",
    "FR": "FRLG",
    "LG": "FRLG",
    "FIRE_RED": "FRLG",
    "LEAF_GREEN": "FRLG",
    "E": "E",
    "EMERALD": "E",
}


def bytes_at(offset, n):
    """
    Read n number of bytes as int value.
    """
    return data[offset : offset + n]


def value_at(offset, n=1, *, signed=False):
    """
    Read n number of bytes as int value.
    """

    bs = bytes_at(offset, n)
    return int.from_bytes(bs, byteorder="little", signed=signed)


def set_bytes_at(offset, bytes):
    """
    Write n number of bytes to offset.
    """

    for index in range(len(bytes)):
        data[offset + index] = bytes[index]


def set_value_at(offset, value, n=1):
    """
    Write n number of bytes to offset.
    """

    bs = value.to_bytes(n, byteorder="little")
    set_bytes_at(offset, bs)


def printb(offset, size=1, *, end="\n"):
    for pos in range(offset, offset + size):
        b = hex(data[pos])[2:].zfill(2).upper()
        print(b, end=" ")

    print(end=end)


def set_version(value):
    global version
    version = VERSION_NAMES[value]


def load(filename):
    global data

    with open(filename, "rb") as f:
        data = bytearray(f.read())

    set_save_offset()
    set_section_table()


def write(filename):
    evaluate_checksums()

    with open(filename, "wb") as f:
        f.write(data)


def set_save_offset():
    global save_offset

    save_index_a = value_at(SAVE_A_OFFEST + SECTION_SAVE_INDEX, 4)
    save_index_b = value_at(SAVE_B_OFFEST + SECTION_SAVE_INDEX, 4)

    active_save = "A" if save_index_a > save_index_b else "B"
    print("Active save:", active_save)

    offset_map = {"A": SAVE_A_OFFEST, "B": SAVE_B_OFFEST}
    save_offset = offset_map[active_save]


def set_section_table():
    global section_table
    section_table = {}

    offset = save_offset
    for _ in range(SECTION_COUNT):
        section_id = value_at(offset + SECTION_ID)
        section_table[SECTION_NAME_TABLE[section_id]] = offset

        offset += SECTION_SIZE


def calculate_checksum(offset):
    """
    https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_in_Generation_III#Checksum
    """

    # The number of bytes to process in this manner is determined by Section ID.
    # size
    size = SECTION_SIZE_TABLE.get(data[offset + SECTION_ID], 0)

    # Initialize a 32-bit checksum variable to zero.
    result = 0

    # Read 4 bytes at a time as 32-bit word (little-endian) and add it to the variable.
    for index in range(offset, offset + size, 4):
        result = result + value_at(index, 4)
        result %= 2 ** 32  # 32-bit word

    # Take the upper 16 bits of the result, and add them to the lower 16 bits of the result.
    result = result // 2 ** 16 + result % 2 ** 16

    # This new 16-bit value is the checksum.
    return result % 2 ** 16


def evaluate_checksums():
    offset = SAVE_A_OFFEST

    while offset < TOTAL_SIZE:
        current = value_at(offset + SECTION_CHECKSUM, 2)
        checksum = calculate_checksum(offset)

        match = current == checksum
        if not match:
            print("Correcting checksum for section...", "0x" + hex(offset)[2:].zfill(6))
            set_value_at(offset + SECTION_CHECKSUM, checksum, 2)

        offset += SECTION_SIZE
