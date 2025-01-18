import pygame
import os

# 현재 파일의 절대 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 두 개의 폰트 경로 설정
font_path_korean = os.path.abspath(os.path.join(current_dir, '..', 'data', 'font', 'font1.otf'))


class InputField:
    def __init__(self, screen, pos, size, font_size, color=(0, 0, 0, 255), outline_color=(255, 255, 255, 255)) -> None:
        # 기존 변수 초기화
        self.outline_color = outline_color
        self.size = size
        self.screen = screen
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.font = pygame.font.Font(font_path_korean, font_size)
        self.text = ""
        self.edit_pos = 0
        self.text_edit = False
        self.text_editing = ""
        self.pos = pos
        self.text_y = (size[1] - font_size) / 2
        self.completed = False

        # 커서 깜빡임 변수
        self.cursor_visible = True
        self.last_cursor_toggle_time = 0
        self.cursor_blink_rate = 500

        # 백스페이스 키 상태 변수
        self.backspace_pressed = False
        self.last_backspace_time = 0
        self.backspace_delay = 500  # 초기 대기 시간 (밀리초)
        self.backspace_repeat_rate = 40  # 연속 입력 간격 (밀리초)
        self.is_backspace_repeat = False

    def event(self, events):
        if not self.completed:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.text_edit:
                            self.text_edit = False
                            self.is_backspace_repeat = True
                        self.backspace_pressed = True
                        self.last_backspace_time = pygame.time.get_ticks()  # 현재 시간 기록
                        self.delete_character()
                    elif event.key == pygame.K_RETURN:
                        self.set_state(True)
                        events.remove(event)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_pressed = False
                        self.is_backspace_repeat = False
                elif event.type == pygame.TEXTEDITING:
                    self.text_edit = True
                    self.text_editing = event.text
                elif event.type == pygame.TEXTINPUT:
                    print(event.text,  " 1234asdf")
                    self.text_edit = False
                    self.text_editing = ""
                    self.text = self.text[:self.edit_pos] + event.text + self.text[self.edit_pos:]
                    self.edit_pos = min(self.edit_pos + len(event.text), len(self.text))
                    self.last_cursor_toggle_time = pygame.time.get_ticks()
                    self.cursor_visible = True

            # 백스페이스 연속 삭제 처리
            if self.backspace_pressed:
                current_time = pygame.time.get_ticks()
                if ((current_time - self.last_backspace_time >=
                        (self.backspace_delay if not self.is_backspace_repeat else self.backspace_repeat_rate))):
                    self.delete_character()
                    self.last_backspace_time = current_time
                    self.is_backspace_repeat = True

    def delete_character(self):
        if self.edit_pos > 0:
            self.text = self.text[:self.edit_pos - 1] + self.text[self.edit_pos:]
            self.edit_pos -= 1

    def draw(self):
        # 기존 draw 함수 그대로 유지
        self.screen.blit(self.image, self.image.get_rect(topleft=self.pos))
        pygame.draw.rect(self.screen, self.outline_color,
                         (self.pos[0] - 5, self.pos[1] - 5, self.size[0] + 10, self.size[1] + 10), 5)
        font = self.font
        string = font.render(self.text + self.text_editing, True, (255, 255, 255))
        self.screen.blit(string, string.get_rect(topleft=(self.pos[0], self.pos[1] + self.text_y)))

        if not self.completed:
            if self.text_editing:
                underline_start_pos = self.pos[0] + font.size(self.text)[0]
                underline_surface = pygame.Surface((font.size(self.text_editing)[0], 2))
                underline_surface.fill((255, 255, 255))
                self.screen.blit(underline_surface, (underline_start_pos, self.pos[1] + font.get_height() + self.text_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_cursor_toggle_time >= self.cursor_blink_rate:
                self.cursor_visible = not self.cursor_visible
                self.last_cursor_toggle_time = current_time

            if self.cursor_visible:
                cursor_x = self.pos[0] + font.size(self.text + self.text_editing)[0]
                cursor_surface = pygame.Surface((2, font.get_height()))
                cursor_surface.fill((255, 255, 255))
                self.screen.blit(cursor_surface, (cursor_x, self.pos[1] + self.text_y))

    def get_text(self):
        if self.completed:
            return self.text
        else:
            return self.text + self.text_editing

    def set_state(self, state: bool):
        if state:
            self.completed = True
            self.text = self.text + self.text_editing
            self.text_editing = ""
            pygame.key.stop_text_input()
        else:
            self.completed = False
            pygame.key.start_text_input()

    def is_completed(self):
        return self.completed



if __name__ == "__main__":
    pygame.init()  # Pygame 초기화
    pygame.key.start_text_input()  # 텍스트 입력 시작
    screen = pygame.display.set_mode((1000, 800))  # 화면 크기 설정

    input_field = InputField(screen, (200, 500), (300, 50), 40)  # InputField 객체 생성

    while True:
        screen.fill((100, 0, 50))  # 화면 배경색 설정

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()  # 종료 시 Pygame 종료
                exit()  # 프로그램 종료

        input_field.event(events)  # 이벤트 처리
        input_field.draw()  # 텍스트 필드 렌더링

        pygame.display.update()  # 화면 업데이트
