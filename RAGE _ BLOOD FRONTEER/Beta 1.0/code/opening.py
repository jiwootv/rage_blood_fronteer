import pygame
import sys
import time

pygame.init()


class Opening:
    def __init__(self, screen):
        """
        main.py에서 메뉴를 담당하는 클래스
        :param screen: pygame의 스크린
        """
        self.screen_x, self.screen_y = 640, 480
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.text = lambda text, size, color: pygame.font.Font("data/font/DungGeunMo.otf", size).render(text, True, color)
        self.texts = ["RAGE:", "BLOOD FRONTEER", "새로 시작", "불러오기", "업적", "설정"]
        self.displayed_texts = ["", "", "", "", "", ""]
        self.char_indices = [0, 0, 0, 0, 0, 0]
        self.last_update = time.time()
        self.update_interval = 0.25  # 250 milliseconds
        self.char_alphas = [[0] * len(t) for t in self.texts]  # Initialize alphas for each character in each text
        self.text_len = 0

    def display_text(self):
        """
        텍스트를 보여줍니다. (그라데이션으로)
        """
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            for i, text in enumerate(self.texts):
                if self.char_indices[i] < len(text):
                    self.displayed_texts[i] += text[self.char_indices[i]]
                    self.char_indices[i] += 1
            self.last_update = current_time
            self.text_len += 1

        # Update alpha values
        for i in range(len(self.texts)):
            for j in range(self.char_indices[i]):
                if self.char_alphas[i][j] < 255:
                    self.char_alphas[i][j] = min(255, self.char_alphas[i][j] + 5)  # Increase alpha value

        # Render each character with its alpha value
        y_offsets = [0, 50, 110, 140, 170, 200]  # Different y offsets for each text
        for i, text in enumerate(self.displayed_texts):
            x_offset = 0
            font_size = 50 if i < 2 else 30  # Set font size 50 for first two texts, 30 for others
            for j, char in enumerate(text):
                char_surface = self.text(char, font_size, (255, 255, 255)).convert_alpha()
                char_surface.set_alpha(self.char_alphas[i][j])
                self.screen.blit(char_surface, (x_offset, y_offsets[i]))
                x_offset += char_surface.get_width()

    def run(self):
        """
        실행 함수
        """
        self.display_text()

    def get_text_len(self):
        return self.text_len
