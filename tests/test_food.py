import pytest

# add path to the snake package
import sys
sys.path.append('C:\Users\Administrator\Documents\ai_game\src\snake')

from snake.food import Food
from snake.game import Game
from snake.settings import Settings

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
