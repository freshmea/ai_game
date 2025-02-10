import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from snake import Food, Game


@pytest.fixture
def food():
    """
    Food 객체를 생성하는 pytest fixture입니다.
    """
    game = Game()
    return Food(game)

def test_food_position(food):
    """
    Food 객체의 위치를 테스트합니다.
    """
    assert 0 <= food.rect.x < food.game.settings.screen_width
    assert 0 <= food.rect.y < food.game.settings.screen_height
