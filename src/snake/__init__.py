"""
snake 패키지는 Snake 게임의 주요 구성 요소를 포함합니다.
"""

from .food import Food
from .game import Game
from .settings import Settings
from .snake import Snake

__all__ = ['Food', 'Settings', 'Snake', 'Game']

# 2023-10-04
