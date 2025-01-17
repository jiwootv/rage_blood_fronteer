import pygame
import sys
import code.MAP as game_map
import code.cousor as cousor
import code.opening as opening
import code.msgbox as msgbox
import code.gui as gui
from code.InputField import InputField
from code.auto_line import draw_text_with_letter_wrapping

pygame.init()


class GuiSet:
    def __init__(self, screen):
        self.screen = screen

    def gui_set(self):
        self.gbar = gui.WidgetBar(100, 50, 150, 25, 100, "data/img/ui/notanium1.png", "right", (0, 0, 255),
                                  current_value=0)
        self.gbar.draw(screen=self.screen)


class Button:
    def __init__(self, x, y, width, height, color, outline=None, text='', text_color=(0, 0, 0), font=None, img=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outline = outline
        self.text = text
        self.font = font if font is not None else pygame.font.Font(None, 30)
        self.img = img
        self.text_color = text_color

    def draw(self, screen):
        # 버튼에 외곽선이 있을 경우 그리기
        if self.outline:
            pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # 버튼 그리기
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        # 버튼에 텍스트가 있을 경우 텍스트 그리기
        if self.text != '':
            text = self.font.render(self.text, 1, self.text_color)
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)
            ))

        # 버튼에 이미지가 있을 경우 이미지 그리기
        if self.img != '':
            img = pygame.image.load(self.img)
            screen.blit(img, (
                self.x + (self.width / 2 - img.get_width() / 2),
                self.y + (self.height / 2 - img.get_height() / 2)
            ))

    def is_over(self, pos):
        # pos는 마우스의 (x, y) 좌표
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


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
        self.Map_c = game_map.Map(self.screen)
        self.input_field = InputField(self.screen, (120, 250), (400, 50), 40)
        self.name = ""
        font = pygame.font.Font("data/font/font1.otf", 30)
        self.name_button = Button(170, 350, 300, 60, (255, 255, 255), text="확인", font=font)
        self.name_yes_button = Button(140, 280, 150, 60, (255, 255, 255), text="네", font=font)
        self.name_no_button = Button(350, 280, 150, 60, (255, 255, 255), text="아니요", font=font)

        pygame.display.set_caption("RAGE: BLOOD FRONTEER")

    def run(self):
        while True:
            self.now_time = pygame.time.get_ticks()
            events = pygame.event.get()  # 이벤트를 한 번만 가져옴

            for event in events:
                if event.type == pygame.QUIT or msgbox.IS_QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.now_screen == 1 and self.opening.get_text_len() >= 6:
                        if event.key == pygame.K_UP:
                            self.cousor_class_opening.cousor_up()
                        if event.key == pygame.K_DOWN:
                            self.cousor_class_opening.cousor_down()
                        if event.key == pygame.K_RETURN:
                            if self.cousor_class_opening.get_cousor_index() == 0:
                                self.now_screen = 2
            if self.now_screen == 0:
                self.say_your_name(self.screen, events)
            if self.now_screen == 1:
                self.opening.run()
                if self.opening.get_text_len() >= 6:
                    self.cousor_class_opening.draw()
            if self.now_screen == 2:
                self.msgbox.run(events)
                if not self.msgbox.is_running():
                    self.now_screen = 3
                    self.Map_c.load_to_list(self.Map_c.mapGet(1))
                    self.Map_c.draw_set()
                    self.Map_c.brickPassSet(1)
            if self.now_screen == 3:
                self.main_screen(events)
            pygame.display.update()
            self.screen.fill(0)
            self.clock.tick(60)

    def main_screen(self, events):
        self.Map_c.draw()
        self.Map_c.event()

        self.gbar.gui_set()

    def say_your_name(self, screen, events):
        name_font = pygame.font.Font("data/font/font1.otf", 40)
        font = pygame.font.Font("data/font/font1.otf", 40)
        if name_font.size(self.input_field.get_text())[0] > 400:
            text = "잠시만요, 당신 이름이 이 텍스트 박스 안에 다 안 들어가요?"
        else:
            text = "당신의 이름은 무엇입니까?"
        draw_text_with_letter_wrapping(screen, text, font, (255, 255, 255),
                                       0, 100, 640, "center")

        self.input_field.event(events)
        self.input_field.draw()
        if self.name_button.is_over(pygame.mouse.get_pos()):
            self.name_button.color = (127, 127, 127)
            if pygame.mouse.get_pressed()[0]:
                self.input_field.set_state(True)
        else:
            self.name_button.color = (255, 255, 255)
        self.name_button.draw(self.screen)
        if self.input_field.is_completed():
            self.name = self.input_field.get_text()
            pygame.draw.rect(screen, (255, 255, 255), (98, 98, 444, 284), 0)
            pygame.draw.rect(screen, (0, 0, 0), (100, 100, 440, 280), 0)
            font = pygame.font.Font("data/font/font1.otf", 30)

            # 이름 이스터애그들
            creator_name = ["qwru0905"]
            with open("data/hangul_almost_no_used.txt", "rb") as file:
                hangul_almost_no_used_text = file.read().decode('utf-8')
                hangul_almost_no_used_list = hangul_almost_no_used_text.split(" ")
            if name_font.size(self.name)[0] > 400:
                text = "와... 엄청 긴 이름을 가졌군요?"
            elif len(self.name) == 1:
                text = "와... 엄청 짧은 이름을 가졌군요?"
            elif len(self.name) == 0:
                text = "와... 아무것도 안 쓰셨네요?"
            elif self.name in creator_name:
                text = "오, 당신 이름이 저희 개발자 중 한 분이랑 겹치네요?"
            else:
                is_include_hangul_almost_no_used = False
                for char in self.name:
                    if char in hangul_almost_no_used_list:
                        text = f"와... 당신 이름에 뭔가 잘 쓰이지 않는 글자가 들어가 있는 것 같네요."
                        is_include_hangul_almost_no_used = True
                        break
                if not is_include_hangul_almost_no_used:
                    text = f"당신의 이름이 {self.name}이 맞습니까?"
            draw_text_with_letter_wrapping(screen, text, font, (255, 255, 255),
                                           0, 150, 400, "center")

            self.name_yes_button.draw(screen)
            self.name_no_button.draw(screen)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.now_screen = 1
                    if event.key == pygame.K_ESCAPE:
                        self.input_field.set_state(False)
            if self.name_yes_button.is_over(pygame.mouse.get_pos()):
                self.name_yes_button.color = (127, 127, 127)
                if pygame.mouse.get_pressed()[0]:
                    self.now_screen = 1
            else:
                self.name_yes_button.color = (255, 255, 255)
            if self.name_no_button.is_over(pygame.mouse.get_pos()):
                self.name_no_button.color = (127, 127, 127)
                if pygame.mouse.get_pressed()[0]:
                    self.input_field.set_state(False)
            else:
                self.name_no_button.color = (255, 255, 255)


G = Game()
G.run()
