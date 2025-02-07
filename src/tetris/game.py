# -*- coding: utf-8 -*-
"""
모듈: game.py
설명: pygame을 사용해 테트리스 게임 기본 실행을 구현합니다.
"""

import sys

import pygame


class TetrisGame:
    """테트리스 게임을 위한 클래스입니다."""

    def __init__(self, width=300, height=600):
        """
        게임 초기화 메소드
        Args:
            width (int): 게임 창 너비
            height (int): 게임 창 높이
        """
        # ...existing code...
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris Game")
        self.clock = pygame.time.Clock()

    def run(self):
        """
        게임 루프 실행 메소드
        """
        # ...existing code...
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # 배경 검은색 채우기
            pygame.display.flip()
            self.clock.tick(60)  # 초당 60 프레임

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    """
    프로그램 실행 진입점
    """
    game = TetrisGame()
    game.run()

# 2023-10-07
