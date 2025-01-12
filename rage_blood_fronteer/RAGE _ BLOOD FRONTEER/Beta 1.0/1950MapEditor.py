# 와 위대한 시작..
# 1950 게임 맵 에디터 메인 코드

"""IRID 타입 총정리
0번: 없음
1번: 다음 방 이동
2번: 이전 방 이동
3번: 없음
"""

import code.button as bt  # 절대 빼먹으면 안되는 것
import code.MAP as m_ap
import pygame
import sys
import json
DEBUG = False
pygame.init()  # pygame 모듈 초기화


class Main:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		self.select_SE = pygame.mixer.Sound(r'data/sound/effect/A Piano.wav')
		self.collect_SE = pygame.mixer.Sound(r'data/sound/effect/Connect.wav')

		if DEBUG: print("성공적으로 Main 클래스가 로드되었습니다")
		self.screen = pygame.display.set_mode((880, 660))  # 640, 480의 2배
		self.preview = pygame.rect.Rect(0, 0, 640, 480)
		self.preview1 = pygame.rect.Rect(0, 480, 640, 180)
		self.preview2 = pygame.rect.Rect(640, 0, 240, 660)
		self.clock = pygame.time.Clock()

		self.tile_size = 60
		self.map_max = 30

		# self.preview1 = pygame.rect.Rect(0, 0, 640, 480)
		self.Map_c = m_ap.Map(self.screen)
		self.file_index = 0
		self.select_IRID = 0
		self.mouserect = 0
		self.select_tileType = 1
		self.map_load_onoff = 0
		self.saveButton = bt.Button(20, 600, pygame.image.load("data/img/save_btn.png"), 1)
		self.loadButton = bt.Button(220, 600, pygame.image.load("data/img/load_btn.png"), 1)
		self.is_wall = 1
		self.playing = True
		# 현재 map list 생성
		self.now_map = list()
		# self.now_map.append("BIN")
		for i in range(1, self.Map_c.MAP_COUNT + 1):
			self.now_map.append(self.Map_c.mapGet(i))
		if DEBUG: print(self.now_map, "\nasd")

		self.IRID_list = ["없음", "다음 방 이동", "이전 방 이동"]
		pygame.display.set_caption("1950 Map Editor")
		self.text = lambda size, text, color, x, y: self.screen.blit(
			pygame.font.Font(r"data/font/DungGeunMo.otf", size).render(text, 1, color), (x, y))
		self.pos_x, pos_y = 0, 0

		self.tile_name_list = list(self.Map_c.assets.keys())
		self.tile_name_list.insert(0, "삭제 모드")
		if DEBUG: print(self.tile_name_list)
		self.map_maxcount = self.Map_c.MAP_COUNT

	def draw_preview(self):
		pygame.draw.rect(self.screen, (0, 0, 0), self.preview)

	def draw_hider(self):

		# self.x1, self.y1 = list(map(lambda pos_x: pos_x*self.tile_size, [self.pos_x, self.y])) print(self.x1,
		# self.y1) self.tile_rect1, self.tile_rect2 = pygame.rect.Rect(self.x1, self.y1, self.tile_size,
		# self.tile_size), pygame.rect.Rect(self.pos_x*self.tile_size+5, self.y*self.tile_size+5, self.tile_size-5,
		# self.tile_size-5) pygame.draw.rect(self.screen, (255, 255, 255), self.tile_rect1) pygame.draw.rect(
		# self.screen, (255, 255, 255), self.tile_rect2)

		pygame.draw.rect(self.screen, (0, 0, 70), self.preview1)
		pygame.draw.rect(self.screen, (0, 0, 70), self.preview2)

	def lines(self):
		for k in range(0, self.map_max * self.tile_size + 1, self.tile_size):  # 가로선
			x, y = self.Map_c.moveposGet()
			pygame.draw.line(self.screen, (255, 255, 255), start_pos=(x, k + y),
							 end_pos=(x + self.map_max * self.tile_size, k + y))

		for k in range(0, self.map_max * self.tile_size + 1, self.tile_size):  # 가로선
			x, y = self.Map_c.moveposGet()
			pygame.draw.line(self.screen, (255, 255, 255), start_pos=(k + x, y),
							 end_pos=(k + x, self.map_max * self.tile_size + y))

	def event(self):

		x, y = pygame.mouse.get_pos()
		self.mouserect = pygame.rect.Rect(x, y, 10, 10)
		pygame.draw.rect(self.screen, (255, 255, 255), self.mouserect)  # 마우스에 Rect개체 덮어 씨우기

		x, y = self.Map_c.moveposGet()  # 맵의 이동 좌표 얻기
		x1, y1 = pygame.mouse.get_pos()  # 마우스 좌표얻기
		self.pos_x, self.pos_y = (x * -1 + x1) // self.tile_size, (
				y * -1 + y1) // self.tile_size  # 그걸 Tile size로 나누어 커서가 위치한 pos 계산
		# print(self.now_map[self.file_index - 1]["tilemap"][f"{self.pos_x};{self.pos_y}"])

		# print(self.pos_x, self.pos_y)  # 그 pos 출력

		# 지금 당장 savefile 저장
		# noinspection PyTypeChecker
		# 위 주석은 무시하셈.

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_i:
					self.select_IRID += 1
					self.select_SE.play()
				if event.key == pygame.K_k and not self.select_IRID == 0:
					self.select_IRID -= 1
					self.select_SE.play()
				if event.key == pygame.K_f and not self.select_tileType == 0:
					if DEBUG: print("POPIPOPIPO")
					self.select_tileType -= 1
					self.select_SE.play()
				if event.key == pygame.K_r and len(self.tile_name_list) != self.select_tileType + 1:
					self.select_tileType += 1
					self.select_SE.play()
				if event.key == pygame.K_UP:
					self.file_index += 1
					# if type(self.now_map[self.file_index-1]) == type(""):
					# self.now_map[self.file_index-1] = self.Map_c.mapGet(self.file_index)
					# print(self.now_map[self.file_index-1])
					# print(self.now_map)
					self.select_SE.play()

					if DEBUG: print("asd")
				if event.key == pygame.K_DOWN and not self.file_index == 0:
					self.file_index -= 1
					# noinspection PyTypeChecker
					# if type(self.now_map[self.file_index-1]) == type(""):
					# self.now_map[self.file_index-1] = self.Map_c.mapGet(self.file_index-1)
					# print(self.now_map[self.file_index-1])
					# print(self.now_map)
					self.select_SE.play()

				if event.key == pygame.K_l:
					self.select_SE.play()
					self.is_wall += 1
					self.is_wall = self.is_wall % 2
				# print("WALL or FLOOR : {}".format(self.is_wall))

		# 버튼 드로우
		if self.loadButton.draw(self.screen):
			self.Map_c.load_to_list(self.now_map[self.file_index])
			self.collect_SE.play()

		# 마우스 클릭 감지 및, 맵 에디터 설정
		if pygame.mouse.get_pressed()[0] and self.pos_x > -1 and self.pos_y > -1:  # 마우스 좌클릭 감지
			if self.mouserect.colliderect(self.preview):
				try:
					if self.select_tileType != 0:
						if DEBUG: print(["floor", "wall"][self.is_wall])
						self.now_map[self.file_index]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"] = {
							"img": self.tile_name_list[self.select_tileType], "type": ["floor", "wall"][self.is_wall],
							"IRID": self.select_IRID,
							"pos": [self.pos_x + 1, self.pos_y + 1]}
					else:
						if DEBUG: print('Delete')
						del self.now_map[self.file_index]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"]
					self.Map_c.load_to_list(self.now_map[self.file_index])
				except KeyError:
					if DEBUG: print("None")

	def nowMapGet(self):
		return self.now_map

	def save(self):
		print("SAVING...")
		for i in range(int(self.map_maxcount)):
			if DEBUG: print(i)
			a = str(json.dumps(self.now_map[i], indent=4, sort_keys=True))
			# print(a)
			with open("data\\map\\room%d.json" % int(i + 1), "w") as file:
				if DEBUG: print(self.now_map[i])
				file.write(a)
				if DEBUG: print("GAY")

	def run(self):
		self.Map_c.load_to_list(self.Map_c.mapGet(1))
		self.Map_c.draw_set()
		self.Map_c.brickPassSet(1)
		while self.playing:

			self.screen.fill((0, 0, 0))
			try:
				a = self.IRID_list[self.select_IRID]
			except:
				a = "존재하지 않는 IRID"

			self.draw_preview()

			self.Map_c.draw()
			self.Map_c.event()

			self.lines()
			self.draw_hider()
			self.event()
			self.text(30, "현재 맵 파일 번호: %d" % int(self.file_index + 1), (255, 255, 255), 500, 600)
			self.text(30, a, (255, 255, 255), 600, 550)
			self.text(30, "현재 IRID: %d" % self.select_IRID, (255, 255, 255), 600, 500)
			self.text(30, "현재 좌표: %d;%d" % (self.pos_x + 1, self.pos_y + 1), (255, 255, 255), 300, 500)
			try:
				self.text(30,
						  "현재 타일:" + self.now_map[self.file_index - 1]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"][
							  "img"], (255, 255, 255), 300, 550)
			except KeyError:
				self.text(30, "현재 타일: 없음", (255, 255, 255), 300, 550)
			self.text(30, f"현재 선택 타일", (255, 255, 255), 650, 0)
			self.text(30, f"벽 여부: {bool(self.is_wall)}", (255, 255, 255), 650, 100)

			try:
				self.text(19,
						  f"현재 타일 벽 여부: {self.now_map[self.file_index - 1]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"]["type"]}",
						  (255, 255, 255), 650, 150)
			except KeyError:
				self.text(19, f"현재 타일 벽 여부: None", (255, 255, 255), 650, 150)
			self.text(20, f"{self.tile_name_list[self.select_tileType]}", (255, 255, 255), 700, 80)
			# 미리보기 드로우
			if self.select_tileType != 0:
				self.screen.blit(
					pygame.transform.scale(self.Map_c.assets[self.tile_name_list[self.select_tileType]], (40, 40)),
					(750, 40))
			pygame.display.update()

			self.clock.tick(60)
		# print(self.now_map[self.file_index])
		# print(json.dumps(self.now_map[self.file_index], indent=4, separators=("{", "="), sort_keys=True))


M = Main()
M.run()
if DEBUG: print("이게맞나")
if DEBUG: print(M.map_maxcount)
M.save()
