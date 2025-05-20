import os
import time
import random

import pygame

from .food import Food
from .models import create_db_and_tables, get_high_scores, save_score
from .settings import Settings
from .snake import Snake
from .enemy_snake import EnemySnake
from .ui import UI
from .wall import Wall


class Game:
    """
    Game 클래스는 게임의 주요 로직을 정의합니다.
    """
    def __init__(self):
        """
        Game 객체를 초기화합니다.
        """
        pygame.init()
        create_db_and_tables()  # DB 초기화
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake Game")
        
        # 배경화면 로드 및 설정 (여러 이미지를 로드하여 주기적으로 교체)
        self.backgrounds = []
        for path in self.settings.background_image_paths:
            try:
                bg = pygame.image.load(path)
                bg = pygame.transform.scale(
                    bg,
                    (self.settings.screen_width, self.settings.screen_height),
                )
                self.backgrounds.append(bg)
            except pygame.error:
                continue
        self.current_background = self.backgrounds[0] if self.backgrounds else None
        self.last_background_change_time = time.time()
            
        # 공통 폰트 객체 생성
        self.font = None
        try:
            current_dir = os.path.dirname(__file__)
            self.font_path = os.path.join(current_dir, 'data', 'malgun.ttf')
            self.font = pygame.font.Font(self.font_path, 20)
        except Exception:
            self.font = pygame.font.SysFont(None, 20)
        # Food 생성 전에 UI 영역 및 벽 두께 정의
        self.ui_height = 60          # docstring: UI 영역 높이 (상단)
        self.wall_thickness = 20     # docstring: 벽 두께 설정
        self.pizzas_eaten = 0        # docstring: 피자 먹은 개수 초기화
        self.snake = Snake(self.settings, self.screen)
        self.enemy_snakes = pygame.sprite.Group()
        self._spawn_enemy_snake()
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_interval = 30  # 초마다 적 뱀 추가
        self.ui = UI(self)           # docstring: UI 인스턴스 생성 (self.font를 사용)
        self.foods = pygame.sprite.Group()
        for _ in range(10):
            self.foods.add(Food(self))
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.walls = pygame.sprite.Group()
        self._create_walls()
        self.last_move_time = pygame.time.get_ticks() / 1000.0
        self.start_time = time.time()  # 게임 시작 시간 기록
        self.high_scores = get_high_scores()  # 최고 점수 로드

    def run(self):
        """
        게임 루프를 실행합니다.
        """
        while True:
            self._check_events()
            if self.game_active:
                current_time = pygame.time.get_ticks() / 1000.0
                keys = pygame.key.get_pressed()
                
                # 키 상태 확인하여 뱀 방향 업데이트
                if keys[pygame.K_a]:
                    self.snake.rotate_left()
                if keys[pygame.K_d]:
                    self.snake.rotate_right()

                self.snake.update()
                for enemy in self.enemy_snakes:
                    enemy.update()

                if time.time() - self.last_enemy_spawn_time >= self.enemy_spawn_interval:
                    self._spawn_enemy_snake()
                    self.last_enemy_spawn_time = time.time()

                self._check_collisions()
                self._check_enemy_collision()
                self._check_wall_collision()
                self._check_self_collision()
                self._update_screen()
            else:
                self._show_start_screen()

    def _check_events(self):
        """
        게임 이벤트를 처리합니다.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_active = True
                elif event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    pygame.quit()
                    exit()

    def _check_collisions(self):
        """
        뱀과 음식의 충돌을 확인합니다.
        """
        collisions = pygame.sprite.spritecollide(self.snake, self.foods, True)  # type: ignore
        if collisions:
            self.snake.grow()
            
            # 새로운 피자 생성 및 게임 상태 업데이트
            for _ in collisions:
                self.foods.add(Food(self))
            self.pizzas_eaten += len(collisions)
            # 속도 증가: 5피자마다 snake_speed 1씩 증가
            self.snake.speed = 1.0 + self.pizzas_eaten / 10

    def _check_enemy_collision(self):
        """플레이어 뱀이 적 뱀과 충돌하는지 확인한다."""
        if pygame.sprite.spritecollide(self.snake, self.enemy_snakes, False):
            self._end_game()

    def _check_wall_collision(self):
        """
        뱀의 머리가 벽과 충돌하는지 확인합니다.
        """
        if pygame.sprite.spritecollide(self.snake, self.walls, False):
            self._end_game()

    def _check_self_collision(self):
        """
        뱀의 머리가 자신의 몸과 충돌하는지 확인합니다.
        처음 40개의 세그먼트는 충돌 검사에서 제외합니다.
        """
        head = self.snake.segments[0]
        # 40번째 세그먼트 이후부터 충돌 검사
        for segment in self.snake.segments[40:]:
            if head.colliderect(segment):
                self._end_game()
                return

    def _end_game(self):
        """
        게임 종료 상태로 전환하고 엔딩 화면을 표시합니다.
        """
        self.game_active = False
        play_time = time.time() - self.start_time
        if hasattr(self, 'initials'):
            save_score(self.initials, self.pizzas_eaten, play_time)
            self.high_scores = get_high_scores()  # 점수 저장 후 최고 점수 다시 로드
        self._show_ending_screen()

    def _show_ending_screen(self):
        """
        엔딩 화면을 표시합니다.
        """
        font = self.font
        line_height = 30
        while True:
            self.screen.fill(self.settings.bg_color)
            
            # 게임 오버 텍스트
            end_text = font.render(
                f"Game Over - 이니셜: {getattr(self, 'initials', '---')}  점수: {self.pizzas_eaten}개",
                True, (255, 255, 255))
            end_rect = end_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 4))
            self.screen.blit(end_text, end_rect)
            
            # 최고 점수 표시
            high_score_text = font.render("최고 점수", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(
                center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - line_height))
            self.screen.blit(high_score_text, high_score_rect)
            
            # 상위 5개 점수 표시
            start_y = self.settings.screen_height // 2
            for i, score in enumerate(self.high_scores):
                score_text = font.render(
                    f"{i+1}. {score.player_initials}: {score.score}점 ({score.play_time:.1f}초)",
                    True, (255, 255, 255))
                score_rect = score_text.get_rect(
                    center=(self.settings.screen_width // 2, start_y + i * line_height))
                self.screen.blit(score_text, score_rect)
            
            # 안내 메시지
            prompt_text = font.render("스페이스바: 재시작, ESC 혹은 Q: 종료", True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(
                center=(self.settings.screen_width // 2, 
                       start_y + (len(self.high_scores) + 2) * line_height))
            self.screen.blit(prompt_text, prompt_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__init__()
                        return
                    elif event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        pygame.quit()
                        exit()
            self.clock.tick(self.settings.fps)

    def _create_walls(self):
        """
        게임 영역의 경계에 벽 Sprite를 생성합니다.
        wall_thickness를 기준으로 정사각형 벽돌들을 배치합니다.
        """
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        wt = self.wall_thickness
        
        # 왼쪽 벽 (UI 영역 아래부터)
        for y in range(self.ui_height, sh - wt, wt):
            left_wall = Wall(0, y, wt, wt)
            self.walls.add(left_wall)
        
        # 오른쪽 벽
        for y in range(self.ui_height, sh - wt, wt):
            right_wall = Wall(sw - wt, y, wt, wt)
            self.walls.add(right_wall)
        
        # 상단 벽 (UI와 게임 영역의 경계)
        for x in range(0, sw, wt):
            top_wall = Wall(x, self.ui_height, wt, wt)
            self.walls.add(top_wall)
        
        # 하단 벽
        for x in range(0, sw, wt):
            bottom_wall = Wall(x, sh - wt, wt, wt)
            self.walls.add(bottom_wall)

    def _spawn_enemy_snake(self):
        """적 뱀을 생성하여 그룹에 추가한다."""
        enemy = EnemySnake(self.settings, self.screen)
        enemy.x = random.randint(40, self.settings.screen_width - 60)
        enemy.y = random.randint(self.ui_height + 40, self.settings.screen_height - 60)
        for seg in enemy.segments:
            seg.x = int(enemy.x)
            seg.y = int(enemy.y)
        enemy.rect.topleft = (int(enemy.x), int(enemy.y))
        self.enemy_snakes.add(enemy)

    def _update_screen(self):
        """
        화면을 업데이트합니다.
        """
        # 배경 그리기
        if self.backgrounds:
            current_time = time.time()
            if current_time - self.last_background_change_time >= self.settings.background_change_interval:
                self.current_background = random.choice(self.backgrounds)
                self.last_background_change_time = current_time
            if self.current_background:
                game_area_background = self.current_background.subsurface(
                    (
                        0,
                        self.ui_height,
                        self.settings.screen_width,
                        self.settings.screen_height - self.ui_height,
                    )
                )
                self.screen.blit(game_area_background, (0, self.ui_height))
        else:
            # 배경화면이 없는 경우 단색 배경
            pygame.draw.rect(self.screen, self.settings.bg_color,
                           (0, self.ui_height,
                            self.settings.screen_width,
                            self.settings.screen_height - self.ui_height))
        
        # UI 영역 그리기
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (0, 0, self.settings.screen_width, self.ui_height))
        self.ui.update()
        self.ui.draw(self.screen)

        # 게임 요소 그리기
        self.walls.draw(self.screen)
        self.snake.draw()
        for enemy in self.enemy_snakes:
            enemy.draw()
        self.foods.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.settings.fps)

    def _show_start_screen(self):
        """
        시작 화면을 표시하고 초기 이니셜 3글자를 입력받습니다.
        """
        initials = ""
        font = self.font
        while True:
            self.screen.fill(self.settings.bg_color)
            # 게임 제목 표시 (영어 -> 한글)
            title_text = font.render("뱀 게임", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 3))
            self.screen.blit(title_text, title_rect)
            # 이니셜 입력 프롬프트 표시 (영어 -> 한글)
            prompt = f"이니셜 입력 (3글자): {initials}"
            prompt_text = font.render(prompt, True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # 이니셜이 3글자인 경우 사용자 이니셜 저장 및 게임 시작
                        if len(initials) == 3:
                            self.initials = initials
                            self.game_active = True
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif event.unicode.isalpha() and len(initials) < 3:
                        initials += event.unicode.upper()
            self.clock.tick(self.settings.fps)
# 2023-10-24
