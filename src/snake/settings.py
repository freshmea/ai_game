import os


class Settings:
    """
    Settings 클래스는 게임 설정을 정의합니다.
    """
    def __init__(self):
        """
        Settings 객체를 초기화합니다.
        """
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.fps = 30

        # 배경화면 설정
        current_dir = os.path.dirname(__file__)
        self.background_image_path = os.path.join(current_dir, 'img', 'bg.gif')
