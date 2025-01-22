import code.MAP as M
import pygame


class Building(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, building_size, tilesize, frame_rate=0.02):
        """
        :param image_paths: 애니메이션 프레임 이미지 경로 리스트
        :param position: (x, y) 위치
        :param building_size: 건물의 크기 (가로, 세로 픽셀)
        :param tilesize: 타일 크기 (픽셀 단위)
        :param frame_rate: 프레임 전환 속도
        """
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (building_size, building_size)) for img in image_paths]
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.tilesize = tilesize  # 타일 크기
        self.position = position  # 실제 위치
        self.rect = self.image.get_rect(topleft=(position[0], position[1]))  # 초기화에 tilesize를 사용하지 않음
        self.frame_rate = frame_rate  # 프레임 전환 속도
        self.last_update = 0

        # 애니메이션 상태 변수
        self.animation_mode = "normal"  # "normal", "to_target", "to_original"
        self.target_frame = 0  # 목표 프레임
        self.reverse = False  # 역방향 진행 여부

    def update(self, dt):
        """애니메이션 업데이트"""
        self.last_update += dt
        if self.last_update >= self.frame_rate:
            self.last_update = 0

            # 애니메이션 모드에 따라 동작
            if self.animation_mode == "normal":
                self.current_frame = (self.current_frame + 1) % len(self.images)
            elif self.animation_mode == "to_target":
                if not self.reverse and self.current_frame < self.target_frame:
                    self.current_frame += 1
                elif self.reverse and self.current_frame > self.target_frame:
                    self.current_frame -= 1
            elif self.animation_mode == "to_original":
                if self.current_frame > 0:
                    self.current_frame -= 1

            # 이미지 갱신
            self.image = self.images[self.current_frame]

    def trigger_animation(self, target_frame, reverse=False):
        """
        애니메이션 상태를 변경
        :param target_frame: 이동할 목표 프레임
        :param reverse: 역방향으로 진행 여부
        """
        self.animation_mode = "to_target"
        self.target_frame = target_frame
        self.reverse = reverse

    def reset_animation(self):
        """
        애니메이션 상태를 초기화하여 원래 상태로 돌아감
        """
        self.animation_mode = "to_original"


# 예제 사용법
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

t_dir = "data/img/tile/planet/Building/PlasmaTower"
# 애니메이션에 사용할 이미지 경로 (예제용으로 이미지를 교체하세요)

image_paths = [f"{t_dir}/{img_n}.png" for img_n in range(1, 12)]

animated_sprite = Building(image_paths, (100, 100), 60, 32)

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
all_sprites.add(animated_sprite)

running = True
# 건물 객체 생성
#image_paths = ["frame1.png", "frame2.png", "frame3.png", "frame4.png", "frame5.png"]
building = Building(image_paths, position=(100, 100), building_size=60, tilesize=32)

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
all_sprites.add(building)


state = 2

while running:
    dt = clock.tick(60) / 1000  # delta time 계산
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 조건에 따른 애니메이션 변경
    if state == 1:
        building.trigger_animation(target_frame=10)  # 0~4번 프레임까지 진행
        state = 0
    elif state == 2 and building.current_frame == 10:
        building.trigger_animation(target_frame=0, reverse=True)  # 4~0번 프레임으로 되돌아감
        state = 0

    # 스프라이트 업데이트
    all_sprites.update(dt)

    # 화면 그리기
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()


