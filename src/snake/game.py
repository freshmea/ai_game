import pygame

from .food import Food
from .settings import Settings
from .snake import Snake
from .ui import UI  # docstring: UI 클래스 임포트
from .wall import Wall  # docstring: Wall 클래스 임포트


class Game:
    """
    Game 클래스는 게임의 주요 로직을 정의합니다.
    """
    def __init__(self):
        """
        Game 객체를 초기화합니다.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake Game")
        # 공통 폰트 객체 생성
        self.font = None
        try:
            self.font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 20)
        except Exception:
            self.font = pygame.font.SysFont(None, 20)
        # Food 생성 전에 UI 영역 및 벽 두께 정의
        self.ui_height = 60          # docstring: UI 영역 높이 (상단)
        self.wall_thickness = 20     # docstring: 벽 두께 설정
        self.pizzas_eaten = 0        # docstring: 피자 먹은 갯수 초기화
        self.snake = Snake(self.settings, self.screen)
        self.ui = UI(self)           # docstring: UI 인스턴스 생성 (self.font를 사용)
        self.foods = pygame.sprite.Group()
        for _ in range(10):
            self.foods.add(Food(self))
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.walls = pygame.sprite.Group()
        self._create_walls()
        # 뱀의 이동 간격(초): 초기 0.5초, 마지막 이동 시간 초기화
        self.snake_move_interval = 0.5
        self.last_move_time = pygame.time.get_ticks() / 1000.0

    def run(self):
        """
        게임 루프를 실행합니다.
        """
        while True:
            self._check_events()
            if self.game_active:
                current_time = pygame.time.get_ticks() / 1000.0
                if current_time - self.last_move_time >= self.snake_move_interval:
                    self.snake.update()
                    self.last_move_time = current_time
                self._check_collisions()
                self._check_wall_collision()  # 벽 충돌 검사
                self._check_self_collision()   # 자기 자신과 충돌 검사
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
                elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    self.snake.change_direction(event.key)

    def _check_collisions(self):
        """
        뱀과 음식의 충돌을 확인합니다.
        """
        collisions = pygame.sprite.spritecollide(self.snake, self.foods, True) # type: ignore
        if collisions:
            self.snake.grow()
            for _ in collisions:
                self.foods.add(Food(self))
            self.pizzas_eaten += len(collisions)
            # 속도 증가: 5피자마다 snake_move_interval 0.05초 감소 (최소 0.1초)
            new_interval = max(0.1, 0.5 - 0.05 * (self.pizzas_eaten // 5))
            self.snake_move_interval = new_interval

    def _check_wall_collision(self):
        """
        뱀의 머리가 벽과 충돌하는지 확인합니다.
        """
        if pygame.sprite.spritecollide(self.snake, self.walls, False):
            self._end_game()

    def _check_self_collision(self):
        """
        뱀의 머리가 자신의 몸과 충돌하는지 확인합니다.
        """
        head = self.snake.segments[0]
        for segment in self.snake.segments[1:]:
            if head.colliderect(segment):
                self._end_game()
                return

    def _end_game(self):
        """
        게임 종료 상태로 전환하고 엔딩 화면을 표시합니다.
        """
        self.game_active = False
        self._show_ending_screen()

    def _show_ending_screen(self):
        """
        엔딩 화면을 표시합니다.
        
        이니셜과 점수를 표시하고, 스페이스바를 누르면 게임을 재시작하며,
        ESC 또는 Q를 누르면 게임을 종료합니다.
        """
        font = self.font  # game에서 생성한 공통 폰트 사용
        while True:
            self.screen.fill(self.settings.bg_color)
            end_text = font.render(
                f"Game Over - 이니셜: {getattr(self, 'initials', '---')}  점수: {self.pizzas_eaten}개",
                True, (255, 255, 255))
            prompt_text = font.render("스페이스바: 재시작, ESC 혹은 Q: 종료", True, (255, 255, 255))
            end_rect = end_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 3))
            prompt_rect = prompt_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
            self.screen.blit(end_text, end_rect)
            self.screen.blit(prompt_text, prompt_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__init__()  # 게임 초기 상태로 재시작
                        return
                    elif event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        pygame.quit()
                        exit()
            self.clock.tick(self.settings.fps)

    def _create_walls(self):
        """
        게임 영역의 경계에 벽 Sprite를 생성합니다.
        
        UI와 게임 영역의 경계를 포함하여 좌측, 우측, 상단(게임 영역 시작) 및 하단 벽을 생성합니다.
        """
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        wt = self.wall_thickness
        # 왼쪽 벽 (게임 영역: UI 영역 아래)
        left_wall = Wall(0, self.ui_height, wt, sh - self.ui_height)
        # 오른쪽 벽
        right_wall = Wall(sw - wt, self.ui_height, wt, sh - self.ui_height)
        # 상단 벽: UI와 게임 영역의 경계 표시
        top_wall = Wall(0, self.ui_height, sw, wt)
        # 하단 벽
        bottom_wall = Wall(0, sh - wt, sw, wt)
        self.walls.add(left_wall, right_wall, top_wall, bottom_wall)

    def _update_screen(self):
        """
        화면을 업데이트합니다.
        """
        # UI 영역 그리기 (상단 50px)
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, self.settings.screen_width, self.ui_height))
        self.ui.update()        # UI 정보 갱신
        self.ui.draw(self.screen)  # UI 정보 표시

        # 게임 영역 그리기 (UI 영역 아래)
        # 게임 영역 배경 채우기
        pygame.draw.rect(self.screen, self.settings.bg_color, 
                         (0, self.ui_height, self.settings.screen_width, self.settings.screen_height - self.ui_height))
        # 벽 그리기
        self.walls.draw(self.screen)
        self.snake.draw()
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
# 2023-10-04
