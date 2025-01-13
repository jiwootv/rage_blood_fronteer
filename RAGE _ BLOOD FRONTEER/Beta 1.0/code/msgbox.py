import sys

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
        정의하자마자 실행됩니다.
        (실행이 끝나야 다음 줄로 넘어갑니다.)
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

        self.text_speed = speed
        self.sound_type = soundtype
        self.text_on = True
        self.quit = False
        self.time = 0
        self.rect1 = pygame.Rect(25, 340, 590, 120)
        self.rect2 = pygame.Rect(30, 350, 580, 100)
        self.rect_t = []
        for i in self.text:
            self.rect_t.append(self.font.render(i, 1, (255, 255, 255)))
        print(self.rect_t)
        self.sound = [pygame.mixer.Sound("data\\sound\\effect\\A Piano.wav"),
                      pygame.mixer.Sound("data\\sound\\effect\\A Piano.wav")]
        self.ev = 0
        try:
            self.draw(more_func=args[1])
        except IndexError:
            self.draw()

    def t_update(self):
        """
        텍스트를 업데이트 합니다.
        """
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

    def _draw(self) -> None:
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

    def draw(self, more_func=None):
        """
        사실 이거 run 함수임.
        본인의 기능을 이곳에서 다 합니다.
        :param more_func: (왜 쓰는지 모르겠다.) (기본값: None)
        """
        clock = pygame.time.Clock()
        self.P = True
        while self.P:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    global IS_QUIT
                    IS_QUIT = True
                    self.quit = True

                    self.P = False

                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and len(
                            self.text[self.text_line]) == self.now_text_count:
                        self.text_on = True
                        self.text_line += 1
                        self.now_text_count = 0
                        self.now_text = ""
                    if event.key == pygame.K_x or event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.now_text = self.text[self.text_line]
                        self.now_text_count = len(self.text[self.text_line])

                if more_func != None:
                    print(type(more_func))
                    more_func(event=event)

            if self.text_line == self.text_maxline:
                self.P = False
                break

            self.t_update()
            self._draw()
            pygame.display.update()
            clock.tick(self.text_speed)
            pygame.display.update()
