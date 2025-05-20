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
    screen = pygame.Surface((settings.screen_width, settings.screen_height))
    return Snake(settings, screen)

def test_initial_position(snake):
    """Snake 객체의 초기 위치를 테스트합니다."""
    assert snake.rect.topleft == (200, 200)

def test_rotate_left_and_right(snake):
    """rotate_left와 rotate_right 동작을 테스트합니다."""
    original = snake.direction_vector.copy()
    snake.rotate_left()
    assert snake.direction_vector != original
    left_vector = snake.direction_vector.copy()
    snake.rotate_right()
    # 왼쪽 회전 후 오른쪽 회전하면 원래 방향으로 돌아와야 함
    assert pytest.approx(snake.direction_vector.x) == pytest.approx(original.x)
    assert pytest.approx(snake.direction_vector.y) == pytest.approx(original.y)
    # rotate_left로 변경된 값과 현재 값은 달라야 함
    assert (snake.direction_vector.x != left_vector.x) or (snake.direction_vector.y != left_vector.y)

def test_grow(snake):
    """
    Snake 객체의 길이 증가를 테스트합니다.
    """
    initial_length = len(snake.segments)
    snake.grow()
    snake.update()
    assert len(snake.segments) == initial_length + 1
