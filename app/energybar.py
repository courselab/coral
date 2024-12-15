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

from app.config import *
from app.game import singleton_instance as gm

class EnergyBar:

    def __init__(self, initalEnergy = MAX_ENERGY):
        self.x = 0
        self.y = 0
        self.width = ENERGY_BAR_WIDTH
        self.height = ENERGY_BAR_HEIGHT
        self.energy = initalEnergy

    def update(self):
        pygame.draw.rect(gm.arena, RED_COLOR, (self.x, self.y, self.width, self.height))
        self.decrease_energy(ENERGY_CONSUMPTION)
        current_width = (self.energy / MAX_ENERGY) * ENERGY_BAR_WIDTH
        pygame.draw.rect(gm.arena, GREEN_COLOR, (self.x, self.y, current_width, self.height))
        label = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/48)).render(f'Energy: {self.energy} / {MAX_ENERGY}', True, WHITE_COLOR)
        gm.arena.blit(label, (self.x, self.y + 3))

    def increase_energy(self, amount):
        self.energy = min(MAX_ENERGY, self.energy + amount)

    def decrease_energy(self, amount):
        self.energy = max(0, self.energy - amount)

    def get_energy(self):
        return self.energy
    
    def set_max_energy(self):
        self.energy = MAX_ENERGY