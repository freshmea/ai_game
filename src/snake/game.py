import pygame

from .food import Food
from .settings import Settings
from .snake import Snake


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
        self.snake = Snake(self.settings, self.screen)
        self.foods = pygame.sprite.Group()
        for _ in range(10):
            self.foods.add(Food(self))
        self.clock = pygame.time.Clock()
        self.game_active = False

    def run(self):
        """
        게임 루프를 실행합니다.
        """
        while True:
            self._check_events()
            if self.game_active:
                self.snake.update()
                self._check_collisions()
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

    def _update_screen(self):
        """
        화면을 업데이트합니다.
        """
        self.screen.fill(self.settings.bg_color)
        self.snake.draw()
        self.foods.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.settings.fps)

    def _show_start_screen(self):
        """
        시작 화면을 표시합니다.
        """
        self.screen.fill(self.settings.bg_color)
        font = pygame.font.SysFont(None, 74)
        text = font.render("Snake Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
