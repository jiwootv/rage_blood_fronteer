# 이거 뭐하는 파일이냐면:
# 그저 쌈@박하게 모듈 테스트 하는 곳
import code.cousor as cousor
import code.opening as opening
import code.gui as gui
import code.gun_shoot as shoot
import pygame, sys, time
root = pygame.display.set_mode((640, 480))
# [0, 50, 110, 140, 170, 200]
c = cousor.Cousor(root, 8, (140, 115), (120, 145), (58, 175), (58, 205))
o = opening.Opening(root)
t = gui.StatsBar(root)
all_sprite = pygame.sprite.Group()
bullet_nums = 10
meg_num = 5
while True:
	time = pygame.time.get_ticks()
	t.parameter_edit(100,0, [bullet_nums, 10, meg_num], "M1911")
	t.draw()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if bullet_nums != 0:
					bullets = shoot.Bullet(320, 480)
					bullet_nums -= 1
					all_sprite.add(bullets)
				else:
					pygame.mixer.Sound("data/sound/effect/Shot0.wav").play()
				print("TEST")
			if event.key == pygame.K_r:
				if meg_num != 0:
					meg_num -= 1
					bullet_nums = 10
					pygame.mixer.Sound("data/sound/effect/Reload0.wav").play()
				else: pygame.mixer.Sound("data/sound/effect/A Piano.wav").play()


	all_sprite.update()
	all_sprite.draw(root)
	pygame.display.update()
	root.fill(0)