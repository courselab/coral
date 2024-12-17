#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

import pygame
from app.fruits.fruitBase import BaseFruit
from app.config import *
from app.game import singleton_instance as gm

class Apple(BaseFruit):
    def __init__(self, snake=None):
        super().__init__(APPLE_COLOR, snake)

    def update(self):
        super().update()
        stem_x = self.rect.centerx
        stem_y = self.rect.top - 2
        pygame.draw.line(gm.arena, STEM_COLOR, (stem_x, stem_y), (stem_x, stem_y - 10), 3)
