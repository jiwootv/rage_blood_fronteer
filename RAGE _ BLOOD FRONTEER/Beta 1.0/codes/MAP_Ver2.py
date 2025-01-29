import json
import os


def get_key(val, dict):
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


class Map:
    def __init__(self, screen, map_dir="data/map_Ver2", pygame_in_game=None, mode="Play"):
        """
        Map 클래스,
        :param screen: pygame의 스크린
        :param map_dir: 맵 위치
        :param pygame_in_game: pygame 객체 (기본값 None)
        :param mode: "Play" or "Edit" (기본값 "Play")
        """

        if pygame_in_game is not None:
            global pygame
            pygame = pygame_in_game
        else:
            import pygame  # 기본 pygame을 참조

        # tile, lava, water, furnance 같은 타일의 이미지 로드
        self.assets = {
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
            "furnance": pygame.image.load("data/img/tile/planet/furnance.png"),
            "Player": pygame.image.load("data/img/player/test.png")
        }

        self.root = screen  # 스크린 설정
        self.tilesize = 60  # 타일 기본 크기
        self.mapW, self.mapH = 0, 0  # map 가로, 세로 설정

        self.tile_list = []
        self.move_pos = [0, 0]

        self.mode = mode
        if self.mode == "Play":
            self.move_speed = 200
        else:
            self.move_speed = 350

        # map 설정
        self.map = {}
        self.map_dir = map_dir

        # 특정 폴더 내 JSON 파일들 전부 읽어오기
        for filename in os.listdir(self.map_dir):
            if filename.endswith(".json"):  # JSON 파일만 처리
                with open(os.path.join(self.map_dir, filename), 'r', encoding='utf-8') as f:
                    self.map[filename] = json.load(f)

    def load_to_list(self, value):
        """
        value에서 가져온 맵 json을 이 클래스의 list들로 변환합니다.
        변하는 리스트는 다음과 같습니다:
            tile_list (json 파일에 있는 타일을 여기에 넣음)
            mapW, mapH
        :param value: json 파일에서 가져온 리스트를 바로 넣습니다.
        예시: load_to_list(json.load(open("data/map/room1.json")))
        """
        self.tile_list = []
        self.mapW, self.mapH = value["size"]
        for w in range(1, self.mapW + 2):
            for h in range(1, self.mapH + 2):
                try:
                    p = value["tilemap"][f"{w};{h}"]
                    self.tile_list.append(p)
                except KeyError:
                    pass

    def draw_set(self):
        """
        draw를 하기에 앞써서 쓰는 코드로 추정
        """
        if self.mode == "Play":
            self.move_pos = self.map["room1.json"]["startpos"]
        else:
            self.move_pos = [0, 0]

        # 모든 assets의 키들 돌아가면서
        # 키가 "Player"로 시작하지 않으면
        # assets[key]의 크기를 타일 크기로 지정한다.
        for i in self.assets.values():
            r = get_key(i, self.assets)
            print(r[:6])
            if r[:6] != "Player":
                self.assets[r] = pygame.transform.scale(self.assets[r], (self.tilesize, self.tilesize))
            else:
                img_w = self.assets[r].get_size()[0]
                change = self.tilesize / img_w
                self.assets[r] = pygame.transform.scale(self.assets[r],
                                                        (self.tilesize, self.assets[r].get_size()[1] * change))

    def draw(self):
        """
        그립니다.
        (당연하게도)
        """
        if self.mode == "Play":
            if len(self.tile_list) != 0:
                # tile을 draw합니다.
                for tile in self.tile_list:
                    try:
                        self.root.blit(self.assets[tile["img"]],
                                       (tile["pos"][0] * self.tilesize - self.tilesize - (self.move_pos[0] - 4.83) * 60,
                                        tile["pos"][1] * self.tilesize - self.tilesize - (self.move_pos[1]-3.5) * 60))

                    except IndexError:
                        pass
            self.root.blit(self.assets["Player"], (290, 150))
        else:
            if len(self.tile_list) != 0:
                # tile을 draw합니다.
                for tile in self.tile_list:
                    try:
                        self.root.blit(self.assets[tile["img"]],
                                       (tile["pos"][0] * self.tilesize - self.tilesize + self.move_pos[0],
                                        tile["pos"][1] * self.tilesize - self.tilesize + self.move_pos[1]))

                    except IndexError:
                        pass

    def mapGet(self, mapNumber):
        """
        map을 반환합니다.
        :param mapNumber: 맵 번호
        :return: 번호에 해당하는 맵
        """
        return self.map[f"room{mapNumber}.json"]

    def get_all_map(self):
        """
        map 전체를 반환합니다.
        :return: self.map
        """
        return self.map

    # def map_dataEdit(self, mapNumber):

    def event(self, delta_time, events=None):
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

        if self.mode == "Play":
            if movetype[0] == 1:  # W
                self.move_pos[1] -= self.move_speed * delta_time

            if movetype[1] == 1:  # S
                self.move_pos[1] += self.move_speed * delta_time

            if movetype[2] == 1:  # D
                self.move_pos[0] += self.move_speed * delta_time

            if movetype[3] == 1:  # A
                self.move_pos[0] -= self.move_speed * delta_time
        else:
            if movetype[0] == 1:
                self.move_pos[1] += self.move_speed * delta_time

            if movetype[1] == 1:
                self.move_pos[1] -= self.move_speed * delta_time

            if movetype[2] == 1:
                self.move_pos[0] -= self.move_speed * delta_time

            if movetype[3] == 1:
                self.move_pos[0] += self.move_speed * delta_time

    def moveposGet(self):
        """
        move_pos (카메라 위치)를 리턴합니다.
        :return: self.move_pos
        """
        return self.move_pos

    def get_map_list(self):
        """
        맵 리스트를 반환합니다.
        :return: self.map의 키
        """
        return self.map.keys()

    def reload_file(self):
        # map 설정
        self.map = {}

        # 특정 폴더 내 JSON 파일들 전부 읽어오기
        for filename in os.listdir(self.map_dir):
            if filename.endswith(".json"):  # JSON 파일만 처리
                with open(os.path.join(self.map_dir, filename), 'r', encoding='utf-8') as f:
                    self.map[filename] = json.load(f)

    def get_size(self):
        """
        맵의 사이즈를 반환합니다.
        :return: [self.mapW, self.mapH]
        """
        return [self.mapW, self.mapH]

    def get_assets(self):
        """
        assets를 반환합니다.
        :return: self.assets
        """
        return self.assets

