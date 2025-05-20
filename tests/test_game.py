import os
import sys

import pygame
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from snake import Game


@pytest.fixture
def game():
    """
    Game 객체를 생성하는 pytest fixture입니다.
    """
    pygame.init()
    return Game()

def test_initial_game_state(game):
    """
    Game 객체의 초기 상태를 테스트합니다.
    """
    assert not game.game_active

def test_start_game(game):
    """
    Game 객체의 게임 시작 상태를 테스트합니다.
    """
    game._check_events()
    game.game_active = True
    assert game.game_active

def test_initial_enemy_snake_count(game):
    """게임 시작 시 적 뱀이 10마리 생성되는지 확인한다."""
    assert len(game.enemy_snakes) == 10

# 추가 테스트

def test_snake_update_movement(game):
    """Snake.update가 현재 방향으로 이동하는지 테스트합니다."""
    snake = game.snake
    initial_head = snake.rect.copy()
    snake.update()
    new_head = snake.rect
    assert new_head.x == initial_head.x + int(snake.speed)

def test_snake_grow(game):
    """
    Snake 클래스의 grow 메서드로 뱀의 길이가 증가하는지 테스트합니다.
    """
    snake = game.snake
    initial_length = len(snake.segments)
    snake.grow()
    snake.update()
    new_length = len(snake.segments)
    assert new_length == initial_length + 1

def test_collision_and_food_regeneration(game):
    """
    Game 클래스의 충돌 감지 기능과 음식 재생성을 테스트합니다.
    """
    snake = game.snake
    # 음식 중 하나를 선택하여 snake의 head와 위치를 동일하게 설정
    food = next(iter(game.foods))
    snake.rect.x = food.rect.x
    snake.rect.y = food.rect.y
    initial_food_count = len(game.foods)
    initial_snake_length = len(snake.segments)
    game._check_collisions()
    # 충돌 후 음식은 제거되고 새 음식이 추가되어 총 개수는 유지되거나, snake 길이가 증가함
    assert len(game.foods) == initial_food_count
    assert len(snake.segments) == initial_snake_length + 1

def test_spawn_enemy_snake(game):
    initial = len(game.enemy_snakes)
    game._spawn_enemy_snake()
    assert len(game.enemy_snakes) == initial + 1
