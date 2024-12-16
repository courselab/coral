# !/usr/bin/python3
#
#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

from app.snake import Snake
from random import randint as rand
import pygame


class Obstacle:
    def __init__(
        self, snake: Snake, width: int, height: int, grid_size: int, color: str
    ) -> None:
        """
        Initialize an obstacle with a random position within the game grid.
        :param snake: you've guessed it.
        :param width: Width of the game arena.
        :param height: Height of the game arena.
        :param grid_size: Size of each grid cell.
        :param color: Color of the obstacle.
        """
        self.color = color
        self.x = rand(0, (width // grid_size) - 1) * grid_size
        while self.x == snake.x:
            self.x = rand(0, (width // grid_size) - 1) * grid_size
        self.y = rand(0, (height // grid_size) - 1) * grid_size
        while self.y == snake.y:
            self.y = rand(0, (height // grid_size) - 1) * grid_size
        self.rect = pygame.Rect(self.x, self.y, grid_size, grid_size)

    def update(self, arena):
        """
        Draw the obstacle on the game arena.
        :param arena: The game arena (pygame surface) where the obstacle will be drawn.
        """
        pygame.draw.rect(arena, self.color, self.rect)
