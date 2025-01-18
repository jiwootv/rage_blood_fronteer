import pygame

class TextBox:
	def __init__(self, screen:pygame.display.set_mode):
		self.screen = screen
		self.text = lambda text, size, color: pygame.font.Font("data/font/DungGeunMo.otf", size).render(text, 0, color)

	def text_draw(self, text, pos: tuple | list, size, color):
		"""
		입력받은 값에 따라 이 함수는 무료로 텍스트를 그려줍니다!
		사용 방법:
		(텍스트, (x, y), 사이즈, 색깔)
		"""
		self.screen.blit(self.text(text,  size, color), pos)

