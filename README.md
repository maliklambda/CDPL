# CDPL
Character DisPLay Program.

## How To
Use `$ python3 main.py` to run the program. You should see a window pop up. At this point, you can start typing.

### Custom Character Set
To include your own custom characters, you have to provide the corresponding bitmap.
You can go to [piskellapp](https://www.piskelapp.com/p/create/sprite/) and create a sprite with the dimensions width = CHAR_WIDTH_BITS and height = CHAR_HEIGHT_BITS. 
(Note that there are WIDTH and HEIGHT properties in generate_char_maps.py. Those need to match the dimensions!)
Click on the right side to export the sprite as a C-File. Make sure you give the file the expected name and save it in the `bitmaps/input/` folder.
After that, you need to generate the correct bitmap, which is done with `$ cd bitmaps; python3 generate_char_maps.py`.


