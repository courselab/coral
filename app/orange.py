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

import random
import pygame

from app.config import *
from app.game import singleton_instance as gm

class Orange:

    def __init__(self):
        self.dropped = False

        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH)/size[configs[1]]) * size[configs[1]]
        self.y = int(random.randint(0, HEIGHT)/size[configs[1]]) * size[configs[1]]

        # Create an orange at that location
        self.rect = pygame.Rect(self.x, self.y, size[configs[1]], size[configs[1]])
        self.radius = size[configs[1]] // 2

    # This function is called each interation of the game loop
    def update(self):

        # Check if the orange is already dropped, if not then maybe drop it
        if self.dropped == False:
            #if random.randint(1, 100) >= 99:
            if True:
                pygame.draw.circle(gm.arena, ORANGE_COLOR, (self.rect.centerx, self.rect.centery), self.radius)
                self.dropped = True

        elif self.dropped == True:
            pygame.draw.circle(gm.arena, ORANGE_COLOR, (self.rect.centerx, self.rect.centery), self.radius)
