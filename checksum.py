TOTAL_SIZE = 0x20000

SAVE_A_OFFEST = 0x000000
SAVE_B_OFFEST = 0x006000

SECTION_SIZE = 0x1000
SECTION_ID = 0x0FF4
SECTION_CHECKSUM = 0x0FF6

SECTION_TABLE = {
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

data = None

def main(args):
    global data
    
    filename = args[1]

    with open(filename, "rb") as f:
        data = bytearray(f.read())
    
    offset = SAVE_A_OFFEST
    while offset < TOTAL_SIZE:        
        print("0x" + hex(offset)[2:].zfill(6), end="  ")
        printb(offset + SECTION_ID, end="  ")

        current = value_at(offset + SECTION_CHECKSUM, 2)
        checksum = calculate_checksum(offset)

        print(str(current).zfill(8), end="  ")
        print(str(checksum).zfill(8), end="  ")

        match = (current == checksum)
        print("CORRECT" if match else "INCORRECT")
         
        if not match:
            print("Correcting...")
            write_at(offset + SECTION_CHECKSUM, checksum, 2)
        
        offset += SECTION_SIZE

    with open(filename, "wb") as f:
        f.write(data)


def value_at(offset, n=1, *, signed=False):
    """
    Read n number of bytes as int value.
    """
    bs = data[offset : offset + n]
    return int.from_bytes(bs, byteorder="little", signed=signed)


def write_at(offset, value, n=1):
    """
    Read n number of bytes as int value.
    """

    bs = value.to_bytes(n, byteorder="little",)
    for index in range(n):
        data[offset + index] = bs[index]


def calculate_checksum(offset):
    """
    https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_in_Generation_III#Checksum
    """

    # The number of bytes to process in this manner is determined by Section ID.
    size = SECTION_TABLE.get(data[offset + SECTION_ID], 0)
    
    # Initialize a 32-bit checksum variable to zero.
    result = 0

    # Read 4 bytes at a time as 32-bit word (little-endian) and add it to the variable.    
    for index in range(offset, offset + size, 4):
        result = result + value_at(index, 4)
        result %= 2**32 # 32-bit word

    # Take the upper 16 bits of the result, and add them to the lower 16 bits of the result.
    result = result // 2**16 + result % 2**16

    # This new 16-bit value is the checksum.
    return result % 2**16


def printb(offset, size=1, *, end="\n"):
    for pos in range(offset, offset + size):
        b = hex(data[pos])[2:].zfill(2).upper()
        print(b, end=" ")

    print(end=end)


if __name__ == "__main__":
    import sys
    main(sys.argv)