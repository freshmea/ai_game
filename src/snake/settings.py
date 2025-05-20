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

        # 배경화면 설정 (10개의 배경화면을 순회하면서 사용)
        current_dir = os.path.dirname(__file__)
        self.background_image_paths = [
            os.path.join(current_dir, 'img', f'bg{i}.gif') for i in range(10)
        ]
        # 배경 교체 주기(초)
        self.background_change_interval = 5
