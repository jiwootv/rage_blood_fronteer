import os

import pygame
import sys


# 글자 단위 줄바꿈 함수
def draw_text_with_letter_wrapping(screen, text, font, color, x, y, max_width, text_align="left"):
    lines = []  # 줄을 저장할 리스트
    current_line = ""  # 현재 줄의 내용
    current_width = 0  # 현재 줄의 너비

    for letter in text:
        # 현재 글자의 너비를 계산
        letter_width = font.size(letter)[0]

        # 화면 너비를 초과하면 줄바꿈
        if current_width + letter_width > max_width:
            lines.append(current_line.strip())  # 현재 줄을 리스트에 추가
            current_line = letter  # 새 줄 시작
            current_width = letter_width  # 새 줄의 너비 초기화
        else:
            current_line += letter  # 현재 줄에 글자 추가
            current_width += letter_width

    # 마지막 줄 추가
    if current_line:
        lines.append(current_line)

    # 줄별로 화면에 출력
    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        if text_align == "left":
            screen.blit(rendered_text, (x, y + i * font.get_linesize()))
        elif text_align == "center":
            screen.blit(rendered_text,
                        (x + (screen.get_width() - rendered_text.get_width())/2, y + i * font.get_linesize()))
        elif text_align == "right":
            screen.blit(rendered_text,
                        (x + screen.get_width() - rendered_text.get_width(), y + i * font.get_linesize()))
        else:
            raise ValueError("Invalid text_align value")


if __name__ == "__main__":
    # 초기화
    pygame.init()

    # 화면 설정
    screen_width = 500
    screen_height = 300
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("글자 단위로 줄바꿈")

    # 색상
    white = (255, 255, 255)
    black = (0, 0, 0)

    # 폰트 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path_korean = os.path.abspath(os.path.join(current_dir, '..', 'data', 'font', 'DungGeunMo.otf'))
    font = pygame.font.Font(font_path_korean, 20)  # 기본 폰트, 크기 36

    # 테스트 텍스트
    long_text = "이것은 Pygame에서 글자 단위로 줄바꿈을 구현한 예제입니다. 글자가 화면을 넘어가면 자동으로 다음 줄로 넘어갑니다."

    # 게임 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 화면 채우기
        screen.fill(white)

        # 텍스트 출력
        draw_text_with_letter_wrapping(screen, long_text, font, black, 0, 20, screen_width - 40, "center")

        # 화면 업데이트
        pygame.display.flip()

    # 종료
    pygame.quit()
    sys.exit()
