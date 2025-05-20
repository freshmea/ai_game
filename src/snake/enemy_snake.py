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
        """무작위로 방향을 바꾸며 이동하고 화면을 넘어가면 반대편에서 등장한다."""
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_change_time >= self.change_interval:
            if random.random() < 0.5:
                self.rotate_left()
            else:
                self.rotate_right()
            self.last_change_time = current_time

        super().update(*args, **kwargs)

        # 화면 경계를 넘어가면 반대편에서 등장하도록 위치 조정
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        new_x, new_y = self.x, self.y
        wrapped = False

        if self.rect.right < 0:
            new_x = sw
            wrapped = True
        elif self.rect.left > sw:
            new_x = 0
            wrapped = True

        if self.rect.bottom < 0:
            new_y = sh
            wrapped = True
        elif self.rect.top > sh:
            new_y = 0
            wrapped = True

        if wrapped:
            dx = new_x - self.x
            dy = new_y - self.y
            self.x = new_x
            self.y = new_y
            for seg in self.segments:
                seg.x += int(dx)
                seg.y += int(dy)
            self.rect.topleft = (int(self.x), int(self.y))
