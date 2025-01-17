import pygame
import os

# 현재 파일의 절대 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 두 개의 폰트 경로 설정
font_path_korean = os.path.abspath(os.path.join(current_dir, '..', 'data', 'font', 'DungGeunMo.otf'))
font_path_japanese = os.path.abspath(os.path.join(current_dir, '..', 'data', 'font', 'BestTen-CRT.otf'))  # 일본어, 한자 지원


class InputField:
    def __init__(self, screen, pos, size, font_size, color=(0, 0, 0, 255), outline_color=(255, 255, 255, 255)) -> None:
        # 필드 크기를 받아서 초기화
        self.outline_color = outline_color
        self.size = size
        self.screen = screen
        self.image = pygame.Surface(size, pygame.SRCALPHA)  # 투명한 배경의 표면 생성
        self.image.fill(color)  # 배경을 검은색으로 채움
        self.font_korean = pygame.font.Font(font_path_korean, font_size)  # 한글 폰트
        self.font_cjk = pygame.font.Font(font_path_japanese, font_size)  # 일본어, 한자 폰트
        self.text = ""  # 입력된 텍스트
        self.edit_pos = 0  # 커서의 위치
        self.text_edit = False  # 텍스트 편집 중 상태
        self.text_editing = ""  # 편집 중인 텍스트
        self.pos = pos
        self.text_y = (size[1] - font_size) / 2
        self.completed = False

        # 커서 깜빡임을 위한 변수
        self.cursor_visible = True
        self.last_cursor_toggle_time = 0
        self.cursor_blink_rate = 500  # 커서 깜빡임 주기 (밀리초 단위)

    def event(self, events):
        if not self.completed:
            for event in events:
                # 이벤트 처리
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # 백스페이스 처리: 커서 앞의 텍스트 삭제
                        if self.edit_pos > 0:
                            self.text = self.text[:self.edit_pos - 1] + self.text[self.edit_pos:]
                            self.edit_pos -= 1  # 커서를 한 칸 뒤로 이동
                    if event.key == pygame.K_RETURN:
                        self.set_state(True)
                elif event.type == pygame.TEXTEDITING:
                    # 텍스트 편집 상태일 때
                    self.text_edit = True
                    self.text_editing = event.text  # 편집 중인 텍스트
                elif event.type == pygame.TEXTINPUT:
                    # 텍스트 입력 처리
                    self.text_edit = False
                    self.text_editing = ""  # 편집 중인 텍스트 초기화
                    # 새로 입력된 텍스트를 기존 텍스트에 삽입
                    self.text = self.text[:self.edit_pos] + event.text + self.text[self.edit_pos:]
                    self.edit_pos = min(self.edit_pos + len(event.text), len(self.text))  # 커서 위치 업데이트

                    # 텍스트가 변경되었을 때 커서 깜빡임 초기화
                    self.last_cursor_toggle_time = pygame.time.get_ticks()
                    self.cursor_visible = True

    def draw(self):
        # 화면에 필드를 그리는 함수
        self.screen.blit(self.image, self.image.get_rect(topleft=self.pos))  # 필드 배경 그리기
        pygame.draw.rect(self.screen, self.outline_color,
                         (self.pos[0] - 5, self.pos[1] - 5, self.size[0] + 10, self.size[1] + 10), 5)

        # 텍스트 렌더링 시 텍스트 내용에 따라 폰트 선택
        def get_font_for_text(text):
            # 텍스트가 한자나 일본어를 포함하면 CJK 폰트 사용
            if any('\u4e00' <= char <= '\u9fff' or '\u3040' <= char <= '\u30ff' for char in text):
                return self.font_cjk
            else:
                return self.font_korean

        font = get_font_for_text(self.text + self.text_editing)  # 텍스트에 맞는 폰트 선택
        string = font.render(self.text + self.text_editing, True, (255, 255, 255))
        self.screen.blit(string, string.get_rect(topleft=(self.pos[0], self.pos[1] + self.text_y)))  # 텍스트 그리기

        if not self.completed:
            # 편집 중인 텍스트 밑줄 그리기
            if self.text_editing:
                underline_start_pos = self.pos[0] + font.size(self.text)[0]  # 텍스트 끝 위치
                underline_surface = pygame.Surface((font.size(self.text_editing)[0], 2))  # 밑줄의 높이는 2로 설정
                underline_surface.fill((255, 255, 255))  # 밑줄 색상
                self.screen.blit(underline_surface, (underline_start_pos, self.pos[1] + font.get_height() + self.text_y))  # 밑줄 그리기

            # 커서 깜빡임 처리
            current_time = pygame.time.get_ticks()
            if current_time - self.last_cursor_toggle_time >= self.cursor_blink_rate:
                self.cursor_visible = not self.cursor_visible
                self.last_cursor_toggle_time = current_time

            if self.cursor_visible:
                # 커서 그리기 (편집 중인 텍스트가 있을 경우 커서 표시)
                cursor_x = self.pos[0] + font.size(self.text + self.text_editing)[0]  # 커서의 x 위치 (현재 커서 위치)
                cursor_surface = pygame.Surface((2, font.get_height()))  # 커서의 크기
                cursor_surface.fill((255, 255, 255))  # 커서 색상 (흰색)
                self.screen.blit(cursor_surface, (cursor_x, self.pos[1] + self.text_y))  # 커서 그리기

    def get_text(self):
        if self.completed:
            return self.text
        else:
            return None

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
