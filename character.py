from bitmaps import CHAR_MAPS_GENERATED


# Width of all characters in bits
CHAR_WIDTH_BITS = 12

# Height of all characters in bits
CHAR_HEIGHT_BITS = 12


# Maps a character code to a bitmap
EMPTY_CHAR = [[0 for _ in range(CHAR_WIDTH_BITS)] for _ in range(CHAR_HEIGHT_BITS)],

class Character:
    def __init__(self, code: int) -> None:
        self.code = code

    # Returns a bitmap of length CHAR_WIDTH_BITS
    def to_bits(self) -> list:
        if not self.code in CHAR_MAPS_GENERATED.keys():
            print(f"Warning: Unknown character code: {self.code}")
            return EMPTY_CHAR
        return CHAR_MAPS_GENERATED[self.code]

