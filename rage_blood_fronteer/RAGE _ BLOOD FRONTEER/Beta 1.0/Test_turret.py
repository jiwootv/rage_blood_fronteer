import pygame
import sys
import math
import code.Turret as turret
import code.attack_alg as atalg

# Pygame 초기화
pygame.init()

# 창 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Movement")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class TurretBullet(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pos
		self.index = 0
		self.image = pygame.Surface((10, 10))  # 총알의 크기 설정
		self.image.fill((255, 255, 0))  # 빨간색 총알
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos[self.index]

	def update(self):
		if self.index < len(self.pos) - 1:
			self.index += 1
			self.rect.topleft = self.pos[self.index]
		else:
			self.kill()  # 경로가 끝나면 스프라이트 제거

# pos1에서 pos2로 이동하는 경로 생성 함수
def generate_path(pos1, pos2, steps=100):
	path = []
	x1, y1 = pos1
	x2, y2 = pos2

	for i in range(steps):
		t = i / (steps - 1)
		x = x1 + (x2 - x1) * t
		y = y1 + (y2 - y1) * t
		path.append((x, y))

	return path


# 객체를 따라 이동시키는 함수
def move_along_path(path):
	for pos in path:
		print(pos)
		screen.fill(WHITE)
		pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), 5)

# 메인 함수
def main():
	pos1 = [300, 300]
	pos2 = [300, 300]
	T = turret.Turret(screen, 1, pos1, radius=300)
	path = generate_path(pos1, pos2, steps=int(atalg.distance(pos1, pos2))*100)
	playerpos = [0, 0]
	#T.shoot(pos2)

	time = 0
	time += 1

	while True:
		time += 1
		print(time)
		if T.is_in(playerpos):
			T._debug_circle_draw(screen, (255, 0, 0))
			a = generate_path([300, 300], playerpos, 25)
			if time > 60:
				time = 0
				T.shoot(playerpos)

		else:
			T._debug_circle_draw(screen, (0, 255, 0))

		player_rect = pygame.Rect(0, 0, 30, 30)
		player_rect.center = playerpos

		pygame.draw.rect(screen, (255, 0, 255), player_rect)
		T.update()

		pygame.display.update()



		pygame.time.Clock().tick(60)
		screen.fill((255, 255, 255))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_w:
					playerpos[1] -= 10
				if event.key == pygame.K_a:
					playerpos[0] -= 10
				if event.key == pygame.K_s:
					playerpos[1] += 10
				if event.key == pygame.K_d:
					playerpos[0] += 10
		k = pygame.key.get_pressed()
		if k[pygame.K_w]:
			playerpos[1] -= 10
		if k[pygame.K_a]:
			playerpos[0] -= 10
		if k[pygame.K_s]:
			playerpos[1] += 10
		if k[pygame.K_d]:
			playerpos[0] += 10



if __name__ == "__main__":
	main()
