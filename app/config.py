#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

# Supported video modes

VIDEO_MODES = [
    (800, 800), (700, 700), (600, 600),
    (500, 500), (400, 400), (300, 300)
]

WIDTH, HEIGHT = 800, 800     # Default game screen dimensions.

SNAKE_COLOR      = "#00aa00"  # Color of the snake's head.
DEAD_SNAKE_COLOR = "#4b0082"  # Color of the dead snake's head.
APPLE_COLOR     = "#aa0000"  # Color of the apple.
ORANGE_COLOR    = "#ffa500"  # Color of the orange.
ARENA_COLOR     = "#202020"  # Color of the ground.
CONFIG_COLOR    = "#D3D3D3"  # Color of the config section.
GRID_COLOR      = "#3c3c3b"  # Color of the grid lines.
SCORE_COLOR     = "#ffffff"  # Color of the scoreboard.
LINE_COLOR     = "#000000"  # Color of lines in scoreboard.
MESSAGE_COLOR   = "#808080"  # Color of the game-over message.
STEM_COLOR      = "#228B22"
SELECTED_CONFIG_COLOR = "#DE6604"  # Color of the selected config.
POISON_APPLE_COLOR = "#5500aa"  # Color of the poison apple.


WINDOW_TITLE    = "Coral"  # Window title.
MAX_QUEUE_SIZE = 3 # Movement queue max size

OBSTACLE_COUNT = 5
OBSTACLE_COLOR = "#FF4500"

velocity = [4, 7, 10,15]
size = [60, 40, 20]  
n_apple = [1, 2, 3] 
base_volume_levels = [0.4, 0.6, 0.7]
volume_multiplier = [0.3, 1.1, 1.9]
configs = [1, 1, 0, 1, 0]


WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 153, 0)

ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT = 200, 20
ENERGY_CONSUMPTION = 1
MAX_ENERGY = 100
APPLE_ENERGY = 50

POISON_APPLE_RESPAWN_MIN = 5    #Minimum time for the poison apple to respawn
POISON_APPLE_RESPAWN_MAX = 10    #Maximum time for the poison apple to respawn
POISON_APPLE_DURATION_MIN = 5    #Minimum time for the poison apple to be active
POISON_APPLE_DURATION_MAX = 10   #Maximum time for the poison apple to be active

hard_mode = False  # Defined normal mode as standart.
border_wrap = False
is_muted = False #Definied is muted as false 
instructions_shown = False

HIGHSCORE_FILENAME = "data/highscore.bin"

language = "english"
