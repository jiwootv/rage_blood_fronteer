# this is main source assets.
# Grappic asset or maps.
import json
import pygame
import sys
#import effect
"""
에셋 종류
Bricks1: 일반 벽돌
Bricks2: 이끼 낀 벽돌
Bricks3: 금간 벽돌
"""

DEBUG = False
print(__name__)

import pygame

class Building(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()


class Map:
    def __init__(self, screen):
        self.assets = \
            {
                "SpaceTile1":pygame.image.load("data/img/tile/SPACESHIPS/SpaceTile1.png"),
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

        # Map Count ( 맵 개수 ) 지정
        self.MAP_COUNT = 5
        with open("data/map/room1.json") as f:
            self.map1 = json.load(f)
        with open("data/map/room2.json") as f:
            self.map2 = json.load(f)
        with open("data/map/room3.json") as f:
            self.map3 = json.load(f)
        with open("data/map/room4.json") as f:
            self.map4 = json.load(f)
        with open("data/map/room5.json") as f:
            self.map5 = json.load(f)

    def get_key(self, val, dict):

        for key, value in dict.items():
            if val == value:
                return key

        return "key doesn't exist"

    def _load(self, mapnumber):
        self.tile_list = []
        self.tile_hitboxes = []
        with open(f"room{mapnumber}.json") as f:
            self.tempMap = json.load(f)
        if DEBUG:
            print("map size: " + str(eval('self.map%d["size"]' % mapnumber)))
        self.mapW, self.mapH = eval('self.map%d["size"]' % mapnumber)
        self.mapNumber = mapnumber

        for w in range(1, self.mapW + 2):
            for h in range(1, self.mapH + 2):
                try:
                    p = eval(f"self.map{mapnumber}[\"tilemap\"][f\"{w};{h}\"]")
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
                    if DEBUG: print(f"pos:{w};{h} | " + "type:" + p["type"] + " | img: " + p["img"])
                except KeyError:
                    pass
                    if DEBUG: print("존재하지 않는 칸")
        if DEBUG:
            print("map size:", self.mapW, self.mapH)
            print(type(self.mapH))

    def draw_set(self):
        self.move_pos = list(map(lambda x: x * 30, self.map1["startpos"]))
        self.new_tile_list = []
        # print(self.move_pos)
        for i in range(len(self.tile_list)):
            self.new_tile_list.append(
                pygame.transform.scale(self.assets[self.tile_list[i]['img']], (self.tilesize, self.tilesize)))

        for _ in self.tile_list:
            self.tile_hitboxes.append("")
        # 2871031
        # 칸 크기 조정
        for i in self.assets.values():
            r = self.get_key(i, self.assets)
            if DEBUG: print(r)
            print(r[:6])
            if r[:6] != "Player": self.assets[r] = pygame.transform.scale(self.assets[r], (self.tilesize, self.tilesize))


    def var_set(self, type, result):
        eval(f"self.{type} = {result}")

    def draw(self):
        json_map1 = self.tile_list
        if len(self.tile_list) != 0:

            for i in range(len(self.new_tile_list)):
                # print(i)
                try:
                    x = json_map1[i]["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0]
                    y = json_map1[i]["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]
                    if json_map1[i]["type"] == "wall": self.tile_hitboxes[i] = (
                        pygame.Rect(x, y, self.tilesize, self.tilesize))
                except IndexError:
                    pass
            self.p_hitbox = pygame.Rect(287, 215, 66, 99)

            for i in range(len(self.tile_list)):
                try:
                    json_map1 = self.tile_list
                    # print(len(self.tile_list), len(self.new_tile_list))
                    # print(i, len(m), json_map1)
                    # try:
                    self.root.blit(self.assets[json_map1[i]["img"]],
                                   (json_map1[i]["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0],
                                    json_map1[i]["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]))

                except IndexError:
                    pass
            # except IndexError: print("인덱스 에러 발생")

            if DEBUG:
                pygame.draw.rect(self.root, self.color, self.p_hitbox)
            #pygame.draw.rect(self.root, self.color, self.tile_hitboxes[0])



    def brickPassSet(self, result):
        self.brickPass = result

    def mapGet(self, mapNumber):
        if DEBUG: print("TEST", str(eval('self.map%d' % mapNumber)))
        return eval('self.map%d' % int(mapNumber))

    # def map_dataEdit(self, mapNumber):

    def event(self):
        #pygame.draw.rect(self.root, (200, 0, 0), self.p_hitbox)
        self.TileHitboxIR = []
        self.tileEvent = []
        for i in range(self.tile_list.__len__()): self.TileHitboxIR.append("None")
        # IRID 지정
        #(self.tile_list.__len__(), self.tile_hitboxes.__len__())
        for i in range(len(self.tile_list)):
            x = self.tile_list[i]["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0]
            y = self.tile_list[i]["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]
            self.TileHitboxIR[i] = (pygame.Rect(x, y, self.tilesize, self.tilesize))

        # IRID 설정
        for tileIR in self.TileHitboxIR:

            if self.p_hitbox.colliderect(tileIR):
                self.tileEvent.append(self.tile_list[self.TileHitboxIR.index(tileIR)]["IRID"])

        # 충돌 / 이동감지

        self.collides = [0, 0, 0, 0]
        self.movetype = [0, 0, 0, 0]
        P = pygame.key.get_pressed()

        if P[pygame.K_w]: self.movetype[0] = 1
        if P[pygame.K_s]: self.movetype[1] = 1
        if P[pygame.K_d]: self.movetype[2] = 1
        if P[pygame.K_a]: self.movetype[3] = 1

        self.collide = False
        for i in [0, 1, 2, 3]:  # 총 4개의 방향 이동 감지
            a, b = 287, 215
            next_x, next_y = 66, 99
            if self.movetype[i]:  # 만약 i번째 키가 눌려있는가:
                c = 0
                if i == 0:  # 만약 위로 이동했을 때:
                    c += 1
                    b -= self.move_speed
                    next_y += self.move_speed
                if i == 1:
                    c += 1
                    b += self.move_speed
                    next_y += self.move_speed
                if i == 3:
                    c += 1
                    a -= self.move_speed
                if i == 2:
                    c += 1
                    a += self.move_speed
                self.p_nexthitbox = pygame.Rect(a, b, next_x, next_y)
                if DEBUG:
                    pygame.draw.rect(self.root, self.color, self.p_nexthitbox)
                for tile_rect in self.tile_hitboxes:
                    if tile_rect != '' and not self.brickPass:
                        #(tile_rect)
                        if self.p_nexthitbox.colliderect(tile_rect):
                            self.collides[i] = 1
                            break

        if self.movetype[0] == 1 and not self.collides[0]:
            self.move_pos[1] += self.move_speed

        if self.movetype[1] == 1 and not self.collides[1]:
            self.move_pos[1] -= self.move_speed

        if self.movetype[2] == 1 and not self.collides[2]:
            self.move_pos[0] -= self.move_speed

        if self.movetype[3] == 1 and not self.collides[3]:
            self.move_pos[0] += self.move_speed
        return self.movetype
    def moveposGet(self):
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


            Screen.blit(M.assets[f"Player{a+1}"], (287, 215))
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
