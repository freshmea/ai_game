import random

import pygame
from pygame.sprite import Sprite


class Food(Sprite):
    """
    Food 클래스는 음식의 속성 및 동작을 정의합니다.
    """
    def __init__(self, game):
        """
        Food 객체를 초기화합니다.

        매개변수:
        game (Game): 게임 객체
        """
        super().__init__()
        self.game = game
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, game.settings.screen_width - 20)
        self.rect.y = random.randint(game.ui_height, game.settings.screen_height - 20)

    def draw(self):
        """
        음식을 화면에 그립니다.
        """
        self.game.screen.blit(self.image, self.rect)
