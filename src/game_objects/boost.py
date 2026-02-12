import pygame
import os
from abc import ABC, abstractmethod

BOOST_IMAGES = {}

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "boosts")

for name, folder in [("CakeBoost", "cake"),
                     ("StrawberryBoost", "strawberry"),
                     ("WatermelonBoost", "watermelon")]:
    file_path = os.path.join(ASSETS_PATH, folder, f"{folder}.png")
    BOOST_IMAGES[name] = pygame.image.load(file_path).convert_alpha()

class Boost(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = BOOST_IMAGES[self.__class__.__name__]
        self.rect = self.image.get_rect(center=(x,y))
        self.eaten = False
    
    def draw(self, screen):
        if not self.eaten:
            screen.blit(self.image, self.rect)
    
    @abstractmethod
    def apply_effect(self, pacman):
        pass


class CakeBoost(Boost):
    def apply_effect(self, pacman):
        pacman.speed += 1

class StrawberryBoost(Boost):
    def apply_effect(self, pacman):
        #pacman.score += 200
        return

class WatermelonBoost(Boost):
    def apply_effect(self, pacman):
        #pacman.invincible = True
        return 