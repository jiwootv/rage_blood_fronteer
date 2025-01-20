import os
import tkinter as tk
import pygame
from pygame.locals import *


def convert_tkinter_key_to_pygame(tkinter_key):
    # Tkinter의 키 코드를 Pygame의 키 코드로 변환
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
        # 다른 키들도 필요에 맞게 추가 가능
    }
    return key_map.get(tkinter_key, None)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tkinter 안의 Pygame")  # 창 제목 설정
        self.root.geometry("800x600")  # Tkinter 창 크기 설정
        self.root.resizable(False, False)  # 창 크기 조절 불가능 설정
        self.running = True

        pygame_frame = tk.Frame(self.root, width=800, height=600)  # Pygame이 렌더링될 영역
        pygame_frame.pack()

        os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())  # SDL 창 ID 설정
        os.environ['SDL_VIDEODRIVER'] = 'windib'  # Windows에서 제대로 동작하도록 드라이버 설정
        self.root.update()  # 창을 업데이트하여 ID가 반영되도록 함

        # Pygame 초기화
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

        # 키 상태 추적용 변수
        self.pressed_keys = set()

        # Tkinter의 키보드 이벤트를 처리할 함수
        self.root.bind('<KeyPress>', self.handle_tkinter_keypress)
        self.root.bind('<KeyRelease>', self.handle_tkinter_keyrelease)

        # Tkinter 이벤트 루프와 Pygame 이벤트 루프 동시 처리
        self.update()

    def handle_tkinter_keypress(self, event):
        # Tkinter에서 받은 키 입력을 Pygame 이벤트로 변환하여 큐에 추가
        pygame_key = convert_tkinter_key_to_pygame(event.keysym)
        if pygame_key and pygame_key not in self.pressed_keys:
            pygame_event = pygame.event.Event(KEYDOWN, key=pygame_key)
            pygame.event.post(pygame_event)
            self.pressed_keys.add(pygame_key)

    def handle_tkinter_keyrelease(self, event):
        # Tkinter에서 키 릴리즈를 처리할 때 Pygame 이벤트로 변환하여 큐에 추가
        pygame_key = convert_tkinter_key_to_pygame(event.keysym)
        if pygame_key in self.pressed_keys:
            pygame_event = pygame.event.Event(KEYUP, key=pygame_key)
            pygame.event.post(pygame_event)
            self.pressed_keys.remove(pygame_key)

    def update(self):
        while self.running:
            # Tkinter의 이벤트 처리
            self.root.update_idletasks()
            self.root.update()

            # Pygame 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    print("Pygame Key Pressed:", event.key)
                elif event.type == KEYUP:
                    print("Pygame Key Released:", event.key)

            # Pygame 화면 업데이트
            self.screen.fill((0, 0, 0))  # 배경을 검정색으로 설정
            pygame.display.flip()

        pygame.quit()


app = App()
