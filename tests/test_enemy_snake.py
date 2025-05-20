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

def test_enemy_snake_wraps(enemy_snake):
    """화면을 벗어나면 반대편에서 나타나는지 확인한다."""
    enemy_snake.change_interval = float("inf")
    enemy_snake.direction_vector = pygame.math.Vector2(1, 0)
    sw = enemy_snake.settings.screen_width
    enemy_snake.x = sw + 5
    for seg in enemy_snake.segments:
        seg.x = int(enemy_snake.x)
    enemy_snake.update()
    assert 0 <= enemy_snake.rect.x <= sw
