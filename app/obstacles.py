# !/usr/bin/python3
#
#   Copyright (c) 2023, Monaco F. J. <monaco@usp.br>
#   Copyright 2024 The Authors of Coral
#
#   This file is part of Coral.
#
#   Coral is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import random

class Obstacle:
    def __init__(self, width, height, grid_size, color):
        """
        Initialize an obstacle with a random position within the game grid.
        :param width: Width of the game arena.
        :param height: Height of the game arena.
        :param grid_size: Size of each grid cell.
        :param color: Color of the obstacle.
        """
        self.color = color
        self.x = random.randint(0, (width // grid_size) - 1) * grid_size
        self.y = random.randint(0, (height // grid_size) - 1) * grid_size
        self.rect = pygame.Rect(self.x, self.y, grid_size, grid_size)

    def update(self, arena):
        """
        Draw the obstacle on the game arena.
        :param arena: The game arena (pygame surface) where the obstacle will be drawn.
        """
        pygame.draw.rect(arena, self.color, self.rect)


def create_obstacles(count, width, height, grid_size, color):
    """
    Create a list of obstacles for the game.
    :param count: Number of obstacles to create.
    :param width: Width of the game arena.
    :param height: Height of the game arena.
    :param grid_size: Size of each grid cell.
    :param color: Color of the obstacles.
    :return: List of Obstacle objects.
    """
    return [Obstacle(width, height, grid_size, color) for _ in range(count)]
