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
import time

##
## Game customization.
##

WIDTH, HEIGHT = 800, 800     # Game screen dimensions.

GRID_SIZE = 50               # Square grid size.

HEAD_COLOR      = "#00aa00"  # Color of the snake's head.
DEAD_HEAD_COLOR = "#4b0082"  # Color of the dead snake's head.
TAIL_COLOR      = "#00ff00"  # Color of the snake's tail.
APPLE_COLOR     = "#aa0000"  # Color of the apple.
POISON_APPLE_COLOR = "#5500aa"  # Color of the poisoned apple.
ARENA_COLOR     = "#202020"  # Color of the ground.
GRID_COLOR      = "#3c3c3b"  # Color of the grid lines.
SCORE_COLOR     = "#ffffff"  # Color of the scoreboard.
MESSAGE_COLOR   = "#808080"  # Color of the game-over message.

WINDOW_TITLE    = "Coral"  # Window title.

CLOCK_TICKS     = 7         # How fast the snake moves.

##
## Game implementation.
##

pygame.init()

clock = pygame.time.Clock()

arena = pygame.display.set_mode((WIDTH, HEIGHT))

# BIG_FONT   = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/8))
# SMALL_FONT = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/20))

BIG_FONT   = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/8))
SMALL_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/20))

pygame.display.set_caption(WINDOW_TITLE)

game_on = 1

## This function is called when the snake dies.

def center_prompt(title, subtitle):

    # Show title and subtitle.

    center_title = BIG_FONT.render(title, True, MESSAGE_COLOR)
    center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT/2))
    arena.blit(center_title, center_title_rect)

    center_subtitle = SMALL_FONT.render(subtitle, True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*2/3))
    arena.blit(center_subtitle, center_subtitle_rect)

    pygame.display.update()

    # Wait for a keypres or a game quit event.

    while (event := pygame.event.wait()):
        if event.type == pygame.KEYDOWN:
            break
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if event.key == pygame.K_q:          # 'Q' quits game     
        pygame.quit()
        sys.exit()

# Add this new function
def calculate_max_snake_length():
    # Total grid squares minus 1 (for the head)
    return (WIDTH // GRID_SIZE) * (HEIGHT // GRID_SIZE) - 1

##
## Snake class
##

class Snake:
    def __init__(self):

        # Dimension of each snake segment.

        self.x, self.y = GRID_SIZE, GRID_SIZE

        # Initial direction
        # xmov :  -1 left,    0 still,   1 right
        # ymov :  -1 up       0 still,   1 dows
        self.xmov = 1
        self.ymov = 0

        # The snake has a head segement,
        self.head = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        
        # and a tail (array of segments).
        self.tail = []

        # The snake is born.
        self.alive = True

        # No collected apples.
        self.got_apple = False

        # Add max length calculation
        self.max_length = calculate_max_snake_length()

    # This function is called at each loop interation.

    def update(self):
        global apple, poison_apple

        # Add win condition check before crash checks
        if len(self.tail) >= self.max_length:
            # Show win message
            center_prompt("You Win!", "Press to play again")
            self.reset()
            return

        # Check for border crash.
        if self.head.x not in range(0, WIDTH) or self.head.y not in range(0, HEIGHT):
            self.alive = False

        # Check for self-bite.
        for square in self.tail:
            if self.head.x == square.x and self.head.y == square.y:
                self.alive = False

         # In the event of death, reset the game arena.
        if not self.alive:

            # Tell the bad news
            pygame.draw.rect(arena, DEAD_HEAD_COLOR, self.head)
            center_prompt("Game Over", "Press to restart")
            self.reset() # Reset the snake

        # If head hasn't moved, tail shouldn't either (otherwise, self-byte).
        if (self.xmov or self.ymov):

            # Prepend a new segment to tail.
            self.tail.insert(0, pygame.Rect(self.head.x, self.head.y, GRID_SIZE, GRID_SIZE))
            
            if self.got_apple:
                self.got_apple = False
            else:
                self.tail.pop()

            # Move the head along current direction.
            self.head.x += self.xmov * GRID_SIZE
            self.head.y += self.ymov * GRID_SIZE

        # Check if snake has eaten a poisoned apple
        if self.head.x == poison_apple.x and self.head.y == poison_apple.y:
            if len(self.tail) == 0:  # Game over if only the head exists
                self.alive = False
                pygame.draw.rect(arena, DEAD_HEAD_COLOR, self.head)
                center_prompt("Game Over", "Press to restart")
                self.reset()
            else:
                self.tail.pop()
            poison_apple = PoisonApple()  # Respawn poisoned apple

    def reset(self):
        """Reset the snake to its initial state after dying."""
        self.x, self.y = GRID_SIZE, GRID_SIZE
        self.head = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        self.tail = []
        self.xmov = 1
        self.ymov = 0
        self.alive = True
        self.got_apple = False
        global apple
        apple = Apple()

##
## The apple class.
##

class Apple:
    def __init__(self):

        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH) / GRID_SIZE) * GRID_SIZE
        self.y = int(random.randint(0, HEIGHT) / GRID_SIZE) * GRID_SIZE
        
        # Create an apple at that location
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    # This function is called each interation of the game loop

    def update(self):

        # Drop the apple
        pygame.draw.rect(arena, APPLE_COLOR, self.rect)

##
## The Poison Apple
##

class PoisonApple:
    def __init__(self):

        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH) / GRID_SIZE) * GRID_SIZE
        self.y = int(random.randint(0, HEIGHT) / GRID_SIZE) * GRID_SIZE
        
        # Create a poisoned apple at that location
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        
        # Set random respawn time
        self.respawn_time = time.time() + random.randint(5, 10)

    def update(self):

        # Check if the time to respawn has passed
        if time.time() >= self.respawn_time:
            self.respawn()

        # Drop the poisoned apple
        pygame.draw.rect(arena, POISON_APPLE_COLOR, self.rect)

    def respawn(self):

        #Respawn the poisoned apple at a new random position.
        self.x = int(random.randint(0, WIDTH) / GRID_SIZE) * GRID_SIZE
        self.y = int(random.randint(0, HEIGHT) / GRID_SIZE) * GRID_SIZE
        
        
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        
        # Set random respawn time
        self.respawn_time = time.time() + random.randint(5, 10)  # Reset respawn time

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
poison_apple = PoisonApple()  # A poisoned apple

center_prompt(WINDOW_TITLE, "Press any key to start")

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

    if game_on:

        snake.update()

        arena.fill(ARENA_COLOR)
        draw_grid()

        apple.update()
        poison_apple.update()

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
        snake.got_apple = True
        apple = Apple()


    # Update display and move clock.
    pygame.display.update()
    clock.tick(CLOCK_TICKS)
