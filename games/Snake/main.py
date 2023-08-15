import sys
import pygame
import random
import math
from pygame import Vector2

# Game settings
BLOCK_SIZE = 20
BOARD_SIZE = 20
SCREEN_SIZE = Vector2(BLOCK_SIZE * BOARD_SIZE, BLOCK_SIZE * BOARD_SIZE)
FPS = 60
TICKS = 20
VSYNC = 1
FLAGS = pygame.HWSURFACE
FRAMES_PER_SECOND = pygame.time.Clock()
SCREEN_SURFACE = pygame.display.set_mode(SCREEN_SIZE, FLAGS, VSYNC)
SCREEN_UPDATE = pygame.USEREVENT


class Fruit:
    def __init__(self):
        self.color = pygame.Color("azure")
        self.position = pygame.math.Vector2
        self.new_position()

    def draw(self):
        fixed_x, fixed_y = self.position.x * BLOCK_SIZE, self.position.y * BLOCK_SIZE
        fruit_rect = pygame.Rect(fixed_x, fixed_y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN_SURFACE, self.color, fruit_rect)

    def get_position(self): return self.position
    def new_position(self): self.position = Vector2(random.randint(1, BOARD_SIZE - 1),
                                                    random.randint(1, BOARD_SIZE - 1))


class Snake:

    def __init__(self):
        self.body = [Vector2(2, 2), Vector2(2, 3), Vector2(2, 4)]
        self.direction = Vector2(0, 0)
        self.speed = 0
        self.add_block = False
        self.color = pygame.Color("chartreuse4")

    def input(self):
        # todo : fix snake turn
        keys = pygame.key.get_pressed()
        # Move up
        if keys[pygame.K_w]:
            self.direction = Vector2(0, -1)
        # Move down
        if keys[pygame.K_s]:
            self.direction = Vector2(0, 1)
        # Move right
        if keys[pygame.K_d]:
            self.direction = Vector2(1, 0)
        # Move left
        if keys[pygame.K_a]:
            self.direction = Vector2(-1, 0)

    def move(self, delta_time):
        acceleration = math.pow(0.5, (delta_time * 0.5))
        self.speed += acceleration
        if self.speed > 10:
            self.speed = self.speed % 10
            if self.add_block:
                self.body.insert(0, self.body[0] + self.direction)
                self.add_block = False
                return
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def draw(self):
        for block in self.body:
            fixed_x, fixed_y = block.x * BLOCK_SIZE, block.y * BLOCK_SIZE
            block_rect = pygame.Rect(fixed_x, fixed_y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN_SURFACE, self.color, block_rect)

    def get_body(self):
        return self.body[1:]

    def get_head(self):
        return self.body[0]

    def new_block(self):
        self.add_block = True


# Main game logic
class GameManager:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def restart(self):
        self.snake = Snake()
        self.fruit.new_position()

    def draw(self):
        self.fruit.draw()
        self.snake.draw()

    def collision(self):
        # Snake collision with self
        for block in self.snake.get_body():
            # todo : BUG game keep restating on startup
            if self.snake.get_head() == block:
                self.restart()
                return
        # Snake collision with walls
        if self.snake.get_head().x >= BOARD_SIZE or self.snake.get_head().x < 0:
            self.restart()
            return
        if self.snake.get_head().y >= BOARD_SIZE or self.snake.get_head().y < 0:
            self.restart()
            return
        # snake collision with fruit
        if self.snake.get_head() == self.fruit.get_position():
            self.snake.new_block()
            self.fruit.new_position()

    def update(self):
        self.snake.input()

    def fixed_update(self, delta_time):
        self.snake.move(delta_time)
        self.collision()


# Set-up pygame
class Main:
    def __init__(self):
        self.__running = True
        self.last_tick = 0
        self.delta_time = 0
        self.game_manager = GameManager()

    def on_init(self):
        pygame.time.set_timer(SCREEN_UPDATE, TICKS)
        pygame.init()
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
                # Pygame exit program
                if event.type == pygame.QUIT:
                    self.on_exit()
                # Fixed update
                if event.type == SCREEN_UPDATE:
                    self.game_manager.fixed_update(self.delta_time)
            SCREEN_SURFACE.fill(pygame.Color("black"))
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
