import pygame
import sys
import time
import code.cousor as cousor
import code.opening as opening
import code.msgbox as msgbox
import code.gui as gui

pygame.init()


class GuiSet:
    def __init__(self, screen):
        self.screen = screen

    def gui_set(self):
        self.gbar = gui.WidgetBar(100, 50, 150, 25, 100, "data/img/ui/notanium1.png", "right", (0, 0, 255),
                                  current_value=0)
        self.gbar.draw(screen=self.screen)


class Game:
    def __init__(self):
        self.now_time = None
        self.screen_x, self.screen_y = 640, 480
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.clock = pygame.time.Clock()
        self.cousor_class_opening = cousor.Cousor(self.screen, 8, (140, 115), (120, 145), (58, 175), (58, 205))
        self.opening = opening.Opening(self.screen)
        self.gbar = GuiSet(self.screen)
        self.msgbox = msgbox.MsgBox(self.screen, ["2972년 11월 21일, 김두한이 죽은지 1000년이 지났을때.", "지구는 이미 생활하기 힘들 정도로 파괴되었다.",
                                                  "그렇게 온 기술을 모아 지구에서는 우주선을 만들어 똑똑하고,", "유능한 일부의 개척민들과",
                                                  "수천 개의 배아들을 실었다. ", "그 우주선의 이름은 YJ-P1", "YJ-P1은 그렇게 인류의 새 개척지를 찾기 위한",
                                                  "아주 길고도 긴 여행을 시작하게 된다."], 10, 0, 20)

        # 0 : 기본값 = 오프닝
        self.now_screen = 0

    def run(self):
        while True:
            self.now_time = pygame.time.get_ticks()
            events = pygame.event.get()  # 이벤트를 한 번만 가져옴

            for event in events:
                if event.type == pygame.QUIT or msgbox.IS_QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.now_screen == 0 and self.now_time > 2000:
                        if event.key == pygame.K_UP:
                            self.cousor_class_opening.cousor_up()
                        if event.key == pygame.K_DOWN:
                            self.cousor_class_opening.cousor_down()
                        if event.key == pygame.K_RETURN:
                            if self.cousor_class_opening.get_cousor_index() == 0:
                                self.now_screen = 1
            if self.now_screen == 0:
                if self.now_time > 2000:
                    self.cousor_class_opening.draw()
                self.opening.run()
            if self.now_screen == 1:
                self.msgbox.run(events)
                if not self.msgbox.is_running():
                    self.now_screen = 2
            if self.now_screen == 2:
                self.gbar.gui_set()
            pygame.display.update()
            self.screen.fill(0)
            self.clock.tick(60)


G = Game()
G.run()
