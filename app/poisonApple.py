# app/fruits/poisonApple.py

import pygame
import random
import time
from app.fruits.fruitBase import BaseFruit
from app.config import *
from app.game import singleton_instance as gm

class PoisonApple(BaseFruit):
    def __init__(self, snake=None):
        super().__init__(POISON_APPLE_COLOR, snake)
        self.active = False
        self.spawn_time = time.time() + random.randint(5, 10)  
        self.duration = random.randint(POISON_APPLE_DURATION_MIN, POISON_APPLE_DURATION_MAX)  
        

    def update(self):
        current_time = time.time()
        print(f"[PoisonApple] Update called. Active: {self.active}, Current Time: {current_time}, Spawn Time: {self.spawn_time}")

        if not self.active and current_time >= self.spawn_time:
            self.active = True
            self.recalc(self.snake)
          
    
        
        if self.active:
            super().update()
            print(f"[PoisonApple] Active. Position: ({self.x}, {self.y})")
            if current_time >= self.spawn_time + self.duration:
                self.active = False
                self.spawn_time = current_time + random.randint(POISON_APPLE_RESPAWN_MIN, POISON_APPLE_RESPAWN_MAX)
                
    
    def respawn(self):
        self.active = True
        self.recalc(self.snake)
        self.spawn_time = time.time()
        
    
    def reset(self):
        self.active = False
        self.spawn_time = time.time() + random.randint(POISON_APPLE_RESPAWN_MIN, POISON_APPLE_RESPAWN_MAX)
        