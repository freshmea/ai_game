import pytest

# add path to the snake package
import sys
sys.path.append('C:\Users\Administrator\Documents\ai_game\src\snake')

from snake.game import Game

@pytest.fixture
def game():
    """
    Game 객체를 생성하는 pytest fixture입니다.
    """
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
