from screen import BUF_HEIGHT, BUF_WIDTH, Screen
from window import init_window, handle_char_input, render_bitmap
import sdl2

SCALE = 5
screen = Screen()
window, renderer = init_window(BUF_WIDTH, BUF_HEIGHT, SCALE)

running = True
event = sdl2.SDL_Event()

while running:
    while sdl2.SDL_PollEvent(event):
        if event.type == sdl2.SDL_QUIT:
            running = False
        else:
            c = handle_char_input(renderer, screen, event)
            if c: 
                print(f"Character input: {c.code}")
                screen.append_char(c)
                render_bitmap(screen.buffer, renderer)

sdl2.SDL_DestroyRenderer(renderer)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()
