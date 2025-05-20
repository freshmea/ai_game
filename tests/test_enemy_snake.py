import os
import sys

import pygame
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from snake import Settings, EnemySnake

@pytest.fixture
def enemy_snake():
    pygame.init()
    settings = Settings()
    screen = pygame.Surface((settings.screen_width, settings.screen_height))
    return EnemySnake(settings, screen)

def test_enemy_snake_moves(enemy_snake):
    initial = enemy_snake.rect.topleft
    enemy_snake.update()
    assert enemy_snake.rect.topleft != initial
