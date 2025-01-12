import pygame, sys

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()

def draw_rect_alpha(screen, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)


# 글자 단위 줄바꿈 함수


class PopUp:
    def __init__(self, screen, text, image):
        self.screen = screen
        self.text = text
        self.image = image
        self.rect = pygame.rect.Rect(100, 150, 440, 180)
        self.cancel_image = pygame.image.load("data/img/ui/cancel.png")
        self.popup_onscreen = True

        self.sound = pygame.mixer.Sound("data/sound/effect/Connect.wav")
        self.sound.play()

    def draw_text_newline(self, surface, text, color, x, y, max_width, font):
        lines = []  # 줄을 저장할 리스트
        current_line = ""  # 현재 줄의 내용
        current_width = 0  # 현재 줄의 너비

        for letter in text:
            # 현재 글자의 너비를 계산
            letter_width = font.size(letter)[0]

            # 화면 너비를 초과하면 줄바꿈
            if current_width + letter_width > max_width:
                lines.append(current_line)  # 현재 줄을 리스트에 추가
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
            surface.blit(rendered_text, (x, y + i * font.get_linesize()))

    def draw(self):
        if self.popup_onscreen:
            draw_rect_alpha(self.screen, (255, 255, 255, 138), self.rect)
            font = pygame.font.Font("data/font/DungGeunMo.otf", 22)
            font.bold = True
            text = font.render(self.text[0], 1, (255, 255, 255))
            self.screen.blit(text, (105, 155))

            font = pygame.font.Font("data/font/DungGeunMo.otf", 20)
            self.draw_text_newline(self.screen, self.text[1], (255, 255, 255), 105, 180, 435, font)

            self.screen.blit(self.cancel_image, (520, 157))

    def event(self):
        mouse_pos = pygame.mouse.get_pos()
        collide_rect = pygame.rect.Rect(520, 157, 16, 16)
        if collide_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.popup_onscreen = False

P = PopUp(screen, ["불복종이 증가했습니다!", "불복종의 증가로 인해 노타민들이 일을 하지 않습니다! 이는 작업효율 감소로 이어집니다."], image=None)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    P.draw()
    P.event()
    pygame.display.update()
    clock.tick(60)

