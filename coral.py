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
import random
import sys
import os

##
## Game customization.
##


# Supported video modes

VIDEO_MODES = [
    (800, 800), (700, 700), (600, 600),
    (500, 500), (400, 400), (300, 300)
]

WIDTH, HEIGHT = 800, 800     # Default game screen dimensions.

HEAD_COLOR      = "#00aa00"  # Color of the snake's head.
DEAD_HEAD_COLOR = "#4b0082"  # Color of the dead snake's head.
TAIL_COLOR      = "#00ff00"  # Color of the snake's tail.
APPLE_COLOR     = "#aa0000"  # Color of the apple.
ORANGE_COLOR    = "#ffa500"  # Color of the orange.
ARENA_COLOR     = "#202020"  # Color of the ground.
CONFIG_COLOR    = "#D3D3D3"  # Color of the config section.
GRID_COLOR      = "#3c3c3b"  # Color of the grid lines.
SCORE_COLOR     = "#ffffff"  # Color of the scoreboard.
LINE_COLOR     = "#000000"  # Color of lines in scoreboard.
MESSAGE_COLOR   = "#808080"  # Color of the game-over message.
STEM_COLOR      = "#228B22"

WINDOW_TITLE    = "Coral"  # Window title.
MAX_QUEUE_SIZE = 3 # Movement queue max size

velocity = [4, 7, 10,15]
size = [60, 40, 20]  
n_apple = [1, 2, 3] 
base_volume_levels = [0.4, 0.6, 0.7]
volume_multiplier = [0.3, 1.1, 1.9]

configs = { "velocidade": 1,
          "tamanho": 1,
          "frequencia": 0,
          "volume" : 1}


WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 153, 0)

ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT = 200, 20
ENERGY_CONSUMPTION = 1
MAX_ENERGY = 100
APPLE_ENERGY = 50

hard_mode = False  # Defined normal mode as standart.
border_wrap = False
is_muted = False #Definied is muted as false 
instructions_shown = False


HIGHSCORE_FILENAME = "data/highscore.bin"
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

# arena = pygame.Surface((WIDTH, HEIGHT))
arena = pygame.display.set_mode((WIDTH, HEIGHT))


# Play background sound and change volume
pygame.mixer.music.set_volume(base_volume_levels[0])
background_music = pygame.mixer.music.load('musics/CPU Talk - FMA - CC BY BoxCat Games.mp3')
pygame.mixer.music.play(-1)

# Set game's sounds effects
got_apple_sound = pygame.mixer.Sound('musics/got_apple.ogg')
got_apple_sound.set_volume(base_volume_levels[1])

game_over_sound = pygame.mixer.Sound('musics/game_over.wav')
game_over_sound.set_volume(base_volume_levels[2])

# BIG_FONT   = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/8))
# SMALL_FONT = pygame.font.Font("assets/font/Ramasuri.ttf", int(WIDTH/20))

BIG_FONT   = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/8))
SMALL_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/20))
IN_GAME_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH/48))

pygame.display.set_caption(WINDOW_TITLE)

game_on = 1

## This function is called when the snake dies.

def center_prompt(title, subtitle):
    global hard_mode, border_wrap, CLOCK_TICKS

    # Show title and subtitle
    center_title = BIG_FONT.render(title, True, MESSAGE_COLOR)
    center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT*(0.3)))
    arena.blit(center_title, center_title_rect)

    center_subtitle = SMALL_FONT.render(subtitle, True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.4)))
    arena.blit(center_subtitle, center_subtitle_rect)
    
    center_subtitle = SMALL_FONT.render("Aperte C para configurar o jogo!", True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.5)))
    arena.blit(center_subtitle, center_subtitle_rect)

    # Add hard mode prompt
    hard_mode_text = SMALL_FONT.render("Press H for Hard Mode", True, MESSAGE_COLOR)
    hard_mode_text_rect = hard_mode_text.get_rect(center=(WIDTH/2, HEIGHT*(0.7)))
    arena.blit(hard_mode_text, hard_mode_text_rect)

    # Add easy mode prompt
    easy_mode_text = SMALL_FONT.render("Press E for Easy Mode", True, MESSAGE_COLOR)
    easy_mode_text_rect = easy_mode_text.get_rect(center=(WIDTH/2, HEIGHT*(0.8)))
    arena.blit(easy_mode_text, easy_mode_text_rect)
    
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
        config_prompt()
    if event.key == pygame.K_h:
        hard_mode = True
        configs['velocidade'] = 2
    if event.key == pygame.K_e:
        border_wrap = True

    # Set CLOCK_TICKS back to normal if not in hard mode
    if not hard_mode:
        configs['velocidade'] = 1
        
