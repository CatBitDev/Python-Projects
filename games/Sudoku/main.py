import random
import sys
from typing import Any

import pygame
import numpy as np
from pygame import Vector2

# Game settings
CELL_SIZE = 40
CELL_MARGIN = 5
CELL_BORDER = 5
SCREEN_SIZE = Vector2(480, 640)
BOARD_CENTER = Vector2(SCREEN_SIZE.x - CELL_SIZE * 9, SCREEN_SIZE.y - CELL_SIZE * 9) / 2
FLAGS = pygame.HWSURFACE
VSYNC = 1
SCREEN_SURFACE = pygame.display.set_mode(SCREEN_SIZE, FLAGS, VSYNC)
SCREEN_UPDATE = pygame.USEREVENT
FRAMES_PER_SECOND = pygame.time.Clock()
FPS = 60
TICKS = 20
# UI Settings
FONT = 'Rubik-Regular.ttf'
FONT_SIZE = 24
BACKGROUND = pygame.image.load("Background.jpg")
# Colors
BLACK = pygame.Color("black")
GRAY = pygame.Color("azure3")
WHITE = pygame.Color("white")
CELL = {
    "ENABLED": {
        "TEXTURE": pygame.image.load('cell.png').convert_alpha(),
        "COLOR": pygame.Color("azure"),
        "TEXT_COLOR": pygame.Color("black")},
    "DISABLED": {
        "TEXTURE": pygame.image.load('cell.png').convert_alpha(),
        "COLOR": pygame.Color("azure3"),
        "TEXT_COLOR": pygame.Color("azure3")},
    "HOVERED": {
        "TEXTURE": pygame.image.load('cell.png').convert_alpha(),
        "COLOR": pygame.Color("darkgoldenrod1"),
        "TEXT_COLOR": pygame.Color("white")},
    "FOCUSED": {
        "TEXTURE": pygame.image.load('cell.png').convert_alpha(),
        "COLOR": pygame.Color("darkorchid2"),
        "TEXT_COLOR": pygame.Color("white")},
    "GROUP_FOCUSED": {
        "TEXTURE": pygame.image.load('cell.png').convert_alpha(),
        "COLOR": pygame.Color("darkorchid3"),
        "TEXT_COLOR": pygame.Color("white")}}


def replace_color(surface, color):
    # Fill all pixels of the surface with color, preserve transparency
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


class Cell(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, font, text):
        super().__init__(groups)
        # Initialize sprite values
        pos_x = x * CELL_SIZE + BOARD_CENTER.x + CELL_MARGIN * x + CELL_MARGIN * (x // 3)
        pos_y = y * CELL_SIZE + BOARD_CENTER.y + CELL_MARGIN * y + CELL_MARGIN * (y // 3)
        self.position = Vector2(x, y)
        self.state = "ENABLED"
        self.text = text
        self.font = font
        # Initialize sprite graphics
        self.image = CELL[self.state]["TEXTURE"]
        self.number = self.font.render(self.text, True, CELL[self.state]["TEXT_COLOR"])
        # Set sprite position
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.number_rect = self.number.get_rect(center=(pos_x, pos_y))

    def set_state(self, state):
        self.state = state

    def set_text(self, text):
        self.text = text

    def set_position(self, pos_x, pos_y):
        self.position = Vector2(pos_x, pos_y)

    def get_position(self): return self.position
    def get_state(self): return self.state

    def update(self):
        self.number = self.font.render(self.text, True, CELL[self.state]["TEXT_COLOR"])
        self.image = CELL[self.state]["TEXTURE"]
        SCREEN_SURFACE.blit(self.number, self.number_rect)


class GameManager:

    def __init__(self):
        # Update cell texture colors for each state
        for state in CELL.keys():
            replace_color(CELL[state]["TEXTURE"], CELL[state]["COLOR"])
        # Load default font
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        # Game visible sprites
        self.board_sprites = pygame.sprite.Group()
        # Create board
        self.board_numbers = np.array([np.arange(1, 10, dtype=int) for i in range(9)])
        for x in range(9):
            for y in range(9):
                # Get board number
                cell_text = str(self.board_numbers[y][x])
                # Create board sprite
                Cell(self.board_sprites, x, y, self.font, cell_text)

        self.mouse_position = pygame.math.Vector2()
        self.mouse_pressed = False
        self.cell_focused = False
        self.cell_focused_position = pygame.math.Vector2()

    def draw(self):
        # Draw background
        SCREEN_SURFACE.blit(BACKGROUND, (0, 0))
        # Draw board sprites
        self.board_sprites.draw(SCREEN_SURFACE)
        self.board_sprites.update()

    def update(self):
        self.mouse_position = pygame.mouse.get_pos()
        for sprite in self.board_sprites:
            if sprite.get_state() == "FOCUSED":
                # Set cell group position
                self.cell_focused = True
                self.cell_focused_position = sprite.get_position()
                # Toggle focused cell state
                if sprite.rect.collidepoint(self.mouse_position[0], self.mouse_position[1]) and self.mouse_pressed:
                    self.mouse_pressed = False
                    self.cell_focused = False
                    sprite.set_state("ENABLED")
                continue
            # Reset cell state
            sprite.set_state("ENABLED")
            # Change cell state rows and cols in the same group
            if self.cell_focused:
                if sprite.get_position().x == self.cell_focused_position.x:
                    sprite.set_state("GROUP_FOCUSED")
                if sprite.get_position().y == self.cell_focused_position.y:
                    sprite.set_state("GROUP_FOCUSED")
            if sprite.rect.collidepoint(self.mouse_position[0], self.mouse_position[1]):
                # Change cell state on hover
                sprite.set_state("HOVERED")
                # Change cell state on pressed
                if self.mouse_pressed:
                    self.mouse_pressed = False
                    # Reset all cells state
                    for reset in self.board_sprites:
                        reset.set_state("ENABLED")
                    sprite.set_state("FOCUSED")

    def tick_update(self, delta_time):
        pass


# Pygame setup
class Main:
    def __init__(self):
        self.__running = True
        self.delta_time = 0
        self.last_tick = 0
        pygame.init()
        pygame.time.set_timer(SCREEN_UPDATE, TICKS)
        self.game_manager = GameManager()
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
                # Game input
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_manager.mouse_pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.game_manager.mouse_pressed = False
                # Tick update
                if event.type == SCREEN_UPDATE:
                    self.game_manager.tick_update(self.delta_time)
            # Clear display
            SCREEN_SURFACE.fill(WHITE)
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
