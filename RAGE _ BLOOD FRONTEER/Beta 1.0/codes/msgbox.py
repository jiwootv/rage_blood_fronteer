import pygame

pygame.init()

DEBUG = True

IS_QUIT = False


def eventset(r):
    global EVENT
    print("EVENT SETTING:", r)
    EVENT = r


class MsgBox:
    def __init__(self, screen, text, speed, soundtype, size, *args):
        """
        언더테일같은 텍스트 박스와 텍스트 출력 클래스
        :param screen: pygame의 스크린
        :param text: 출력할 텍스트
        :param speed: 텍스트가 나오는 속도
        :param soundtype: 텍스트가 나올 때 무슨 소리가 나는지 정의 (data/sound/effect/A Piano.wav 고정임)
        :param size: 텍스트 사이즈
        :param args: [y좌표 - 323 (기본값 20), more_func (안 쓰고 있음)] (안 쓰는 것이 좋음)
        """
        self.font = pygame.font.Font("data\\font\\DungGeunMo.otf", size)
        try:
            self.y = args[0]
        except IndexError:
            self.y = 20
        self.root = screen
        self.P = True
        self.size = size
        self.text = text
        self.now_text = ""
        self.now_text_count = 0
        print(self.text)
        self.text_line = 0
        self.text_maxline = self.text.__len__()
        self.gap = 60 / speed
        self.gap_count = 0

        self.text_speed = speed
        self.sound_type = soundtype
        self.text_on = True
        self.quit = False
        self.time = 0
        self.rect1 = pygame.Rect(25, 340, 590, 120)
        self.rect2 = pygame.Rect(30, 350, 580, 100)
        self.rect_t = self.font.render(self.now_text, 1, (255, 255, 255))
        self.sound = [pygame.mixer.Sound("data\\sound\\effect\\A Piano.wav"),
                      pygame.mixer.Sound("data\\sound\\effect\\A Piano.wav")]
        self.ev = 0

        try:
            self.more_func = args[1]
        except IndexError:
            self.more_func = None

    def t_update(self):
        """
        텍스트를 업데이트 합니다.
        """
        try:
            self.rect_t = self.font.render(self.now_text, 1, (255, 255, 255))
            if not len(self.text[self.text_line]) == self.now_text_count or self.now_text_count == 0 and not self.text_on:
                print(self.text[self.text_line].__len__() == len(self.now_text))
                if DEBUG:
                    print("------")

                self.now_text += self.text[self.text_line][self.now_text_count]
                self.now_text_count += 1
                if self.now_text_count != 0 and self.text[self.text_line][self.now_text_count - 1] != " ": self.sound[
                    self.sound_type].play()
                if DEBUG:
                    print("현재 글자:", self.now_text)
                    print("현재 글자 순서:", self.now_text_count)
        except IndexError:
            pass

    def draw(self) -> None:
        """
        본인을 draw 합니다.
        """
        pygame.draw.rect(self.root, (255, 255, 255), self.rect1)
        pygame.draw.rect(self.root, 0, self.rect2)
        self.root.blit(self.rect_t, (15 + self.size, 323 + self.y + self.size))

    # 아 왜 변경안됨 ;;
    # ㄴ 이걸 쓰는 곳이 어디 있는데요?
    def timer(self) -> None:
        self.time = pygame.time.get_ticks()

    def get_event(self) -> int:
        return IS_QUIT

    def is_running(self) -> bool:
        return self.P

    def run(self, events):
        """
        본인의 기능을 이곳에서 다 합니다.
        """
        for event in events:
            if event.type == pygame.QUIT:
                global IS_QUIT
                IS_QUIT = True
                self.quit = True

                self.P = False

            if event.type == pygame.KEYDOWN:
                try:
                    if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and len(
                            self.text[self.text_line]) == self.now_text_count:
                        self.text_on = True
                        self.text_line += 1
                        self.now_text_count = 0
                        self.now_text = ""
                    if event.key == pygame.K_x or event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.now_text = self.text[self.text_line]
                        self.now_text_count = len(self.text[self.text_line])

                    if self.more_func is not None:
                        print(type(self.more_func))
                        self.more_func(event=event)
                except IndexError:
                    pass

        self.gap_count += 1
        if self.gap_count >= self.gap:
            self.gap_count = 0
            if self.text_line == self.text_maxline:
                self.P = False
            self.t_update()

        self.draw()
        pygame.display.update()

