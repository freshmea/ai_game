import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from snake import Settings


def test_initial_settings():
    """
    Settings 객체의 초기 설정을 테스트합니다.
    """
    settings = Settings()
    assert settings.screen_width == 800
    assert settings.screen_height == 600
    assert settings.bg_color == (0, 0, 0)
    assert settings.fps == 30
