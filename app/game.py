#  Copyright (c) 2023, Monaco F. J. <monaco@usp.br>
#  Copyright 2024 The Authors of Coral
#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

import pygame
import sys
import os

from app.config import *
from app.translation import Translator


# singleton_module.py
class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        display_info = pygame.display.Info()

        mon_w = display_info.current_w
        mon_h = display_info.current_h

        # Default window size
        self.win_res = WIDTH

        # If default video_mode doesn't fit, look for video mode that fits user's screen size
        if mon_w < WIDTH or mon_h < HEIGHT:
            self.min_dim = min(mon_w, mon_h)
            self.win_res = VIDEO_MODES[-1][0]  # The default is the smallest one
            for mode in VIDEO_MODES:
                if mode[0] < mon_w and mode[1] < mon_h:
                    self.win_res = mode[0]
                    break

        self.win = pygame.display.set_mode((self.win_res, self.win_res))

        # arena = pygame.Surface((WIDTH, HEIGHT))
        self.arena = pygame.display.set_mode((WIDTH, HEIGHT))

        # Play background sound and change volume
        pygame.mixer.music.set_volume(base_volume_levels[0])
        self.background_music = pygame.mixer.music.load(
            "musics/CPU Talk - FMA - CC BY BoxCat Games.mp3"
        )
        pygame.mixer.music.play(-1)

        # Set game's sounds effects
        self.got_apple_sound = pygame.mixer.Sound("musics/got_apple.ogg")
        self.got_apple_sound.set_volume(base_volume_levels[1])

        self.game_over_sound = pygame.mixer.Sound("musics/game_over.wav")
        self.game_over_sound.set_volume(base_volume_levels[2])

        self.BIG_FONT = pygame.font.Font(
            "assets/font/MidnightLetters.ttf", int(WIDTH / 10)
        )
        self.SMALL_FONT = pygame.font.Font(
            "assets/font/MidnightLetters.ttf", int(WIDTH / 20)
        )
        self.IN_GAME_FONT = pygame.font.Font(
            "assets/font/MidnightLetters.ttf", int(WIDTH / 48)
        )

        pygame.display.set_caption(WINDOW_TITLE)

        self.game_on = 1

        self.score = self.BIG_FONT.render("1", True, MESSAGE_COLOR)
        self.score_rect = self.score.get_rect(
            center=(WIDTH / 2, HEIGHT / 20 + HEIGHT / 30)
        )

        self.highscore = self.get_high_score()

        self.translator = Translator()

    def center_prompt(self, title, subtitle) -> bool:
        global hard_mode, border_wrap, CLOCK_TICKS
        resize_grid = False

        # Show title and subtitle
        center_title = self.BIG_FONT.render(title, True, MESSAGE_COLOR)
        center_title_rect = center_title.get_rect(center=(WIDTH / 2, HEIGHT * (0.3)))
        self.arena.blit(center_title, center_title_rect)

        center_subtitle = self.SMALL_FONT.render(subtitle, True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(
            center=(WIDTH / 2, HEIGHT * (0.4))
        )
        self.arena.blit(center_subtitle, center_subtitle_rect)

        center_subtitle = self.SMALL_FONT.render(
            self.translator.message("configuration"), True, MESSAGE_COLOR
        )
        center_subtitle_rect = center_subtitle.get_rect(
            center=(WIDTH / 2, HEIGHT * (0.5))
        )
        self.arena.blit(center_subtitle, center_subtitle_rect)

        # Add hard mode prompt
        hard_mode_text = self.SMALL_FONT.render(
            self.translator.message("hard_mode"), True, MESSAGE_COLOR
        )
        hard_mode_text_rect = hard_mode_text.get_rect(
            center=(WIDTH / 2, HEIGHT * (0.7))
        )
        self.arena.blit(hard_mode_text, hard_mode_text_rect)

        # Add easy mode prompt
        easy_mode_text = self.SMALL_FONT.render(
            self.translator.message("easy_mode"), True, MESSAGE_COLOR
        )
        easy_mode_text_rect = easy_mode_text.get_rect(
            center=(WIDTH / 2, HEIGHT * (0.8))
        )
        self.arena.blit(easy_mode_text, easy_mode_text_rect)

        pygame.display.update()

        while ( event := pygame.event.wait() ):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    # Save current display for restoring later
                    old_surface = self.arena.copy()
                    
                    # Show instructions
                    self.arena.fill(ARENA_COLOR)  # Fill with black background
                    self.display_instructions()
                    pygame.display.update()
                    
                    # Wait for I to be pressed again
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                            break
                    
                    # Restore game over screen
                    self.arena.fill(ARENA_COLOR)  # Fill with black background
                    self.arena.blit(old_surface, (0, 0))
                    pygame.display.update()
                    continue

                break
        # Reset game configurations before starting a new game
        border_wrap = False

        if event.key == pygame.K_ESCAPE:  # 'ESC' quits game
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_c:
            resize_grid = self.config_prompt()
        if event.key == pygame.K_h:
            hard_mode = True
            configs[0] = 2
        if event.key == pygame.K_e:
            border_wrap = True

        # Set CLOCK_TICKS back to normal if not in hard mode
        if not hard_mode:
            configs[0] = 1

        return resize_grid;

    def display_instructions(self):
        instruction_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Fill the surface with a semi-transparent black (RGBA color)
        instruction_surface.fill((0, 0, 0, 128))

        # Blit the overlay surface on top of the game window (arena)
        self.arena.blit(instruction_surface, (0, 0))

        instructions = [
            self.translator.message("instructions_1"),
            self.translator.message("instructions_2"),
            self.translator.message("instructions_3"),
            self.translator.message("instructions_4"),
            self.translator.message("instructions_5"),
            self.translator.message("instructions_6"),
            self.translator.message("instructions_7"),
        ]

        y_offset = HEIGHT / 3
        for line in instructions:
            text_surface = self.SMALL_FONT.render(line, True, (255, 255, 255))
            self.arena.blit(text_surface, (50, y_offset))
            y_offset += 50

    def get_options(self):
        options = [
            ["velocity_low", "velocity_medium", "velocity_high", "velocity_extreme"],
            ["size_low", "size_medium", "size_high"],
            ["frequency_low", "frequency_medium", "frequency_high"],
            ["sound_low", "sound_medium", "sound_high"],
            self.translator.available_languages
        ]
        return options

    def draw_config_line(self, title, subtitle, position, selected, translate=True):
        center_subtitle = self.SMALL_FONT.render(self.translator.message(title), True, LINE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH / 2, HEIGHT * (position)))
        self.arena.blit(center_subtitle, center_subtitle_rect)

        text_color = SELECTED_CONFIG_COLOR if selected else MESSAGE_COLOR
        text = self.translator.message(subtitle) if translate else subtitle
        center_subtitle = self.SMALL_FONT.render(text, True, text_color)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH / 2, HEIGHT * (position + 0.05)))
        self.arena.blit(center_subtitle, center_subtitle_rect)

    def draw_config(self, conf=[1, 1, 1, 1, 1], actualPos=0):
        # Title
        self.arena.fill(CONFIG_COLOR)
        center_title = self.BIG_FONT.render(
            self.translator.message("title_configuration"), True, MESSAGE_COLOR
        )
        center_title_rect = center_title.get_rect(center=(WIDTH / 2, HEIGHT * (0.20)))
        self.arena.blit(center_title, center_title_rect)

        # Subtitle
        center_subtitle = self.SMALL_FONT.render(
            self.translator.message("configuration_1"), True, MESSAGE_COLOR
        )
        center_subtitle_rect = center_subtitle.get_rect(
            center=(WIDTH / 2, HEIGHT * (0.30))
        )
        self.arena.blit(center_subtitle, center_subtitle_rect)
        center_subtitle = self.SMALL_FONT.render(
            self.translator.message("configuration_2"), True, MESSAGE_COLOR
        )
        center_subtitle_rect = center_subtitle.get_rect(
            center=(WIDTH / 2, HEIGHT * (0.35))
        )
        self.arena.blit(center_subtitle, center_subtitle_rect)

        # Configs
        options = self.get_options();
        for index in range(5):
            self.draw_config_line(
                title = "configuration_{}".format(index + 3),
                subtitle = options[index][conf[index]],
                position = 0.45 + 0.10 * index,
                selected = actualPos == index,
                translate = index != 4
            )

        pygame.display.update()

    def update_volume(self):
        pygame.mixer.music.set_volume(
            base_volume_levels[0] * volume_multiplier[configs[3]]
        )
        self.got_apple_sound.set_volume(
            base_volume_levels[1] * volume_multiplier[configs[3]]
        )
        self.game_over_sound.set_volume(
            base_volume_levels[2] * volume_multiplier[configs[3]]
        )

    def config_prompt(self) -> bool:
        self.draw_config()

        # Wait for a keypress or a game quit event.
        n = 0
        stop = 0
        while True:
            if stop == 1:
                break
            for event in pygame.event.get():
                if stop == 1:
                    break
                # App terminated
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Key pressed
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_DOWN | pygame.K_s:
                            n = (n + 1) % 5
                        case pygame.K_UP | pygame.K_w:
                            n = (n - 1) % 5
                        case key if key in (
                            pygame.K_RIGHT,
                            pygame.K_d,
                            pygame.K_LEFT,
                            pygame.K_a,
                        ):
                            options = self.get_options()[n]
                            if key in (pygame.K_RIGHT, pygame.K_d):
                                configs[n] += 1
                            else:
                                configs[n] -= 1
                            configs[n] %= len(options)
                            if n == 3:
                                self.update_volume()
                            elif n == 4:
                                self.translator.set_language(
                                    self.translator.available_languages[configs[4]]
                            )
                        case pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        case pygame.K_j:
                            stop = 1
                self.draw_config(configs, actualPos=n)
        # Returns true if the grid size changed
        if (n == 1):
            return True
        return False

    ## Get and save highscore from/in a file
    def save_high_score(self, score):
        if not os.path.exists("../data/"):
            os.makedirs("../data/")

        try:
            with open(HIGHSCORE_FILENAME, "wb+") as file:
                file.write(score.to_bytes(4, byteorder="big"))
        except (FileNotFoundError, ValueError):
            return 0

    def get_high_score(self):
        try:
            with open(HIGHSCORE_FILENAME, "rb") as file:
                return int.from_bytes(file.read(4), byteorder="big")
        except (FileNotFoundError, ValueError):
            return 0

    ## Display highscore
    def display_highscore(self, score):
        new_highscore = ""
        if score > self.highscore:
            # Update highscore
            self.highscore = score
            self.save_high_score(score)

            new_highscore = "NEW "

        text = new_highscore + "Highscore: " + str(self.highscore)

        # Display highscore value
        center_highscore = self.SMALL_FONT.render(text, True, MESSAGE_COLOR)
        center_highscore_rect = center_highscore.get_rect(
            center=(WIDTH / 2, HEIGHT * 1 / 5)
        )
        self.arena.blit(center_highscore, center_highscore_rect)

        pygame.display.update()

    ##
    ## Draw the arena
    ##
    def draw_grid(self):
        num_cells_x = WIDTH // size[configs[1]]
        num_cells_y = HEIGHT // size[configs[1]]

        cell_width = WIDTH // num_cells_x
        cell_height = HEIGHT // num_cells_y

        for x in range(0, WIDTH, cell_width):
            for y in range(0, HEIGHT, cell_height):
                rect = pygame.Rect(x, y, cell_width, cell_height)  # Correção da identação
                pygame.draw.rect(self.arena, GRID_COLOR, rect, 1)

singleton_instance = Game()
