from ast import literal_eval
from pathlib import Path

WIDTH = 12
HEIGHT = 12
OUT_FILE_PATH = "__init__.py"


def read_file(fname: str):
    if fname == " .c": fname = "SPACE.c"
    fname = "input/"+fname
    path = Path(fname)
    if not path.exists():
        # print(f"Missing File: {path}. Returning default!")
        return [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    with open(fname, 'r') as file:
        s = []
        read = False
        for line in file.readlines():
            if line.startswith("}"): 
                read = False
                print("Ending")

            if read: 
                l = literal_eval(f"[{line}]")
                s.append([1 if (pixel >> 24) & 0xff else 0 for pixel in l])

            if line.startswith("{"): 
                read = True
                print("Starting")
        print(f"s: {s}")
    return s



bitmaps = {}
for c in range(256):
    bitmaps[c] = read_file(f"{chr(c)}.c")

with open(OUT_FILE_PATH, "w") as f:
    f.truncate()
    f.write(f"CHAR_MAPS_GENERATED = {bitmaps}")



# print(f"Finished reading.\n\n\nBitmaps: {bitmaps}")
