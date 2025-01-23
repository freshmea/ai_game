import random

import pygame
from pygame.sprite import Sprite


class Food(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, game.settings.screen_width - 20)
        self.rect.y = random.randint(0, game.settings.screen_height - 20)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
