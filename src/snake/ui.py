import time

import pygame
from pygame.sprite import Sprite


class UI(Sprite):
    """
    UI 클래스는 게임 정보를 화면에 표시합니다.
    
    피자를 먹은 갯수와 실행 경과 시간을 표시합니다.
    """
    def __init__(self, game):
        """
        UI 객체를 초기화합니다.
        
        매개변수:
        game (Game): 게임 객체 (피자 먹은 갯수 속성을 포함해야 함)
        """
        super().__init__()
        self.game = game
        self.start_time = time.time()
        try:
            # Windows 기본 폰트 경로에서 malgun.ttf 사용
            self.font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 36)
        except Exception:
            # 예외 발생 시 fallback으로 기본 폰트 사용
            self.font = pygame.font.SysFont(None, 36)
            print('malgun.ttf 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.')
        self.image = None
        self.rect = None
        # 피자 먹은 갯수 초기화 (게임 객체에서 관리되지 않으면 독자적으로 관리)
        self.pizzas_eaten = 0
        self.update()

    def update(self):
        """
        게임 정보를 갱신합니다.
        """
        elapsed_time = time.time() - self.start_time
        # 게임 객체에 피자 먹은 갯수가 있다면 사용, 없으면 로컬 변수 사용
        count = getattr(self.game, 'pizzas_eaten', self.pizzas_eaten)
        ui_text = f"피자: {count}개, 경과시간: {elapsed_time:.1f}초"
        self.image = self.font.render(ui_text, True, (255, 255, 255))
        self.rect = self.image.get_rect(topleft=(10, 10))

    def draw(self, surface):
        """
        UI 정보를 화면에 그립니다.
        
        매개변수:
        surface (pygame.Surface): 게임 화면 객체
        """
        surface.blit(self.image, self.rect)

# 2023-10-04
