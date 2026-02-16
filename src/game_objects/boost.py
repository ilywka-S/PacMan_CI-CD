import pygame
import os
from abc import ABC, abstractmethod

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "boosts")
BOOST_CONFIGS = {
    "CakeBoost": "cake",
    "StrawberryBoost": "strawberry",
    "WatermelonBoost": "watermelon"
}
class Boost(ABC):
    _images = {}
    def __init__(self, x, y):
        self.x = x
        self.y = y

        class_name = self.__class__.__name__
        if class_name not in Boost._images:
            folder = BOOST_CONFIGS[class_name]
            file_path = os.path.join(ASSETS_PATH, folder, f"{folder}.png")
            Boost._images[class_name] = pygame.image.load(file_path).convert_alpha()

        self.image = Boost._images[class_name]
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
        print("ate a cake")

class StrawberryBoost(Boost):
    def apply_effect(self, pacman):
        #pacman.score += 200
        print("ate a strawberry")

class WatermelonBoost(Boost):
    def apply_effect(self, pacman):
        #pacman.invincible = True
        print("ate a watermelon")