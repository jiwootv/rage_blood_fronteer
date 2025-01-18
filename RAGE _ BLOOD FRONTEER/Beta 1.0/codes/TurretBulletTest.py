import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Sprite Example")

# 색상 정의
WHITE = (255, 255, 255)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))  # 파란색으로 채우기
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Sprite 그룹 생성
all_sprites = pygame.sprite.Group()

# Player 객체 생성 및 그룹에 추가
player = Player(100, 100)
all_sprites.add(player)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 모든 스프라이트 업데이트
    all_sprites.update()

    # 화면을 하얀색으로 채우기
    screen.fill(WHITE)

    # 모든 스프라이트 그리기
    all_sprites.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(FPS)

# Pygame 종료
pygame.quit()
sys.exit()
