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

        # 화면을 벗어나면 반대쪽에서 나오게 함
        if head.x >= self.settings.screen_width:
            head.x = 0
        elif head.x < 0:
            head.x = self.settings.screen_width - 20
        elif head.y >= self.settings.screen_height:
            head.y = 0
        elif head.y < 0:
            head.y = self.settings.screen_height - 20

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
        self.segments.append(self.segments[-1].copy())

    def draw(self):
        """
        뱀을 화면에 그립니다.
        """
        for segment in self.segments:
            pygame.draw.rect(self.screen, (0, 255, 0), segment)
