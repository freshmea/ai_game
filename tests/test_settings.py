# add path to the snake package
import sys
sys.path.append('C:\Users\Administrator\Documents\ai_game\src\snake')

from snake.settings import Settings

def test_initial_settings():
    """
    Settings 객체의 초기 설정을 테스트합니다.
    """
    settings = Settings()
    assert settings.screen_width == 800
    assert settings.screen_height == 600
    assert settings.bg_color == (0, 0, 0)
    assert settings.fps == 15