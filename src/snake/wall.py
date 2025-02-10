import pygame
from pygame.sprite import Sprite


class Wall(Sprite):
    """
    Wall 클래스는 게임 벽을 정의합니다.
    
    파란색 사각형 이미지로 표시됩니다.
    """
    def __init__(self, x, y, width, height):
        """
        Wall 객체를 초기화합니다.
        
        매개변수:
        x (int): 벽의 x 좌표
        y (int): 벽의 y 좌표
        width (int): 벽의 너비
        height (int): 벽의 높이
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))  # 파란색
        self.rect = self.image.get_rect(topleft=(x, y))

# 2023-10-04
