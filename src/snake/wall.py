"""
Wall 클래스는 게임의 벽을 정의합니다.
"""

import os

import pygame
from pygame.sprite import Sprite


class Wall(Sprite):
    """
    Wall 클래스는 게임의 벽을 정의하며 벽돌 이미지를 사용합니다.
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
        
        # 이미지 파일 경로 설정
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, 'img', 'brick.gif')
        
        try:
            # 원본 이미지 로드
            self.original_image = pygame.image.load(image_path).convert_alpha()
            
            # 전체 벽의 크기에 맞게 이미지 리사이즈
            self.image = pygame.transform.scale(self.original_image, (width, height))
            
        except pygame.error:
            # 이미지 로드 실패 시 파란색 사각형으로 대체
            self.image = pygame.Surface((width, height))
            self.image.fill((0, 0, 255))
            
        self.rect = self.image.get_rect(topleft=(x, y))

# 2023-10-24