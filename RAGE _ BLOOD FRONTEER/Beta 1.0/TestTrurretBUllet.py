import pygame

# Pygame 스프라이트 초기화
pygame.init()

# TurretBullet 클래스 정의
class TurretBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.index = 0
        self.image = pygame.Surface((10, 10))  # 총알의 크기 설정
        self.image.fill((255, 0, 0))  # 빨간색 총알
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[self.index]

    def update(self):
        if self.index < len(self.pos) - 1:
            self.index += 1
            self.rect.topleft = self.pos[self.index]
        else:
            self.kill()  # 경로가 끝나면 스프라이트 제거

# Pygame 화면 설정 (예시)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TurretBullet Example")

# 스프라이트 그룹 생성
bullet_group = pygame.sprite.Group()

# TurretBullet 인스턴스 생성 및 그룹에 추가
bullet_path = [[100, 100], [200, 200], [300, 300], [400, 400], [500, 500]]
bullet = TurretBullet(bullet_path)
bullet_group.add(bullet)

# 게임 루프 (예시)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 지우기
    screen.fill((0, 0, 0))

    # 스프라이트 그룹 업데이트 및 그리기
    bullet_group.update()
    bullet_group.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
