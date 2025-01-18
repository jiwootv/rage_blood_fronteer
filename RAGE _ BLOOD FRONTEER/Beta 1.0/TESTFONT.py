import pygame
import sys
import math
import codes.Turret as turret
import codes.TextBoxes as Text

# Pygame 초기화
pygame.init()

# 창 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Movement")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)


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
	T = turret.Turret(1, pos1, 100)
	TB = Text.TextBox(screen)
	path = generate_path(pos1, pos2, 10)
	playerpos = [0, 0]
	T.shoot(pos2)

	while True:
		print(T.is_in(playerpos))
		if T.is_in(playerpos):
			T._debug_circle_draw(screen, (255, 0, 0))
			TB.text_draw("포탑에 근접했습니다", (0, 0), 20, (255, 0, 255))

		else:
			T._debug_circle_draw(screen, (0, 255, 0))

		player_rect = pygame.Rect(0, 0, 30, 30)
		player_rect.center = playerpos

		pygame.draw.rect(screen,(255, 0, 255), player_rect)

		pygame.display.update()
		pygame.time.Clock().tick(30)
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





if __name__ == "__main__":
	main()
