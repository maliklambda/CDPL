import sys
from character import CHAR_HEIGHT_BITS, CHAR_WIDTH_BITS, Character

BUF_WIDTH = 200
BUF_HEIGHT = 200

class Screen:
    def __init__(self) -> None:
        self.buffer = [[0 for _ in range(BUF_WIDTH)] for _ in range(BUF_HEIGHT)]
        self.current_y = 0
        self.current_x = 0
        self.idx_latest_chars = [] # hold index of latest character per line -> revert-newline

    def clear(self):
        self.buffer = [[0* BUF_WIDTH] * BUF_HEIGHT]

    # Appends a character to the current buffer.
    def append_char(self, char: Character):
        print(f"Appending char: {char}")
        if (BUF_WIDTH - self.current_x) <= CHAR_WIDTH_BITS: self._wrap_around_newline()
        self.set_current_char_inline(char)

    # Sets the current character in this line.
    # Wrap around to newline should be done outside.
    def set_current_char_inline(self, char: Character):
        print(f"BW:{BUF_WIDTH} - CX:{self.current_x} - CWB:{CHAR_WIDTH_BITS}")
        assert (BUF_WIDTH - self.current_x) > CHAR_WIDTH_BITS, "Not enough room for char setting."
        self._set_char(char, self.current_x, self.current_y)
        self.current_x += CHAR_WIDTH_BITS

    # Sets a character at a 
    def _set_char(self, char: Character, x: int, y: int):
        print(f"Setting char {char} @({x}, {y})")
        assert x < BUF_WIDTH and y < BUF_HEIGHT
        bits = char.to_bits()
        print(f"Bits: {bits}")
        for row in range(CHAR_HEIGHT_BITS):
            self.buffer[y+row][x:x+CHAR_WIDTH_BITS] = bits[row]

    def remove_latest_char(self):
        print("Removing latest character")
        if self.current_x < CHAR_WIDTH_BITS:
            self._revert_newline()
            # sys.exit("TODO: revert newline")
        else:
            self.current_x -= CHAR_WIDTH_BITS
        self._set_char(Character(ord(" ")), self.current_x, self.current_y)

    def _wrap_around_newline(self):
        print("Wrapping around to newline.")
        if self.current_y + CHAR_HEIGHT_BITS >= BUF_HEIGHT:
            sys.exit("TODO: Scroll")
        else: 
            self.idx_latest_chars.append(self.current_x)
            self.current_y += CHAR_HEIGHT_BITS
            self.current_x = 0


    def _revert_newline(self):
        if len(self.idx_latest_chars) > 0: self.current_x = self.idx_latest_chars.pop()
        else: self.current_x = 0
        if self.current_y > 0:
            self.current_y -= CHAR_HEIGHT_BITS