def display_instructions():
    instruction_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # Fill the surface with a semi-transparent black (RGBA color)
    instruction_surface.fill((0, 0, 0, 128))

    # Blit the overlay surface on top of the game window (arena)
    arena.blit(instruction_surface, (0, 0))
    
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
        text_surface = SMALL_FONT.render(line, True, (255, 255, 255))
        arena.blit(text_surface, (50, y_offset))
        y_offset += 50

def draw_config(config = {}, current_option = 0):
    conf=[1,1,1,1]
    if config:
        conf[0] = config['velocidade']
        conf[1] = config['tamanho']
        conf[2] = config['frequencia']
        conf[3] = config['volume']
    velocity_string = ["Baixa", "Média", "Alta", "Extrema"]
    size_string = ["Pequeno", "Médio", "Grande"]
    f_string = ["Baixa", "Normal", "Alta"]
    sound_string = ["Baixo", "Médio", "Alto"]

    arena.fill(CONFIG_COLOR)
    center_title = BIG_FONT.render("Configuração", True, MESSAGE_COLOR)
    center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT*(0.20)))
    arena.blit(center_title, center_title_rect)

    center_subtitle = SMALL_FONT.render("Utilize as setas para navegar!", True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.30)))
    arena.blit(center_subtitle, center_subtitle_rect)
    center_subtitle = SMALL_FONT.render("Aperte J para jogar!", True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.35)))
    arena.blit(center_subtitle, center_subtitle_rect)

    indicator_subtitle = SMALL_FONT.render(">", True, LINE_COLOR)
    indicator_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2 - 1, HEIGHT*(0.5 + 0.1*current_option)))
    arena.blit(indicator_subtitle, indicator_subtitle_rect)

    center_subtitle = SMALL_FONT.render("Velocidade:", True, LINE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.45)))
    arena.blit(center_subtitle, center_subtitle_rect)
    center_subtitle = SMALL_FONT.render("{}".format(velocity_string[conf[0]]), True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.50)))
    arena.blit(center_subtitle, center_subtitle_rect)
    
    center_subtitle = SMALL_FONT.render("Tamanho:", True, LINE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.55)))
    arena.blit(center_subtitle, center_subtitle_rect)
    center_subtitle = SMALL_FONT.render("{}".format(size_string[conf[1]]), True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.60)))
    arena.blit(center_subtitle, center_subtitle_rect)
    
    center_subtitle = SMALL_FONT.render("Frequência:", True, LINE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.65)))
    arena.blit(center_subtitle, center_subtitle_rect)
    center_subtitle = SMALL_FONT.render("{}".format(f_string[conf[2]]), True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.70)))
    arena.blit(center_subtitle, center_subtitle_rect)

    center_subtitle = SMALL_FONT.render("Volume:", True, LINE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.75)))
    arena.blit(center_subtitle, center_subtitle_rect)
    center_subtitle = SMALL_FONT.render("{}".format(sound_string[conf[3]]), True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.80)))
    arena.blit(center_subtitle, center_subtitle_rect)
    
    pygame.display.update()

def update_volume():
    pygame.mixer.music.set_volume(base_volume_levels[0] * volume_multiplier[configs['volume']])
    got_apple_sound.set_volume(base_volume_levels[1] * volume_multiplier[configs['volume']])
    game_over_sound.set_volume(base_volume_levels[2] * volume_multiplier[configs['volume']])

    
def config_prompt():
    draw_config()

   # Wait for a keypress or a game quit event.
    n = 0
    draw_config(configs, n)

    stop = 0
    while True:
        opcao = 'velocidade'
        match n:
            case 0:
                opcao = 'velocidade'
            case 1:
                opcao = 'tamanho'
            case 2:
                opcao = 'frequencia'
            case 3:
                opcao = 'volume'

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
                    if configs[opcao] == 2:
                        configs[opcao] = 0
                    else:
                        configs[opcao] += 1
                    if n == 3:
                        update_volume()
                elif event.key == pygame.K_LEFT:  
                    if configs[opcao] == 0:
                        configs[opcao] = 2
                    else:
                        configs[opcao] -= 1
                    if n == 3:
                        update_volume()
                elif event.key == pygame.K_q:     
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_j: 
                    stop = 1
            draw_config(configs, n)   

