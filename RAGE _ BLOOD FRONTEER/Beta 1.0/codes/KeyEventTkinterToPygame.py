import pygame
import tkinter as tk
import os
import threading
from pygame.locals import *
from collections import defaultdict

# 키 상태를 추적하는 defaultdict
key_state = defaultdict(lambda: False)

def add_key_event_from_tk_to_pygame(root, pygame_in_game):
    global pygame
    pygame = pygame_in_game
    root.bind('<KeyPress>', handle_tkinter_keypress)
    root.bind('<KeyRelease>', handle_tkinter_keyrelease)
    pygame.key.get_pressed = custom_get_pressed

def handle_tkinter_keypress(event):
    pygame_key = convert_tkinter_key_to_pygame(event.keysym)
    if pygame_key is not None:
        key_state[pygame_key] = True  # 키를 눌렀다고 상태 변경
        pygame_event = pygame.event.Event(KEYDOWN, key=pygame_key)
        pygame.event.post(pygame_event)

def handle_tkinter_keyrelease(event):
    pygame_key = convert_tkinter_key_to_pygame(event.keysym)
    if pygame_key is not None:
        key_state[pygame_key] = False  # 키를 떼었다고 상태 변경
        pygame_event = pygame.event.Event(KEYUP, key=pygame_key)
        pygame.event.post(pygame_event)

def convert_tkinter_key_to_pygame(tkinter_key):
    key_map = {
        'a': pygame.K_a, 'b': pygame.K_b, 'c': pygame.K_c, 'd': pygame.K_d,
        'e': pygame.K_e, 'f': pygame.K_f, 'g': pygame.K_g, 'h': pygame.K_h,
        'i': pygame.K_i, 'j': pygame.K_j, 'k': pygame.K_k, 'l': pygame.K_l,
        'm': pygame.K_m, 'n': pygame.K_n, 'o': pygame.K_o, 'p': pygame.K_p,
        'q': pygame.K_q, 'r': pygame.K_r, 's': pygame.K_s, 't': pygame.K_t,
        'u': pygame.K_u, 'v': pygame.K_v, 'w': pygame.K_w, 'x': pygame.K_x,
        'y': pygame.K_y, 'z': pygame.K_z,
        'Up': pygame.K_UP, 'Down': pygame.K_DOWN, 'Left': pygame.K_LEFT, 'Right': pygame.K_RIGHT,
        'Return': pygame.K_RETURN, 'BackSpace': pygame.K_BACKSPACE,
        'Control_L': pygame.K_LCTRL, 'Control_R': pygame.K_RCTRL,
    }
    return key_map.get(tkinter_key, None)

def pygame_event_loop():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                print("Pygame Key Pressed:", event.key)
            elif event.type == KEYUP:
                print("Pygame Key Released:", event.key)
        screen.fill((0, 0, 0))
        pygame.display.flip()

# pygame.key.get_pressed() 함수 대체
def custom_get_pressed():
    return key_state

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tkinter 안의 Pygame")
    root.geometry("800x600")
    root.resizable(False, False)

    pygame_frame = tk.Frame(root, width=800, height=600)
    pygame_frame.pack()

    os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    root.update()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    add_key_event_from_tk_to_pygame(root, pygame)

    running = True
    pygame_thread = threading.Thread(target=pygame_event_loop)
    pygame_thread.daemon = True
    pygame_thread.start()

    while running:
        root.update_idletasks()
        root.update()

        keys = custom_get_pressed()
        if keys[pygame.K_LEFT]:
            print("Left arrow key is pressed")
