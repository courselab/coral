#!/usr/bin/python3
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
import sys

##
## Game customization.
##


# Supported video modes

VIDEO_MODES = [
    (800, 800), (700, 700), (600, 600),
    (500, 500), (400, 400), (300, 300)
]

WIDTH, HEIGHT = 800, 800     # Default game screen dimensions.

GRID_SIZE = 50               # Square grid size.

HEAD_COLOR      = "#00aa00"  # Color of the snake's head.
DEAD_HEAD_COLOR = "#4b0082"  # Color of the dead snake's head.
TAIL_COLOR      = "#00ff00"  # Color of the snake's tail.
APPLE_COLOR     = "#aa0000"  # Color of the apple.
ARENA_COLOR     = "#202020"  # Color of the ground.
GRID_COLOR      = "#3c3c3b"  # Color of the grid lines.
SCORE_COLOR     = "#ffffff"  # Color of the scoreboard.
MESSAGE_COLOR   = "#808080"  # Color of the game-over message.

WINDOW_TITLE    = "Coral"  # Window title.

CLOCK_TICKS     = 7         # How fast the snake moves.

WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 153, 0)

ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT = 200, 20
ENERGY_CONSUMPTION = 1
MAX_ENERGY = 100
APPLE_ENERGY = 50

hard_mode = False  # Defined normal mode as standart.

##
## Game implementation.
##

pygame.init()

clock = pygame.time.Clock()

display_info = pygame.display.Info()

mon_w = display_info.current_w
mon_h = display_info.current_h

# Default window size
win_res = WIDTH

# If default video_mode doesn't fit, look for video mode that fits user's screen size
if (mon_w<WIDTH or mon_h<HEIGHT):
    min_dim = min(mon_w, mon_h)
    win_res = VIDEO_MODES[-1][0] # The default is the smallest one
    for mode in VIDEO_MODES:
        if mode[0] < mon_w and mode[1] < mon_h:
            win_res = mode[0]
            break

win = pygame.display.set_mode((win_res, win_res))
arena = pygame.Surface((WIDTH, HEIGHT))

# Play background sound and change volume
pygame.mixer.music.set_volume(0.4)
background_music = pygame.mixer.music.load('musics/CPU Talk - FMA - CC BY BoxCat Games.mp3')
pygame.mixer.music.play(-1)

# Set game's sounds effects
got_apple_sound = pygame.mixer.Sound('musics/got_apple.ogg')
got_apple_sound.set_volume(0.6)

game_over_sound = pygame.mixer.Sound('musics/game_over.wav')
game_over_sound.set_volume(0.7)

# BIG_FONT   = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/8))
# SMALL_FONT = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/20))

BIG_FONT   = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/8))
SMALL_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/20))
IN_GAME_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/48))

pygame.display.set_caption(WINDOW_TITLE)

game_on = 1

## This function is called when the snake dies.

def center_prompt(title, subtitle):
    global hard_mode, CLOCK_TICKS

    # Show title and subtitle
    center_title = BIG_FONT.render(title, True, MESSAGE_COLOR)
    center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT/2))
    arena.blit(center_title, center_title_rect)

    center_subtitle = SMALL_FONT.render(subtitle, True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*2/3))
    arena.blit(center_subtitle, center_subtitle_rect)

    # Add hard mode prompt
    hard_mode_text = SMALL_FONT.render("Press H for Hard Mode", True, MESSAGE_COLOR)
    hard_mode_text_rect = hard_mode_text.get_rect(center=(WIDTH/2, HEIGHT*3/4))
    arena.blit(hard_mode_text, hard_mode_text_rect)
    
    # Scaling surface to display size
    win.blit(pygame.transform.rotozoom(arena, 0, win_res/WIDTH), (0, 0))

    pygame.display.update()

    # Wait for a keypress or a game quit event
    while (event := pygame.event.wait()):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:  # 'H' for Hard mode
                hard_mode = True
                CLOCK_TICKS = 12  # Increase speed for hard mode
                break
            elif event.key == pygame.K_q:  # 'Q' quits game
                pygame.quit()
                sys.exit()
            else:  # Any other key for normal mode
                hard_mode = False
                break
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Set CLOCK_TICKS back to normal if not in hard mode
    if not hard_mode:
        CLOCK_TICKS = 7


