import pygame
from pygame.sprite import Sprite


class Snake(Sprite):
    """
    Snake 클래스는 뱀의 속성 및 동작을 정의합니다.
    """
    def __init__(self, settings, screen):
        """
        Snake 객체를 초기화합니다.

        매개변수:
        settings (Settings): 게임 설정 객체
        screen (pygame.Surface): 게임 화면 객체
        """
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)
        self.segments = [self.rect]
        self.direction = pygame.K_RIGHT
        self.grow_pending = 0  # 성장 대기 횟수 초기화

    def update(self, *args, **kwargs):
        """
        뱀의 위치를 업데이트합니다.
        """
        head = self.rect.copy()
        if self.direction == pygame.K_RIGHT:
            head.x += 20
        elif self.direction == pygame.K_LEFT:
            head.x -= 20
        elif self.direction == pygame.K_UP:
            head.y -= 20
        elif self.direction == pygame.K_DOWN:
            head.y += 20

        # grow_pending 값에 따라 마지막 꼬리 제거 여부 결정
        if self.grow_pending > 0:
            self.segments = [head] + self.segments
            self.grow_pending -= 1
        else:
            self.segments = [head] + self.segments[:-1]
        self.rect = self.segments[0]

    def change_direction(self, key):
        """
        뱀의 이동 방향을 변경합니다.

        매개변수:
        key (int): 방향키 값
        """
        if key == pygame.K_w and self.direction != pygame.K_DOWN:
            self.direction = pygame.K_UP
        elif key == pygame.K_a and self.direction != pygame.K_RIGHT:
            self.direction = pygame.K_LEFT
        elif key == pygame.K_s and self.direction != pygame.K_UP:
            self.direction = pygame.K_DOWN
        elif key == pygame.K_d and self.direction != pygame.K_LEFT:
            self.direction = pygame.K_RIGHT

    def grow(self):
        """
        뱀의 길이를 증가시킵니다.
        """
        self.grow_pending += 1

    def draw(self):
        """
        뱀을 화면에 그립니다.
        """
        for segment in self.segments:
            pygame.draw.rect(self.screen, (0, 255, 0), segment)
