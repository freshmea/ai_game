import pygame
from pygame.sprite import Sprite


class Snake(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)
        self.segments = [self.rect]
        self.direction = pygame.K_RIGHT

    def update(self, *args, **kwargs):
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
        if head.x >= self.game.settings.screen_width:
            head.x = 0
        elif head.x < 0:
            head.x = self.game.settings.screen_width - 20
        elif head.y >= self.game.settings.screen_height:
            head.y = 0
        elif head.y < 0:
            head.y = self.game.settings.screen_height - 20

        self.segments = [head] + self.segments[:-1]
        self.rect = self.segments[0]

    def change_direction(self, key):
        if key == pygame.K_w and self.direction != pygame.K_DOWN:
            self.direction = pygame.K_UP
        elif key == pygame.K_a and self.direction != pygame.K_RIGHT:
            self.direction = pygame.K_LEFT
        elif key == pygame.K_s and self.direction != pygame.K_UP:
            self.direction = pygame.K_DOWN
        elif key == pygame.K_d and self.direction != pygame.K_LEFT:
            self.direction = pygame.K_RIGHT

    def grow(self):
        self.segments.append(self.segments[-1].copy())

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(self.game.screen, (0, 255, 0), segment)
