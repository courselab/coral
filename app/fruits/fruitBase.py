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
from app.config import *
from app.game import singleton_instance as gm

class BaseFruit:
    def __init__(self, color, snake=None):
        self.color = color
        self.x = int(random.randint(0, WIDTH) / size[configs[1]]) * size[configs[1]]
        self.y = int(random.randint(0, HEIGHT) / size[configs[1]]) * size[configs[1]]

        if snake:
            while snake.is_in_position(self.x, self.y):
                # Prevent fruits from spawning on top of the snake
                self.x = int(random.randint(0, WIDTH) / size[configs[1]]) * size[configs[1]]
                self.y = int(random.randint(0, HEIGHT) / size[configs[1]]) * size[configs[1]]

        self.rect = pygame.Rect(self.x, self.y, size[configs[1]], size[configs[1]])
        self.radius = size[configs[1]] // 2

    def update(self):
        pygame.draw.circle(gm.arena, self.color, (self.rect.centerx, self.rect.centery), self.radius)
