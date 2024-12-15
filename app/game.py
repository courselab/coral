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
        if (mon_w<WIDTH or mon_h<HEIGHT):
            self.min_dim = min(mon_w, mon_h)
            self.win_res = VIDEO_MODES[-1][0] # The default is the smallest one
            for mode in VIDEO_MODES:
                if mode[0] < mon_w and mode[1] < mon_h:
                    self.win_res = mode[0]
                    break

        self.win = pygame.display.set_mode((self.win_res, self.win_res))

        # arena = pygame.Surface((WIDTH, HEIGHT))
        self.arena = pygame.display.set_mode((WIDTH, HEIGHT))


        # Play background sound and change volume
        pygame.mixer.music.set_volume(base_volume_levels[0])
        self.background_music = pygame.mixer.music.load('musics/CPU Talk - FMA - CC BY BoxCat Games.mp3')
        pygame.mixer.music.play(-1)

        # Set game's sounds effects
        self.got_apple_sound = pygame.mixer.Sound('musics/got_apple.ogg')
        self.got_apple_sound.set_volume(base_volume_levels[1])

        self.game_over_sound = pygame.mixer.Sound('musics/game_over.wav')
        self.game_over_sound.set_volume(base_volume_levels[2])

        # BIG_FONT   = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/8))
        # SMALL_FONT = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/20))

        self.BIG_FONT   = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/8))
        self.SMALL_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/20))
        self.IN_GAME_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/48))

        pygame.display.set_caption(WINDOW_TITLE)

        self.game_on = 1
        
        self.score = self.BIG_FONT.render("1", True, MESSAGE_COLOR)
        self.score_rect = self.score.get_rect(center=(WIDTH/2, HEIGHT/20+HEIGHT/30))
    
        self.highscore = self.get_high_score()

 
    def center_prompt(self,title, subtitle):
        global hard_mode, border_wrap, CLOCK_TICKS

        # Show title and subtitle
        center_title = self.BIG_FONT.render(title, True, MESSAGE_COLOR)
        center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT*(0.3)))
        self.arena.blit(center_title, center_title_rect)

        center_subtitle = self.SMALL_FONT.render(subtitle, True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.4)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        
        center_subtitle = self.SMALL_FONT.render("Aperte C para configurar o jogo!", True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.5)))
        self.arena.blit(center_subtitle, center_subtitle_rect)

        # Add hard mode prompt
        hard_mode_text = self.SMALL_FONT.render("Press H for Hard Mode", True, MESSAGE_COLOR)
        hard_mode_text_rect = hard_mode_text.get_rect(center=(WIDTH/2, HEIGHT*(0.7)))
        self.arena.blit(hard_mode_text, hard_mode_text_rect)

        # Add easy mode prompt
        easy_mode_text = self.SMALL_FONT.render("Press E for Easy Mode", True, MESSAGE_COLOR)
        easy_mode_text_rect = easy_mode_text.get_rect(center=(WIDTH/2, HEIGHT*(0.8)))
        self.arena.blit(easy_mode_text, easy_mode_text_rect)
        
        pygame.display.update()
            
        while ( event := pygame.event.wait() ):
            if event.type == pygame.KEYDOWN:
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Reset game configurations before starting a new game
        border_wrap = False

        if event.key == pygame.K_q:          # 'Q' quits game
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_c:
            self.config_prompt()
        if event.key == pygame.K_h:
            hard_mode = True
            configs[0] = 2
        if event.key == pygame.K_e:
            border_wrap = True

        # Set CLOCK_TICKS back to normal if not in hard mode
        if not hard_mode:
            configs[0] = 1
            
    def display_instructions(self):
        instruction_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Fill the surface with a semi-transparent black (RGBA color)
        instruction_surface.fill((0, 0, 0, 128))

        # Blit the overlay surface on top of the game window (arena)
        self.arena.blit(instruction_surface, (0, 0))
        
        instructions = [
            "Game Controls:",
            "- Arrow Keys/WASD: Move",
            "- P: Pause/Unpause",
            "- I: Show/Hide Instructions",
            "",
            "Press I to return to the game"
        ]
        
        y_offset = HEIGHT/3
        for line in instructions:
            text_surface = self.SMALL_FONT.render(line, True, (255, 255, 255))
            self.arena.blit(text_surface, (50, y_offset))
            y_offset += 50

    def draw_config(self,conf=[1,1,1,1]):
        velocity_string = ["Baixa", "Média", "Alta", "Extrema"]
        size_string = ["Pequeno", "Médio", "Grande"]
        f_string = ["Baixa", "Normal", "Alta"]
        sound_string = ["Baixo", "Médio", "Alto"]

        self.arena.fill(CONFIG_COLOR)
        center_title = self.BIG_FONT.render("Configuração", True, MESSAGE_COLOR)
        center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT*(0.20)))
        self.arena.blit(center_title, center_title_rect)

        center_subtitle = self.SMALL_FONT.render("Utilize as setas para navegar!", True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.30)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        center_subtitle = self.SMALL_FONT.render("Aperte J para jogar!", True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.35)))
        self.arena.blit(center_subtitle, center_subtitle_rect)

        center_subtitle = self.SMALL_FONT.render("Velocidade:", True, LINE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.45)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        center_subtitle = self.SMALL_FONT.render("{}".format(velocity_string[conf[0]]), True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.50)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        
        center_subtitle = self.SMALL_FONT.render("Tamanho:", True, LINE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.55)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        center_subtitle = self.SMALL_FONT.render("{}".format(size_string[conf[1]]), True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.60)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        
        center_subtitle = self.SMALL_FONT.render("Frequência:", True, LINE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.65)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        center_subtitle = self.SMALL_FONT.render("{}".format(f_string[conf[2]]), True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.70)))
        self.arena.blit(center_subtitle, center_subtitle_rect)

        center_subtitle = self.SMALL_FONT.render("Volume:", True, LINE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.75)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        center_subtitle = self.SMALL_FONT.render("{}".format(sound_string[conf[3]]), True, MESSAGE_COLOR)
        center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.80)))
        self.arena.blit(center_subtitle, center_subtitle_rect)
        
        pygame.display.update()

    def update_volume(self):
        pygame.mixer.music.set_volume(base_volume_levels[0] * volume_multiplier[configs[3]])
        self.got_apple_sound.set_volume(base_volume_levels[1] * volume_multiplier[configs[3]])
        self.game_over_sound.set_volume(base_volume_levels[2] * volume_multiplier[configs[3]])

    def config_prompt(self):
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
                    if event.key == pygame.K_DOWN:  
                        if n == 3:
                            n = 0  
                        else:
                            n += 1
                    elif event.key == pygame.K_UP:   
                        if n == 0:
                            n = 3 
                        else:
                            n -= 1
                    elif event.key == pygame.K_RIGHT: 
                        if configs[n] == 2:
                            configs[n] = 0
                        else:
                            configs[n] += 1
                        if n == 3:
                            self.update_volume()
                    elif event.key == pygame.K_LEFT:  
                        if configs[n] == 0:
                            configs[n] = 2
                        else:
                            configs[n] -= 1
                        if n == 3:
                            self.update_volume()
                    elif event.key == pygame.K_q:     
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_j: 
                        stop = 1
                self.draw_config(configs)   

    ## Get and save highscore from/in a file
    def save_high_score(self,score):
        if not os.path.exists("../data/"):
            os.makedirs("../data/")

        try:
            with open(HIGHSCORE_FILENAME, "wb+") as file:
                file.write(score.to_bytes(4, byteorder='big'))
        except (FileNotFoundError, ValueError):
            return 0

    def get_high_score(self):
        try:
            with open(HIGHSCORE_FILENAME, "rb") as file:
                return int.from_bytes(file.read(4), byteorder='big')
        except (FileNotFoundError, ValueError):
            return 0


    ## Display highscore
    def display_highscore(self,score):
        new_highscore = ""
        if score > self.highscore:
            # Update highscore
            self.highscore = score
            self.save_high_score(score)

            new_highscore = "NEW "

        text = new_highscore + "Highscore: " + str(self.highscore)

        # Display highscore value
        center_highscore = self.SMALL_FONT.render(text, True, MESSAGE_COLOR)
        center_highscore_rect = center_highscore.get_rect(center=(WIDTH/2, HEIGHT*1/5))
        self.arena.blit(center_highscore, center_highscore_rect)

        pygame.display.update()

    ##
    ## Draw the arena
    ##
    def draw_grid(self):
        for x in range(0, WIDTH, size[configs[1]]):
            for y in range(0, HEIGHT, size[configs[1]]):
                rect = pygame.Rect(x, y, size[configs[1]], size[configs[1]])
                pygame.draw.rect(self.arena, GRID_COLOR, rect, 1)

    

singleton_instance = Game()