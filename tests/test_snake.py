import os
import sys

import pygame
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from snake import Settings, Snake


@pytest.fixture
def snake():
    """
    Snake 객체를 생성하는 pytest fixture입니다.
    """
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    return Snake(settings, screen)

def test_initial_position(snake):
    """
    Snake 객체의 초기 위치를 테스트합니다.
    """
    assert snake.rect.topleft == (100, 100)

def test_change_direction(snake):
    """
    Snake 객체의 방향 변경을 테스트합니다.
    """
    snake.change_direction(pygame.K_w)
    assert snake.direction == pygame.K_UP
    snake.change_direction(pygame.K_a)
    assert snake.direction == pygame.K_LEFT
    snake.change_direction(pygame.K_s)
    assert snake.direction == pygame.K_DOWN
    snake.change_direction(pygame.K_d)
    assert snake.direction == pygame.K_RIGHT

def test_grow(snake):
    """
    Snake 객체의 길이 증가를 테스트합니다.
    """
    initial_length = len(snake.segments)
    snake.grow()
    assert len(snake.segments) == initial_length + 1
