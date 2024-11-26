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
from app.fruits.fruitBase import BaseFruit
from app.config import *
from app.game import singleton_instance as gm

class Apple(BaseFruit):
    def __init__(self, snake=None):
        super().__init__(APPLE_COLOR, snake)

    def update(self):
        super().update()
        stem_x = self.rect.centerx
        stem_y = self.rect.top - 5
        pygame.draw.line(gm.arena, STEM_COLOR, (stem_x, stem_y), (stem_x, stem_y - 10), 3)
