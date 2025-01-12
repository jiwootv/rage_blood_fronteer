import pygame, sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
PURPLE = (128, 0, 128)

def text_draw(surface, size, text, color, posx, posy, sort=0):
	font = pygame.font.Font("data\\font\\DungGeunMo.otf", size)
	t = font.render(text, True, color)
	if sort: surface.blit(t, (posx-t.get_size()[0], posy))
	else: surface.blit(t, (posx, posy))

class WidgetBar:
	def __init__(self, x, y, width, height, max_value, icon_id, direction, color, current_value=0):
		self.rect = pygame.Rect(x, y, width, height)
		self.max_value = max_value
		self.current_value = min(current_value, max_value)
		self.icon = pygame.image.load(icon_id)
		self.icon = pygame.transform.scale(self.icon, (height-5, height-5))
		self.direction = direction
		self.color = color
		self.height = height

	def draw(self, screen):
		font_size = int(self.rect.height * 0.6)  # 텍스트 크기를 위젯 바 높이에 비례하여 설정
		font = pygame.font.Font("data\\font\\DungGeunMo.otf", font_size)
		pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=20)
		if self.current_value != 0:

			# Draw background bar


			# Calculate width of the filled part
			fill_width = (self.current_value / self.max_value) * self.rect.width + 10
			fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)

			# Draw filled part
			pygame.draw.rect(screen, self.color, fill_rect, border_radius=20)

			# Draw text
		text_surface = font.render(f"{self.current_value} / {self.max_value}", True, WHITE)
		if self.current_value < self.max_value / 2:
			text_rect = text_surface.get_rect(midleft=(self.rect.x + self.rect.height + 10, self.rect.centery))
		else:
			text_rect = text_surface.get_rect(midright=(self.rect.right - self.rect.height - 10, self.rect.centery))
		screen.blit(text_surface, text_rect)

			# Draw icon
		icon_pos = (self.rect.right - self.rect.height + 15, self.rect.y+self.height/9) if self.direction == 'right' else (self.rect.x + 15, self.rect.y+self.height/9)
		screen.blit(self.icon, icon_pos)

	def update_value(self, new_value):
		self.current_value = min(new_value, self.max_value)

class StatsBar:
	def __init__(self, screen):
		self.screen = screen
		self.hp = 0
		self.rect = pygame.rect.Rect(620 - self.hp, 440, self.hp, 20)
		self.room_N = 0
		self.heartbeat = pygame.mixer.Sound("data\\sound\\effect\\HeartBeat.mp3")
		self.gun_bullet_img = [pygame.image.load("data\\img\\Gun\\bullet1.png"), pygame.image.load("data\\img\\Gun\\bullet2.png")]
		self.gun_bullet_img = list(map(lambda x: pygame.transform.scale(x, (18, 32)), self.gun_bullet_img))
		self.gun_bullets = []
		self.heartbeat.play(-1)
		self.heartbeat.set_volume(0)
		self.now_gun = None
		self.now_gun_name = None

	def parameter_edit(self, *args):
		self.hp = args[0]
		self.room_N = args[1]
		self.rect = pygame.rect.Rect(620 - self.hp, 440, self.hp, 20)
		self.gun_bullets = args[2]
		self.now_gun = pygame.transform.scale(pygame.image.load(f"data/img/gun/{args[3]}.png"), (52, 35))
		self.now_gun_name = args[3]

	def draw(self):
		self._drawNowRoom()
		self._drawStatusBar()
		self._drawNowBullet()
		self.screen.blit(self.now_gun,dest=(15, 390))
		text_draw(self.screen, 30, self.now_gun_name, (255, 255, 255), 15, 360)

	def _drawNowBullet(self):
		a = 100
		text_draw(self.screen, 20, f"{self.gun_bullets[0]} / {self.gun_bullets[2]*self.gun_bullets[1]}", (255, 255, 255), 118, 410, sort=1)
		for i in range(self.gun_bullets[1], 0, -1):  # 전체 탄환 수로 반복문 돌리기
			self.screen.blit(self.gun_bullet_img[int(self.gun_bullets[0]<self.gun_bullets[1]-i+1)], (i*(a/self.gun_bullets[1]), 432))

	def _drawNowRoom(self):
		t = "현재 위치 | GAYGAY YA"
		text_draw(self.screen, 30, t, (255, 255, 255), 0, 0)  # 620-t.__len__()*10,

	def _drawStatusBar(self):
		color = (255, 255, 255)
		h = self.hp // 10

		if h < 2:
			color = pygame.Color("red")
			self.heartbeat.set_volume(1)
		elif h < 4:
			color = (200, 0, 0)
			self.heartbeat.set_volume(0.5)
		elif h < 8:
			color = (255, 255, 0)
			self.heartbeat.set_volume(0.1)
		else: self.heartbeat.set_volume(0)
		text = "HP | {}".format(self.hp)
		text_draw(self.screen, 20, text, color, 620, 420, sort=1)
		pygame.draw.rect(self.screen, color, self.rect)

if __name__ == "__main__":
	pygame.init()
	window = pygame.display.set_mode((640, 480))
	clock = pygame.time.Clock()
	k = 100
	roomnumber = 0
	a, b, c = 10, 10, 3
	asd = 0
	S = StatsBar(window)
	widget_bar = WidgetBar(100, 50, 150, 25, 100, "data/img/ui/notanium1.png", "right",(0, 0, 255),  current_value=0) # 아이콘 경로를 설정해야 합니다.
	while True:
		# if k == 360: k = 0
		window.fill((0))
		#S.parameter_edit(k, roomnumber, (a, b, c))
		#S.draw()
		p = pygame.key.get_pressed()

		if p[pygame.K_u]: asd += 1
		if p[pygame.K_j]: asd -= 1
		widget_bar.update_value(asd)
		widget_bar.draw(window)  # 위젯 바를 그립니다.
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN and not k == 10:
					k -= 10
				if event.key == pygame.K_UP and not k == 200:
					k += 10
				if event.key == pygame.K_t: roomnumber += 1
				if event.key == pygame.K_g: roomnumber -= 1
				if event.key == pygame.K_r and a != b:
					a+=1
				if event.key == pygame.K_f and a != 0: a -= 1
				if event.key == pygame.K_c:
					a = 0
					b += 1
				if event.key == pygame.K_d:
					a = 0
					b -= 1
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				sys.exit()
		pygame.display.update()
		clock.tick(30)
