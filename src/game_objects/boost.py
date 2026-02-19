import pygame, os, time
from abc import ABC, abstractmethod
from src.utils.constants import PACMAN_SPEED, BOOST_DURATION, MAP_OFFSET_Y

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
            shifted_rect = self.rect.move(0, MAP_OFFSET_Y)
            screen.blit(self.image, shifted_rect)
    
    @abstractmethod
    def apply_effect(self, pacman):
        pass


class CakeBoost(Boost):
    def apply_effect(self, pacman):
        pacman.speed = PACMAN_SPEED + 2
        pacman.active_boosts["speed"] = time.time() + BOOST_DURATION

class StrawberryBoost(Boost):
    def apply_effect(self, pacman):
        pacman.score += 1000  #можна змінити з часом

class WatermelonBoost(Boost):
    def apply_effect(self, pacman):
        pacman.shielded = True
        pacman.active_boosts["shield"] = time.time() + BOOST_DURATION