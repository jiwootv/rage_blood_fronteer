import pygame

# Pygame 초기화
pygame.init()

# 창 크기 설정
screen = pygame.display.set_mode((800, 600))

# 이미지 로드
image = pygame.image.load('data/img/load_btn.png')

# 회전 각도 설정
angle = 45

# 메인 루프
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# 화면 채우기
	screen.fill((255, 255, 255))

	# 이미지 회전
	rotated_image = pygame.transform.rotate(image, angle)

	# 이미지 그리기
	rect = rotated_image.get_rect(center=(400, 300))
	screen.blit(rotated_image, rect.topleft)

	# 화면 업데이트
	pygame.display.flip()
	angle += 1
	if angle > 360: angle = 0
	pygame.time.Clock().tick(20)

# Pygame 종료
pygame.quit()
