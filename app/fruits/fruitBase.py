#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

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
