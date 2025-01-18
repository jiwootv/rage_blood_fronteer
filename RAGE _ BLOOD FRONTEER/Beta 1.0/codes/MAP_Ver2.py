# this is main source assets.
# Grappic asset or maps.
import json
import os

import pygame
import sys
# import effect

"""
에셋 종류
Bricks1: 일반 벽돌
Bricks2: 이끼 낀 벽돌
Bricks3: 금간 벽돌
"""

DEBUG = False
print(__name__)


class Building(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        """
        이거 아직은 안 쓰는 클래스라 뭐 하는 건지 모르겠음
        :param image_path: image_path 지정
        :param position: (안 씀)
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()


class Map:
    def __init__(self, screen, map_dir="data/map_Ver2"):
        """
        Map 클래스,
        :param screen: pygame의 스크린
        """

        # tile, lava, water, furnance 같은 타일의 이미지 로드
        self.assets = \
            {
                "SpaceTile1": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTile1.png"),
                "SpaceTileCorner1": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileCorner1.png"),
                "SpaceTileCorner2": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileCorner2.png"),
                "SpaceTileCorner3": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileCorner3.png"),
                "SpaceTileCorner4": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileCorner4.png"),
                "SpaceTileSide1": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileSide1.png"),
                "SpaceTileSide2": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileSide2.png"),
                "SpaceTileSide3": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileSide3.png"),
                "SpaceTileSide4": pygame.image.load("data/img/tile/SPACESHIPS/SpaceTileSide4.png"),
                "PlanetFloor1": pygame.image.load("data/img/tile/planet/PlanetFloor1.png"),
                "PlanetFloor2": pygame.image.load("data/img/tile/planet/PlanetFloor2.png"),
                "PlanetFloor3": pygame.image.load("data/img/tile/planet/PlanetFloor3.png"),
                "lava": pygame.image.load("data/img/tile/planet/lava.png"),
                "water": pygame.image.load("data/img/tile/planet/water.png"),
                "furnance": pygame.image.load("data/img/tile/planet/furnance.png")
            }

        self.p_hitbox = pygame.rect.Rect(287, 215, 66, 99)
        print(self.p_hitbox, "SAD")
        self.p_nexthitbox = 0  # 플레이어 이동시 미리 히트박스 계산

        self.root = screen  # 스크린 설정
        self.tilesize = 60  # 타일 기본 크기
        self.mapW, self.mapH = 0, 0  # map 가로, 세로 설정

        self.rect_mask = []
        self.brickPass = False
        self.tile_list = []
        self.new_tile_list = []
        self.mapNumber = 1  # 임시지정
        self.tile_hitboxes = []
        self.TileHitboxIR = []
        self.move_pos = [0, 0]
        self.move_speed = 5

        # 귀여운 미니함수~
        self.value_to_key = lambda x, y: {i for i in x if x[i] == y}

        self.color = (255, 0, 0)
        self.tileEvent = []

        # map 설정
        self.map = {}

        # 특정 폴더 내 JSON 파일들 전부 읽어오기
        for filename in os.listdir(map_dir):
            if filename.endswith(".json"):  # JSON 파일만 처리
                with open(os.path.join(map_dir, filename), 'r', encoding='utf-8') as f:
                    self.map[filename] = json.load(f)

        self.MAP_COUNT = len(self.map)  # JSON 파일 개수

    def get_key(self, val, dict):
        """
        리스트의 키를 가져옵니다.
        :param val: 값
        :param dict: 리스트
        :return: 리스트에 있는 값에 해당하는 키 (없을 경우 None을 반환함)
        """
        for key, value in dict.items():
            if val == value:
                return key

        return None

    def _load(self, mapnumber):
        """
        저장된 맵 json 파일을 불러와 mapNumber, mapW, mapH, tile_list, tile_hitboxes를 정의합니다.
        :param mapnumber: 맵 번호
        """
        self.tile_list = []
        self.tile_hitboxes = []
        with open(f"room{mapnumber}.json") as f:
            self.tempMap = json.load(f)
        if DEBUG:
            print("map size: " + str(self.map[f"room{mapnumber}.json"]["size"]))
        self.mapW, self.mapH = self.map[f"room{mapnumber}.json"]["size"]
        self.mapNumber = mapnumber

        for w in range(1, self.mapW + 2):
            for h in range(1, self.mapH + 2):
                try:
                    p = self.map[f"room{mapnumber}.json"]["tilemap"][f"{w};{h}"]
                    self.tile_list.append(p)
                    if DEBUG:
                        print(f"pos:{w};{h} | " + "type:" + p["type"] + " | img: " + p["img"])
                except KeyError:
                    pass
                    if DEBUG:
                        print("존재하지 않는 칸")
        if DEBUG:
            print("map size:", self.mapW, self.mapH)
        if DEBUG:
            print(type(self.mapH))

    def load_to_list(self, value):
        """
        value에서 가져온 맵 json을 이 클래스의 list들로 변환합니다.
        변하는 리스트는 다음과 같습니다:
            tile_hitboxes ([]으로 바뀜)
            tile_list (json 파일에 있는 타일을 여기에 넣음)
            mapW, mapH
        :param value: json 파일에서 가져온 리스트를 바로 넣습니다.
        예시: load_to_list(json.load(open("data/map/room1.json")))
        (근데 걍 _load 쓰면 되는거 아닌가)
        """
        self.tile_hitboxes = []
        if DEBUG:
            print(value)
        if DEBUG:
            print("map size: " + str(value["size"]))
        self.tile_list = []
        self.mapW, self.mapH = value["size"]
        for w in range(1, self.mapW + 2):
            for h in range(1, self.mapH + 2):
                try:
                    # p = eval(f"self.map{mapnumber}[\"tilemap\"][f\"{w};{h}\"]")
                    p = value["tilemap"][f"{w};{h}"]
                    self.tile_list.append(p)
                    if DEBUG:
                        print(f"pos:{w};{h} | " + "type:" + p["type"] + " | img: " + p["img"])
                except KeyError:
                    pass
                    if DEBUG:
                        print("존재하지 않는 칸")
        if DEBUG:
            print("map size:", self.mapW, self.mapH)
            print(type(self.mapH))

    def draw_set(self):
        """
        draw를 하기에 앞써서 쓰는 코드로 추정
        """
        # self.move_pos를 self.map[1]["startpos"] (0, -1) 에 30을 곱해 넣습니다. (0, -30)
        self.move_pos = list(map(lambda x: x * 30, self.map["room1.json"]["startpos"]))

        # new_tile_list에 타일 크기가 적용된 사진을 넣습니다.
        self.new_tile_list = []
        for i in range(len(self.tile_list)):
            self.new_tile_list.append(
                pygame.transform.scale(self.assets[self.tile_list[i]['img']], (self.tilesize, self.tilesize)))

        # tile_hitboxes에 tile_list만큼 ""를 넣습니다 (초기화)
        for _ in self.tile_list:
            self.tile_hitboxes.append("")

        # 모든 assets의 키들 돌아가면서
        # 키가 "Player"로 시작하지 않으면
        # assets[key]의 크기를 타일 크기로 지정한다.
        for i in self.assets.values():
            r = self.get_key(i, self.assets)
            if DEBUG:
                print(r)
            print(r[:6])
            if r[:6] != "Player":
                self.assets[r] = pygame.transform.scale(self.assets[r], (self.tilesize, self.tilesize))

    def var_set(self, type, result):
        """
        self.type를 result로 정합니다.
        (왜 만든거임)
        :param type: 변수
        :param result: 값
        """
        setattr(self, type, result)

    def draw(self):
        """
        그립니다.
        (당연하게도)
        """
        if len(self.tile_list) != 0:
            # tile_list에서 type가 wall이면 tile_hitboxes를 설정합니다.
            # x = tile.x * tilesize - tilesize + movepos.x
            # y = tile.y * tilesize - tilesize + movepos.y
            for i in range(len(self.tile_list)):
                try:
                    x = self.tile_list[i]["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0]
                    y = self.tile_list[i]["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]
                    if self.tile_list[i]["type"] == "wall":
                        self.tile_hitboxes[i] = pygame.Rect(x, y, self.tilesize, self.tilesize)
                except IndexError:
                    pass

            # 플레이어의 히트박스를 설정합니다...? (안 씀)
            self.p_hitbox = pygame.Rect(287, 215, 66, 99)

            # tile을 draw합니다.
            for tile in self.tile_list:
                try:
                    self.root.blit(self.assets[tile["img"]],
                                   (tile["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0],
                                    tile["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]))

                except IndexError:
                    pass

            if DEBUG:
                pygame.draw.rect(self.root, self.color, self.p_hitbox)

    def brickPassSet(self, result):
        """
        brickPass를 result로 설정합니다.
        왜 쓰는건지 아직 모름...
        :param result: 값 (bool)
        """
        self.brickPass = result

    def mapGet(self, mapNumber):
        """
        map을 반환합니다.
        :param mapNumber: 맵 번호
        :return: 번호에 해당하는 맵
        """
        if DEBUG:
            print("TEST", str(self.map[f"room{mapNumber}.json"]))
        return self.map[f"room{mapNumber}.json"]

    # def map_dataEdit(self, mapNumber):

    def event(self):
        self.TileHitboxIR = []
        self.tileEvent = []
        # TileHitboxIR 사이즈 지정 (tile_list의 사이즈 동기화)
        for i in range(self.tile_list.__len__()):
            self.TileHitboxIR.append("None")
        # IRID 지정
        # (TileHitboxIR에 타일 범위의 Rect를 설정)
        for i in range(len(self.tile_list)):
            x = self.tile_list[i]["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0]
            y = self.tile_list[i]["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]
            self.TileHitboxIR[i] = pygame.Rect(x, y, self.tilesize, self.tilesize)

        # IRID 설정
        for tileIR in self.TileHitboxIR:

            if self.p_hitbox.colliderect(tileIR):
                self.tileEvent.append(self.tile_list[self.TileHitboxIR.index(tileIR)]["IRID"])

        # 충돌 / 이동감지
        # (이동은 movetile이라는 list를 만들어서 그걸로 이벤트 처리)
        collides = [0, 0, 0, 0]
        movetype = [0, 0, 0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            movetype[0] = 1
        if keys[pygame.K_s]:
            movetype[1] = 1
        if keys[pygame.K_d]:
            movetype[2] = 1
        if keys[pygame.K_a]:
            movetype[3] = 1

        if movetype[0] == 1 and not collides[0]:
            self.move_pos[1] += self.move_speed

        if movetype[1] == 1 and not collides[1]:
            self.move_pos[1] -= self.move_speed

        if movetype[2] == 1 and not collides[2]:
            self.move_pos[0] -= self.move_speed

        if movetype[3] == 1 and not collides[3]:
            self.move_pos[0] += self.move_speed
        return movetype

    def moveposGet(self):
        """
        move_pos (카메라 위치)를 리턴합니다.
        :return: self.move_pos
        """
        return self.move_pos


if __name__ == "__main__":
    pygame.init()
    Screen = pygame.display.set_mode((640, 480))
    M = Map(Screen)
    Clock = pygame.time.Clock()
    ROOMNUMBER = 1
    M._load(ROOMNUMBER)


    def main():
        a = 1
        global ROOMNUMBER
        M.draw_set()
        while True:
            Screen.fill(0)
            Mtype = M.event()

            for i in range(4):
                if Mtype[i] == 1:
                    a = i
                    break

            M.draw()

            Screen.blit(M.assets[f"Player{a + 1}"], (287, 215))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for i in M.tileEvent:
                if i == 1:
                    ROOMNUMBER += 1
                    M._load(ROOMNUMBER)
                    M.draw_set()
            Clock.tick(60)


    main()