## This function generate random positions for the snake
def random_position():

    # Not too close to the border (minimum of 2 border squares)
    x = int(random.randint(GRID_SIZE*2, WIDTH - GRID_SIZE*2)/GRID_SIZE) * GRID_SIZE
    y = int(random.randint(GRID_SIZE*2, HEIGHT - GRID_SIZE*2)/GRID_SIZE) * GRID_SIZE

    # Calculate distances to the borders
    left_dist = x
    right_dist = WIDTH - x
    top_dist = y
    bottom_dist = HEIGHT - y

    # Decide movement direction (horizontal or vertical)
    if min(left_dist, right_dist) < min(top_dist, bottom_dist): # Move horizontally
        if left_dist < right_dist:
            xmov = 1 
        else:
            xmov = -1 
        ymov = 0
    else:  # Move vertically
        if top_dist < bottom_dist: 
            ymov = 1  
        else:
            ymov = -1 
        xmov = 0

    return x, y, xmov, ymov
##
## Energy bar class
##
class EnergyBar:
    def __init__(self, initalEnergy = MAX_ENERGY):
        self.x = 0
        self.y = 0
        self.width = ENERGY_BAR_WIDTH
        self.height = ENERGY_BAR_HEIGHT
        self.energy = initalEnergy

    def update(self):
        pygame.draw.rect(arena, RED_COLOR, (self.x, self.y, self.width, self.height))
        self.decrease_energy(ENERGY_CONSUMPTION)
        current_width = (self.energy / MAX_ENERGY) * ENERGY_BAR_WIDTH
        pygame.draw.rect(arena, GREEN_COLOR, (self.x, self.y, current_width, self.height))
        label = IN_GAME_FONT.render(f'Energy: {self.energy} / {MAX_ENERGY}', True, WHITE_COLOR)
        arena.blit(label, (self.x, self.y + 3))

    def increase_energy(self, amount):
        self.energy = min(MAX_ENERGY, self.energy + amount)

    def decrease_energy(self, amount):
        self.energy = max(0, self.energy - amount)

    def get_energy(self):
        return self.energy
    
    def set_max_energy(self):
        self.energy = MAX_ENERGY

##
## Snake class
##
class Snake:
    def __init__(self):

        # Initial direction
        # xmov :  -1 left,    0 still,   1 right
        # ymov :  -1 up       0 still,   1 dows

        # Dimension of each snake segment.

        self.x, self.y, self.xmov, self.ymov = random_position()

        # The snake has a head segement,
        self.head = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

        # and a tail (array of segments).
        self.tail = []

        # The snake is born.
        self.alive = True

        # No collected apples.
        self.got_apple = False

        # The energy is full
        self.energy = EnergyBar(MAX_ENERGY)
        
    # This function is called at each loop interation.

    def update(self):
        global apple

        # Check for border crash.
        if self.head.x not in range(0, WIDTH) or self.head.y not in range(0, HEIGHT):
            self.alive = False

        # Check for self-bite.
        for square in self.tail:
            if self.head.x == square.x and self.head.y == square.y:
                self.alive = False

        # Check for not enough energy
        if self.energy.get_energy() <= 0:
            self.alive = False

        # In the event of death, reset the game arena.
        if not self.alive:
            
            # Play game over sound effect
            pygame.mixer.music.stop()
            game_over_sound.play()

            # Tell the bad news
            pygame.draw.rect(arena, DEAD_HEAD_COLOR, snake.head)
            center_prompt("Game Over", "Press to restart")

            # Respan the head with initial directions
            self.x, self.y, self.xmov, self.ymov = random_position()

            self.head = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

            # Respan the initial tail
            self.tail = []

            # Resurrection
            self.alive = True
            self.got_apple = False
            self.energy.set_max_energy()
            pygame.mixer.music.play()

            # Drop an apple
            apple = Apple()


        # Move the snake.

        # If head hasn't moved, tail shouldn't either (otherwise, self-byte).
        if (self.xmov or self.ymov):

            # Prepend a new segment to tail.
            self.tail.insert(0,pygame.Rect(self.head.x, self.head.y, GRID_SIZE, GRID_SIZE))

            if self.got_apple:
                self.got_apple = False
                self.energy.increase_energy(APPLE_ENERGY)
            else:
                self.tail.pop()

            # Move the head along current direction.
            self.head.x += self.xmov * GRID_SIZE
            self.head.y += self.ymov * GRID_SIZE

