import sdl2
import ctypes
import sys

from character import Character
from screen import Screen


def init_window(width: int, height: int, scale: int):

    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print("SDL_Init failed:", sdl2.SDL_GetError().decode())
        sys.exit(1)

    window = sdl2.SDL_CreateWindow(
        b"My SDL2 Window",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        height*scale,
        width*scale,
        sdl2.SDL_WINDOW_SHOWN,
    )

    if not window:
        print("SDL_CreateWindow failed:", sdl2.SDL_GetError().decode())
        sdl2.SDL_Quit()
        sys.exit(1)

    renderer = sdl2.SDL_CreateRenderer(
        window, -1, sdl2.SDL_RENDERER_ACCELERATED
    )

    if not renderer:
        print("SDL_CreateRenderer failed:", sdl2.SDL_GetError().decode())
        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()
        sys.exit(1)

    return (window, renderer)


def handle_char_input(renderer: sdl2.SDL_Renderer, screen: Screen, event: sdl2.SDL_Event) -> Character | None:
    typed_text = ""
    if event.type == sdl2.SDL_KEYDOWN:
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            running = False
        if event.key.keysym.sym == sdl2.SDLK_BACKSPACE:
            screen.remove_latest_char()
            render_bitmap(screen.buffer, renderer)
            return None
        if event.key.keysym.sym == sdl2.SDLK_RETURN:
            screen._wrap_around_newline()
            render_bitmap(screen.buffer, renderer)
            return None
        # For a one-time action, ignore held-key repeat events:
        elif not event.key.repeat:
            print("Key pressed:", sdl2.SDL_GetKeyName(
                event.key.keysym.sym
            ).decode())

    elif event.type == sdl2.SDL_TEXTINPUT:
        # SDL text input is UTF-8; the field is a null-terminated byte array.
        text = bytes(event.text.text).split(b"\0", 1)[0].decode("ascii")
        typed_text += text
        print("Typed:", text)
        assert len(text) == 1, "Too long text"
        return Character(ord(text[0]))




def render_bitmap(bitmap, renderer):
    print("Rendering bitmap...")
    height = len(bitmap)
    width = len(bitmap[0])

    if height == 0 or width == 0 or any(len(row) != width for row in bitmap):
        raise ValueError("bitmap must be a non-empty rectangular list")

    # Convert each 0/1 pixel to opaque black/white RGBA.
    pixels = bytearray()
    for row in bitmap:
        for value in row:
            shade = 255 if value else 0
            pixels.extend((shade, shade, shade, 255))

    texture = sdl2.SDL_CreateTexture(
        renderer,
        sdl2.SDL_PIXELFORMAT_RGBA32,
        sdl2.SDL_TEXTUREACCESS_STATIC,
        width,
        height,
    )
    if not texture:
        raise RuntimeError(sdl2.SDL_GetError().decode())

    pixel_array = (ctypes.c_uint8 * len(pixels)).from_buffer(pixels)
    result = sdl2.SDL_UpdateTexture(texture, None, pixel_array, width * 4)
    if result != 0:
        sdl2.SDL_DestroyTexture(texture)
        raise RuntimeError(sdl2.SDL_GetError().decode())

    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_RenderCopy(renderer, texture, None, None)  # scales to window size
    sdl2.SDL_RenderPresent(renderer)

    sdl2.SDL_DestroyTexture(texture)
