import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from snake import Game


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