##
## The apple class.
##

class Apple:
    def __init__(self):

        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH)/GRID_SIZE) * GRID_SIZE
        self.y = int(random.randint(0, HEIGHT)/GRID_SIZE) * GRID_SIZE

        # Create an apple at that location
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    # This function is called each interation of the game loop

    def update(self):

        # Drop the apple
        pygame.draw.rect(arena, APPLE_COLOR, self.rect)


##
## Draw the arena
##

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(arena, GRID_COLOR, rect, 1)

score = BIG_FONT.render("1", True, MESSAGE_COLOR)
score_rect = score.get_rect(center=(WIDTH/2, HEIGHT/20+HEIGHT/30))

draw_grid()

snake = Snake()    # The snake

apple = Apple()    # An apple

center_prompt(WINDOW_TITLE, "Press to start")

##
## Main loop
##

while True:

    for event in pygame.event.get():           # Wait for events

       # App terminated
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

          # Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:    # Down arrow:  move down
                snake.ymov = 1
                snake.xmov = 0
            elif event.key == pygame.K_UP:    # Up arrow:    move up
                snake.ymov = -1
                snake.xmov = 0
            elif event.key == pygame.K_RIGHT: # Right arrow: move right
                snake.ymov = 0
                snake.xmov = 1
            elif event.key == pygame.K_LEFT:  # Left arrow:  move left
                snake.ymov = 0
                snake.xmov = -1
            elif event.key == pygame.K_q:     # Q         : quit game
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_p:     # S         : pause game
                game_on = not game_on

    ## Update the game

    ## Show "Paused" and "Press P to continue" messages in the center of the grid
    if not game_on:
        pause_text = BIG_FONT.render("Paused", True, MESSAGE_COLOR)
        pause_text_rect = pause_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        arena.blit(pause_text, pause_text_rect)
        
        continue_text = SMALL_FONT.render("Press P to continue", True, MESSAGE_COLOR)
        continue_text_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        arena.blit(continue_text, continue_text_rect)
        
        
        pygame.display.update()
        continue  # Skip the rest of the loop when paused
    
    if game_on:

        snake.update()

        arena.fill(ARENA_COLOR)
        draw_grid()

        apple.update()

        snake.energy.update()

    # Draw the tail
    for square in snake.tail:
        pygame.draw.rect(arena, TAIL_COLOR, square)

    # Draw head
    pygame.draw.rect(arena, HEAD_COLOR, snake.head)

    # Show score (snake length = head + tail)
    score = BIG_FONT.render(f"{len(snake.tail)}", True, SCORE_COLOR)
    arena.blit(score, score_rect)

    # If the head pass over an apple, lengthen the snake and drop another apple
    if snake.head.x == apple.x and snake.head.y == apple.y:
        #snake.tail.append(pygame.Rect(snake.head.x, snake.head.y, GRID_SIZE, GRID_SIZE))
        snake.got_apple = True;
        apple = Apple()
        got_apple_sound.play()


    # Update display and move clock.

    # Scaling surface to display size
    win.blit(pygame.transform.rotozoom(arena, 0, win_res/WIDTH), (0, 0))
    pygame.display.update()
    clock.tick(CLOCK_TICKS)
