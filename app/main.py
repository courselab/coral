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
import sys
import os

from app.config import *
from app.snake import Snake
from app.apple import Apple
from app.orange import Orange
from app.game import singleton_instance as gm


gm.draw_grid()
snake = Snake()    # The snake
apple = Apple()    # An apple
orange = Orange()  # An orange
gm.center_prompt(WINDOW_TITLE, "Press to start")

game_on = gm.game_on
while True:

    for event in pygame.event.get():           # Wait for events

       # App terminated
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

          # Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:             # Q         : quit game
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_p and not instructions_shown:           # P         : pause game
                game_on = not game_on
            elif event.key == pygame.K_m:
                is_muted = not is_muted  
                pygame.mixer.music.set_volume(0 if is_muted else 0.4) 
            elif event.key == pygame.K_i:  # Toggle instructions screen
                instructions_shown = not instructions_shown
                game_on = True

            # Allow movement only if the game is not paused
            if game_on and not instructions_shown:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and snake.ymov == 0:    # Down arrow:  move down
                    snake.set_direction(0, 1)
                elif event.key == pygame.K_UP or event.key == pygame.K_w and snake.ymov == 0:    # Up arrow:    move up
                    snake.set_direction(0, -1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and snake.xmov == 0: # Right arrow: move right
                    snake.set_direction(1, 0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a and snake.xmov == 0:  # Left arrow:  move left
                    snake.set_direction(-1, 0)

    ## Update the game

    # Show instructions if the flag is set
    if instructions_shown:
        gm.display_instructions() 
        pygame.display.update()
        continue  # Skip the rest of the loop if instructions are shown

    ## Show "Paused" and "Press P to continue" messages in the center of the grid
    if not game_on:
        gm.arena.fill(ARENA_COLOR)  # Clear the arena to prevent overlap
        
        pause_text = gm.BIG_FONT.render("Paused", True, MESSAGE_COLOR)
        pause_text_rect = pause_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        gm.arena.blit(pause_text, pause_text_rect)
        
        continue_text = gm.SMALL_FONT.render("Press P to continue", True, MESSAGE_COLOR)
        continue_text_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        gm.arena.blit(continue_text, continue_text_rect)
        
        quit_text = gm.SMALL_FONT.render("Press q to quit", True, MESSAGE_COLOR)
        quit_text_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 125))
        gm.arena.blit(quit_text, quit_text_rect)
        # Draw the pause menu and update the display
        gm.win.blit(pygame.transform.rotozoom(gm.arena, 0, gm.win_res / WIDTH), (0, 0))
        pygame.display.update()
        
        # Skip the rest of the loop when paused, preventing unnecessary updates
        continue  

    
    if game_on:

        snake.update()

        gm.arena.fill(ARENA_COLOR)
        gm.draw_grid()

        apple.update()
        orange.update()

    # Draw the tail
    for square in snake.tail:
        if square is snake.tail[-1]:
            if (len(snake.tail) == 1):
                snake.draw_tail(square, (snake.xmov, snake.ymov))
            else:
                snake.draw_tail(square, (snake.tail[-2][0] - square[0], snake.tail[-2][1] - square[1]))
        else:
            pygame.draw.rect(gm.arena, HEAD_COLOR, square)
    # Draw head
    snake.draw_head()

    if game_on:
        snake.energy.update()
        
    # Show score (snake length = head + tail)
    score = gm.BIG_FONT.render(f"{len(snake.tail)}", True, SCORE_COLOR)
    gm.arena.blit(score, gm.score_rect)

    # If the head pass over an apple, lengthen the snake and drop another apple
    if snake.head.x == apple.x and snake.head.y == apple.y:
        #snake.tail.append(pygame.Rect(snake.head.x, snake.head.y, GRID_SIZE, GRID_SIZE))
        snake.got_apple = True
        apple = Apple(snake)
        gm.got_apple_sound.play()

    # If the head passes over an orange, lengthen the snake and drop another orange
    if snake.head.x == orange.x and snake.head.y == orange.y:
        #snake.tail.append(pygame.Rect(snake.head.x, snake.head.y, GRID_SIZE, GRID_SIZE))
        snake.speed += 0.04
        orange = Orange()
        gm.got_apple_sound.play()


    # Add the "Press (I)nstructions" text in the top-right corner
    instruction_text = gm.IN_GAME_FONT.render("Press (I)nstructions", True, WHITE_COLOR)
    instruction_text_rect = instruction_text.get_rect(topright=(WIDTH - 10, 10))  # Padding from the edge
    gm.arena.blit(instruction_text, instruction_text_rect)

    # Update display and move clock.
    pygame.display.update()
    gm.clock.tick(snake.speed*velocity[configs[0]])

