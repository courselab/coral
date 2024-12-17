#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Coral, a derivative work of KobraPy.

from app.config import *
from app.fruits.fruitBase import BaseFruit


class Orange(BaseFruit):
    def __init__(self, snake=None):
        super().__init__(ORANGE_COLOR, snake)
        self.dropped = False

    def update(self):
        if not self.dropped:
            self.dropped = True
        if self.dropped:
            super().update()
