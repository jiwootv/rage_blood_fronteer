import pygame
import sys
import math

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
		screen.fill(WHITE)
		pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), 5)
		pygame.display.flip()
		pygame.time.delay(30)


# 메인 함수
def main():
	pos1 = [300, 300]
	pos2 = [500, 400]
	path = generate_path(pos1, pos2, 10)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		move_along_path(path)


if __name__ == "__main__":
	main()
