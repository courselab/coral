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

from app.config import *
from app.snake import Snake
from app.apple import Apple
from app.orange import Orange
from app.game import singleton_instance as gm
from app.translation import Translator


gm.draw_grid()
snake = Snake()    # The snake
apple = Apple()    # An apple
orange = Orange()  # An orange
translator = Translator()
gm.center_prompt(WINDOW_TITLE, translator.message("start"))

speed_multiplier = 1  # Inicia com velocidade padrão
game_on = gm.game_on

while True:

    for event in pygame.event.get():  # Aguarda eventos
        # App encerrado
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Tecla pressionada
        if event.type == pygame.KEYDOWN:
            key = event.key

            # Ações globais
            if key == pygame.K_q:  # Sair do jogo
                pygame.quit()
                sys.exit()
            elif key == pygame.K_p and not instructions_shown:  # Pausar jogo
                game_on = not game_on
            elif key == pygame.K_m:  # Mute
                is_muted = not is_muted
                pygame.mixer.music.set_volume(0 if is_muted else 0.4)
            elif key == pygame.K_i:  # Alternar tela de instruções
                instructions_shown = not instructions_shown
                game_on = True
            elif key == pygame.K_SPACE:  # Aumentar velocidade
                speed_multiplier = 2  # Multiplica a velocidade

            # Controles de movimento
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
                    if (x_dir != 0 and snake.xmov == 0) or (y_dir != 0 and snake.ymov == 0):
                        snake.set_direction(x_dir, y_dir)

        # Tecla solta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:  # Voltar à velocidade normal
                speed_multiplier = 1

    ## Atualizar o jogo
    if instructions_shown:
        gm.display_instructions() 
        pygame.display.update()
        continue

    if not game_on:
        gm.arena.fill(ARENA_COLOR)
        pause_text = gm.BIG_FONT.render(translator.message("paused"), True, MESSAGE_COLOR)
        pause_text_rect = pause_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        gm.arena.blit(pause_text, pause_text_rect)
        continue_text = gm.SMALL_FONT.render(translator.message("continue"), True, MESSAGE_COLOR)
        continue_text_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        gm.arena.blit(continue_text, continue_text_rect)
        quit_text = gm.SMALL_FONT.render(translator.message("quit"), True, MESSAGE_COLOR)
        quit_text_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 125))
        gm.arena.blit(quit_text, quit_text_rect)
        gm.win.blit(pygame.transform.rotozoom(gm.arena, 0, gm.win_res / WIDTH), (0, 0))
        pygame.display.update()
        continue

    if game_on:
        snake.update()
        gm.arena.fill(ARENA_COLOR)
        gm.draw_grid()
        apple.update()
        orange.update()

    snake.draw()
    if game_on:
        snake.energy.update()

    score = gm.BIG_FONT.render(f"{len(snake.tail)}", True, SCORE_COLOR)
    gm.arena.blit(score, gm.score_rect)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.got_apple = True
        apple = Apple(snake)
        gm.got_apple_sound.play()

    if snake.head.x == orange.x and snake.head.y == orange.y:
        snake.speed += 0.04
        orange = Orange()
        gm.got_apple_sound.play()

    instruction_text = gm.IN_GAME_FONT.render(translator.message("instructions"), True, WHITE_COLOR)
    instruction_text_rect = instruction_text.get_rect(topright=(WIDTH - 10, 10))
    gm.arena.blit(instruction_text, instruction_text_rect)

    pygame.display.update()
    gm.clock.tick(snake.speed * velocity[configs[0]] * speed_multiplier)
