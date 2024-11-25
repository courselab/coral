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

import random
import pygame

from app.config import *
from app.apple import Apple
from app.energybar import EnergyBar
from app.game import singleton_instance as gm

##
## Snake class
##
class Snake:
    __surface = None

    def __init__(self):

        self.__surface = gm.arena
        # Initial direction
        # xmov :  -1 left,    0 still,   1 right
        # ymov :  -1 up       0 still,   1 dows

        # Dimension of each snake segment.

        self.x, self.y, self.xmov, self.ymov = self.random_position()

        # The snake has a head segement,
        self.head = pygame.Rect(self.x, self.y, size[configs[1]], size[configs[1]])

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


    ## This function generate random positions for the snake
    def random_position(self):

        # Not too close to the border (minimum of 2 border squares)
        x = int(random.randint(size[configs[1]]*2, WIDTH - size[configs[1]]*2)/size[configs[1]]) * size[configs[1]]
        y = int(random.randint(size[configs[1]]*2, HEIGHT - size[configs[1]]*2)/size[configs[1]]) * size[configs[1]]

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

        # In the event of death, reset the game arena.
        if not self.alive:
            
            # Play game over sound effect
            pygame.mixer.music.stop()
            gm.game_over_sound.play()

            # Tell the bad news

            gm.display_highscore(len(self.tail))

            self.draw_head()
            gm.center_prompt("Game Over", "Press to restart")

            # Respawn the head with initial directions
            self.x, self.y, self.xmov, self.ymov = self.random_position()
            self.head.x = self.x
            self.head.y = self.y

            self.draw_head()

            # Respawn the initial tail
            self.tail = []

            # Resurrection
            gm.game_over_sound.stop()
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
            self.tail.insert(0,pygame.Rect(self.head.x, self.head.y, size[configs[1]], size[configs[1]]))

            if self.got_apple:
                self.got_apple = False
                self.energy.increase_energy(random.randint(APPLE_ENERGY - 25, APPLE_ENERGY))
            else:
                self.tail.pop()

            # Move the head along current direction.
            self.head.x += self.xmov * size[configs[1]]
            self.head.y += self.ymov * size[configs[1]]
            
        if border_wrap:
            self.head.x %= WIDTH
            self.head.y %= HEIGHT

    # Draw stylized head 
    def draw_head(self):
        # Define head and rectangle dimensions
        GRID_SIZE = size[configs[1]]
        head_radius = GRID_SIZE // 2
        head_center = (self.head.x + head_radius, self.head.y + head_radius)
        
        # Select color based on snake's alive status
        head_color = HEAD_COLOR if self.alive else DEAD_HEAD_COLOR
        
        # Draw the rounded head
        pygame.draw.circle(self.__surface, head_color, head_center, head_radius)
        
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

        pygame.draw.rect(self.__surface, head_color, body_rect)

        eye_radius = 7
        left_eye_pos = (head_center[0] + left_eye[0], head_center[1] + left_eye[1])
        right_eye_pos = (head_center[0] + right_eye[0], head_center[1] + right_eye[1])
        
        # Draw eyes based on snake's alive status
        if self.alive:
            pupil_radius = 4
            pygame.draw.circle(self.__surface, "#FFFFFF", left_eye_pos, eye_radius)
            pygame.draw.circle(self.__surface, "#FFFFFF", right_eye_pos, eye_radius)
            pygame.draw.circle(self.__surface, "#000000", left_eye_pos, pupil_radius)
            pygame.draw.circle(self.__surface, "#000000", right_eye_pos, pupil_radius)
        else:
            eye_line_length = 3
            pygame.draw.circle(self.__surface, "#FFFFFF", left_eye_pos, eye_radius)
            pygame.draw.circle(self.__surface, "#FFFFFF", right_eye_pos, eye_radius)
            pygame.draw.line(self.__surface, "#000000", 
                            (left_eye_pos[0] - eye_line_length, left_eye_pos[1] - eye_line_length), 
                            (left_eye_pos[0] + eye_line_length, left_eye_pos[1] + eye_line_length), 3)
            pygame.draw.line(self.__surface, "#000000", 
                            (left_eye_pos[0] - eye_line_length, left_eye_pos[1] + eye_line_length), 
                            (left_eye_pos[0] + eye_line_length, left_eye_pos[1] - eye_line_length), 3)
            pygame.draw.line(self.__surface, "#000000", 
                            (right_eye_pos[0] - eye_line_length, right_eye_pos[1] - eye_line_length), 
                            (right_eye_pos[0] + eye_line_length, right_eye_pos[1] + eye_line_length), 3)
            pygame.draw.line(self.__surface, "#000000", 
                            (right_eye_pos[0] - eye_line_length, right_eye_pos[1] + eye_line_length), 
                            (right_eye_pos[0] + eye_line_length, right_eye_pos[1] - eye_line_length), 3)

        # Randomly display the tongue
        if self.alive and random.randint(0, 10) > 8:  # Adjust chance of appearance here
            pygame.draw.rect(self.__surface, "#FF0000", pygame.Rect(tongue_pos, tongue_direction))
            
    # Draw stylized tail
    def draw_tail(self, tail, direction):
        # Define tail dimensions
        GRID_SIZE = size[configs[1]]
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
        pygame.draw.circle(self.__surface, tail_color, tail_center, tail_radius)

        # Draw the rectangular part connecting to the next segment
        pygame.draw.circle(self.__surface, tail_color, big_tail_center, 3 / 2* tail_radius)

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