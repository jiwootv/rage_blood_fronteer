import pygame
# noinspection PyUnresolvedReferences
import codes.attack_alg as atalg
# 위 구문은 원래 작동 안되는게 정상임 ㅋ
# 하지만 실제 실행은 code 폴더가 아닌 외부 폴더, 즉 main 파일들이나 Test 계열에서 실행되기에 문제가 없음.
# 위 noinspection 어쩌구는 Pycharm에서 오류로 표시되는게 거슬려서 저렇게 해놓은거라고 생각하면 됨.

import math

bullet_group = pygame.sprite.Group()

class TurretBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.index = 0
        self.image = pygame.image.load("data/img/gun/bullet1.png")
        self.rect = self.image.get_rect()
        self.r_a = self.image.get_rect().width, self.image.get_rect().height
        self.rect.center = self.pos[0]
        self.image = pygame.transform.scale(self.image, list(map(lambda x: x*1.5, self.r_a)))

        # Calculate the angle between the first and second position
        if len(self.pos) > 1:
            angle = atalg.calculate_angle(self.pos[0], self.pos[1])
            self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.index < len(self.pos) - 1:
            self.index += 1
            self.rect.center = self.pos[self.index]
        else:
            self.kill()



class Turret(pygame.sprite.Sprite):
	def __init__(self, screen, turret_type, turret_pos, radius=10):
		self.turret_type = turret_type
		self.screen = screen
		self.turret_pos = turret_pos
		self.radius = radius
		super().__init__()

	def shoot(self, pos1):
		path_pos = atalg.generate_path(self.turret_pos, pos1, int(atalg.distance(self.turret_pos, pos1)/10))
		bullet_group.add(TurretBullet(path_pos))


	# print(self.path_pos)

	def is_in(self, pos2: list):
		return atalg.radius_detect(self.turret_pos, pos2, self.radius)

	def _debug_circle_draw(self, screen, color=(255, 0, 0)):
		pygame.draw.circle(screen, color, (self.turret_pos), radius=self.radius)

	def update(self):
		#print("UPDATE")
		bullet_group.draw(self.screen)
		bullet_group.update()