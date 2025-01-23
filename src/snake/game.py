import pygame

# from snake import Food, Settings, Snake
from snake import Food, Settings, Snake


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake Game")
        self.snake = Snake(self)
        self.foods = pygame.sprite.Group()
        for _ in range(10):
            self.foods.add(Food(self))
        self.clock = pygame.time.Clock()
        self.game_active = False

    def run(self):
        while True:
            self._check_events()
            if self.game_active:
                self.snake.update()
                self._check_collisions()
                self._update_screen()
            else:
                self._show_start_screen()

    def _check_events(self):
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
        collisions = pygame.sprite.spritecollide(self.snake, self.foods, True) # type: ignore
        if collisions:
            self.snake.grow()
            for _ in collisions:
                self.foods.add(Food(self))

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.snake.draw()
        self.foods.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.settings.fps)

    def _show_start_screen(self):
        self.screen.fill(self.settings.bg_color)
        font = pygame.font.SysFont(None, 74)
        text = font.render("Snake Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
