import pygame

class Cousor:
	def __init__(self, screen, size, *pos):
		self.pos = pos
		self.cousor_img = pygame.image.load("data/img/cousor.png")
		self.cousor_img.get_size()
		# print(list(map(lambda x: x/size,self.cousor_img.get_size())))
		self.cousor_img = pygame.transform.scale(self.cousor_img, list(map(lambda x: x/size,self.cousor_img.get_size())))
		self.p_len = len(pos)
		self.root = screen
		self.now_index = 0
		self.cousor_sound = pygame.mixer.Sound("data/sound/effect/A piano.wav")

	def cousor_up(self):
		if self.now_index != 0:
			self.now_index -= 1
			self.cousor_sound.play()

	def cousor_down(self):
		if self.now_index != self.p_len-1:
			self.now_index += 1
			self.cousor_sound.play()


	def get_cousor_index(self):
		print(self.pos[self.now_index], self.now_index)
		return self.now_index

	def draw(self):
		self.root.blit(self.cousor_img, self.pos[self.now_index])