## This function generate random positions for the snake
def random_position():

    # Not too close to the border (minimum of 2 border squares)
    x = int(random.randint(size[configs['tamanho']]*2, WIDTH - size[configs['tamanho']]*2)/size[configs['tamanho']]) * size[configs['tamanho']]
    y = int(random.randint(size[configs['tamanho']]*2, HEIGHT - size[configs['tamanho']]*2)/size[configs['tamanho']]) * size[configs['tamanho']]

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
  
## The score based on the length and number of collected oranges
def get_score(snake):
    return len(snake.tail) + snake.oranges

## Get and save highscore from/in a file
def save_high_score(score):
    if not os.path.exists("data/"):
        os.makedirs("data/")

    try:
        with open(HIGHSCORE_FILENAME, "wb+") as file:
            file.write(score.to_bytes(4, byteorder='big'))
    except (FileNotFoundError, ValueError):
        return 0


def get_high_score():
    try:
        with open(HIGHSCORE_FILENAME, "rb") as file:
            return int.from_bytes(file.read(4), byteorder='big')
    except (FileNotFoundError, ValueError):
        return 0


highscore = get_high_score()

## Display highscore
def display_highscore(score):
    global highscore
    new_highscore = ""
    if score > highscore:
        # Update highscore
        highscore = score
        save_high_score(score)

        new_highscore = "NEW "

    text = new_highscore + "Highscore: " + str(highscore)

    # Display highscore value
    center_highscore = SMALL_FONT.render(text, True, MESSAGE_COLOR)
    center_highscore_rect = center_highscore.get_rect(center=(WIDTH/2, HEIGHT*1/5))
    arena.blit(center_highscore, center_highscore_rect)

    pygame.display.update()

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
        self.head = pygame.Rect(self.x, self.y, size[configs['tamanho']], size[configs['tamanho']])

        # and a tail (array of segments).
        self.tail = []

        # The snake is born.
        self.alive = True

        # No collected apples.
        self.got_apple = False

        # The energy is full
        self.energy = EnergyBar(MAX_ENERGY)

        # Movement queue
        self.move_queue = []
        
        # Multiplier based on number of collected oranges.
        self.speed = 1 

    # Add movement to movement queuedef
    def set_direction(self, xmov, ymov):
        if not(xmov == -self.xmov and ymov == -self.ymov) and len(self.move_queue) <= MAX_QUEUE_SIZE:
            self.move_queue.append((xmov, ymov))


    # This function is called at each loop interation.
    def update(self):
        global apple, border_wrap

        # Read and pop movement from queue.
        if self.move_queue:
            self.xmov, self.ymov = self.move_queue.pop(0)

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

        # Number of collected oranges (for score purposes; they are worth 2 points).
        self.oranges = int(50*(self.speed - 1))

        # In the event of death, reset the game arena.
        if not self.alive:
            
            # Play game over sound effect
            pygame.mixer.music.stop()
            game_over_sound.play()

            # Tell the bad news

            display_highscore(get_score(self))

            self.draw_head()
            center_prompt("Game Over", "Press to restart")

            # Respawn the head with initial directions
            self.x, self.y, self.xmov, self.ymov = random_position()
            self.head.x = self.x
            self.head.y = self.y

            self.draw_head()

            # Respawn the initial tail
            self.tail = []

            # Reset speed
            self.speed = 1

            # Resurrection
            game_over_sound.stop()
            self.alive = True
            self.got_apple = False
            self.energy.set_max_energy()
            pygame.mixer.music.play(-1)

            # Drop an apple
            apple = Apple()


        # Move the snake.

        # If head hasn't moved, tail shouldn't either (otherwise, self-bite).
        if (self.xmov or self.ymov):

            # Prepend a new segment to tail.
            self.tail.insert(0,pygame.Rect(self.head.x, self.head.y, size[configs['tamanho']], size[configs['tamanho']]))

            if self.got_apple:
                self.got_apple = False
                self.energy.increase_energy(random.randint(APPLE_ENERGY - 25, APPLE_ENERGY))
            else:
                self.tail.pop()

            # Move the head along current direction.
            self.head.x += self.xmov * size[configs['tamanho']]
            self.head.y += self.ymov * size[configs['tamanho']]
            
        if border_wrap:
            self.head.x %= WIDTH
            self.head.y %= HEIGHT

    # Draw stylized head 
    def draw_head(self):
        # Define head and rectangle dimensions
        GRID_SIZE = size[configs['tamanho']]
        head_radius = GRID_SIZE // 2
        head_center = (self.head.x + head_radius, self.head.y + head_radius)
        
        # Select color based on snake's alive status
        head_color = HEAD_COLOR if self.alive else DEAD_HEAD_COLOR
        
        # Draw the rounded head
        pygame.draw.circle(arena, head_color, head_center, head_radius)
        
        # Draw the rectangle body behind the head circle based on direction
        eye_offset = head_radius // 2
        if self.xmov == 1:  # Moving right
            body_rect = pygame.Rect(self.head.x, self.head.y, GRID_SIZE // 2, GRID_SIZE)
            right_eye = (eye_offset, -eye_offset)
            left_eye = (eye_offset, eye_offset)
            tongue_pos = (head_center[0] + head_radius, head_center[1])
            tongue_direction = (10, 2)  # Horizontal tongue
        elif self.xmov == -1:  # Moving left
            body_rect = pygame.Rect(self.head.x + head_radius, self.head.y, GRID_SIZE // 2, GRID_SIZE)
            right_eye = (-eye_offset, -eye_offset)
            left_eye = (-eye_offset, eye_offset)
            tongue_pos = (head_center[0] - 3 / 2 * head_radius, head_center[1])
            tongue_direction = (10, 2)  # Horizontal tongue
        elif self.ymov == 1:  # Moving down
            body_rect = pygame.Rect(self.head.x, self.head.y, GRID_SIZE, GRID_SIZE // 2)
            right_eye = (-eye_offset, eye_offset)
            left_eye = (eye_offset, eye_offset)
            tongue_pos = (head_center[0], head_center[1] + head_radius)
            tongue_direction = (2, 10)  # Vertical tongue
        else:  # Moving up
            body_rect = pygame.Rect(self.head.x, self.head.y + head_radius, GRID_SIZE, GRID_SIZE // 2)
            right_eye = (-eye_offset, -eye_offset)
            left_eye = (eye_offset, -eye_offset)
            tongue_pos = (head_center[0], head_center[1] - 3 / 2 * head_radius)
            tongue_direction = (2, 10)  # Vertical tongue

        pygame.draw.rect(arena, head_color, body_rect)

        eye_radius = 7
        left_eye_pos = (head_center[0] + left_eye[0], head_center[1] + left_eye[1])
        right_eye_pos = (head_center[0] + right_eye[0], head_center[1] + right_eye[1])
        
        # Draw eyes based on snake's alive status
        if self.alive:
            pupil_radius = 4
            pygame.draw.circle(arena, "#FFFFFF", left_eye_pos, eye_radius)
            pygame.draw.circle(arena, "#FFFFFF", right_eye_pos, eye_radius)
            pygame.draw.circle(arena, "#000000", left_eye_pos, pupil_radius)
            pygame.draw.circle(arena, "#000000", right_eye_pos, pupil_radius)
        else:
            eye_line_length = 3
            pygame.draw.circle(arena, "#FFFFFF", left_eye_pos, eye_radius)
            pygame.draw.circle(arena, "#FFFFFF", right_eye_pos, eye_radius)
            pygame.draw.line(arena, "#000000", 
                            (left_eye_pos[0] - eye_line_length, left_eye_pos[1] - eye_line_length), 
                            (left_eye_pos[0] + eye_line_length, left_eye_pos[1] + eye_line_length), 3)
            pygame.draw.line(arena, "#000000", 
                            (left_eye_pos[0] - eye_line_length, left_eye_pos[1] + eye_line_length), 
                            (left_eye_pos[0] + eye_line_length, left_eye_pos[1] - eye_line_length), 3)
            pygame.draw.line(arena, "#000000", 
                            (right_eye_pos[0] - eye_line_length, right_eye_pos[1] - eye_line_length), 
                            (right_eye_pos[0] + eye_line_length, right_eye_pos[1] + eye_line_length), 3)
            pygame.draw.line(arena, "#000000", 
                            (right_eye_pos[0] - eye_line_length, right_eye_pos[1] + eye_line_length), 
                            (right_eye_pos[0] + eye_line_length, right_eye_pos[1] - eye_line_length), 3)

        # Randomly display the tongue
        if self.alive and random.randint(0, 10) > 8:  # Adjust chance of appearance here
            pygame.draw.rect(arena, "#FF0000", pygame.Rect(tongue_pos, tongue_direction))
            
    # Draw stylized tail
    def draw_tail(self, tail, direction):
        # Define tail dimensions
        GRID_SIZE = size[configs['tamanho']]
        tail_radius = GRID_SIZE // 3  # Smaller radius for the tail
        big_tail_center = (tail[0] + tail_radius, tail[1] + tail_radius)
        tail_center = (tail[0] + tail_radius, tail[1] + tail_radius)

        # Determine tail shape and position based on the last segment's movement
        if direction[0] > 0:  # Moving right
            big_tail_center = (tail[0] + GRID_SIZE, tail[1] + GRID_SIZE // 2)
            tail_center = (tail[0] + GRID_SIZE - tail_radius, tail[1] + GRID_SIZE // 2)
        elif direction[0] < 0:  # Moving left
            big_tail_center = (tail[0], tail[1] + GRID_SIZE // 2)
            tail_center = (tail[0] + tail_radius, tail[1] + GRID_SIZE // 2)
        elif direction[1] > 0:  # Moving down
            big_tail_center = (tail[0] + GRID_SIZE // 2 , tail[1] + GRID_SIZE)
            tail_center = (tail[0] + GRID_SIZE // 2, tail[1] + 2 * tail_radius)
        else:  # Moving up
            big_tail_center = (tail[0] + GRID_SIZE // 2 , tail[1])
            tail_center = (tail[0] + GRID_SIZE // 2, tail[1] + tail_radius)

        # Choose color based on alive status
        tail_color = HEAD_COLOR if self.alive else DEAD_HEAD_COLOR

        # Draw the main part of the tail (rounded edge)
        pygame.draw.circle(arena, tail_color, tail_center, tail_radius)

        # Draw the rectangular part connecting to the next segment
        pygame.draw.circle(arena, tail_color, big_tail_center, 3 / 2* tail_radius)

    def is_in_position(self, x, y):
        """ Determine whether any part of the snake is in position (x, y). """
        """This could be optimized by always maintaining a hashmap of the positions
        of the snake's segments, which felt unecessary by now. """

        if self.head.x == x and self.head.y == y:
            return True
        for square in self.tail: 
            if square.x == x and square.y == y:
                return True
        return False

##
## The apple class.
##

class Apple:
    def __init__(self, snake=None):

        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH)/size[configs['tamanho']]) * size[configs['tamanho']]
        self.y = int(random.randint(0, HEIGHT)/size[configs['tamanho']]) * size[configs['tamanho']]

        if snake:
            while snake.is_in_position(self.x, self.y):
                # Prevent apples from spawning on top of the snake
                self.x = int(random.randint(0, WIDTH)/size[configs['tamanho']]) * size[configs['tamanho']]
                self.y = int(random.randint(0, HEIGHT)/size[configs['tamanho']]) * size[configs['tamanho']]

        # Create an apple at that location
        self.rect = pygame.Rect(self.x, self.y, size[configs['tamanho']], size[configs['tamanho']])
        self.radius = size[configs['tamanho']] // 2

    # This function is called each interation of the game loop

    def update(self):

        # Drop the apple
        pygame.draw.circle(arena, APPLE_COLOR, (self.rect.centerx, self.rect.centery), self.radius)
        
        stem_x = self.rect.centerx
        stem_y = self.rect.top - 5  # Um pouco acima da maçã
        pygame.draw.line(arena, STEM_COLOR, (stem_x, stem_y), (stem_x, stem_y - 10), 3)


##
## The orange class.
##

class Orange:
    def __init__(self):

        self.dropped = False

        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH)/size[configs['tamanho']]) * size[configs['tamanho']]
        self.y = int(random.randint(0, HEIGHT)/size[configs['tamanho']]) * size[configs['tamanho']]

        # Create an orange at that location
        self.rect = pygame.Rect(self.x, self.y, size[configs['tamanho']], size[configs['tamanho']])
        self.radius = size[configs['tamanho']] // 2

    # This function is called each interation of the game loop
    def update(self):

        # Check if the orange is already dropped, if not then maybe drop it
        if self.dropped == False:
            if random.randint(1, 100) >= 99:
                pygame.draw.circle(arena, ORANGE_COLOR, (self.rect.centerx, self.rect.centery), self.radius)
                self.dropped = True

        elif self.dropped == True:
            pygame.draw.circle(arena, ORANGE_COLOR, (self.rect.centerx, self.rect.centery), self.radius)

##
## Draw the arena
##

def draw_grid():
    for x in range(0, WIDTH, size[configs['tamanho']]):
        for y in range(0, HEIGHT, size[configs['tamanho']]):
            rect = pygame.Rect(x, y, size[configs['tamanho']], size[configs['tamanho']])
            pygame.draw.rect(arena, GRID_COLOR, rect, 1)

score = BIG_FONT.render("1", True, MESSAGE_COLOR)
score_rect = score.get_rect(center=(WIDTH/2, HEIGHT/20+HEIGHT/30))

draw_grid()

snake = Snake()    # The snake

apple = Apple()    # An apple

orange = Orange()  # An orange

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
        display_instructions() 
        pygame.display.update()
        continue  # Skip the rest of the loop if instructions are shown

    ## Show "Paused" and "Press P to continue" messages in the center of the grid
    if not game_on:
        arena.fill(ARENA_COLOR)  # Clear the arena to prevent overlap
        
        pause_text = BIG_FONT.render("Paused", True, MESSAGE_COLOR)
        pause_text_rect = pause_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        arena.blit(pause_text, pause_text_rect)
        
        continue_text = SMALL_FONT.render("Press P to continue", True, MESSAGE_COLOR)
        continue_text_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        arena.blit(continue_text, continue_text_rect)
        
        quit_text = SMALL_FONT.render("Press q to quit", True, MESSAGE_COLOR)
        quit_text_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 125))
        arena.blit(quit_text, quit_text_rect)
        # Draw the pause menu and update the display
        win.blit(pygame.transform.rotozoom(arena, 0, win_res / WIDTH), (0, 0))
        pygame.display.update()
        
        # Skip the rest of the loop when paused, preventing unnecessary updates
        continue  

    
    if game_on:

        snake.update()

        arena.fill(ARENA_COLOR)
        draw_grid()

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
            pygame.draw.rect(arena, HEAD_COLOR, square)
    # Draw head
    snake.draw_head()

    if game_on:
        snake.energy.update()
        
    # Show score
    score = BIG_FONT.render(f"{get_score(snake)}", True, SCORE_COLOR)
    arena.blit(score, score_rect)

    # If the head pass over an apple, lengthen the snake and drop another apple
    if snake.head.x == apple.x and snake.head.y == apple.y:
        #snake.tail.append(pygame.Rect(snake.head.x, snake.head.y, GRID_SIZE, GRID_SIZE))
        snake.got_apple = True
        apple = Apple(snake)
        got_apple_sound.play()

    # If the head passes over an orange, lengthen the snake and drop another orange
    if snake.head.x == orange.x and snake.head.y == orange.y:
        #snake.tail.append(pygame.Rect(snake.head.x, snake.head.y, GRID_SIZE, GRID_SIZE))
        snake.energy.increase_energy(APPLE_ENERGY)
        snake.speed += 0.04
        orange = Orange()
        got_apple_sound.play()


    # Add the "Press (I)nstructions" text in the top-right corner
    instruction_text = IN_GAME_FONT.render("Press (I)nstructions", True, WHITE_COLOR)
    instruction_text_rect = instruction_text.get_rect(topright=(WIDTH - 10, 10))  # Padding from the edge
    arena.blit(instruction_text, instruction_text_rect)

    # Update display and move clock.
    pygame.display.update()
    clock.tick(snake.speed*velocity[configs['velocidade']])

