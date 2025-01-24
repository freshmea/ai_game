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
        self.fps = 15
