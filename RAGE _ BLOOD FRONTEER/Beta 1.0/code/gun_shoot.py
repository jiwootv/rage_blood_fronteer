import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("data/img/gun/bullet1.png"), (20, 20))
		self.rect = self.image.get_rect()
		pygame.mixer.Sound("data/sound/effect/Rebolber1.mp3").play()
		self.bullet_distance = 0
		self.rect.center = (x, y)
		self.bullet_speed = 5

	def update(self):
		self.rect.y -= self.bullet_speed  # Move the bullet upwards
		self.bullet_distance -= self.bullet_speed
		if self.bullet_distance < -1000:
			print("꽥")
			self.kill()  # Remove the bullet if it goes off-screen

class Gun:
	def __init__(self, screen, gun_type):
		self.gun_img = pygame.image.load(f"data/gun/{gun_type}.png")
		self.bullet = pygame.image.load("data/gun/bullet1.png")
		self.screen = screen

