#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

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

GRID_SIZE = size[configs[1]] 
snake = Snake()  # The snake
apple = Apple()  # An apple
orange = Orange()  # An orange
obstacles = [
    Obstacle(snake, WIDTH, HEIGHT, GRID_SIZE, OBSTACLE_COLOR)
    for _ in range(OBSTACLE_COUNT)
]
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
                snake.speed = 2.0

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
                    if (x_dir != 0 and snake.xmov == 0) or (
                        y_dir != 0 and snake.ymov == 0
                    ):
                        snake.set_direction(x_dir, y_dir)

        # Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:  # Go back to normal speed
                snake.speed = 1.0

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
        grid_resize = snake.update()
        gm.arena.fill(ARENA_COLOR)
        gm.draw_grid()
        apple.update()
        orange.update()


        # Redraw fruits if the grid was resized
        if grid_resize:
            apple.recalc(snake)
            orange.recalc(snake)
            obstacles = []
            GRID_SIZE = size[configs[1]] 
            obstacles = [
                Obstacle(snake, WIDTH, HEIGHT, GRID_SIZE, OBSTACLE_COLOR)
                for _ in range(OBSTACLE_COUNT)
            ]
        # Update and draw obstacles
        for obstacle in obstacles:
            obstacle.update(gm.arena)

        # Prevent fruits from being inside obstacles
        restart_test = True 
        while restart_test:
            restart_test = False
            for obstacle in obstacles:
                if obstacle.x == apple.x and obstacle.y == apple.y:
                    apple.recalc(snake)
                    apple.update()
                    restart_test = True
                if obstacle.x == orange.x and obstacle.y == orange.y:
                    orange.recalc(snake)
                    orange.update()
                    restart_test = True

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if snake.head.colliderect(obstacle.rect):
                # End the game if the snake collides with an obstacle
                snake.alive = False

    # Draw snake
    snake.draw()
    if game_on:
        snake.energy.update()

    # Show score (snake length = head + tail)
    score = gm.BIG_FONT.render(f"{len(snake.tail)}", True, SCORE_COLOR)
    gm.arena.blit(score, gm.score_rect)

    # If the head pass over an apple, lengthen the snake and drop another apple
    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.got_apple = True
        apple = Apple(snake)
        gm.got_apple_sound.play()

    # If the head passes over an orange, lengthen the snake and drop another orange
    if snake.head.x == orange.x and snake.head.y == orange.y:
        snake.speed += 0.05
        orange = Orange()
        gm.got_apple_sound.play()

    # Add the "Press (I)nstructions" text in the top-right corner
    instruction_text = gm.IN_GAME_FONT.render(
        translator.message("instructions"), True, WHITE_COLOR
    )
    instruction_text_rect = instruction_text.get_rect(topright=(WIDTH - 10, 10)) 
    gm.arena.blit(instruction_text, instruction_text_rect)

    # Update display and move clock.
    pygame.display.update()
    gm.clock.tick(velocity[configs[0]] * snake.speed)
