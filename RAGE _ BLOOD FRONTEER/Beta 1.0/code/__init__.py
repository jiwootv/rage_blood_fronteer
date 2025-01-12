# import pygame
# import sys
#
# # Initialize Pygame
# pygame.init()
#
# # Screen dimensions
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
#
# # Load Bullet1 image
# BULLET_IMAGE = pygame.image.load(
# 	'../data/img/gun/bullet1.png')  # Make sure Bullet1.png is in the same directory or provide the correct path
#
#
# # GunBullets class definition
# class GunBullets(pygame.sprite.Sprite):
# 	def __init__(self, x, y):
# 		super().__init__()
# 		self.image = BULLET_IMAGE
# 		self.rect = self.image.get_rect()
# 		self.rect.center = (x, y)
#
# 	def update(self):
# 		self.rect.y -= 5  # Move the bullet upwards
# 		if self.rect.bottom < 0:
# 			self.kill()  # Remove the bullet if it goes off-screen
#
#
# # Main game loop
# def main():
# 	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 	pygame.display.set_caption("GunBullets Example")
#
# 	all_sprites = pygame.sprite.Group()
#
# 	clock = pygame.time.Clock()
#
# 	while True:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				pygame.quit()
# 				sys.exit()
#
# 		# Add a bullet for demonstration purposes
# 		if pygame.mouse.get_pressed()[0]:  # Left mouse button
# 			bullet = GunBullets(*pygame.mouse.get_pos())
# 			all_sprites.add(bullet)
#
# 		all_sprites.update()
#
# 		screen.fill((0, 0, 0))  # Clear screen with black
# 		all_sprites.draw(screen)
#
# 		pygame.display.flip()
#
# 		clock.tick(60)
#
#
# if __name__ == "__main__":
# 	main()
