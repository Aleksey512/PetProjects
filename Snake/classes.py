import os
import random
from typing import List

import pygame
from pygame import Surface

from settings import (
    CELL_SIZE,
    HEIGHT_CELL_COUNT,
    WIDTH_CELL_COUNT,
    GRID_COLOR,
    SPEED,
    FPS,
    SNAKE_OUTER_COLOR,
    RIGHT,
    UP,
    DOWN,
    LEFT,
    GRID_HEIGHT,
    GRID_WIDTH,
)

current_dir = os.path.dirname(os.path.abspath(__file__))


class GameOver(Exception):
    pass


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False

    @property
    def x_coord(self):
        return self.x * CELL_SIZE

    @property
    def y_coord(self):
        return self.y * CELL_SIZE


class Grid:
    def __init__(self):
        self.cells = self.__generate_grid()

    def __generate_grid(self) -> List[Cell]:
        cells = []
        for y in range(HEIGHT_CELL_COUNT):
            for x in range(WIDTH_CELL_COUNT):
                new_cell = Cell(x, y)
                cells.append(new_cell)
        return cells

    def draw(self, display: Surface):
        for cell in self.cells:
            pygame.draw.rect(
                display,
                GRID_COLOR,
                (cell.x_coord, cell.y_coord, CELL_SIZE, CELL_SIZE),
                1,
            )


class Snake:
    def __init__(self):
        self.head = Cell(15, 15)
        self.head_image_right = pygame.image.load(
            os.path.join(current_dir, "sprites/snake_head_right.png")
        )
        self.head_image_left = pygame.image.load(os.path.join(current_dir, "sprites/snake_head_left.png"))
        self.head_image_up = pygame.image.load(os.path.join(current_dir, "sprites/snake_head_up.png"))
        self.head_image_down = pygame.image.load(os.path.join(current_dir, "sprites/snake_head_down.png"))
        self.body = [Cell(13, 15), Cell(14, 15)]
        self.direction = "RIGHT"
        self.speed = SPEED

    def move(self):
        if self.speed < FPS:
            self.speed += SPEED
            return
        if self.check_collision():
            raise GameOver
        self.body.insert(0, self.head)
        self.body.pop()
        if self.direction == "UP":
            self.head = Cell(self.head.x, self.head.y - 1)
        elif self.direction == "DOWN":
            self.head = Cell(self.head.x, self.head.y + 1)
        elif self.direction == "LEFT":
            self.head = Cell(self.head.x - 1, self.head.y)
        elif self.direction == "RIGHT":
            self.head = Cell(self.head.x + 1, self.head.y)
        self.speed = SPEED

    def draw(self, display: Surface):
        for cell in self.body:
            pygame.draw.rect(
                display,
                SNAKE_OUTER_COLOR,
                (cell.x_coord, cell.y_coord, CELL_SIZE, CELL_SIZE),
                border_radius=9,
            )
        if self.direction == RIGHT:
            display.blit(self.head_image_right, (self.head.x_coord, self.head.y_coord))
        if self.direction == UP:
            display.blit(self.head_image_up, (self.head.x_coord, self.head.y_coord))
        if self.direction == DOWN:
            display.blit(self.head_image_down, (self.head.x_coord, self.head.y_coord))
        if self.direction == LEFT:
            display.blit(self.head_image_left, (self.head.x_coord, self.head.y_coord))

    def add_tail(self):
        new_tail = Cell(self.body[-1].x_coord, self.body[-1].y_coord)
        self.body.insert(0, new_tail)

    def check_eat_apple(self, apple: "Apple") -> bool:
        if self.head == apple.cell:
            return True
        return False

    def check_collision(self) -> bool:
        if self.head in self.body:
            return True
        elif (
                self.head.x_coord < 0
                or self.head.x_coord >= GRID_WIDTH
                or self.head.y_coord < 0
                or self.head.y_coord >= GRID_HEIGHT
        ):
            return True
        return False


class Apple:
    def __init__(self, snake: Snake, grid: Grid):
        self.cell = self.__generate_apple(snake, grid)
        self.apple_image = pygame.image.load(os.path.join(current_dir, "sprites/apple.png"))

    def __generate_apple(self, snake: Snake, grid: Grid) -> Cell:
        exclude_cells = [snake.head, *snake.body]
        return random.choice([i for i in grid.cells if i not in exclude_cells])

    def draw(self, display: pygame.display):
        display.blit(self.apple_image, (self.cell.x_coord, self.cell.y_coord))
