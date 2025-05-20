import pygame
from pygame.sprite import Sprite
import os
import math
import colorsys
import random
vec = pygame.math.Vector2

class Snake(Sprite):
    """
    Snake 클래스는 뱀의 속성 및 동작을 정의합니다.
    """
    def __init__(self, settings, screen):
        """
        Snake 객체를 초기화합니다.

        매개변수:
        settings (Settings): 게임 설정 객체
        screen (pygame.Surface): 게임 화면 객체
        """
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.direction_vector = vec(1, 0)  # 초기 방향은 오른쪽

        # 이미지 로드 및 설정
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, 'img', 'snake_head.gif')
        # 이미지 로드 후 크기 조정
        self.original_image = pygame.image.load(image_path).convert()
        self.original_image = pygame.transform.scale(self.original_image, (20, 20))
        # 흰색을 투명하게 처리
        self.original_image.set_colorkey((255, 255, 255))

        self.image = pygame.transform.rotate(self.original_image,
                                          self.direction_vector.angle_to(pygame.math.Vector2(0, -1)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 200)
        # 초기 40개의 세그먼트로 시작
        self.segments = [pygame.Rect(200, 200, 20, 20)]
        for i in range(39):
            segment = pygame.Rect(200, 200, 20, 20)
            self.segments.append(segment)
        self.grow_pending = 0
        # 초기 각도 설정
        self.angle = 0


        # 회전 각속도 (도/초)
        self.rotation_speed = 4.0
        # 이동 속도
        self.speed = 1.0
        self.current_angle = 0  # 현재 각도

        # float 기반 위치 추적을 위한 변수 추가
        self.x = float(200)
        self.y = float(200)
        self.current_angle = 0.0

        # 무지개 색을 위한 색상 순환 값
        self.color_cycle = 0.0

    def update(self, *args, **kwargs):
        """
        뱀의 위치를 업데이트합니다.
        float 기반으로 부드러운 이동을 구현합니다.
        """
        # float 위치 업데이트
        self.x += self.direction_vector.x * self.speed
        self.y += self.direction_vector.y * self.speed

        # 색상 순환 값 업데이트
        self.color_cycle = (self.color_cycle + 0.02) % 1.0

        # 머리 위치 업데이트 (float -> int 변환)
        head = self.segments[0]
        head.x = int(self.x)
        head.y = int(self.y)

        # 세그먼트 업데이트
        if self.grow_pending > 0:
            tail = self.segments[-1].copy()
            self.segments.append(tail)
            self.grow_pending -= 1

        # 세그먼트 이동 (첫 번째 세그먼트는 이미 업데이트됨)
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i-1].x
            self.segments[i].y = self.segments[i-1].y

        # 이미지 위치 업데이트
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def rotate_left(self):
        """
        뱀을 왼쪽으로 회전시킵니다.
        """
        self.direction_vector.rotate_ip(-self.rotation_speed)
        self.image = pygame.transform.rotate(self.original_image,
                                          self.direction_vector.angle_to(pygame.math.Vector2(0, -1)))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def rotate_right(self):
        """
        뱀을 오른쪽으로 회전시킵니다.
        """
        self.direction_vector.rotate_ip(self.rotation_speed)
        self.image = pygame.transform.rotate(self.original_image,
                                          self.direction_vector.angle_to(pygame.math.Vector2(0, -1)))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def grow(self):
        """
        뱀의 길이를 증가시킵니다.
        한 번에 20개의 세그먼트를 추가합니다.
        """
        self.grow_pending += 20  # 20개씩 세그먼트 추가

    def draw(self):
        """
        뱀을 화면에 그립니다.
        먼저 몸통을 그리고 마지막에 머리를 그립니다.
        """
        # 몸통 그리기 (초기 10개 세그먼트는 머리와 겹치므로 제외)
        for idx, segment in enumerate(self.segments[10:]):
            hue = (self.color_cycle + idx * 0.05) % 1.0
            brightness = 0.8 + 0.2 * random.random()
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, brightness)
            color = (int(r * 255), int(g * 255), int(b * 255))
            pygame.draw.circle(
                self.screen, color, segment.center, segment.width // 2
            )

        # 머리 그리기 (마지막에 그려서 항상 보이게 함)
        self.screen.blit(self.image, self.rect)