import random
import pygame
from .snake import Snake

class EnemySnake(Snake):
    """무작위로 움직이는 적 뱀 클래스."""

    def __init__(self, settings, screen):
        super().__init__(settings, screen)
        # 방향 전환 주기(초)
        self.change_interval = 1.0
        self.last_change_time = pygame.time.get_ticks() / 1000.0

    def update(self, *args, **kwargs):
        """무작위로 방향을 바꾸며 이동한다."""
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_change_time >= self.change_interval:
            if random.random() < 0.5:
                self.rotate_left()
            else:
                self.rotate_right()
            self.last_change_time = current_time
        super().update(*args, **kwargs)
