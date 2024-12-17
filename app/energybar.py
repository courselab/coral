#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

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

        label = pygame.font.Font("assets/font/MidnightLetters.ttf", int(WIDTH/48)).render(f'Energy: {self.energy} / {MAX_ENERGY}', True, WHITE_COLOR)

        gm.arena.blit(label, (self.x, self.y + 3))

    def increase_energy(self, amount):
        self.energy = min(MAX_ENERGY, self.energy + amount)

    def decrease_energy(self, amount):
        self.energy = max(0, self.energy - amount)

    def get_energy(self):
        return self.energy
    
    def set_max_energy(self):
        self.energy = MAX_ENERGY
