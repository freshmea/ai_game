import os
import sys
import time
import unittest

# SDL 비디오 드라이버를 dummy로 설정하여 화면 없이 테스트할 수 있도록 한다.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from snake.ui import UI

class DummySnake:
    """
    DummySnake 클래스는 UI 테스트용 더미 뱀 객체입니다.
    """
    def __init__(self):
        self.speed = 2
        self.direction_vector = pygame.math.Vector2(1, 0)
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect(topleft=(200, 200))
        self.segments = [pygame.Rect(200, 200, 20, 20)]
        for i in range(39):
            segment = pygame.Rect(200, 200, 20, 20)
            self.segments.append(segment)

class DummyGame:
    """
    DummyGame 클래스는 UI 테스트용 더미 게임 객체입니다.
    """
    def __init__(self):
        self.pizzas_eaten = 5
        self.font = pygame.font.Font(None, 36)
        self.snake = DummySnake()
class TestUI(unittest.TestCase):
    """
    UI 클래스 동작 테스트
    """
    def setUp(self):
        """
        테스트 환경을 초기화합니다.
        """
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.game = DummyGame()
        self.ui = UI(self.game)

    def test_ui_update(self):
        """
        UI 업데이트 시 이미지와 rect가 생성되는지 확인합니다.
        """
        self.ui.update()
        self.assertIsNotNone(self.ui.image)
        self.assertIsNotNone(self.ui.rect)

    def test_ui_draw(self):
        """
        UI draw 메서드가 예외 없이 실행되는지 확인합니다.
        """
        try:
            self.ui.draw(self.screen)
        except Exception as e:
            self.fail(f"UI.draw() raised Exception: {e}")

    def tearDown(self):
        """
        pygame 종료 처리를 합니다.
        """
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

# 2023-10-04
