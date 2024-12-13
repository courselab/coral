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

import sys

import pygame

from app.apple import Apple
from app.config import *
from app.game import singleton_instance as gm
from app.obstacles import Obstacle
from app.orange import Orange
from app.snake import Snake
from app.translation import Translator

gm.draw_grid()
translator = Translator()

gm.center_prompt(WINDOW_TITLE, translator.message("start"))


game_on = gm.game_on

while True:
    for event in pygame.event.get():  # Wait for events
        # App terminated
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key pressed
        if event.type == pygame.KEYDOWN:
            key = event.key

            # Global actions
            if key == pygame.K_ESCAPE:  # Quit game
                pygame.quit()
                sys.exit()
            elif key == pygame.K_p and not instructions_shown:  # Pause game
                game_on = not game_on
            elif key == pygame.K_m:  # Mute/unmute game
                is_muted = not is_muted
                pygame.mixer.music.set_volume(0 if is_muted else 0.4)
            elif key == pygame.K_i:  # Toggle instructions screen
                instructions_shown = not instructions_shown
                game_on = True
            elif key == pygame.K_SPACE:  # Increase speed
                gm.snake.speed = 2.0

            # Movement controls (only if game is not paused or showing instructions)
            if game_on and not instructions_shown:
                movement_keys = {
                    pygame.K_DOWN: (0, 1),
                    pygame.K_s: (0, 1),
                    pygame.K_UP: (0, -1),
                    pygame.K_w: (0, -1),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_d: (1, 0),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_a: (-1, 0),
                }

                if key in movement_keys:
                    x_dir, y_dir = movement_keys[key]
                    if (x_dir != 0 and gm.snake.xmov == 0) or (
                        y_dir != 0 and gm.snake.ymov == 0
                    ):
                        gm.snake.set_direction(x_dir, y_dir)

        # Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:  # Go back to normal speed
                gm.snake.speed = 1.0

    # Show instructions if the flag is set
    if instructions_shown:
        gm.display_instructions()
        pygame.display.update()
        continue

    # Show "Paused" and "Press P to continue" messages in the center of the grid
    if not game_on:
        gm.arena.fill(ARENA_COLOR)  # Clear the arena to prevent overlap
        pause_text = gm.BIG_FONT.render(
            translator.message("paused"), True, MESSAGE_COLOR
        )
        pause_text_rect = pause_text.get_rect(
            center=(WIDTH / 2, HEIGHT / 2 - GRID_SIZE)
        )
        gm.arena.blit(pause_text, pause_text_rect)

        continue_text = gm.SMALL_FONT.render(
            translator.message("continue"), True, MESSAGE_COLOR
        )
        continue_text_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        gm.arena.blit(continue_text, continue_text_rect)

        quit_text = gm.SMALL_FONT.render(
            translator.message("quit"), True, MESSAGE_COLOR
        )
        quit_text_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 125))
        gm.arena.blit(quit_text, quit_text_rect)

        # Draw the pause menu and update the display
        gm.win.blit(pygame.transform.rotozoom(gm.arena, 0, gm.win_res / WIDTH), (0, 0))
        pygame.display.update()

        # Skip the rest of the loop when paused, preventing unnecessary updates
        continue

    if game_on:
        gm.snake.update()
        gm.arena.fill(ARENA_COLOR)
        gm.draw_grid()
        gm.apple.update(gm.arena)
        gm.orange.update(gm.arena)

        # Update and draw obstacles
        for obstacle in gm.obstacles:
            obstacle.update(gm.arena)
            # fixes apples and oranges spawning on top of obstacles
            if obstacle.x == gm.apple.x and obstacle.y == gm.apple.y:
                gm.apple.x = obstacle.x - 1 % size[configs[1]]
                gm.apple.y = obstacle.x - 1 % size[configs[1]]
            if obstacle.x == gm.orange.x and obstacle.y == gm.orange.y:
                gm.orange.x = obstacle.x - 1 % size[configs[1]]
                gm.orange.y = obstacle.x - 1 % size[configs[1]]

        # Check for collisions with obstacles
        for obstacle in gm.obstacles:
            if gm.snake.head.colliderect(obstacle.rect):
                # End the game if the snake collides with an obstacle
                gm.snake.alive = False
                gm.game_over_sound.play()

    # Draw snake
    gm.snake.draw()
    if game_on:
        gm.snake.energy.update()

    # Show score (snake length = head + tail)
    score = gm.BIG_FONT.render(f"{len(gm.snake.tail)}", True, SCORE_COLOR)
    gm.arena.blit(score, gm.score_rect)

    # If the head pass over an apple, lengthen the gm. and drop another apple
    if gm.snake.head.x == gm.apple.x and gm.snake.head.y == gm.apple.y:
        gm.snake.got_apple = True
        gm.apple = Apple(gm.snake)
        gm.got_apple_sound.play()

    # If the head passes over an orange, lengthen the snake and drop another orange
    if gm.snake.head.x == gm.orange.x and gm.snake.head.y == gm.orange.y:
        gm.snake.speed += 0.05
        gm.orange = Orange()
        gm.got_apple_sound.play()

    # Add the "Press (I)nstructions" text in the top-right corner
    instruction_text = gm.IN_GAME_FONT.render(
        translator.message("instructions"), True, WHITE_COLOR
    )
    instruction_text_rect = instruction_text.get_rect(topright=(WIDTH - 10, 10))
    gm.arena.blit(instruction_text, instruction_text_rect)

    # Update display and move clock.
    pygame.display.update()
    gm.clock.tick(velocity[configs[0]] * gm.snake.speed)
