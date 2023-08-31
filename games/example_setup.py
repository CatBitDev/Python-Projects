import sys
import pygame
from pygame import Vector2
# Game settings
SCREEN_SIZE = Vector2(640, 480)
FLAGS = pygame.HWSURFACE
VSYNC = 1
SCREEN_SURFACE = pygame.display.set_mode(SCREEN_SIZE, FLAGS, VSYNC)
SCREEN_UPDATE = pygame.USEREVENT
FRAMES_PER_SECOND = pygame.time.Clock()
FPS = 60
TICKS = 20


class GameManager:
    def __init__(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def tick_update(self, delta_time):
        pass


# Pygame setup
class Main:
    def __init__(self):
        self.__running = True
        self.delta_time = 0
        self.last_tick = 0
        self.game_manager = GameManager()

    def on_init(self):
        pygame.init()
        pygame.time.set_timer(SCREEN_UPDATE, TICKS)
        self.on_execute()

    def on_exit(self):
        self.__running = False
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if not self.__running:
            self.on_exit()
        # Main loop
        while self.__running:
            for event in pygame.event.get():
                # Game exit
                if event.type == pygame.QUIT:
                    self.on_exit()
                # Tick update
                if event.type == SCREEN_UPDATE:
                    self.game_manager.tick_update(self.delta_time)
            # Clear display
            SCREEN_SURFACE.fill(pygame.Color("white"))
            # Update game
            self.game_manager.update()
            self.game_manager.draw()
            pygame.display.update()
            # Calculate delta time
            t = pygame.time.get_ticks()
            self.delta_time = (t - self.last_tick) / 1000.0
            self.last_tick = t
            # Lock game FPS
            FRAMES_PER_SECOND.tick(FPS)


if __name__ == '__main__':
    game = Main()
    game.on_init()
