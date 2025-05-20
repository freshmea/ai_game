import time

import pygame
from pygame.sprite import Sprite


class UI(Sprite):
    """
    UI 클래스는 게임 정보를 화면에 표시합니다.

    피자를 먹은 개수와 실행 경과 시간을 표시합니다.
    """
    def __init__(self, game):
        """
        UI 객체를 초기화합니다.

        매개변수:
        game (Game): 게임 객체 (피자 먹은 개수 속성을 포함해야 함)
        """
        super().__init__()
        self.game = game
        # game 폰트를 사용
        self.font = self.game.font
        self.start_time = time.time()
        self.image = None
        self.rect = None
        self.pizzas_eaten = 0
        self.update()

    def update(self):
        """
        게임 정보를 갱신합니다.
        """
        elapsed_time = time.time() - self.start_time
        count = getattr(self.game, 'pizzas_eaten', self.pizzas_eaten)
        initials = getattr(self.game, 'initials', '')
        speed = getattr(self.game.snake, 'speed', 2)  # 뱀의 이동 간격(초)
        ui_text = f"이니셜: {initials}  피자: {count}개, 경과시간: {elapsed_time:.1f}초, 속도: {speed:.2f}"
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
# 2023-10-24
